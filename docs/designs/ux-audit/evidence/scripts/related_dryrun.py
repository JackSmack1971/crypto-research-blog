#!/usr/bin/env python3
"""Write a deterministic review report for Slice 4a related-note ranking."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

import build  # noqa: E402


CATALOG_PATH = ROOT / "content" / "articles.json"
OUTPUT_PATH = ROOT / "docs" / "designs" / "ux-audit" / "evidence" / "related-dryrun.md"


def score_parts(note: dict, candidate: dict) -> tuple[int, list[str], bool, bool]:
    shared_assets = sorted(set(note["assets"]) & set(candidate["assets"]))
    same_topic = note["topic"] == candidate["topic"]
    same_type = note["research_type"] == candidate["research_type"]
    score = 2 * len(shared_assets) + int(same_topic) + int(same_type)
    return score, shared_assets, same_topic, same_type


def markdown_table(rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join("---" for _ in rows[0]) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return lines


def main() -> None:
    notes = build.load_notes()
    raw_notes = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    comparisons = []
    for note in notes:
        loaded_result = build.rank_related_notes(note, notes)
        raw_note = next(entry for entry in raw_notes if entry["slug"] == note["slug"])
        raw_result = build.rank_related_notes(raw_note, raw_notes)
        loaded_selection = (loaded_result["variant"], [entry["slug"] for entry in loaded_result["notes"]])
        raw_selection = (raw_result["variant"], [entry["slug"] for entry in raw_result["notes"]])
        if loaded_selection != raw_selection:
            comparisons.append((note["slug"], loaded_selection, raw_selection))
    if comparisons:
        details = "\n".join(
            f"{slug}: load_notes={loaded!r}; raw_catalog={raw!r}"
            for slug, loaded, raw in comparisons
        )
        raise SystemExit("Ranking differs between load_notes and raw catalog order:\n" + details)

    results = [(note, build.rank_related_notes(note, notes)) for note in notes]
    counts = {
        variant: sum(result["variant"] == variant for _, result in results)
        for variant in ("related", "latest", "none")
    }
    flagged = [note["slug"] for note, result in results if result["variant"] in {"latest", "none"}]

    lines = [
        "# Slice 4a related-note ranking dry-run",
        "",
        "| Variant | Article count |",
        "| --- | ---: |",
        f"| related | {counts['related']} |",
        f"| latest | {counts['latest']} |",
        f"| none | {counts['none']} |",
        "",
        "Flagged slugs (variant is `latest` or `none`): "
        + (", ".join(f"`{slug}`" for slug in flagged) if flagged else "none"),
        "",
        "Sanity check: selections from `load_notes()` and raw `content/articles.json` order are identical for every article.",
        "",
    ]

    for note, result in results:
        candidates = []
        for index, candidate in enumerate(notes):
            if candidate["slug"] == note["slug"]:
                continue
            score, shared, same_topic, same_type = score_parts(note, candidate)
            candidates.append((score, candidate["date"], index, candidate, shared, same_topic, same_type))
        candidates.sort(key=lambda item: (-item[0], -build.date.fromisoformat(item[1]).toordinal(), item[2]))

        lines.extend(
            [
                f"## `{note['slug']}`",
                "",
                f"- Date: {note['date']}",
                f"- Topic: `{note['topic']}`",
                f"- Research type: `{note['research_type']}`",
                f"- Assets: {', '.join(f'`{asset}`' for asset in note['assets']) if note['assets'] else 'none'}",
                f"- Selected variant: `{result['variant']}`",
                "- Sorted candidate order: "
                + (", ".join(f"`{item[3]['slug']}`" for item in candidates) if candidates else "none"),
                "- Selected notes: "
                + (", ".join(f"`{entry['slug']}`" for entry in result["notes"]) if result["notes"] else "none"),
                "",
            ]
        )
        rows = [["Position", "Candidate slug", "Score", "Shared assets (2 each)", "Same topic (+1)", "Same type (+1)"]]
        rows.extend(
            [
                str(position),
                f"`{candidate['slug']}`",
                str(score),
                ", ".join(f"`{asset}`" for asset in shared) if shared else "none",
                "yes" if same_topic else "no",
                "yes" if same_type else "no",
            ]
            for position, (score, _, _, candidate, shared, same_topic, same_type) in enumerate(candidates, start=1)
        )
        lines.extend(markdown_table(rows))
        lines.extend(["", "---", ""])

    lines.extend(
        [
            "Slice 4 Gate: Bret records approved or deferred, plus an ISO date, here.",
            "",
        ]
    )
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} for {len(notes)} articles")
    print(f"related={counts['related']} latest={counts['latest']} none={counts['none']}")
    print("flagged=" + (", ".join(flagged) if flagged else "none"))
    print("load_notes/raw_catalog selections identical for every article")


if __name__ == "__main__":
    main()
