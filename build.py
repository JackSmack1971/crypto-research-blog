#!/usr/bin/env python3
"""Build the Crypto Research static site into dist/.

No third-party packages. Run from the repository root:

    python3 build.py
"""

from __future__ import annotations

import base64
import json
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as xml_escape

from image_validation import MAX_BYTES, inspect_image

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
SITE_PATH = ROOT / "site.json"
FAVICON = ROOT / "assets" / "favicon.svg"
DESIGN_SYSTEM = ROOT / "assets" / "design-system.css"
SEARCH_SCRIPT = ROOT / "assets" / "search.js"

NETLIFY_ASSET_HEADERS = """/assets/*
  Cache-Control: public, max-age=86400, stale-while-revalidate=604800

/design-system.css
  Cache-Control: public, max-age=86400

/search.js
  Cache-Control: public, max-age=86400
"""

TITLE_SUFFIXES = (
    " | Crypto Market Analysis",
    " | Pyth Network Analysis",
    " | Independent Market Analysis",
    " | Independent Crypto Analysis",
    " | Independent Analysis",
    " — October 2026 Crypto Market Essay",
)

MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOPICS = {
    "bitcoin": "Bitcoin",
    "market-structure": "Market Structure",
    "liquidity": "Liquidity",
    "tokenomics": "Tokenomics",
    "protocol-research": "Protocol Research",
    "risk-verification": "Risk & Verification",
}
RESEARCH_TYPES = {
    "market-snapshot": "Market Snapshot",
    "investigative-analysis": "Investigative Analysis",
    "token-due-diligence": "Token Due Diligence",
}
ASSET_RE = re.compile(r"^[A-Z0-9]{2,12}$")


def die(message: str) -> None:
    raise SystemExit(f"error: {message}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        die(f"{path.relative_to(ROOT)} is not valid JSON ({exc})")


class MetaCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.metas: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "meta":
            self.metas.append({k.lower(): (v or "") for k, v in attrs})


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if self.skip == 0:
            self.parts.append(data)


class ImgCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            values = {k.lower(): (v or "") for k, v in attrs}
            if values.get("src"):
                self.srcs.append(values["src"])


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []
        self.css_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): (v or "") for k, v in attrs}
        if tag in ("a", "link") and values.get("href"):
            self.hrefs.append(values["href"])
        if tag in ("img", "script", "source", "video", "audio") and values.get("src"):
            self.hrefs.append(values["src"])
        if tag == "link" and values.get("imagesrcset"):
            self.css_urls.extend(_srcset_urls(values["imagesrcset"]))
        if values.get("srcset"):
            self.css_urls.extend(_srcset_urls(values["srcset"]))
        style = values.get("style") or ""
        self.css_urls.extend(_css_urls(style))

    def handle_data(self, data: str) -> None:
        return


