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

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
SITE_PATH = ROOT / "site.json"
FAVICON = ROOT / "assets" / "favicon.svg"
DESIGN_SYSTEM = ROOT / "assets" / "design-system.css"

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
    return site


def load_notes() -> list[dict]:
    raw = load_json(CONTENT / "articles.json")
    if not isinstance(raw, list) or not raw:
        die("content/articles.json must be a non-empty list")
    notes = []
    seen: set[str] = set()
    for index, entry in enumerate(raw, start=1):
        if not isinstance(entry, dict):
            die(f"articles.json item {index} must be an object")
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
            }
        )
    notes.sort(key=lambda note: note["date"], reverse=True)
    return notes


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
    if "twitter:card" not in head:
        parts.append('<meta name="twitter:card" content="summary">')
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
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="design-system.css">
  <link rel="alternate" type="application/rss+xml" title="{escape(site["title"], quote=True)}" href="feed.xml">
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
  <a class="skip" href="#notes">Skip to notes</a>
  {main}
</body>
</html>
"""


def render_home(notes: list[dict], site: dict) -> str:
    count = len(notes)
    label = "1 note" if count == 1 else f"{count} notes"
    entries = []
    for note in notes:
        entries.append(
            f"""<a class="entry" href="{escape(note["slug"], quote=True)}/">
      <time datetime="{escape(note["date"], quote=True)}">{escape(pretty_date(note["date"]))}</time>
      <div>
        <h2>{escape(note["title"])}</h2>
        <p class="dek">{escape(note["dek"])}</p>
      </div>
    </a>"""
        )
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
        <nav class="tools" aria-label="Subscribe"><a href="feed.xml">RSS</a></nav>
      </div>
      <h1>{escape(site["title"])}</h1>
      <p class="lede">{escape(site["description"])}</p>
    </div>
  </header>
  <main id="notes">
    <div class="wrap">
      <p class="count">{label}</p>
      {"".join(entries)}
    </div>
  </main>
  <footer>
    <div class="wrap colophon">
      <p>{escape(site["title"])}</p>
      <a href="feed.xml">Subscribe via RSS</a>
    </div>
  </footer>"""
    return page_shell(
        site,
        document_title=site["title"],
        description=site["description"],
        canonical=site["url"] + "/",
        main=main,
        structured_data=structured_data,
    )


def render_404(site: dict) -> str:
    main = f"""<main id="notes" class="wrap missing">
    <p class="kicker">Missing page</p>
    <h1>That page is not on this site.</h1>
    <p class="lede">The research notes are collected on the home page.</p>
    <p><a class="back" href="index.html">Back to {escape(site["title"])}</a></p>
  </main>"""
    return page_shell(
        site,
        document_title=f"Page not found · {site['title']}",
        description=f"That page is not on {site['title']}.",
        canonical=site["url"] + "/404.html",
        main=main,
    )


def render_feed(notes: list[dict], site: dict) -> str:
    items = []
    for index, note in enumerate(notes):
        published = datetime.strptime(note["date"], "%Y-%m-%d").replace(
            tzinfo=timezone.utc, hour=18
        ) - timedelta(seconds=index)
        link = f"{site['url']}/{note['slug']}/"
        items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{xml_escape(note['title'])}</title>",
                    f"      <link>{xml_escape(link)}</link>",
                    f'      <guid isPermaLink="true">{xml_escape(link)}</guid>',
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
    verify(notes)
    print(f"Built {len(notes)} notes → {DIST.relative_to(ROOT)}")
    for note in notes:
        print(f"  {note['date']}  {note['slug']}")


if __name__ == "__main__":
    main()
