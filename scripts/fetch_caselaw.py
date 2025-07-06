import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional

import requests


API_ROOT = "https://www.courtlistener.com/api/rest/v3"


def fetch_opinions(court: str = "colo", page_size: int = 100, api_key: Optional[str] = None) -> List[Dict]:
    """Fetch opinions from CourtListener API for a given court."""
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Token {api_key}"

    url = f"{API_ROOT}/opinions/?court={court}&page_size={page_size}"
    opinions: List[Dict] = []

    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        opinions.extend(data.get("results", []))
        url = data.get("next")
    return opinions


def save_opinions(opinions: List[Dict], output_file: Path) -> None:
    with output_file.open("w", encoding="utf-8") as f:
        for op in opinions:
            f.write(json.dumps(op, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Colorado caselaw from CourtListener")
    parser.add_argument("output_file", type=Path, help="Path to write opinions JSONL")
    parser.add_argument("--court", default="colo", help="Court slug (default: colorado)")
    parser.add_argument("--page_size", type=int, default=100, help="Number of results per page")
    parser.add_argument("--api_key", help="Optional CourtListener API key")
    args = parser.parse_args()

    ops = fetch_opinions(args.court, args.page_size, args.api_key)
    save_opinions(ops, args.output_file)
