# Editorial Content Package

## Overview

`content/` holds the article catalog and individual standalone HTML essays that the site generator uses as publication inputs. Essay styles are inline in the HTML sources; the catalog determines each article's route, date, display metadata, taxonomy, assets, research type, and optional featured image. [articles.json:slug] [articles.json:source] [build.py:load_notes]

## Interface

- `articles.json` is an ordered JSON array of article records consumed by `build.load_notes()`. Each record points to an individual HTML source file under this directory. [`articles.json`](./articles.json) [build.py:load_notes]
- Article routes are formed from `slug`; the source filename is provided by `source`. Optional `title`, `dek`, and featured-image metadata supplement the source HTML. [articles.json:slug] [articles.json:source] [articles.json:image] [build.py:render_article]

## Invariants

- Slugs are unique lowercase hyphenated strings, dates use `YYYY-MM-DD`, source files resolve inside `content/`, and catalog entries use approved `topic`, `research_type`, and uppercase `assets` values. [build.py:SLUG_RE] [build.py:load_notes] [build.py:TOPICS] [build.py:RESEARCH_TYPES] [build.py:ASSET_RE]
- A supplied `dek` must appear in the visible text of its article. If omitted, the generator can use the article description metadata. [build.py:load_notes] [build.py:visible_text]
- Featured artwork metadata is optional. When present, its path, signature, alt text, dimensions, and MIME type are checked by `featured_image()`. [build.py:featured_image]
- The generator sorts notes newest first while retaining catalog order for same-date entries. [build.py:load_notes]
- Essay files remain independent article sources; the generator adds publication framing and metadata without replacing their editorial substance. [build.py:render_article] [README.md:Add a note]

## Side Effects

- None. These files are generator inputs; output is written under the repository's `dist/` directory by `build.py`. [build.py:main]

## Verification

- Run from repository root: `python3 build.py`
- Content and metadata checks: `python3 -m unittest discover -s tests -p 'test_*.py'`
