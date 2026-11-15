"""Build the results page.

    python -m legislag.site [--run pilot|full]

Injects outputs/<run>_site_data.json into the run's template and writes a
single self-contained page: site/pilot.html or site/index.html. The full run
also writes docs/index.html, a standalone copy for GitHub Pages.
"""
from __future__ import annotations

import argparse
import sys

from .config import ROOT

MARK = "/*__DATA__*/"


# The artifact host wraps a page in a document skeleton. GitHub Pages serves
# the file as it is, so the public copy carries its own.
PUBLIC_HEAD = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<meta name="description" content="How stale is the AI evidence UK and Australian '
    'parliamentarians cite? Results from 613 coded Hansard speeches.">\n'
    "<style>:root{color-scheme:light;box-sizing:border-box}body{margin:0}"
    "img{max-width:100%}[hidden]{display:none!important}</style>\n"
)
PUBLIC_PAGE = ROOT / "docs" / "index.html"   # served by GitHub Pages from main:/docs

# run -> (template, page)
PAGES = {"pilot": ("template_pilot.html", "pilot.html"), "full": ("template_full.html", "index.html")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", choices=sorted(PAGES), default="pilot")
    args = ap.parse_args()
    template_name, page_name = PAGES[args.run]
    template_path = ROOT / "site" / template_name
    if not template_path.exists():
        print(f"site/{template_name} does not exist yet")
        return 1
    template = template_path.read_text(encoding="utf-8")
    data = (ROOT / "outputs" / f"{args.run}_site_data.json").read_text(encoding="utf-8").strip()
    if MARK not in template:
        print("template has no data marker")
        return 1
    # "</" must not appear inside a script element.
    page = template.replace(MARK, data.replace("</", "<\\/"))
    (ROOT / "site" / page_name).write_text(page, encoding="utf-8")
    print(f"wrote site/{page_name} ({len(page) // 1024} KB)")
    if args.run == "full":
        # The page opens with its title, meta, link and style tags, which a
        # browser keeps in the head. The body starts at the first element after them.
        PUBLIC_PAGE.write_text(PUBLIC_HEAD + page + "\n</html>\n", encoding="utf-8")
        (PUBLIC_PAGE.parent / ".nojekyll").write_text("")
        print(f"wrote docs/index.html for GitHub Pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
