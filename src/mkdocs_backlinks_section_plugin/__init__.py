# builtin

# The idea is based roughly on https://github.com/danodic-dev/mkdocs-backlinks, but instead of dealing with a template, this plugin just injects the backlinks into the HTML at the bottom of the page
import os
import html
from pathlib import PurePath
import random
import re
from typing import Optional
import urllib.parse
# pip
from mkdocs.config.base import Config
from mkdocs.config.config_options import Type, ListOfItems
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

# Marks URLs that should be ignored
BAD_URL_STARTS = ["http://", "https://", "tel:", "#"]
# Regular expression for anchor tags
LINK_START_TAG_REGEX = re.compile(r"<a[^>]*>", re.MULTILINE)
# Logger
LOGGER = get_plugin_logger(__name__)

class BacklinksSectionConfig(Config):
    title = Type(str, default="Backlinks")
    description = Type(str, default="The following pages link to this page:")
    description_no_links = Type(str, default="No other pages link to this page.")
    ignore_links_from = ListOfItems(Type(str), [])
    ignore_links_to = ListOfItems(Type(str), [])

class BacklinksSectionPlugin(BasePlugin[BacklinksSectionConfig]):
    def __init__(self):
        # Use a random placeholder to prevent accidential collisions with strings like BACKLINK_PLUGIN
        self.backlink_placeholder = f"BACKLINK_PLUGIN_{random.randint(0,10000000)}_PLACEHOLDER"
    
    def on_nav(self, nav, config: MkDocsConfig, files: Files):
        # self.backlinks | normalized_url: str -> (page_url: str, page_title: str)
        self.backlinks: dict[str,set[tuple[str,str]]] = {normalize_link(file.url): set() for file in files}
        self.ignore_links_from = [normalize_link(x) for x in self.config.ignore_links_from]
        self.ignore_links_to = [x[1:] if x.startswith("/") else x for x in self.config.ignore_links_to]

        if not hasattr(PurePath("/"), "full_match"):
            # Fullmatch "**" is not supported. Check if the patterns actually use it
            if "**" in ",".join(self.ignore_links_from + self.ignore_links_to):
                LOGGER.warning("Your Python does not support the Path.full_match method. Since you use '**' in your patterns, this may not be interpreted correctly. To fix it update your Python to 3.13")
        return nav

    def on_page_markdown(self, markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
        if should_ignore_page(page, self.ignore_links_to):
            # Ignore the page and skip the backlinks section
            return markdown
        else:
            # Add backlinks section placeholder
            # We need to do this in the Markdown phase, so that the new section is added to the table of contents
            return f"{markdown}\n\n## {self.config.title}\n\n{self.backlink_placeholder}"

    def on_page_content(self, html, page: Page, config: MkDocsConfig, files: Files) -> str:
        if should_ignore_page(page, self.ignore_links_from):
            LOGGER.debug(f"Ignoring links from page: {page.file.src_uri}")
        else:
            # Collect the backlinks
            for url in parse_links_to_other_pages(html):
                destination_link = normalize_link(url, page.url)

                # Prevent the same page from linking back to itself
                # @TODO: this only works for directory URLs. Also not sure how reliable it is
                if destination_link != normalize_link("", page.url):
                    if destination_link in self.backlinks:
                        self.backlinks[destination_link].add((page.url, page.title))
                else:
                    LOGGER.debug(f"Link to self on {page.url} ignored")

        return html

    def on_post_page(self, output: str, page: Page, config: MkDocsConfig) -> str:
        if should_ignore_page(page, self.ignore_links_to):
            # Ignore the page and skip the backlinks section
            return output
        else:
            # Insert the backlink list
            key = normalize_link(page.url, "")
            links = self.backlinks[key]
            if links:
                backlink_html = f"<p>{html.escape(self.config.description)}</p>" if self.config.description else ""
                backlink_html += "<ul>"
                # sort by title
                for link, title in sorted(links, key=lambda x: x[1]):
                    link_to_page = get_relative_path_from(page.url, link)
                    backlink_html += f'<li><a href="{link_to_page}">{html.escape(title)}</a></li>'
                backlink_html += "</ul>"
                output = output.replace(self.backlink_placeholder, backlink_html)
            else:
                output = output.replace(self.backlink_placeholder, f"<p>{html.escape(self.config.description_no_links)}</p>")
            return output


def get_relative_path_from(current_page: str, absolute_destination_link: str) -> str:
    level = current_page.count("/")
    relative_url = ("../" * level) + absolute_destination_link

    return relative_url


def should_ignore_page(page: Page, ignore_pattern_list: list[str]) -> bool:
    page_path = PurePath(page.file.src_uri)
    for ignore_pattern in ignore_pattern_list:
        if path_try_full_match(page_path, ignore_pattern, False):
            return True
    
    return False

def path_try_full_match(page_path: PurePath, ignore_pattern: str, case_sensitive: bool) -> bool:
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.full_match
    # Sadly it only exists in 3.13. So I need to use the worse version "match" if we have an old python version
    if hasattr(page_path, "full_match"):
        return page_path.full_match(ignore_pattern, case_sensitive=case_sensitive)
    else:
        # Case sensitive is only available from Python 3.12
        return page_path.match(ignore_pattern)


def normalize_link(path: str, base_url: str = "") -> str:
    path = path.split("#", 1)[0] # Remove anything after a hashtag (exact anchor on page)

    # decode URLs in case they contain URL encoded data
    path = urllib.parse.unquote(path)

    # Since some operating systems can have canse insensitive paths, we convert them to lowercase
    path = path.lower()

    if path.startswith("/"):
        # Absolute URL
        path = os.path.normpath(path)[1:]
    else:
        if base_url:
            path = os.path.join(os.path.dirname(base_url), path)
    
        path = os.path.normpath(path)

    if path.endswith("/index.html") or path == "index.html":
        path = path[:-len("index.html")]

    return path

def is_valid_link(url: str) -> bool:
    url = url.lower()
    for bad_pattern in BAD_URL_STARTS:
        if url.startswith(bad_pattern):
            # Url is not a local path
            return False
    # Url is probably a local file
    return True


def parse_href_from_anchor_tag(anchor_tag: str) -> Optional[str]:
    for part in anchor_tag.split():
        if part.endswith(">"):
            part = part[:-1]
        if part.startswith("href="):
            link = part[5:]
            if link[0] in ["\"", "'"]:
                if link[0] == link[-1]:
                    return link[1:-1]
                else:
                    LOGGER.warning(f"href does not have matching quotes: {link}")
                    return ""
            else:
                return link
    
    LOGGER.warning(f"anchor tag has no href: {anchor_tag}")
    return ""


def parse_links_to_other_pages(html: str) -> list[str]:
    results = []
    for link_start_tag in LINK_START_TAG_REGEX.findall(html):
        link = parse_href_from_anchor_tag(link_start_tag)
        if link and is_valid_link(link):
            results.append(link)
    
    return results