def _css_urls(css: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", css)]


def _srcset_urls(srcset: str) -> list[str]:
    urls = []
    for part in srcset.split(","):
        piece = part.strip().split()
        if piece:
            urls.append(piece[0])
    return urls


def visible_text(html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    parser.close()
    return " ".join("".join(parser.parts).split())


def image_srcs(html: str) -> list[str]:
    parser = ImgCollector()
    parser.feed(html)
    parser.close()
    return parser.srcs


def head_html(html: str) -> str:
    match = re.search(r"</head>", html, flags=re.I)
    if not match:
        die("article is missing </head>")
    return html[: match.end()]


def document_title(html: str) -> str:
    match = re.search(r"<title\b[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    if not match:
        die("article is missing a <title>")
    title = " ".join(match.group(1).split())
    for suffix in TITLE_SUFFIXES:
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()
    if not title:
        die("article <title> is empty")
    return title


def meta_values(html: str, key: str) -> list[str]:
    head = head_html(html)
    parser = MetaCollector()
    parser.feed(head)
    parser.close()
    found = []
    for meta in parser.metas:
        name = (meta.get("name") or meta.get("property") or "").lower()
        if name == key.lower() and meta.get("content"):
            found.append(" ".join(meta["content"].split()))
    return found


def pretty_date(iso: str) -> str:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", iso):
        die(f"date must be YYYY-MM-DD, got {iso!r}")
    try:
        parsed = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        die(f"date must be YYYY-MM-DD, got {iso!r}")
    return f"{MONTHS[parsed.month - 1]} {parsed.day}, {parsed.year}"


def site_url(site: dict) -> str:
    url = str(site.get("url") or "").strip().rstrip("/")
    if not url.startswith("https://"):
        die("site.json url must be an https URL with no trailing path issues")
    return url


def load_site() -> dict:
    site = load_json(SITE_PATH)
    if not isinstance(site, dict):
        die("site.json must be an object")
    title = str(site.get("title") or "").strip()
    if not title:
        die("site.json title is empty")
    site["title"] = title
    site["tagline"] = str(site.get("tagline") or "").strip()
    site["description"] = str(site.get("description") or "").strip()
    if not site["description"]:
        die("site.json description is empty")
    site["home_title"] = str(site.get("home_title") or title).strip() or title
    site["language"] = str(site.get("language") or "en").strip() or "en"
    site["url"] = site_url(site)
    guid_origin = str(site.get("rss_guid_origin") or site["url"]).strip().rstrip("/")
    if not guid_origin.startswith("https://"):
        die("site.json rss_guid_origin must be an https URL")
    site["rss_guid_origin"] = guid_origin
    featured_slug = str(site.get("featured_slug") or "").strip()
    if featured_slug and not SLUG_RE.fullmatch(featured_slug):
        die("site.json featured_slug must be a valid article slug")
    site["featured_slug"] = featured_slug
    return site


def featured_image(entry: dict, slug: str) -> dict | None:
    """Validate the optional social image and return normalized metadata."""
    name = str(entry.get("image") or "").strip()
    if not name:
        return None
    if not re.fullmatch(r"assets/featured/[a-z0-9][a-z0-9-]*\.(?:jpg|jpeg|png|webp)", name):
        die(f"{slug} image path must be under assets/featured/ and use a safe filename")
    path = ROOT / name
    if not path.is_file():
        die(f"{slug} missing featured image: {name}")
    if path.stat().st_size > MAX_BYTES:
        die(f"{slug} featured image exceeds the 8 MiB inspection limit: {name}")
    raw = path.read_bytes()
    ext = path.suffix.lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png" if ext == ".png" else "image/webp"
    try:
        intrinsic = inspect_image(raw, mime)
    except (ValueError, IndexError, OverflowError) as error:
        die(f"{slug} invalid featured image {name}: {error}")
    alt = str(entry.get("image_alt") or "").strip()
    if not alt:
        die(f"{slug} image_alt is required")
    width, height = entry.get("image_width", 1200), entry.get("image_height", 630)
    if type(width) is not int or type(height) is not int or (width, height) != (1200, 630):
        die(f"{slug} image dimensions must be 1200 x 630")
    if intrinsic != (width, height):
        die(f"{slug} declared image dimensions disagree with intrinsic dimensions")
    if entry.get("image_mime_type") and entry["image_mime_type"] != mime:
        die(f"{slug} image_mime_type disagrees with image extension")
    return {"path": name, "alt": alt, "width": width, "height": height, "mime": mime}


def load_notes() -> list[dict]:
    raw = load_json(CONTENT / "articles.json")
    if not isinstance(raw, list) or not raw:
        die("content/articles.json must be a non-empty list")
    notes = []
    seen: set[str] = set()
    for index, entry in enumerate(raw, start=1):
        if not isinstance(entry, dict):
            die(f"articles.json item {index} must be an object")
        topic = str(entry.get("topic") or "").strip()
        research_type = str(entry.get("research_type") or "").strip()
        assets = entry.get("assets")
        if topic not in TOPICS:
            die(f"article {index} topic must be one of: {', '.join(TOPICS)}")
        if research_type not in RESEARCH_TYPES:
            die(f"article {index} research_type must be one of: {', '.join(RESEARCH_TYPES)}")
        if not isinstance(assets, list) or any(
            not isinstance(asset, str) or not ASSET_RE.fullmatch(asset)
            for asset in assets
        ):
            die(f"article {index} assets must be an array of uppercase ticker symbols")
        if len(set(assets)) != len(assets):
            die(f"article {index} assets must not contain duplicate tickers")
        slug = str(entry.get("slug") or "").strip()
        source_name = str(entry.get("source") or "").strip()
        date = str(entry.get("date") or "").strip()
        if not SLUG_RE.fullmatch(slug):
            die(f"invalid slug {slug!r}; use lowercase words separated by hyphens")
        if slug in seen:
            die(f"duplicate slug {slug}")
        seen.add(slug)
        pretty_date(date)
        source = (CONTENT / source_name).resolve()
        try:
            source.relative_to(CONTENT.resolve())
        except ValueError:
            die(f"{slug} source escapes content/")
        if not source.is_file():
            die(f"missing article file for {slug}: content/{source_name}")
        html = source.read_text(encoding="utf-8")
        if not re.search(r"<body\b", html, flags=re.I):
            die(f"{slug} is missing <body>")
        # Optional real edit date. Empty means "never edited since publication";
        # never fill it from the build date.
        updated = str(entry.get("updated") or "").strip()
        if updated:
            pretty_date(updated)
            if updated < date:
                die(f"{slug} updated date is earlier than its publication date")
        title = str(entry.get("title") or "").strip() or document_title(html)
        descriptions = meta_values(html, "description")
        dek = str(entry.get("dek") or "").strip() or (descriptions[0] if descriptions else "")
        if not dek:
            die(f"{slug} needs a dek or a meta description")
        collapsed = visible_text(html)
        if str(entry.get("dek") or "").strip() and dek not in collapsed:
            die(f"{slug} dek was not found in the article text; copy it from the piece")
        notes.append(
            {
                "slug": slug,
                "source": source,
                "date": date,
                "updated": updated,
                "title": title,
                "dek": dek,
                "description": descriptions[0] if descriptions else dek,
                "author": (meta_values(html, "author") or [None])[0],
                "html": html,
                "image": featured_image(entry, slug),
                "topic": topic,
                "topic_label": TOPICS.get(topic, "Research"),
                "assets": assets,
                "research_type": research_type,
                "research_type_label": RESEARCH_TYPES.get(research_type, "Research"),
            }
        )
    notes.sort(key=lambda note: note["date"], reverse=True)
    return notes


def select_featured(notes: list[dict], site: dict) -> dict:
    slug = site["featured_slug"]
    if slug:
        for note in notes:
            if note["slug"] == slug:
                return note
        die(f"site.json featured_slug does not match an article: {slug}")
    return notes[0]


def json_ld(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{payload}</script>'


LD_JSON_RE = re.compile(
    r"<script\b(?=[^>]*\btype\s*=\s*([\"'])application/ld\+json\1)[^>]*>(.*?)</script\s*>",
    re.I | re.S,
)


def blog_postings(data):
    if isinstance(data, list):
        return [post for item in data for post in blog_postings(item)]
    if not isinstance(data, dict):
        return []
    types = data.get("@type", [])
    if isinstance(types, str):
        types = [types]
    found = [data] if "BlogPosting" in types else []
    return found + blog_postings(data.get("@graph", []))


def existing_blog_postings(html: str, slug: str) -> list[dict]:
    found = []
    for match in LD_JSON_RE.finditer(head_html(html)):
        try:
            found.extend(blog_postings(json.loads(match.group(2))))
        except (ValueError, TypeError):
            die(f"{slug} has invalid JSON-LD")
    if len(found) > 1:
        die(f"{slug} has multiple BlogPosting entities; keep one article identity")
    return found


def has_schema_type(html: str, schema_type: str, slug: str) -> bool:
    def contains(data) -> bool:
        if isinstance(data, list):
            return any(contains(item) for item in data)
        if not isinstance(data, dict):
            return False
        types = data.get("@type", [])
        if isinstance(types, str):
            types = [types]
        return schema_type in types or contains(data.get("@graph", []))

    for match in LD_JSON_RE.finditer(head_html(html)):
        try:
            if contains(json.loads(match.group(2))):
                return True
        except (ValueError, TypeError):
            die(f"{slug} has invalid JSON-LD")
    return False


def article_posting(note: dict, site: dict) -> dict:
    url = f"{site['url']}/{note['slug']}/"
    title, description = note["title"], note["description"]
    author = note["author"] or site["title"]
    posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": note["date"],
        "dateModified": note["updated"] or note["date"],
        "mainEntityOfPage": url,
        "url": url,
        "author": {"@type": "Person" if note["author"] else "Organization", "name": author},
        "publisher": {
            "@type": "Organization",
            "name": site["title"],
            "logo": {
                "@type": "ImageObject",
                "url": site["url"] + "/favicon.svg",
            },
        },
    }
    if note["image"]:
        posting["image"] = f"{site['url']}/{note['image']['path']}"
    return posting


def augment_article_schema(html: str, note: dict, site: dict) -> str:
    if not existing_blog_postings(html, note["slug"]):
        return html
    defaults = article_posting(note, site)

    def augment(match):
        data = json.loads(match.group(2))
        posts = blog_postings(data)
        if not posts:
            return match.group(0)
        for key, value in defaults.items():
            posts[0].setdefault(key, value)
        publisher = posts[0].get("publisher")
        if isinstance(publisher, dict):
            publisher.setdefault("logo", defaults["publisher"]["logo"])
        # Registered artwork is the authoritative social image.
        if note["image"]:
            posts[0]["image"] = defaults["image"]
        if note["updated"]:
            posts[0]["dateModified"] = note["updated"]
        return json_ld(data)

    # Only head scripts are publication metadata; preserve article scripts verbatim.
    end = re.search(r"</head>", html, flags=re.I).start()
    return LD_JSON_RE.sub(augment, html[:end]) + html[end:]


def article_breadcrumbs(note: dict, site: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": site["url"] + "/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": note["topic_label"],
                "item": f"{site['url']}/topics/{note['topic']}/",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": note["title"],
                "item": f"{site['url']}/{note['slug']}/",
            },
        ],
    }


def article_extra_head(note: dict, site: dict) -> str:
    html = note["html"]
    head = head_html(html).lower()
    url = f"{site['url']}/{note['slug']}/"
    title = note["title"]
    description = note["description"]
    parts = [
        '<link rel="stylesheet" href="../design-system.css">',
    ]
    if 'rel="canonical"' not in head and "rel='canonical'" not in head:
        parts.append(f'<link rel="canonical" href="{escape(url, quote=True)}">')
    if "application/rss+xml" not in head:
        parts.append(
            f'<link rel="alternate" type="application/rss+xml" title="{escape(site["title"], quote=True)}" href="../feed.xml">'
        )
    if 'rel="icon"' not in head and "rel='icon'" not in head:
        parts.append('<link rel="icon" href="../favicon.svg" type="image/svg+xml">')
    if "og:site_name" not in head:
        parts.append(
            f'<meta property="og:site_name" content="{escape(site["title"], quote=True)}">'
        )
    if "og:type" not in head:
        parts.append('<meta property="og:type" content="article">')
    if "og:title" not in head:
        parts.append(f'<meta property="og:title" content="{escape(title, quote=True)}">')
    if "og:description" not in head:
        parts.append(
            f'<meta property="og:description" content="{escape(description, quote=True)}">'
        )
    if "og:url" not in head:
        parts.append(f'<meta property="og:url" content="{escape(url, quote=True)}">')
    if note["image"]:
        image = note["image"]
        image_url = f"{site['url']}/{image['path']}"
        for tag in ("og:image", "og:image:secure_url", "og:image:type", "og:image:width", "og:image:height", "og:image:alt", "twitter:image"):
            if meta_values(html, tag):
                die(f"{note['slug']} already defines {tag}; remove conflicting source metadata")
        existing_card = meta_values(html, "twitter:card")
        if existing_card and existing_card != ["summary_large_image"]:
            die(f"{note['slug']} twitter:card conflicts with featured image")
        for key, value in (("og:image", image_url), ("og:image:secure_url", image_url), ("og:image:type", image["mime"]), ("og:image:width", str(image["width"])), ("og:image:height", str(image["height"])), ("og:image:alt", image["alt"])):
            parts.append(f'<meta property="{key}" content="{escape(value, quote=True)}">')
        parts.append(f'<meta name="twitter:image" content="{escape(image_url, quote=True)}">')
    if "twitter:card" not in head:
        parts.append(f'<meta name="twitter:card" content="{"summary_large_image" if note["image"] else "summary"}">')
        parts.append(f'<meta name="twitter:title" content="{escape(title, quote=True)}">')
        parts.append(
            f'<meta name="twitter:description" content="{escape(description, quote=True)}">'
        )
    if not existing_blog_postings(html, note["slug"]):
        parts.append(json_ld(article_posting(note, site)))
    if not has_schema_type(html, "BreadcrumbList", note["slug"]):
        parts.append(json_ld(article_breadcrumbs(note, site)))
    return "\n".join(parts) + "\n"


def article_outline(html: str) -> tuple[str, list[tuple[str, str]]]:
    """Add collision-free heading anchors; leave scripts and existing IDs verbatim."""
    offsets = [0]
    for line in html.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    class Sections(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.ids = set()
            self.headings = []
            self.current = None

        def position(self):
            line, column = self.getpos()
            return offsets[line - 1] + column

        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            if values.get("id"):
                self.ids.add(values["id"])
            if tag == "h2":
                end = self.position() + len(self.get_starttag_text())
                self.current = (end, values.get("id"))

        def handle_endtag(self, tag):
            if tag == "h2" and self.current:
                end, target = self.current
                title = visible_text(html[end:self.position()])
                if title:
                    self.headings.append((end, target, title))
                self.current = None

    parser = Sections()
    parser.feed(html)
    parser.close()
    outline, insertions = [], []
    for end, target, title in parser.headings:
        if not target:
            target = f"cr-section-{len(outline) + 1}"
            while target in parser.ids:
                target += "-section"
            parser.ids.add(target)
            insertions.append((end - 1, f' id="{target}"'))
        outline.append((target, title))
    for position, attributes in reversed(insertions):
        html = html[:position] + attributes + html[position:]
    return html, outline


def article_bar(site: dict, note: dict, outline: list[tuple[str, str]]) -> str:
    title = escape(site["title"])
    links = "".join(
        f'<li><a href="#{escape(target, quote=True)}">{escape(label)}</a></li>'
        for target, label in outline
    )
    guide = (
        '<details class="cr-outline"><summary>In this investigation</summary>'
        f'<ol>{links}</ol></details>' if links else ""
    )
    updated_line = (
        f'<time datetime="{note["updated"]}">Updated {pretty_date(note["updated"])}</time>'
        if note.get("updated")
        else ""
    )
    return (
        '<nav id="cr-sitebar" aria-label="Site">'
        '<div class="cr-sitebar-inner">'
        f'<a class="cr-home" href="../"><span class="cr-monogram" aria-hidden="true">IMN</span>{title}</a>'
        '<a class="cr-all" href="../#notes">Research archive <span class="cr-arrow" aria-hidden="true"></span></a>'
        '</div><div class="cr-context">'
        f'<span>{escape(note["topic_label"])}</span>'
        f'<span>{escape(note["research_type_label"])}</span>'
        f'<time datetime="{note["date"]}">{pretty_date(note["date"])}</time>'
        f'{updated_line}'
        f'{guide}</div></nav>'
    )


RELATED_LINKS = 3
# Twice the average inbound count (RELATED_LINKS). Stops one article becoming a
# hub for everything without forcing irrelevant links.
RELATED_MAX_INBOUND = 2 * RELATED_LINKS


def _relatedness(note: dict, candidate: dict) -> int:
    shared_assets = len(set(note["assets"]) & set(candidate["assets"]))
    return (
        2 * shared_assets
        + (1 if candidate["topic"] == note["topic"] else 0)
        + (1 if candidate["research_type"] == note["research_type"] else 0)
    )


def _relevance_key(note: dict, candidate: dict, cidx: int):
    """Display order and base preference: relevance, newest, then catalog order."""
    return (
        -_relatedness(note, candidate),
        -date.fromisoformat(candidate["date"]).toordinal(),
        cidx,
    )


def balanced_related_indexes(notes: list[dict]) -> list[list[int]]:
    """Choose related notes for every article, deterministically.

    1. In catalog order, each article takes its best-ranked candidates, where
       equal relevance prefers the candidate with fewer inbound links so far,
       and candidates already at RELATED_MAX_INBOUND are skipped.
    2. Any article still without an inbound link replaces the weakest slot of
       its most relevant source whose current target keeps at least one other
       inbound link.
    A note is never linked to another entry with its own slug.
    Returns, per input index, the chosen candidate indexes sorted for display.
    """
    n = len(notes)
    slugs = [note["slug"] for note in notes]
    want = min(RELATED_LINKS, len({*slugs}) - 1)
    inbound = [0] * n
    chosen: list[list[int]] = [[] for _ in range(n)]
    for i, note in enumerate(notes):
        order = sorted(
            (c for c in range(n) if slugs[c] != slugs[i]),
            key=lambda c: (-_relatedness(note, notes[c]), inbound[c])
            + _relevance_key(note, notes[c], c)[1:],
        )
        under = [c for c in order if inbound[c] < RELATED_MAX_INBOUND]
        picks = under[:want]
        if len(picks) < want:  # cap too tight for a tiny catalog: fill anyway
            picks += [c for c in order if c not in picks][: want - len(picks)]
        chosen[i] = picks
        for c in picks:
            inbound[c] += 1
    for orphan in range(n):
        if inbound[orphan] or want == 0:
            continue
        sources = sorted(
            (s for s in range(n) if slugs[s] != slugs[orphan]),
            key=lambda s: _relevance_key(notes[s], notes[orphan], orphan),
        )
        for s in sources:
            donors = [c for c in chosen[s] if inbound[c] > 1]
            if not donors:
                continue
            drop = min(
                donors,
                key=lambda c: (
                    _relatedness(notes[s], notes[c]),
                    -inbound[c],
                    -chosen[s].index(c),
                ),
            )
            chosen[s][chosen[s].index(drop)] = orphan
            inbound[drop] -= 1
            inbound[orphan] += 1
            break
    return [
        sorted(chosen[i], key=lambda c: _relevance_key(notes[i], notes[c], c))
        for i in range(n)
    ]


def rank_related_notes(note: dict, notes: list[dict]) -> dict:
    if not any(c["slug"] != note["slug"] for c in notes):
        return {"variant": "none", "notes": []}
    position = next((i for i, c in enumerate(notes) if c is note), None)
    if position is None:
        position = next((i for i, c in enumerate(notes) if c["slug"] == note["slug"]), None)
    if position is None:
        notes = notes + [note]
        position = len(notes) - 1
    picks = balanced_related_indexes(notes)[position]
    selected = [notes[c] for c in picks]
    top = max(_relatedness(note, c) for c in selected) if selected else 0
    variant = "related" if top > 0 else "latest"
    return {"variant": variant, "notes": selected}


def render_related_notes(note: dict, notes: list[dict]) -> str:
    result = rank_related_notes(note, notes)
    variant = result["variant"]
    parts = ['<nav id="cr-related" aria-label="More notes"><div class="cr-related-inner">']
    if variant != "none":
        heading = "Related notes" if variant == "related" else "Latest notes"
        parts.extend((f"<h2>{escape(heading)}</h2>", "<ul>"))
        for related in result["notes"]:
            slug = escape(str(related["slug"]), quote=True)
            title = escape(str(related["title"]))
            date_value = escape(str(related["date"]), quote=True)
            parts.append(
                f'<li><a href="../{slug}/">{title}</a> '
                f'<time datetime="{date_value}">{date_value}</time></li>'
            )
        parts.append("</ul>")
    parts.extend(('<a href="../">All notes</a>', "</div></nav>"))
    return "".join(parts)


SCROLL_REGION_LABELS = {
    "aero-at-0-68": ("table-scroll", "AERO unlock data table"),
    "bitcoin-buying-imbalance": (
        "tablewrap",
        "Bitcoin buying imbalance data table",
    ),
    "token-unlock-liquidity-illusion-90-day-calendar": (
        "scroll",
        "90-day token unlock calendar data table",
    ),
}


def add_scroll_region_accessibility(slug: str, html: str) -> str:
    target = SCROLL_REGION_LABELS.get(slug)
    if target is None:
        return html

    class_name, label = target
    matches = []
    for match in re.finditer(r"<div\b[^>]*>", html, flags=re.I):
        class_match = re.search(r'\bclass=["\']([^"\']*)["\']', match.group(0), flags=re.I)
        if class_match and class_name in class_match.group(1).split():
            matches.append(match)
    if len(matches) != 1:
        die(f"{slug} must contain exactly one .{class_name} wrapper")

    match = matches[0]
    opening_tag = match.group(0)
    if re.search(r'\b(?:tabindex|role|aria-label)\s*=', opening_tag, flags=re.I):
        die(f"{slug} .{class_name} wrapper already has accessibility attributes")
    accessible_tag = (
        opening_tag[:-1]
        + f' tabindex="0" role="region" aria-label="{escape(label, quote=True)}">'
    )
    return html[: match.start()] + accessible_tag + html[match.end() :]


ROBOTS_CONTENT = "index,follow,max-image-preview:large"
ROBOTS_META = f'<meta name="robots" content="{ROBOTS_CONTENT}">'


def normalize_robots_meta(html: str, slug: str) -> str:
    """Emit one consistent indexable robots meta per article.

    Source documents are never edited: any author-supplied robots meta is
    replaced in the generated output. A source asking for noindex or nofollow
    is a deliberate editorial choice and fails the build rather than being
    silently overridden.
    """
    head_end = re.search(r"</head>", html, flags=re.I)
    if not head_end:
        die(f"{slug} is missing </head>")
    head, rest = html[: head_end.start()], html[head_end.start() :]
    pattern = r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>'
    for tag in re.findall(pattern, head, flags=re.I):
        content = re.search(r'content=["\']([^"\']*)["\']', tag, flags=re.I)
        if content and re.search(r"no(index|follow)", content.group(1), flags=re.I):
            die(f"{slug} source robots meta restricts indexing; resolve editorially")
    head = re.sub(pattern, "", head, flags=re.I)
    return head + ROBOTS_META + rest


def render_article(
    note: dict, site: dict, notes: list[dict] | None = None
) -> str:
    if notes is None:
        notes = [note]
    html = note["html"]
    article_url = f'{site["url"]}/{note["slug"]}/'
    # A configured domain change must replace canonicals embedded in source
    # articles so every generated route agrees with the site's public origin.
    html = re.sub(
        r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>',
        f'<link rel="canonical" href="{escape(article_url, quote=True)}">',
        html,
        count=1,
        flags=re.I,
    )
    html = normalize_robots_meta(html, note["slug"])
    html = augment_article_schema(html, note, site)
    html = add_scroll_region_accessibility(note["slug"], html)
    extra = article_extra_head(dict(note, html=html), site)
    head_match = re.search(r"</head>", html, flags=re.I)
    if not head_match:
        die(f"{note['slug']} is missing </head>")
    html = html[: head_match.start()] + extra + html[head_match.start() :]
    html, outline = article_outline(html)
    body_match = re.search(r"<body\b[^>]*>", html, flags=re.I)
    if not body_match:
        die(f"{note['slug']} is missing <body>")
    # Scope the shared reading layer without changing source documents.
    opening = body_match.group(0)
    class_pattern = r"(\sclass\s*=\s*)([\"'])(.*?)\2"
    if re.search(class_pattern, opening, flags=re.I | re.S):
        opening = re.sub(
            class_pattern,
            lambda match: f'{match[1]}{match[2]}cr-article {match[3]}{match[2]}',
            opening, count=1, flags=re.I | re.S,
        )
    else:
        opening = opening[:-1] + ' class="cr-article">'
    html = html[:body_match.start()] + opening + html[body_match.end():]
    body_match = re.search(r"<body\b[^>]*>", html, flags=re.I)
    bar = article_bar(site, note, outline)
    related = render_related_notes(note, notes)
    body_end = re.search(r"</body>", html, flags=re.I)
    if not body_end:
        die(f"{note['slug']} is missing </body>")
    html = html[: body_match.end()] + bar + html[body_match.end() :]
    body_end = re.search(r"</body>", html, flags=re.I)
    return html[: body_end.start()] + related + html[body_end.start() :]


def page_shell(
    site: dict,
    *,
    document_title: str,
    description: str,
    canonical: str,
    main: str,
    structured_data: dict | None = None,
    asset_base: str = "",
    indexable: bool = True,
) -> str:
    if structured_data is None:
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": document_title,
            "description": description,
            "url": canonical,
        }
    head_directives = (
        f'<link rel="canonical" href="{escape(canonical, quote=True)}">'
        if indexable
        else '<meta name="robots" content="noindex">'
    )
    return f"""<!DOCTYPE html>
<html lang="{escape(site["language"], quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#172420">
  <title>{escape(document_title)}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  {head_directives}
  <link rel="icon" href="{escape(asset_base, quote=True)}favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{escape(asset_base, quote=True)}design-system.css">
  <link rel="alternate" type="application/rss+xml" title="{escape(site["title"], quote=True)}" href="{escape(asset_base, quote=True)}feed.xml">
  <meta property="og:site_name" content="{escape(site["title"], quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(document_title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(canonical, quote=True)}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{escape(document_title, quote=True)}">
  <meta name="twitter:description" content="{escape(description, quote=True)}">
  {json_ld(structured_data)}
</head>
<body class="cr-home">
  <a class="skip" href="#main-content">Skip to main content</a>
  {main}
</body>
</html>
"""


def render_home(notes: list[dict], site: dict) -> str:
    count = len(notes)
    label = "1 investigation" if count == 1 else f"{count} investigations"
    featured = select_featured(notes, site)
    entries = []
    for note in notes:
        if note["slug"] == featured["slug"]:
            continue
        tags = "".join(f'<span>{escape(asset)}</span>' for asset in note["assets"][:3])
        entries.append(
            f"""<article class="entry" data-slug="{escape(note["slug"], quote=True)}" data-topic="{escape(note["topic"], quote=True)}" data-research-type="{escape(note["research_type"], quote=True)}" data-assets="{escape(' '.join(note["assets"]), quote=True)}">
      <a class="entry-link" href="{escape(note["slug"], quote=True)}/">
        <div class="entry-copy">
          <p class="entry-meta"><span>{escape(note["topic_label"])}</span><time datetime="{escape(note["date"], quote=True)}">{escape(pretty_date(note["date"]))}</time></p>
        <h3>{escape(note["title"])}</h3>
        <p class="dek">{escape(note["dek"])}</p>
        <p class="asset-tags">{tags}<span class="entry-type">{escape(note["research_type_label"])}</span></p>
        </div>
      </a>
    </article>"""
        )
    feature_image = featured["image"]
    feature_art = (
        f'<img src="{escape(feature_image["path"], quote=True)}" '
        f'alt="{escape(feature_image["alt"], quote=True)}" '
        f'width="{feature_image["width"]}" height="{feature_image["height"]}">'
        if feature_image
        else '<span class="feature-art-fallback" aria-hidden="true">IMN</span>'
    )
    topics = "".join(f'<option value="{key}">{escape(value)}</option>' for key, value in TOPICS.items())
    topic_links = "".join(
        f'<a href="topics/{key}/">{escape(value)}</a>'
        for key, value in TOPICS.items()
        if topic_notes(key, notes)
    )
    types = "".join(f'<option value="{key}">{escape(value)}</option>' for key, value in RESEARCH_TYPES.items())
    posts = [
        {
            "@type": "BlogPosting",
            "headline": note["title"],
            "datePublished": note["date"],
            "url": f"{site['url']}/{note['slug']}/",
            "description": note["dek"],
        }
        for note in notes
    ]
    structured_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "name": site["title"],
                "description": site["description"],
                "url": site["url"] + "/",
                "blogPost": posts,
            },
            {
                "@type": "WebSite",
                "name": site["title"],
                "url": site["url"] + "/",
            },
        ],
    }
    latest_entries = []
    for index, note in enumerate(notes[:3], 1):
        latest_entries.append(f"""<article class="latest-entry" data-latest-slug="{escape(note['slug'], quote=True)}">
          <p class="entry-meta"><span class="latest-number" aria-hidden="true">0{index}</span><time datetime="{note['date']}">{pretty_date(note['date'])}</time></p>
          <h3><a href="{escape(note['slug'], quote=True)}/">{escape(note['title'])}</a></h3>
          <p class="dek">{escape(note['dek'])}</p>
          <p class="section-label">{escape(note['research_type_label'])}</p>
        </article>""")
    main = f"""<header class="mast">
    <div class="wrap">
      <div class="topline">
        <a class="publication-mark" href="./">IMN <span>Independent research journal</span></a>
        <nav class="tools" aria-label="Publication links"><a href="./#latest">Latest</a><a href="#notes">Archive</a><a href="#methodology">Methodology</a></nav>
      </div>
      <p class="kicker">{escape(site["tagline"] or "Independent digital-asset intelligence")}</p>
      <h1>{escape(site["title"])}</h1>
      <p class="lede">{escape(site["description"])}</p>
      <div class="mast-actions"><a class="primary-link" href="#notes">Explore investigations <span class="cr-arrow" aria-hidden="true"></span></a><a href="#methodology">Our research approach <span class="cr-arrow" aria-hidden="true"></span></a></div>
      <nav class="topic-nav" aria-label="Browse by topic">{topic_links}</nav>
    </div>
  </header>
  <main id="main-content" tabindex="-1">
    <div data-feature-slot hidden></div>
    <section class="feature wrap" aria-labelledby="feature-title" data-featured-search data-slug="{escape(featured["slug"], quote=True)}" data-topic="{escape(featured["topic"], quote=True)}" data-research-type="{escape(featured["research_type"], quote=True)}" data-assets="{escape(' '.join(featured["assets"]), quote=True)}">
      <a class="feature-art" href="{escape(featured["slug"], quote=True)}/" aria-label="Read featured investigation: {escape(featured["title"], quote=True)}">{feature_art}</a>
      <div class="feature-copy">
        <p class="section-label">Featured investigation <span aria-hidden="true">/</span> {escape(featured["topic_label"])}</p>
        <h2 id="feature-title"><a href="{escape(featured["slug"], quote=True)}/">{escape(featured["title"])}</a></h2>
        <p class="dek">{escape(featured["dek"])}</p>
        <p class="entry-meta"><time datetime="{escape(featured["date"], quote=True)}">{escape(pretty_date(featured["date"]))}</time><span>{escape(featured["research_type_label"])}</span></p>
      </div>
    </section>
    <section class="latest wrap" id="latest" aria-labelledby="latest-title" data-latest-section>
      <div class="section-heading"><div><p class="section-label">The current edition</p><h2 id="latest-title">Latest research</h2></div><a href="#notes">View the full archive <span class="cr-arrow" aria-hidden="true"></span></a></div>
      <div class="latest-grid">{"".join(latest_entries)}</div>
    </section>
    <section class="archive wrap" id="notes" aria-labelledby="archive-title">
      <div class="archive-heading"><div><p class="section-label">Browse the archive</p><h2 id="archive-title">The research archive</h2></div><p class="count" data-result-count>{label}</p></div>
      <form class="filters" role="search" aria-label="Search research" data-search-form>
        <label class="search-field"><span class="sr-only">Search by topic, asset ticker, or title</span><input type="search" name="q" placeholder="Search topics, tickers, or titles" autocomplete="off"></label>
        <label><span class="sr-only">Filter by topic</span><select name="topic"><option value="">All topics</option>{topics}</select></label>
        <label><span class="sr-only">Filter by research type</span><select name="research_type"><option value="">All research types</option>{types}</select></label>
        <button type="reset">Clear</button>
      </form>
      <p class="search-status" aria-live="polite" data-search-status>{label}</p>
      <div class="archive-grid" data-archive-grid>
      {"".join(entries)}
      </div>
      <p class="empty-state" data-empty-state hidden>No investigations match those filters. Try a broader search.</p>
    </section>
    <section class="method wrap" id="methodology" aria-labelledby="method-title">
      <div class="method-intro"><p class="section-label">Methodology &amp; editorial standards</p><h2 id="method-title">Evidence first.<br>Conviction second.</h2><p>These independent market notes separate observable data from interpretation, flag uncertainty, and show what would change the thesis.</p></div>
      <div class="method-principles">
        <div><span aria-hidden="true">01</span><h3>Follow the evidence</h3><p>Read the linked sources, dated observations, and data notes alongside each investigation.</p></div>
        <div><span aria-hidden="true">02</span><h3>Keep uncertainty visible</h3><p>Distinguish reported facts from interpretations, conditional scenarios, and questions that remain unresolved.</p></div>
        <div><span aria-hidden="true">03</span><h3>Research before a trade</h3><p>A useful investigation can end with a trade idea, a failed setup, or no trade at all. Historical observations are not live market data.</p></div>
      </div>
    </section>
  </main>
  <footer>
    <div class="wrap colophon">
      <div class="footer-identity"><span class="footer-mark">IMN</span><p>{escape(site["title"])}<br><span>Independent digital-asset research. Read the evidence.</span></p></div>
      <div><a href="#notes">Research archive</a><a href="#methodology">Methodology</a><a href="feed.xml">Subscribe via RSS</a><a href="#main-content">Back to top</a></div>
    </div>
  </footer>"""
    home = page_shell(
        site,
        document_title=site["home_title"],
        description=site["description"],
        canonical=site["url"] + "/",
        main=main,
        structured_data=structured_data,
    )
    script_tag = '<script src="search.js" defer></script>'
    return home.replace("</body>", f"  {script_tag}\n</body>")


