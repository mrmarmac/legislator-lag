"""Shared settings: date window, chambers, AI filter, paths."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"  # not committed

START_DATE = "2026-07-01"


@dataclass(frozen=True)
class Chamber:
    key: str            # stable id used in speech_id and file paths
    country: str        # "UK" | "AU"
    label: str
    bulk_index: str     # directory listing of dated XML files
    api_base: str       # getDebates endpoint
    api_type: str       # value of the API `type` argument
    web_url: str        # public page for one speech; {gid} is substituted
    key_env: str        # environment variable holding the API key


TWFY = "https://www.theyworkforyou.com"
OA = "https://www.openaustralia.org.au"

CHAMBERS = [
    Chamber("uk-commons", "UK", "House of Commons",
            f"{TWFY}/pwdata/scrapedxml/debates/", f"{TWFY}/api/getDebates",
            "commons", f"{TWFY}/debates/?id={{gid}}", "TWFY_API_KEY"),
    Chamber("uk-westminsterhall", "UK", "Westminster Hall",
            f"{TWFY}/pwdata/scrapedxml/westminhall/", f"{TWFY}/api/getDebates",
            "westminsterhall", f"{TWFY}/whall/?id={{gid}}", "TWFY_API_KEY"),
    Chamber("uk-lords", "UK", "House of Lords",
            f"{TWFY}/pwdata/scrapedxml/lordspages/", f"{TWFY}/api/getDebates",
            "lords", f"{TWFY}/lords/?id={{gid}}", "TWFY_API_KEY"),
    Chamber("au-representatives", "AU", "House of Representatives",
            "https://data.openaustralia.org.au/scrapedxml/representatives_debates/",
            f"{OA}/api/getDebates", "representatives",
            f"{OA}/debates/?id={{gid}}", "OPENAUSTRALIA_API_KEY"),
    Chamber("au-senate", "AU", "Senate",
            "https://data.openaustralia.org.au/scrapedxml/senate_debates/",
            f"{OA}/api/getDebates", "senate",
            f"{OA}/senate/?id={{gid}}", "OPENAUSTRALIA_API_KEY"),
]
CHAMBER_BY_KEY = {c.key: c for c in CHAMBERS}

# A speech enters the corpus if it matches this pattern. Case-sensitive on
# purpose: "AI" must be upper case so that ordinary words never match.
AI_PATTERN = re.compile(
    r"\b("
    r"[Aa]rtificial [Ii]ntelligence|AI|A\.I\.|[Mm]achine[- ]learning|"
    r"[Ll]arge language models?|LLMs?|[Cc]hatbots?|ChatGPT|[Dd]eepfakes?|"
    r"[Ss]uperintelligen\w+|AGI|[Ff]rontier models?|OpenAI|Anthropic|DeepMind"
    r")\b"
)

# Search terms used by the API fetcher. The API cannot run a regex, so these
# approximate AI_PATTERN; results are re-filtered with AI_PATTERN afterwards.
API_SEARCH_TERMS = [
    '"artificial intelligence"', "AI", '"machine learning"',
    '"large language model"', "LLM", "chatbot", "ChatGPT", "deepfake",
    "superintelligence", "AGI", '"frontier model"', "OpenAI", "Anthropic",
    "DeepMind",
]
