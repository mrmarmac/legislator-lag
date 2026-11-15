"""Build the results page.

    python -m legislag.site [--run pilot|full]

Injects outputs/<run>_site_data.json into the run's template and writes a
single self-contained page: site/pilot.html or site/index.html.
"""
from __future__ import annotations

import argparse
import sys

from .config import ROOT

MARK = "/*__DATA__*/"


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
    return 0


if __name__ == "__main__":
    sys.exit(main())
