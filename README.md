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

## Notable changes

### Version 0.0.1

- Initial version
