# MkDocs Backlinks Section Plugin

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-backlinks-section-plugin)](https://pypi.org/project/mkdocs-backlinks-section-plugin/)
![License](https://img.shields.io/pypi/l/mkdocs-backlinks-section-plugin)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-backlinks-section-plugin)

Adds a backlinks section that lists every page linking to the current page.

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

## Notable changes

### HEAD

- Added `ignore_links_from` and `ignore_links_to` configuration options

### Version 0.0.1

- Initial version
