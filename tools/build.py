#!/usr/bin/env python3
"""Build the generated parts of gymtwins.com.

    python3 tools/build.py [--app ../Gymtwin]

- exercises/: the exercise library, from the Gym Twin app's JSON files (only with --app)
- contact.html: the FAQPage JSON-LD block, read from the page's own <details> FAQ
- sitemap.xml: every indexable page, lastmod from the last git commit that touched it

GitHub Pages serves the repository as it is, so the output is committed.
"""
import argparse, datetime, html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://gymtwins.com/"
sys.path.insert(0, str(ROOT / "tools"))


def page_files():
    """Indexable pages: every .html except the 404 page and anything marked noindex."""
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "tools/", "node_modules/")) or rel == "404.html":
            continue
        if 'name="robots" content="noindex' in p.read_text(encoding="utf-8"):
            continue
        out.append(rel)
    return out


def url_for(rel):
    if rel == "index.html":
        return SITE
    if rel.endswith("/index.html"):
        return SITE + rel[: -len("index.html")]
    return SITE + rel


def lastmod(rel):
    """Date of the last commit that touched the file; today for a file with uncommitted changes."""
    path = ROOT / rel
    dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if not dirty:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if d:
            return d
    return datetime.date.today().isoformat()


def build_sitemap():
    rows = []
    for rel in page_files():
        rows.append(f"  <url>\n    <loc>{html.escape(url_for(rel))}</loc>\n    <lastmod>{lastmod(rel)}</lastmod>\n  </url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    return len(rows)


def text_of(fragment):
    t = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


FAQ_START = "<!-- faq-jsonld:start (tools/build.py) -->"
FAQ_END = "<!-- faq-jsonld:end -->"


def build_faq_jsonld():
    path = ROOT / "contact.html"
    src = path.read_text(encoding="utf-8")
    pairs = re.findall(r"<summary>(.*?)</summary>\s*<div class=\"faq-answer\">(.*?)</div>\s*</details>", src, re.S)
    if not pairs:
        raise SystemExit("contact.html: no FAQ found")
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": text_of(q), "acceptedAnswer": {"@type": "Answer", "text": text_of(a)}}
            for q, a in pairs
        ],
    }
    block = f'{FAQ_START}\n    <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n    {FAQ_END}'
    if FAQ_START in src:
        src = re.sub(re.escape(FAQ_START) + r".*?" + re.escape(FAQ_END), lambda _: block, src, flags=re.S)
    else:
        src = src.replace("</head>", f"    {block}\n</head>", 1)
    path.write_text(src, encoding="utf-8")
    return len(pairs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", help="path to the Gym Twin app repository (regenerates exercises/)")
    args = ap.parse_args()
    if args.app:
        import exercises
        n = exercises.generate(pathlib.Path(args.app).resolve(), ROOT)
        print(f"exercises: {n} pages")
    print(f"faq: {build_faq_jsonld()} questions")
    print(f"sitemap: {build_sitemap()} urls")


if __name__ == "__main__":
    main()
