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
from datetime import datetime, timedelta, timezone
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
    author = note["author"] or site["title"]
    posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "datePublished": note["date"],
        "mainEntityOfPage": url,
        "url": url,
        "author": {"@type": "Person" if note["author"] else "Organization", "name": author},
        "publisher": {"@type": "Organization", "name": site["title"]},
    }
    if note["image"]:
        posting["image"] = f"{site['url']}/{note['image']['path']}"
    if "application/ld+json" not in head:
        parts.append(json_ld(posting))
    return "\n".join(parts) + "\n"


def article_bar(site: dict) -> str:
    title = escape(site["title"])
    return (
        '<nav id="cr-sitebar" aria-label="Site">'
        '<div class="cr-sitebar-inner">'
        f'<a class="cr-home" href="../">{title}</a>'
        '<a class="cr-all" href="../">All notes</a>'
        "</div></nav>"
    )


def render_article(note: dict, site: dict) -> str:
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
    extra = article_extra_head(note, site)
    head_match = re.search(r"</head>", html, flags=re.I)
    if not head_match:
        die(f"{note['slug']} is missing </head>")
    html = html[: head_match.start()] + extra + html[head_match.start() :]
    body_match = re.search(r"<body\b[^>]*>", html, flags=re.I)
    if not body_match:
        die(f"{note['slug']} is missing <body>")
    bar = article_bar(site)
    return html[: body_match.end()] + bar + html[body_match.end() :]


def page_shell(
    site: dict,
    *,
    document_title: str,
    description: str,
    canonical: str,
    main: str,
    structured_data: dict | None = None,
    asset_base: str = "",
) -> str:
    if structured_data is None:
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": document_title,
            "description": description,
            "url": canonical,
        }
    return f"""<!DOCTYPE html>
<html lang="{escape(site["language"], quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#172420">
  <title>{escape(document_title)}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="{escape(canonical, quote=True)}">
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
        image = note["image"]
        artwork = (
            f'<img src="{escape(image["path"], quote=True)}" '
            f'alt="{escape(image["alt"], quote=True)}" width="{image["width"]}" '
            f'height="{image["height"]}" loading="lazy">'
            if image
            else '<span class="card-art-fallback" aria-hidden="true">IMN</span>'
        )
        tags = "".join(f'<span>{escape(asset)}</span>' for asset in note["assets"][:3])
        entries.append(
            f"""<article class="entry" data-slug="{escape(note["slug"], quote=True)}" data-topic="{escape(note["topic"], quote=True)}" data-research-type="{escape(note["research_type"], quote=True)}" data-assets="{escape(' '.join(note["assets"]), quote=True)}">
      <a class="entry-link" href="{escape(note["slug"], quote=True)}/">
        <div class="entry-art">{artwork}</div>
        <div class="entry-copy">
          <p class="entry-meta"><span>{escape(note["topic_label"])}</span><time datetime="{escape(note["date"], quote=True)}">{escape(pretty_date(note["date"]))}</time></p>
        <h2>{escape(note["title"])}</h2>
        <p class="dek">{escape(note["dek"])}</p>
        <p class="asset-tags">{tags}</p>
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
        f'<a href="?topic={key}#notes">{escape(value)}</a>'
        for key, value in TOPICS.items()
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
        "@type": "Blog",
        "name": site["title"],
        "description": site["description"],
        "url": site["url"] + "/",
        "blogPost": posts,
    }
    tagline = f'<p class="kicker">{escape(site["tagline"])}</p>' if site["tagline"] else ""
    main = f"""<header class="mast">
    <div class="wrap">
      <div class="topline">
        {tagline}
        <nav class="tools" aria-label="Publication links"><a href="#notes">Research archive</a><a href="feed.xml">RSS</a></nav>
      </div>
      <h1>{escape(site["title"])}</h1>
      <p class="lede">{escape(site["description"])}</p>
      <nav class="topic-nav" aria-label="Browse by topic">{topic_links}</nav>
    </div>
  </header>
  <main id="main-content">
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
    <section class="archive wrap" id="notes" aria-labelledby="archive-title">
      <div class="archive-heading"><div><p class="section-label">Browse the archive</p><h2 id="archive-title">Research, with receipts.</h2></div><p class="count" data-result-count>{label}</p></div>
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
    <section class="method wrap" aria-labelledby="method-title"><p class="section-label">How we work</p><h2 id="method-title">Evidence first. Conviction second.</h2><p>These independent market notes separate observable data from interpretation, flag uncertainty, and show what would change the thesis. A useful investigation can end with a trade idea, a failed setup, or no trade at all.</p></section>
  </main>
  <footer>
    <div class="wrap colophon">
      <p>{escape(site["title"])}</p>
      <div><a href="#notes">Browse the archive</a><a href="feed.xml">Subscribe via RSS</a></div>
    </div>
  </footer>"""
    home = page_shell(
        site,
        document_title=site["title"],
        description=site["description"],
        canonical=site["url"] + "/",
        main=main,
        structured_data=structured_data,
    )
    script_tag = '<script src="search.js" defer></script>'
    return home.replace("</body>", f"  {script_tag}\n</body>")


def render_404(site: dict) -> str:
    main = f"""<main id="notes" class="wrap missing">
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
    )


def render_feed(notes: list[dict], site: dict) -> str:
    items = []
    for index, note in enumerate(notes):
        published = datetime.strptime(note["date"], "%Y-%m-%d").replace(
            tzinfo=timezone.utc, hour=18
        ) - timedelta(seconds=index)
        link = f"{site['url']}/{note['slug']}/"
        guid = f"{site['rss_guid_origin']}/{note['slug']}/"
        items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{xml_escape(note['title'])}</title>",
                    f"      <link>{xml_escape(link)}</link>",
                    f'      <guid isPermaLink="true">{xml_escape(guid)}</guid>',
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
    newest = notes[0]["date"]
    urls = [(site["url"] + "/", newest)]
    urls.extend((f"{site['url']}/{note['slug']}/", note["date"]) for note in notes)
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
        if visible_text(strip_site_bar(body_inner(built))) != visible_text(body_inner(note["html"])):
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
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    for note in notes:
        out = DIST / note["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_article(note, site), encoding="utf-8")
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
