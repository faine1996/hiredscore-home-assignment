from __future__ import annotations
import argparse
from typing import List
from common.http import fetch_json
from common.types import Candidate
from section1.parsing import normalize_candidate
from .filters import apply_filters
from .transform import total_experience_years, skills_of, industries_of
from .mongo_io import connect, insert_filtered
from collections import Counter

DEFAULT_URL = "https://recruiting-test-resume-data.hiredscore.com/ps-dev-allcands-full-api_hub_b1f6.json"

def top_counts(items, k=15):
    return "\n".join(f"{name}: {count}" for name, count in Counter(items).most_common(k))

def dataset_report(cands: List[Candidate]) -> str:
    all_inds = []
    all_sk   = []
    for c in cands:
        all_inds.extend(sorted(list(industries_of(c))))
        all_sk.extend(sorted(list(skills_of(c))))
    return (
        "top industries:\n" + top_counts(all_inds, 20) + "\n\n" +
        "top skills:\n" + top_counts(all_sk, 30)
    )

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
    ap.add_argument("--explain", action="store_true")
    ap.add_argument("--show-n", type=int, default=0, help="Print first N matched candidate names")
    args = ap.parse_args()

    raw = fetch_json(args.url)
    if not isinstance(raw, list):
        raise RuntimeError("unexpected jSON shape: expected a list of candidates")
    cands: List[Candidate] = [normalize_candidate(r) for r in raw]
    if args.explain:
        print(dataset_report(cands))

    filtered = apply_filters(cands, args.industry, args.skills, args.min_years)
    docs = [to_doc(c) for c in filtered]
    if args.explain:
        print(f"\nMatched {len(filtered)} candidates "
        f"(industry={args.industry!r}, skills={args.skills!r}, min_years={args.min_years})")

    # preview top N matches
    if args.show_n and args.show_n > 0:
        for c in filtered[: args.show_n]:
            print(c.get("name", "Unknown"))

    if args.dry_run:
        print(f"would insert {len(docs)} candidates matching filters.")
        return

    client = connect(args.mongo)
    db = client["assignment"]
    insert_filtered(db, docs)
    print(f"inserted {len(docs)} docs into assignment.filtered_candidates.")

if __name__ == "__main__":
    main()