TOPIC_INTROS = {
    "bitcoin": "Bitcoin price, flow and positioning notes: what the dated evidence supports, what failed, and what remains unproven.",
    "market-structure": "Cross-market structure notes on breadth, relative strength, leverage and regulation.",
    "liquidity": "Order-book depth and small-cap liquidity: whether quoted markets can absorb real size.",
    "tokenomics": "Token supply, unlock schedules, buybacks and value capture, tested against the primary records that exist.",
    "protocol-research": "Protocol-level research into launches, products and how their economics work in practice.",
    "risk-verification": "Incident reconstructions and verification work: custody, concentration and what the record can and cannot show.",
}


def topic_notes(topic: str, notes: list[dict]) -> list[dict]:
    return [n for n in notes if n["topic"] == topic]


def render_topic_hub(topic: str, notes: list[dict], site: dict) -> str:
    label = TOPICS[topic]
    members = topic_notes(topic, notes)
    count = len(members)
    noun = "investigation" if count == 1 else "investigations"
    canonical = f"{site['url']}/topics/{topic}/"
    newest, oldest = members[0]["date"], members[-1]["date"]
    description = (
        f"{count} {label} {noun} from Independent Market Notes, "
        f"{pretty_date(oldest)} to {pretty_date(newest)}. {TOPIC_INTROS[topic]}"
    )
    entries = "\n".join(
        f"""<article class="entry">
      <a class="entry-link" href="../../{escape(n["slug"], quote=True)}/">
        <div class="entry-copy">
          <p class="entry-meta"><span>{escape(n["research_type_label"])}</span><time datetime="{escape(n["date"], quote=True)}">{escape(pretty_date(n["date"]))}</time></p>
          <h3>{escape(n["title"])}</h3>
          <p class="dek">{escape(n["dek"])}</p>
        </div>
      </a>
    </article>"""
        for n in members
    )
    others = "".join(
        f'<a href="../{key}/">{escape(value)}</a>'
        for key, value in TOPICS.items()
        if key != topic and topic_notes(key, notes)
    )
    main = f"""<header class="mast">
    <div class="wrap">
      <div class="topline">
        <a class="publication-mark" href="../../">IMN <span>Independent research journal</span></a>
        <nav class="tools" aria-label="Publication links"><a href="../../">Home</a><a href="../../#notes">Archive</a></nav>
      </div>
      <nav aria-label="Breadcrumb"><a href="../../">Home</a> / {escape(label)}</nav>
      <h1>{escape(label)}</h1>
      <p class="lede">{escape(TOPIC_INTROS[topic])}</p>
      <p class="count">{count} {noun}</p>
    </div>
  </header>
  <main id="main-content" tabindex="-1">
    <section class="archive wrap" aria-labelledby="hub-title">
      <h2 id="hub-title">All {escape(label)} notes, newest first</h2>
      <div class="archive-grid">
      {entries}
      </div>
      <nav class="topic-nav" aria-label="Other topics">{others}</nav>
    </section>
  </main>"""
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": canonical + "#page",
                "url": canonical,
                "name": f"{label} research notes",
                "description": description,
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": i,
                            "url": f"{site['url']}/{n['slug']}/",
                            "name": n["title"],
                        }
                        for i, n in enumerate(members, 1)
                    ],
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": site["url"] + "/"},
                    {"@type": "ListItem", "position": 2, "name": label, "item": canonical},
                ],
            },
        ],
    }
    return page_shell(
        site,
        document_title=f"{label} research notes \u2014 {site['title']}",
        description=description,
        canonical=canonical,
        main=main,
        structured_data=data,
        asset_base="../../",
    )


