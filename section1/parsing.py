from __future__ import annotations
from typing import List, Dict, Any
from datetime import date
from .dates import parse_date
from common.types import Candidate, WorkEntry

def _pick(d: Dict, *keys, default=None):
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return default

def extract_name(raw: Dict[str, Any]) -> str:
    #prefer contact_info.name.formatted_name
    try:
        name = raw.get("contact_info", {}).get("name", {}).get("formatted_name")
        if name:
            return str(name).strip()
    except Exception:
        pass
    #fallbacks
    for k in ("name", "full_name", "candidate_name"):
        if isinstance(raw.get(k), str) and raw[k].strip():
            return raw[k].strip()
    return "Unknown"

def _location_str(exp: Dict[str, Any]) -> str:
    loc = exp.get("location") or {}
    if isinstance(loc, dict):
        if loc.get("short_display_address"):
            return str(loc["short_display_address"]).strip()
        # stitch parts if present
        parts = []
        for key in ("city", "state", "region", "country"):
            v = loc.get(key)
            if v:
                parts.append(str(v))
        if parts:
            return ", ".join(parts)
    # last resort
    return str(exp.get("company_location") or "").strip()

def extract_experiences(raw: Dict[str, Any]) -> List[WorkEntry]:
    exps = []
    for exp in raw.get("experience", []) or []:
        title = _pick(exp, "title", "role", "position", default="Unknown")
        start_s = _pick(exp, "start_date", "startDate")
        end_s = _pick(exp, "end_date", "endDate")
        current = bool(exp.get("current_job") or exp.get("is_current") or False)

        start_d = parse_date(start_s)
        end_d = parse_date(end_s)
        #if explicitly current and no end date, we’ll print end later as needed
        exps.append(WorkEntry(
            title=title,
            start_date=start_s if start_s else None,
            end_date=end_s if end_s else None,
            location=_location_str(exp) or None,
            current=current
        ))
    #sort by end desc then start desc using parsed dates
    def _parsed_end(e) -> date:
        pd = parse_date(e.get("end_date"))
        #none should come as very old so current jobs go first only if they have end None?
        #for printing order, treat None as "today" if marked current, else very old.
        if pd:
            return pd
        return date.max if e.get("current") else date.min

    def _parsed_start(e) -> date:
        pd = parse_date(e.get("start_date"))
        return pd if pd else date.min

    exps.sort(key=lambda e: (_parsed_end(e), _parsed_start(e)), reverse=True)
    return exps

def normalize_candidate(raw: Dict[str, Any]) -> Candidate:
    name = extract_name(raw)
    experiences = extract_experiences(raw)
    # skills
    skills = []
    for s in raw.get("extracted_skills", []) or []:
        if isinstance(s, str):
            skills.append(s)
        elif isinstance(s, dict) and s.get("name"):
            skills.append(str(s["name"]))
    #industries from experiences
    inds = set()
    for exp in raw.get("experience", []) or []:
        ind = (exp.get("company_details") or {}).get("industry")
        if ind:
            inds.add(str(ind))
    return {
        "name": name,
        "experiences": experiences,
        "skills": skills,
        "industries": list(inds),
        "raw": raw,
    }
