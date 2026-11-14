"""Build the results page.

    python -m legislag.site

Injects outputs/pilot_site_data.json into site/template.html and writes
site/index.html, a single self-contained file.
"""
from __future__ import annotations

import sys

from .config import ROOT

MARK = "/*__DATA__*/"


def main() -> int:
    template = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    data = (ROOT / "outputs" / "pilot_site_data.json").read_text(encoding="utf-8").strip()
    if MARK not in template:
        print("template has no data marker")
        return 1
    # "</" must not appear inside a script element.
    page = template.replace(MARK, data.replace("</", "<\\/"))
    (ROOT / "site" / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote site/index.html ({len(page) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