def render_404(site: dict) -> str:
    main = f"""<main id="main-content" class="wrap missing" tabindex="-1">
    <p class="kicker">Missing page</p>
    <h1>That page is not on this site.</h1>
    <p class="lede">The research notes are collected on the home page.</p>
    <p><a class="back" href="{escape(site["url"] + "/", quote=True)}">Back to {escape(site["title"])}</a></p>
  </main>"""
    return page_shell(
        site,
        document_title=f"Page not found · {site['title']}",
        description=f"That page is not on {site['title']}.",
        canonical=site["url"] + "/404.html",
        main=main,
        asset_base=site["url"] + "/",
        indexable=False,
    )


def render_feed(notes: list[dict], site: dict) -> str:
    items = []
    for note in notes:
        published = datetime.strptime(note["date"], "%Y-%m-%d").replace(
            tzinfo=timezone.utc, hour=18
        )
        link = f"{site['url']}/{note['slug']}/"
        guid = f"{site['rss_guid_origin']}/{note['slug']}/"
        items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{xml_escape(note['title'])}</title>",
                    f"      <link>{xml_escape(link)}</link>",
                    f'      <guid isPermaLink="false">{xml_escape(guid)}</guid>',
                    f"      <pubDate>{format_datetime(published)}</pubDate>",
                    f"      <description><![CDATA[{note['dek'].replace(']]>', ']]]]><![CDATA[>')}]]></description>",
                    "    </item>",
                ]
            )
        )
    self_link = f"{site['url']}/feed.xml"
    last_build = format_datetime(datetime.now(timezone.utc))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{xml_escape(site["title"])}</title>
    <link>{xml_escape(site["url"] + "/")}</link>
    <description>{xml_escape(site["description"])}</description>
    <language>{xml_escape(site["language"])}</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{xml_escape(self_link)}" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""


