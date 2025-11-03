from __future__ import annotations
from typing import List, Set, Optional
from common.types import Candidate
from .transform import skills_of, industries_of, total_experience_years

def by_industry(cands: List[Candidate], industry: Optional[str]) -> List[Candidate]:
    if not industry:
        return cands
    needle = industry.strip().lower()
    #substring match against normalized industries
    return [c for c in cands if any(needle in ind for ind in industries_of(c))]



def by_skills_any(cands: List[Candidate], skills: Set[str]) -> List[Candidate]:
    if not skills:
        return cands
    req = {s.strip().lower() for s in skills if s.strip()}
    return [c for c in cands if skills_of(c) & req]

def by_min_years(cands: List[Candidate], min_years: Optional[float]) -> List[Candidate]:
    if not min_years or min_years <= 0:
        return cands
    out = []
    for c in cands:
        years = total_experience_years(c.get("experiences", []))
        if years >= float(min_years):
            out.append(c)
    return out

def apply_filters(cands: List[Candidate], industry: Optional[str], skills_csv: Optional[str], min_years: Optional[float]) -> List[Candidate]:
    c = by_industry(cands, industry)
    skills = set()
    if skills_csv:
        for piece in skills_csv.replace(";", ",").split(","):
            t = piece.strip().lower()
            if t:
                skills.add(t)
    c = by_skills_any(c, skills)
    c = by_min_years(c, min_years)
    return c
