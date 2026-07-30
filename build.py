#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.6", "python-frontmatter>=1.1"]
# ///
"""Turn the markdown files in this directory into a static site in _site/.

Every .md file at the repo root becomes a page. Front matter is optional:

    ---
    title: projects
    description: things i have built
    slug: projects
    aliases: [work, portfolio]
    ---

It is real YAML, so a value containing a colon has to be quoted.

Defaults: slug is the filename (home.md becomes the site root), title is the
slug, description falls back to site.json's description.

Two build-time conveniences:

  - Links to other pages stay written as `projects.md` in the markdown, so the
    files remain readable on GitHub. The build rewrites them to `/projects/`.
  - `<!-- news limit=5 -->` expands into a table built from news.json.

Run by .github/workflows/deploy.yml on every push to main. Nothing needs to be
built or run locally; `uv run build.py` just previews what the workflow will do.
"""

import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

import frontmatter
import markdown
import yaml

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
ASSETS = ROOT / "assets"
TEMPLATE = ROOT / "templates" / "base.html"

# Copied verbatim into the output root.
STATIC_FILES = ["CNAME", "favicon.svg"]

MD_EXTENSIONS = ["extra", "sane_lists"]


def read_json(path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"error: {path.name} is not valid JSON\n"
            f"  {error}\n"
            "  a trailing comma after the last item in a list is the usual cause"
        ) from error


def load_page(path):
    """Parse one markdown file's front matter, with a legible error if it is bad.

    Raw YAML errors are unhelpful when the edit came from a phone, and the most
    common cause by far is an unquoted colon.
    """
    try:
        return frontmatter.load(path)
    except yaml.YAMLError as error:
        raise SystemExit(
            f"error: could not parse the front matter in {path.name}\n"
            f"  {error}\n"
            "  if a value contains a colon, wrap the whole value in quotes"
        ) from error


def as_list(value):
    """Accept `aliases: papers` and `aliases: [papers, work]` alike."""
    if not value:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value]


def url_for(slug):
    return "/" if slug == "" else f"/{slug}/"


def collect_pages():
    """Every root-level .md file, in a stable order, with front matter parsed."""
    pages = []
    for path in sorted(ROOT.glob("*.md")):
        if path.name == "README.md":
            continue
        post = load_page(path)
        meta = post.metadata
        slug = str(meta.get("slug") or ("" if path.stem == "home" else path.stem))
        pages.append(
            {
                "source": path.name,
                "slug": slug,
                "url": url_for(slug),
                "title": str(meta.get("title") or slug or "home"),
                "description": str(meta.get("description") or ""),
                "aliases": as_list(meta.get("aliases")),
                "sitemap": meta.get("sitemap", True),
                "noindex": meta.get("noindex", False),
                "image": str(meta.get("image") or ""),
                "body": post.content,
            }
        )
    return pages


def rewrite_links(rendered, link_map):
    """Point `foo.md` and legacy `/?content=foo.md` hrefs at their built URLs.

    External links are left alone, including the https link to this repo's own
    projects.md on GitHub.
    """

    def replace(match):
        href = match.group(1)
        if re.match(r"^(https?:|mailto:|#|/assets/)", href):
            return match.group(0)
        target = href
        target = re.sub(r"^/?\?content=", "", target)
        path, _, fragment = target.partition("#")
        new = link_map.get(path.lstrip("/"))
        if new is None:
            return match.group(0)
        return f'href="{new}{"#" + fragment if fragment else ""}"'

    return re.sub(r'href="([^"]*)"', replace, rendered)


def render_news(md, limit):
    """Static news table. Rows past `limit` ship hidden for the load-more button."""
    items = read_json(ROOT / "news.json", [])
    items = sorted(items, key=lambda item: item["date"], reverse=True)

    rows = []
    for index, item in enumerate(items):
        stamp = date.fromisoformat(item["date"])
        headline = md.reset().convert(item["headline"])
        hidden = " hidden" if limit is not None and index >= limit else ""
        rows.append(
            f'<tr{hidden}><td><time datetime="{item["date"]}">'
            f"{stamp.strftime('%-d %b %Y')}:</time></td>"
            f"<td>{headline}</td></tr>"
        )

    table = (
        '<table class="newstable" id="news-table">\n<tbody>\n'
        + "\n".join(rows)
        + "\n</tbody>\n</table>"
    )
    if limit is not None and len(items) > limit:
        # Wrapped so markdown treats it as a block and does not add a <p>.
        table += (
            f'\n<div><button id="news_load_btn" data-step="{limit}" hidden>'
            "...load more</button></div>"
        )
    return table


