from __future__ import annotations
from typing import List, Set, Tuple
from datetime import date
from common.types import Candidate, WorkEntry
from section1.dates import parse_date

def merged_intervals(exps: List[WorkEntry]) -> List[Tuple[date, date]]:
    #build (start, end) with None filtered out
    spans: List[Tuple[date, date]] = []
    for e in exps:
        s = parse_date(e.get("start_date"))
        eend = parse_date(e.get("end_date"))
        if s and eend and eend >= s:
            spans.append((s, eend))
    if not spans:
        return []

    spans.sort(key=lambda x: x[0])  #by start asc
    merged = [spans[0]]
    for s, e in spans[1:]:
        last_s, last_e = merged[-1]
        if s <= last_e:  #overlap
            merged[-1] = (last_s, max(last_e, e))
        else:
            merged.append((s, e))
    return merged

def total_experience_years(exps: List[WorkEntry]) -> float:
    merged = merged_intervals(exps)
    days = sum((e - s).days + 1 for s, e in merged)  #inclusive
    return round(days / 365.25, 2)

def skills_of(c: Candidate) -> Set[str]:
    out = set()
    for s in c.get("skills", []) or []:
        for piece in str(s).replace(";", ",").split(","):
            t = piece.strip().lower()
            if t:
                out.add(t)
    return out

def industries_of(c: Candidate) -> Set[str]:
    out = set()
    for ind in c.get("industries", []) or []:
        t = str(ind).strip().lower()
        if t:
            out.add(t)
    return out