def render_sitemap(notes: list[dict], site: dict) -> str:
    def lastmod(note: dict) -> str:
        return note["updated"] or note["date"]

    newest = max(lastmod(note) for note in notes)
    urls = [(site["url"] + "/", newest)]
    urls.extend(
        (f"{site['url']}/topics/{key}/", topic_notes(key, notes)[0]["date"])
        for key in TOPICS
        if topic_notes(key, notes)
    )
    urls.extend((f"{site['url']}/{note['slug']}/", lastmod(note)) for note in notes)
    body = "\n".join(
        f"""  <url>
    <loc>{xml_escape(loc)}</loc>
    <lastmod>{xml_escape(lastmod)}</lastmod>
  </url>"""
        for loc, lastmod in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def render_robots(site: dict) -> str:
    return f"""User-agent: *
Allow: /

Sitemap: {site["url"]}/sitemap.xml
"""


def body_inner(html: str) -> str:
    start = re.search(r"<body\b[^>]*>", html, flags=re.I)
    end = re.search(r"</body>", html, flags=re.I)
    if not start or not end:
        die("article is missing a body")
    return html[start.end() : end.start()]


def strip_site_bar(html: str) -> str:
    stripped, count = re.subn(
        r'<nav id="cr-sitebar"[^>]*>.*?</nav>', "", html, count=1, flags=re.S
    )
    if count != 1:
        die("built article is missing the site header")
    return stripped


def strip_related_nav(html: str) -> str:
    stripped, count = re.subn(
        r'<nav id="cr-related"[^>]*>.*?</nav>', "", html, count=1, flags=re.S
    )
    if count != 1:
        die("built article is missing the related notes navigation")
    return stripped


def looks_external(url: str) -> bool:
    if url.startswith(("mailto:", "tel:", "data:", "javascript:", "#")):
        return True
    parts = urlsplit(url)
    return parts.scheme in ("http", "https")


def check_data_image(src: str, where: str) -> None:
    if not src.startswith("data:image/"):
        return
    header, sep, payload = src.partition(",")
    if not sep or "base64" not in header:
        die(f"{where} has an image data URI this build does not understand")
    try:
        raw = base64.b64decode(payload, validate=False)
    except Exception as exc:  # noqa: BLE001 - report any decode failure
        die(f"{where} has an image that does not decode ({exc})")
    if len(raw) < 24:
        die(f"{where} has an image that decoded to almost nothing")
    ok = (
        raw.startswith(b"\x89PNG\r\n\x1a\n")
        or raw.startswith(b"\xff\xd8\xff")
        or raw.startswith((b"GIF87a", b"GIF89a"))
        or (raw.startswith(b"RIFF") and raw[8:12] == b"WEBP")
    )
    if not ok:
        die(f"{where} has an image that is not a PNG, JPEG, GIF, or WebP")


def resolve_local(page: Path, url: str) -> None:
    bare = url.split("#", 1)[0].split("?", 1)[0].strip()
    if bare == "" or looks_external(url):
        if bare.startswith("data:image/"):
            check_data_image(bare, str(page.relative_to(DIST)))
        return
    if bare.startswith("//"):
        return
    if bare.startswith("/"):
        die(
            f"{page.relative_to(DIST)} links to {url}, a root-absolute path. "
            "Use a relative path so the page works under /crypto-research-blog/."
        )
    target = (page.parent / bare).resolve()
    try:
        target.relative_to(DIST.resolve())
    except ValueError:
        die(f"{page.relative_to(DIST)} links outside the site: {url}")
    if target.is_dir():
        if not (target / "index.html").is_file():
            die(f"{page.relative_to(DIST)} links to a directory without index.html: {url}")
        return
    if not target.is_file():
        die(f"{page.relative_to(DIST)} has a broken link: {url}")


def check_page_links(page: Path) -> None:
    html = page.read_text(encoding="utf-8")
    parser = LinkCollector()
    parser.feed(html)
    parser.close()
    for href in parser.hrefs:
        resolve_local(page, href)
    for url in parser.css_urls:
        resolve_local(page, url)
    for src in image_srcs(html):
        if src.startswith("data:image/"):
            check_data_image(src, str(page.relative_to(DIST)))


def verify(notes: list[dict]) -> None:
    index = (DIST / "index.html").read_text(encoding="utf-8")
    if f">{escape(notes[0]['title'])}<" not in index and escape(notes[0]["title"]) not in index:
        die("home page is missing the newest title")
    for note in notes:
        href = f'href="{note["slug"]}/"'
        if href not in index:
            die(f"home page does not link to {note['slug']}")
        page = DIST / note["slug"] / "index.html"
        if not page.is_file():
            die(f"missing built page for {note['slug']}")
        built = page.read_text(encoding="utf-8")
        if 'href="../"' not in built:
            die(f"{note['slug']} is missing the link back home")
        body = body_inner(built)
        if len(re.findall(r'<nav id="cr-sitebar"(?=[\s>])', body)) != 1:
            die(f"{note['slug']} must contain exactly one site header")
        if len(re.findall(r'<nav id="cr-related"(?=[\s>])', body)) != 1:
            die(f"{note['slug']} must contain exactly one related notes navigation")
        if not body.lstrip().startswith('<nav id="cr-sitebar"'):
            die(f"{note['slug']} site header is not the first body child")
        if not re.search(r'<nav id="cr-related"[^>]*>.*?</nav>\s*$', body, flags=re.S):
            die(f"{note['slug']} related notes navigation is not the last body child")
        related_match = re.search(r'<nav id="cr-related"[^>]*>.*?</nav>', body, flags=re.S)
        related_parser = LinkCollector()
        related_parser.feed(related_match.group(0))
        related_parser.close()
        expected_hrefs = [f"../{item['slug']}/" for item in rank_related_notes(note, notes)["notes"]]
        expected_hrefs.append("../")
        if related_parser.hrefs != expected_hrefs:
            die(f"{note['slug']} related notes links do not match the catalog ranking")
        for href in related_parser.hrefs:
            resolve_local(page, href)
        visible_body = strip_related_nav(strip_site_bar(body))
        if visible_text(visible_body) != visible_text(body_inner(note["html"])):
            die(f"{note['slug']} body text changed during the build")
        if note["image"]:
            img = note["image"]
            image_url = f"{load_site()['url']}/{img['path']}"
            for key, expected in (("og:image", image_url), ("og:image:alt", img["alt"]), ("og:image:width", str(img["width"])), ("og:image:height", str(img["height"])), ("twitter:image", image_url), ("twitter:card", "summary_large_image")):
                if meta_values(built, key) != [expected]:
                    die(f"{note['slug']} incorrect {key} metadata")
            if not (DIST / img["path"]).is_file():
                die(f"{note['slug']} featured image was not copied")
        if image_srcs(built) != image_srcs(note["html"]):
            die(f"{note['slug']} images changed during the build")
        original_title = re.search(r"<title\b[^>]*>.*?</title>", note["html"], flags=re.I | re.S)
        if original_title and original_title.group(0) not in built:
            die(f"{note['slug']} document title was rewritten")
    for page in DIST.rglob("*.html"):
        check_page_links(page)
    ET.parse(DIST / "feed.xml")
    ET.parse(DIST / "sitemap.xml")
    home_hrefs = re.findall(r'href="([^"]+)"', index)
    for href in home_hrefs:
        if href.endswith("/") and not href.startswith(("http://", "https://", "../")):
            slug = href.strip("/")
            if not (DIST / slug / "index.html").is_file():
                die(f"home page link does not resolve: {href}")


def main() -> None:
    site = load_site()
    notes = load_notes()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copyfile(FAVICON, DIST / "favicon.svg")
    shutil.copyfile(DESIGN_SYSTEM, DIST / "design-system.css")
    shutil.copyfile(SEARCH_SCRIPT, DIST / "search.js")
    for relative in sorted({n["image"]["path"] for n in notes if n["image"]}):
        target = DIST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    inline_src = ROOT / "assets" / "inline"
    if inline_src.is_dir():
        shutil.copytree(inline_src, DIST / "inline")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / "_headers").write_text(NETLIFY_ASSET_HEADERS, encoding="utf-8")
    for note in notes:
        out = DIST / note["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_article(note, site, notes), encoding="utf-8")
    for key in TOPICS:
        if topic_notes(key, notes):
            hub_out = DIST / "topics" / key / "index.html"
            hub_out.parent.mkdir(parents=True, exist_ok=True)
            hub_out.write_text(render_topic_hub(key, notes, site), encoding="utf-8")
    (DIST / "index.html").write_text(render_home(notes, site), encoding="utf-8")
    (DIST / "404.html").write_text(render_404(site), encoding="utf-8")
    (DIST / "feed.xml").write_text(render_feed(notes, site), encoding="utf-8")
    (DIST / "sitemap.xml").write_text(render_sitemap(notes, site), encoding="utf-8")
    (DIST / "robots.txt").write_text(render_robots(site), encoding="utf-8")
    index_data = []
    for note in notes:
        index_data.append(
            {
                "slug": note["slug"],
                "title": note["title"],
                "dek": note["dek"],
                "topic": note["topic"],
                "assets": note["assets"],
                "research_type": note["research_type"],
                "date": note["date"],
            }
        )
    (DIST / "search-index.json").write_text(json.dumps(index_data, ensure_ascii=False).replace("<", "\\u003c"), encoding="utf-8")
    verify(notes)
    print(f"Built {len(notes)} notes → {DIST.relative_to(ROOT)}")
    for note in notes:
        print(f"  {note['date']}  {note['slug']}")


if __name__ == "__main__":
    main()
