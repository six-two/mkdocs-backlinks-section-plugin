# MkDocs Backlinks Section Plugin

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-backlinks-section-plugin)](https://pypi.org/project/mkdocs-backlinks-section-plugin/)
![License](https://img.shields.io/pypi/l/mkdocs-backlinks-section-plugin)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-backlinks-section-plugin)

Adds a backlinks section that lists every page linking to the current page.

The added backlinks section looks like this, but you can also customize the title and the text show above the list:

![Screenshot of the backlinks section](https://github.com/six-two/mkdocs-backlinks-section-plugin/raw/main/screenshot.png)

## Comparison to similar plugins

I wrote my plugin after trying some existing plugins and not being 100% happy with them.
But depending on your intended use case, they may be a better fit.

### mkdocs-backlinks

My plugin is similar in concept to [mkdocs-backlinks](https://github.com/danodic-dev/mkdocs-backlinks), but I wanted a plugin that works out of the box.

With [mkdocs-backlinks](https://github.com/danodic-dev/mkdocs-backlinks) you can specify exactly where and how you want to have your backlinks shown, but at the cost of having to potentially alter your template files.

With my plugin you just need to add the plugin to your `mkdocs.yml`, but the backlinks can only be added as a section at the bottom of each page.

### mkdocs-publisher

[mkdocs-publisher](https://github.com/mkdocs-publisher/mkdocs-publisher) is a bundle of plugins.
The `pub-obsidian` also has a backlinks feature.

While my plugin does a single job and has minimal dependencies, mkdocs-publisher offers many more features but at the cost of many more dependencies.

## Installation

You can install it with `pip`:
```bash
pip install mkdocs-backlinks-section-plugin
```

## Usage

Add the plugin to your `mkdocs.yml`:
```yaml
plugins:
- search
- backlinks_section
```

## Configuration

### Text

You can customize the text inserted by the plugin with the configuration values below:

Option | Type | Default value
--- | --- | ---
`title` | string | `Backlinks`
`description` | string | `The following pages link to this page:`
`description_no_links` | string | `No other pages link to this page.`


So for example if you would want the text to be in German, you could do this in your `mkdocs.yml`:
```yaml
plugins:
- search
- backlinks_section:
    title: Rückverweise
    description: "Die folgenden Seiten referenzieren die aktuelle Seite:"
    description_no_links: Es gibt keine Verweise auf diese Seite.
```

### Ignore pages

You can ignore source and destination pages for the backlink section.
The values are interpreted as [glob-like](https://docs.python.org/3/library/pathlib.html#pathlib-pattern-language) patterns, wich are matched against the paths of the Markdown source files.

Option | Type | Default value
--- | --- | ---
`ignore_links_from` | list of strings | `[]`
`ignore_links_to` | list of strings | `[]`

For example you may have a page listing all [tags](https://squidfunk.github.io/mkdocs-material/setup/setting-up-tags/) (and thus linking to almost all pages) and want to prevent every page having a backlink to it:

```yaml
plugins:
- search
- backlinks_section:
    ignore_links_from:
    - path/with/globs/**/to/tags.md
```

If you do not want a backlinks section on some pages, you can disable it with the `ignore_links_to` option:
```yaml
plugins:
- search
- backlinks_section:
    ignore_links_to:
    - path/with/globs/**/to/files-without-backlink-section-*.md
    - index.md
```

### Hide section

Option | Type | Default value
--- | --- | ---
`add_to_toc` | boolean | `true`
`hide_if_empty` | boolean | `false`

If you do not want a backlinks section to be added to the table of contents of search page, you can set the `add_to_toc` parameter to `false`:
```yaml
plugins:
- search
- backlinks_section:
    add_to_toc: false
```

If you want to hide the backlinks section from pages which have no backlinks, you can set the `hide_if_empty` attribute to `true`.
Please note that in the current implementation this also requires always hiding the section title (even if the section exists) from the table of contents.
To suppress the warning about this it is recommended to explicitly set `add_to_toc` to `false` too:
```yaml
plugins:
- search
- backlinks_section:
    add_to_toc: false
    hide_if_empty: true
```

### Troubleshooting

Option | Type | Default value
--- | --- | ---
`debug` | boolean | `false`

Used by me to debug problems with backlink generation.
If you open a GitHub issue, it would be best to provide me a minimum working example, with which I can reproduce your problem.
If that is not possible (for example because your project is private), it would help me if you supply the output of mkdocs when you set `debug: True`.

## Notable changes

### Version 0.0.7

- Fixed false positive warnings about missing `hrefs` for tags starting with `<a` (`<autoref>`, `<audio>`, etc). Thank you @kzndotsh (see #4)

### Version 0.0.6

- Fixed an issue with backlinks not appearing on some pages (see #3)
- Added `debug` option to help with troubleshooting

### Version 0.0.5

- Ignore empty link tags created by listings with line numbers (`linenums="1"`)
- In warning messages show which file caused the warning

### Version 0.0.4

- Added `add_to_toc` option, which controls whether to add the backlinks section to the table of contents.
- Added `hide_if_empty` option, which will hide the backlinks section, if no backlinks exist.
    This requires `add_to_toc` to be false, otherwise the table of contents would point to a potentially non-existent section.

### Version 0.0.3

- Fixed crash with Python <= 3.12

### Version 0.0.2

- Added `ignore_links_from` and `ignore_links_to` configuration options

### Version 0.0.1

- Initial version
