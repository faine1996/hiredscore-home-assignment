from __future__ import annotations
from typing import List
from datetime import date
from .dates import parse_date, format_date, gap_days
from common.types import WorkEntry

def format_greeting(name: str) -> str:
    return f"Hello {name},"

def format_experience(e: WorkEntry) -> str:
    start = format_date(parse_date(e.get("start_date")))
    end_d = parse_date(e.get("end_date"))
    # if end missing but current=True, we still need a date string; use blank if truly missing
    end = format_date(end_d) if end_d else ""
    loc = e.get("location") or ""
    return f"Worked as: {e.get('title','Unknown')}, From {start} To {end} in {loc}"

def format_gap(days: int) -> str:
    return f"Gap in CV for {days} days"
