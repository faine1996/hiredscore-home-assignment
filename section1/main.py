from __future__ import annotations
import argparse
from datetime import date
from typing import Any, List
from common.http import fetch_json
from common.types import Candidate
from .parsing import normalize_candidate
from .dates import parse_date, gap_days, inclusive_gap_days
from .formatting import format_greeting, format_experience, format_gap

DEFAULT_URL = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"

def candidate_output(c: Candidate) -> str:
    lines: List[str] = [format_greeting(c.get("name","Unknown"))]
    exps = c.get("experiences") or []
    for idx, e in enumerate(exps):
        lines.append(format_experience(e))
        if idx < len(exps) - 1:
            curr_start = parse_date(e.get("start_date"))      # newer job start
            prev_end   = parse_date(exps[idx + 1].get("end_date"))  # older job end
            g = inclusive_gap_days(prev_end, curr_start)
            if g > 0:
                lines.append(format_gap(g))
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Section 1: Print candidates and gaps.")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--limit", type=int, default=0, help="Limit number of candidates printed")
    args = ap.parse_args()

    data = fetch_json(args.url)
    if not isinstance(data, list):
        raise RuntimeError("Unexpected JSON shape: expected a list of candidates")

    count = 0
    for raw in data:
        c = normalize_candidate(raw)
        print(candidate_output(c))
        print()  #blank line between candidates as a courtesy
        count += 1
        if args.limit and count >= args.limit:
            break

if __name__ == "__main__":
    main()
