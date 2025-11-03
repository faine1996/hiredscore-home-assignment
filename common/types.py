from __future__ import annotations
from typing import TypedDict, Optional, List

class WorkEntry(TypedDict, total=False):
    title: str
    start_date: Optional[str]
    end_date: Optional[str]
    location: Optional[str]
    current: Optional[bool]

class Candidate(TypedDict, total=False):
    name: str
    experiences: List[WorkEntry]
    skills: List[str]
    industries: List[str]
    raw: dict  # keep original for edge fields