# Accepts `<!-- news -->`, `<!-- news all -->`, `<!-- news 5 -->`,
# and `<!-- news limit=5 -->`. Anything but a number means every item.
NEWS_MARKER = re.compile(
    r"^<!--\s*news(?:\s+(?:limit=)?(\w+))?\s*-->$", re.MULTILINE
)


def expand_news(body, md):
    def replace(match):
        raw = match.group(1)
        limit = int(raw) if raw and raw.isdigit() else None
        return "\n" + render_news(md, limit) + "\n"

    return NEWS_MARKER.sub(replace, body)


def head_extra(page, site, base_url):
    """The conditional head tags, so the template holds no empty ones."""
    tags = []

    image = page["image"] or site.get("image", "")
    if image:
        url = image if image.startswith("http") else base_url + image
        tags.append(f'<meta property="og:image" content="{url}">')
        tags.append(f'<meta name="twitter:image" content="{url}">')
    # Without an image a large card renders as an empty box, so only ask for
    # one when there is something to put in it.
    tags.append(
        '<meta name="twitter:card" content="'
        + ("summary_large_image" if image else "summary")
        + '">'
    )

    if page["noindex"]:
        tags.append('<meta name="robots" content="noindex, follow">')

    # Lets Google show "hrishik.me > projects" in place of the raw URL.
    if page["slug"] != "":
        crumbs = [("home", base_url + "/"), (page["title"], base_url + page["url"])]
        breadcrumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": name,
                    "item": url,
                }
                for position, (name, url) in enumerate(crumbs, start=1)
            ],
        }
        tags.append(
            '<script type="application/ld+json">'
            + json.dumps(breadcrumbs, ensure_ascii=False)
            + "</script>"
        )

    # Tells search engines that the accounts linked from the homepage are the
    # same person as the subject of the site.
    if page["slug"] == "" and site.get("person"):
        person = {
            "@context": "https://schema.org",
            "@type": "Person",
            "url": base_url + "/",
            **site["person"],
        }
        tags.append(
            '<script type="application/ld+json">'
            + json.dumps(person, ensure_ascii=False)
            + "</script>"
        )

    return "\n  ".join(tags)


def fill(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def build():
    site = read_json(ROOT / "site.json")
    base_url = site["url"].rstrip("/")
    template = TEMPLATE.read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    pages = collect_pages()

    # `projects.md` -> `/projects/`, plus every alias so old links keep working.
    link_map = {}
    for page in pages:
        link_map[page["source"]] = page["url"]
        for alias in page["aliases"]:
            link_map[f"{alias}.md"] = page["url"]

    # Fail loudly rather than have one page quietly overwrite another. An empty
    # `slug:` on anything but home.md is the likely way to hit this.
    claimed = {}
    for page in pages:
        for slug in [page["slug"], *page["aliases"]]:
            if slug in claimed:
                raise SystemExit(
                    f"error: {page['source']} and {claimed[slug]} both claim "
                    f"{url_for(slug)} - check their slug/aliases"
                )
            claimed[slug] = page["source"]

    # Serves the legacy `/?content=projects.md` URLs from the old SPA.
    redirects = json.dumps({source: url for source, url in link_map.items()})

    nav = "\n".join(
        f'      <li><a href="{url_for(item["slug"])}">{html.escape(item["label"])}</a></li>'
        for item in site["nav"]
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    written = []
    for page in pages:
        content = rewrite_links(
            md.reset().convert(expand_news(page["body"], md)), link_map
        )
        title = (
            site["title"]
            if page["slug"] == ""
            else f'{page["title"]} | {site["title"]}'
        )
        description = page["description"] or site["description"]
        canonical = base_url + page["url"]

        rendered = fill(
            template,
            {
                "title": html.escape(title),
                "description": html.escape(description),
                "canonical": canonical,
                "site_title": html.escape(site["title"]),
                "site_name": html.escape(site["name"]),
                "nav": nav,
                "redirects": redirects,
                "head_extra": head_extra(page, site, base_url),
                "content": content,
            },
        )

        for slug in [page["slug"], *page["aliases"]]:
            destination = OUT / slug / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered, encoding="utf-8")
            written.append(url_for(slug))

    shutil.copytree(ASSETS, OUT / "assets")
    for name in STATIC_FILES:
        source = ROOT / name
        if source.exists():
            shutil.copy2(source, OUT / name)

    urls = "\n".join(
        f"  <url><loc>{base_url}{page['url']}</loc></url>"
        for page in pages
        if page["sitemap"]
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"built {len(written)} pages into {OUT.relative_to(ROOT)}/")
    for url in sorted(written):
        print(f"  {url}")


if __name__ == "__main__":
    build()
