#!/usr/bin/env python3
"""Build the site from catalog.json.

What it does, in order:
  1. Checks catalog.json (unique slugs, known topics, every paper has papers/<slug>/index.html).
  2. For each paper page: if it is still a body fragment (a claude.ai artifact page, no <!doctype>),
     wraps it into a full document; then refreshes the navigation strip between the vap:nav markers.
  3. Refreshes the navigation strip on each topic page under topics/<id>/index.html.
  4. Regenerates the home page index.html from tools/home.template.html.
  5. Regenerates the paper list in README.md between the catalog:start / catalog:end markers.
  6. Checks that every local file a page references (fig/..., relative links) exists.

Run from anywhere:  python3 tools/build.py
It only rewrites a file when its content changes, so re-running is safe.
"""
import html
import json
import os
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "tools", "home.template.html")

# Same reset the claude.ai artifact skeleton applies, so wrapped pages render as they did there.
SKELETON_HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" href="data:,">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Noto Sans SC",sans-serif;background:#fafaf9}
img{max-width:100%}
[hidden]{display:none!important}
</style>"""

# Leading <title>/<meta>/<link>/<style> run of an artifact fragment; moved into <head> when wrapping.
HEAD_RUN = re.compile(
    r"\A(?:\s+|<!--.*?-->|<title>.*?</title>|<meta\b[^>]*>|<link\b[^>]*>|<style\b[^>]*>.*?</style>)+",
    re.S,
)

NAV_STYLE = """<!-- vap:nav-style -->
<style>
.vapnav{box-sizing:border-box;width:100%;border-bottom:1px solid color-mix(in srgb,currentColor 14%,transparent);color:inherit}
.vapnav-in{box-sizing:border-box;max-width:1200px;margin:0 auto;padding:10px 16px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 20px;font:500 13px/1.45 "Noto Sans SC",system-ui,-apple-system,"PingFang SC",sans-serif;letter-spacing:0}
.vapnav a{color:inherit;text-decoration:none;opacity:.7}
.vapnav a:hover,.vapnav a:focus-visible{opacity:1;text-decoration:underline;text-underline-offset:3px}
.vapnav a:focus-visible{outline:2px solid currentColor;outline-offset:2px}
.vapnav a[aria-current="page"]{opacity:1;font-weight:700}
.vapnav-crumb,.vapnav-links{display:flex;flex-wrap:wrap;align-items:center;gap:4px 14px}
.vapnav-sep{opacity:.4}
</style>
<!-- /vap:nav-style -->"""

NAV_STYLE_RE = re.compile(r"<!-- vap:nav-style -->.*?<!-- /vap:nav-style -->\n?", re.S)
NAV_RE = re.compile(r"<!-- vap:nav -->.*?<!-- /vap:nav -->\n?", re.S)
BODY_OPEN = re.compile(r"<body\b[^>]*>\n?", re.I)
HEAD_CLOSE = re.compile(r"</head\s*>", re.I)

problems = []
to_check = []  # (path, text) pairs; links are checked after every file is written


def esc(s):
    return html.escape(str(s), quote=True)


def load_catalog():
    with open(os.path.join(ROOT, "catalog.json"), encoding="utf-8") as f:
        cat = json.load(f)
    topics = {t["id"]: t for t in cat.get("topics", [])}
    seen = set()
    for p in cat.get("papers", []):
        if p["slug"] in seen:
            problems.append(f"catalog: duplicate slug {p['slug']}")
        seen.add(p["slug"])
        for t in p.get("topics", []):
            if t not in topics:
                problems.append(f"catalog: {p['slug']} uses unknown topic {t}")
        if not os.path.isfile(os.path.join(ROOT, "papers", p["slug"], "index.html")):
            problems.append(f"missing page: papers/{p['slug']}/index.html")
    on_disk = set()
    papers_dir = os.path.join(ROOT, "papers")
    if os.path.isdir(papers_dir):
        on_disk = {d for d in os.listdir(papers_dir) if os.path.isdir(os.path.join(papers_dir, d))}
    for d in sorted(on_disk - seen):
        print(f"note: papers/{d}/ is not in catalog.json, so it is not linked from the home page")
    return cat, topics


def papers_in(cat, topic_id):
    ps = [p for p in cat["papers"] if topic_id in p.get("topics", [])]
    return sorted(ps, key=lambda p: (p.get("date", ""), p["title"].lower()))


def nav_html(cat, topics, topic_id=None, current_slug=None):
    """Nav strip for a page two levels deep (papers/<slug>/ or topics/<id>/)."""
    crumb = ['<a href="../../">全部论文</a>']
    links = []
    if topic_id:
        t = topics[topic_id]
        cur = ' aria-current="page"' if current_slug is None else ""
        crumb.append('<span class="vapnav-sep" aria-hidden="true">/</span>')
        crumb.append(f'<a href="../../{esc(t["page"])}"{cur}>{esc(t["title"])}</a>')
        for p in papers_in(cat, topic_id):
            cur = ' aria-current="page"' if p["slug"] == current_slug else ""
            links.append(f'<a href="../../papers/{esc(p["slug"])}/"{cur}>{esc(p["title"])}</a>')
    return (
        "<!-- vap:nav -->\n"
        '<div class="vapnav" role="navigation" aria-label="论文导航"><div class="vapnav-in">'
        f'<span class="vapnav-crumb">{"".join(crumb)}</span>'
        f'<span class="vapnav-links">{"".join(links)}</span>'
        "</div></div>\n<!-- /vap:nav -->\n"
    )


def wrap_fragment(page):
    m = HEAD_RUN.match(page)
    head_part = m.group(0).strip() if m else ""
    body_part = page[m.end():] if m else page
    return (
        '<!doctype html>\n<html lang="zh-CN">\n<head>\n'
        f"{SKELETON_HEAD}\n{head_part}\n</head>\n<body>\n{body_part.strip()}\n</body>\n</html>\n"
    )


def set_nav(page, nav):
    page = NAV_STYLE_RE.sub("", page)
    page = NAV_RE.sub("", page)
    page = HEAD_CLOSE.sub(lambda m: NAV_STYLE + "\n" + m.group(0), page, count=1)
    page = BODY_OPEN.sub(lambda m: m.group(0).rstrip("\n") + "\n" + nav, page, count=1)
    return page


def write_if_changed(path, text):
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
    if old != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False


ATTR_REF = re.compile(r"""\b(?:src|href|poster)\s*=\s*["']([^"']+)["']""", re.I)
JS_REF = re.compile(r"""["'`]((?:\./)?fig/[^"'`$\s]+)["'`]""")


def check_refs(page_path, page):
    base = os.path.dirname(page_path)
    refs = set(ATTR_REF.findall(page)) | set(JS_REF.findall(page))
    for ref in sorted(refs):
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", ref, re.I) or "${" in ref:
            continue
        path = unquote(urlsplit(ref).path)
        if not path:
            continue
        target = os.path.normpath(os.path.join(base, path))
        if path.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            problems.append(f"broken link in {os.path.relpath(page_path, ROOT)}: {ref}")


def build_pages(cat, topics):
    changed = []
    for p in cat["papers"]:
        path = os.path.join(ROOT, "papers", p["slug"], "index.html")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            page = f.read()
        if not re.match(r"\s*<!doctype", page, re.I):
            page = wrap_fragment(page)
        first_topic = (p.get("topics") or [None])[0]
        page = set_nav(page, nav_html(cat, topics, first_topic, p["slug"]))
        if write_if_changed(path, page):
            changed.append(os.path.relpath(path, ROOT))
        to_check.append((path, page))
    for t in topics.values():
        path = os.path.join(ROOT, t["page"], "index.html")
        if not os.path.isfile(path):
            problems.append(f"missing topic page: {t['page']}index.html")
            continue
        with open(path, encoding="utf-8") as f:
            page = f.read()
        page = set_nav(page, nav_html(cat, topics, t["id"]))
        if write_if_changed(path, page):
            changed.append(os.path.relpath(path, ROOT))
        to_check.append((path, page))
    return changed


def paper_row(p):
    arxiv = ""
    if p.get("arxiv"):
        arxiv = (f'<a class="ax" href="https://arxiv.org/abs/{esc(p["arxiv"])}" target="_blank" '
                 f'rel="noopener">arXiv {esc(p["arxiv"])}</a>')
    return (
        '<li class="paper">'
        f'<div class="pmeta"><span class="pdate">{esc(p.get("date", ""))}</span>{arxiv}</div>'
        '<div class="pbody">'
        f'<h3><a href="papers/{esc(p["slug"])}/">{esc(p["title"])}</a></h3>'
        f'<p class="pfull">{esc(p.get("full_title", ""))}</p>'
        f'<p class="psum">{esc(p.get("summary", ""))}</p>'
        f'<p class="porg">{esc(p.get("org", ""))}</p>'
        "</div></li>"
    )


def build_home(cat, topics):
    blocks = []
    for t in cat.get("topics", []):
        ps = papers_in(cat, t["id"])
        if not ps:
            continue
        path = " / ".join(esc(x) for x in t.get("path", []))
        blocks.append(
            f'<section class="topic" id="{esc(t["id"])}">'
            f'<div class="thead"><div><div class="tpath">{path}</div>'
            f'<h2><a href="{esc(t["page"])}">{esc(t["title"])}</a><span class="tcount">{len(ps)} 篇</span></h2>'
            f'<p class="tsum">{esc(t.get("summary", ""))}</p></div>'
            f'<a class="tgo" href="{esc(t["page"])}">专题对照 →</a></div>'
            f'<ul class="papers">{"".join(paper_row(p) for p in ps)}</ul></section>'
        )
    loose = sorted((p for p in cat["papers"] if not p.get("topics")),
                   key=lambda p: (p.get("date", ""), p["title"].lower()))
    if loose:
        blocks.append(
            '<section class="topic" id="misc"><div class="thead"><div>'
            f'<h2>未归入专题<span class="tcount">{len(loose)} 篇</span></h2></div></div>'
            f'<ul class="papers">{"".join(paper_row(p) for p in loose)}</ul></section>'
        )
    n_topics = sum(1 for t in cat.get("topics", []) if papers_in(cat, t["id"]))
    updated = max((p.get("added", "") for p in cat["papers"]), default="")
    stats = f'{len(cat["papers"])} 篇论文 · {n_topics} 个专题 · 最近更新 {esc(updated)}'
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    out = tpl.replace("{{STATS}}", stats).replace("{{TOPICS}}", "\n".join(blocks))
    path = os.path.join(ROOT, "index.html")
    changed = write_if_changed(path, out)
    to_check.append((path, out))
    return changed


README_RE = re.compile(r"(<!-- catalog:start -->\n).*?(<!-- catalog:end -->)", re.S)


def build_readme(cat):
    """Regenerate the paper list in README.md between the catalog markers."""
    path = os.path.join(ROOT, "README.md")
    if not os.path.isfile(path):
        return False
    with open(path, encoding="utf-8") as f:
        readme = f.read()
    if not README_RE.search(readme):
        return False
    site = cat.get("site_url", "").rstrip("/") + "/"
    lines = []
    for t in cat.get("topics", []):
        ps = papers_in(cat, t["id"])
        if not ps:
            continue
        path_str = " / ".join(t.get("path", []))
        lines.append(f'### {t["title"]}（{path_str}）\n')
        lines.append(f'[专题对照页]({site}{t["page"]})\n')
        for p in ps:
            ax = f' · arXiv [{p["arxiv"]}](https://arxiv.org/abs/{p["arxiv"]})' if p.get("arxiv") else ""
            lines.append(f'- [{p["title"]}]({site}papers/{p["slug"]}/) · {p.get("date", "")}{ax} — {p.get("summary", "")}')
        lines.append("")
    loose = [p for p in cat["papers"] if not p.get("topics")]
    if loose:
        lines.append("### 未归入专题\n")
        for p in sorted(loose, key=lambda p: (p.get("date", ""), p["title"].lower())):
            lines.append(f'- [{p["title"]}]({site}papers/{p["slug"]}/) · {p.get("date", "")} — {p.get("summary", "")}')
        lines.append("")
    body = "\n".join(lines)
    new = README_RE.sub(lambda m: m.group(1) + body + m.group(2), readme)
    return write_if_changed(path, new)


def main():
    cat, topics = load_catalog()
    changed = build_pages(cat, topics)
    if build_home(cat, topics):
        changed.append("index.html")
    if build_readme(cat):
        changed.append("README.md")
    for path, text in to_check:
        check_refs(path, text)
    print("updated: " + (", ".join(changed) if changed else "nothing (already up to date)"))
    if problems:
        print("\nproblems:")
        for x in problems:
            print("  - " + x)
        sys.exit(1)
    print(f"ok: {len(cat['papers'])} papers, {len(topics)} topics, all local links resolve")


if __name__ == "__main__":
    main()
