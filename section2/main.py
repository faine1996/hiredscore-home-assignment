from __future__ import annotations
import argparse
from typing import List
from common.http import fetch_json
from common.types import Candidate
from section1.parsing import normalize_candidate
from .filters import apply_filters
from .transform import total_experience_years, skills_of, industries_of
from .mongo_io import connect, insert_filtered

DEFAULT_URL = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"

def to_doc(c: Candidate) -> dict:
    return {
        "name": c.get("name", "Unknown"),
        "skills": sorted(list(skills_of(c))),
        "industries": sorted(list(industries_of(c))),
        "total_years": total_experience_years(c.get("experiences", [])),
        "experiences": c.get("experiences", []),
    }

def main():
    ap = argparse.ArgumentParser(description="Section 2: Filter candidates and write to MongoDB.")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--industry", default=None, help='e.g. "finance"')
    ap.add_argument("--skills", default=None, help='comma/semicolon-separated, e.g. "python,mongodb"')
    ap.add_argument("--min-years", type=float, default=None)
    ap.add_argument("--mongo", default="mongodb://localhost:27017")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw = fetch_json(args.url)
    if not isinstance(raw, list):
        raise RuntimeError("Unexpected JSON shape: expected a list of candidates")
    cands: List[Candidate] = [normalize_candidate(r) for r in raw]

    filtered = apply_filters(cands, args.industry, args.skills, args.min_years)
    docs = [to_doc(c) for c in filtered]

    if args.dry_run:
        print(f"Would insert {len(docs)} candidates matching filters.")
        return

    client = connect(args.mongo)
    db = client["assignment"]
    insert_filtered(db, docs)
    print(f"Inserted {len(docs)} docs into assignment.filtered_candidates.")

if __name__ == "__main__":
    main()
