#!/usr/bin/env python3
"""Refresh reviewed article text and metadata fixtures after catalog edits."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import signatures  # noqa: E402
import test_site_structure  # noqa: E402


def main() -> None:
    # Build and verify the site before rewriting either fixture.
    test_site_structure.write_metadata()
    signatures.write_fixture()
    print("Review the fixture diff before committing.")


if __name__ == "__main__":
    main()
