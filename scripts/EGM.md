# Maintenance Scripts Package

## Overview

`scripts/` contains a Python utility for explicitly refreshing reviewed article and metadata fixtures. CI runs the Python build and content/structure checks. [refresh_fixtures.py:main]

## Interface

- Run the fixture refresh utility with `python3 scripts/refresh_fixtures.py`. It rebuilds and verifies the site, then writes metadata and content-signature fixtures. [refresh_fixtures.py:main]

## Invariants

- Fixture refresh calls metadata generation and signature generation only after the build and structural checks have run. [refresh_fixtures.py:main] [test_site_structure.py:write_metadata]

## Side Effects

- Fixture refresh rewrites `tests/fixtures/metadata.json` and `tests/fixtures/content-signatures.json`. [refresh_fixtures.py:main] [test_site_structure.py:write_metadata] [signatures.py:write_fixture]

## Verification

- Fixture refresh: `python3 scripts/refresh_fixtures.py` (review resulting fixture diffs)
