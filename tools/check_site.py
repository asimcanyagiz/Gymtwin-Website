#!/usr/bin/env python3
"""Checks every page of gymtwins.com before it ships. Exit 1 on any problem.

    python3 tools/check_site.py

- one <h1>, a <title> of at most 65 characters, a meta description of 50 to 165 characters
- a canonical URL equal to the page's own address (indexable pages)
- every local href and src points at a file that exists, and every #fragment at an id on that page
- every <img> has an alt attribute; every JSON-LD block is valid JSON with an @context
- sitemap.xml lists exactly the indexable pages; robots.txt names the sitemap
"""
import html.parser, json, pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from build import page_files, url_for, SITE  # noqa: E402


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.title = ""
        self._in = None
        self.meta = {}
        self.canonical = None
        self.links = []
        self.ids = set()
        self.imgs_without_alt = 0
        self.jsonld = []
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in, self._buf = "title", []
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in, self._buf = "jsonld", []
        elif tag == "meta" and "name" in a:
            self.meta[a["name"]] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "img" and "alt" not in a:
            self.imgs_without_alt += 1
        for key in ("href", "src"):
            if key in a and a[key] is not None and not (tag == "link" and a.get("rel") == "canonical"):
                self.links.append(a[key])

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._in == "title" and tag == "title":
            self.title, self._in = "".join(self._buf).strip(), None
        elif self._in == "jsonld" and tag == "script":
            self.jsonld.append("".join(self._buf))
            self._in = None


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def main():
    errors = []
    pages = {}
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "tools/")):
            continue
        pages[rel] = parse(path)
    indexable = set(page_files())
    for rel, p in pages.items():
        err = lambda m: errors.append(f"{rel}: {m}")
        if p.h1 != 1:
            err(f"{p.h1} <h1> elements, expected 1")
        if not p.title or len(p.title) > 65:
            err(f"title {len(p.title)} chars: {p.title!r}")
        desc = p.meta.get("description", "")
        if not 50 <= len(desc) <= 165:
            err(f"meta description {len(desc)} chars (50-165)")
        if rel in indexable and p.canonical != url_for(rel):
            err(f"canonical {p.canonical!r} != {url_for(rel)!r}")
        if p.imgs_without_alt:
            err(f"{p.imgs_without_alt} <img> without alt")
        for block in p.jsonld:
            try:
                data = json.loads(block)
                if "@context" not in data:
                    err("JSON-LD without @context")
            except json.JSONDecodeError as e:
                err(f"JSON-LD does not parse: {e}")
        base = (ROOT / rel).parent
        for link in p.links:
            u = urllib.parse.urlsplit(link)
            if u.scheme in ("http", "https", "mailto", "tel", "data") or link.startswith("//"):
                continue
            if rel == "404.html" and link.startswith("/"):
                target = ROOT / u.path.lstrip("/")
            else:
                target = (base / u.path) if u.path else ROOT / rel
            if target.is_dir() or u.path.endswith("/") or u.path == "":
                target = target / "index.html" if (target.is_dir() or u.path.endswith("/")) else target
            if not target.exists():
                err(f"broken link {link!r}")
                continue
            if u.fragment and target.suffix == ".html":
                trel = target.resolve().relative_to(ROOT).as_posix()
                if trel in pages and u.fragment not in pages[trel].ids:
                    err(f"missing anchor {link!r}")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    listed = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
    expected = {url_for(r) for r in indexable}
    for u in sorted(expected - listed):
        errors.append(f"sitemap.xml: missing {u}")
    for u in sorted(listed - expected):
        errors.append(f"sitemap.xml: lists {u}, which is not an indexable page")
    if f"Sitemap: {SITE}sitemap.xml" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
        errors.append("robots.txt: no Sitemap line")
    for e in errors:
        print(e)
    print(f"{len(pages)} pages checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
