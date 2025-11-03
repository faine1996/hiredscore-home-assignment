from __future__ import annotations
from datetime import date, datetime
from typing import Optional

# accepted input examples:
# "jan/05/2020", "Jan/2020", "2020-01-05", "2020/01/05", "2020"
_INPUT_FORMATS = [
    "%b/%d/%Y",
    "%b/%Y",        # missing day -> we'll add later
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y",
]

def parse_date(s: Optional[str]) -> Optional[date]:
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    for fmt in _INPUT_FORMATS:
        try:
            dt = datetime.strptime(s, fmt)
            # if format lacked a day, set day to 1
            if fmt == "%b/%Y":
                return date(dt.year, dt.month, 1)
            if fmt == "%Y":
                return date(dt.year, 1, 1)
            return dt.date()
        except ValueError:
            continue
    # as a last resort, try to split weird "MMM/DD/YYYY" where DD might be 1 digit
    try:
        parts = s.replace("-", "/").split("/")
        if len(parts) == 3 and len(parts[1]) == 1:
            parts[1] = parts[1].zfill(2)
            dt = datetime.strptime("/".join(parts), "%b/%d/%Y")
            return dt.date()
    except Exception:
        pass
    return None

def format_date(d: Optional[date]) -> str:
    if not d:
        return ""
    return d.strftime("%b/%d/%Y")

def gap_days(prev_end: Optional[date], next_start: Optional[date]) -> int:
    if not prev_end or not next_start:
        return 0
    delta = (prev_end - next_start).days
    # we compare in Section 1 after sorting by end desc; adjust sign properly
    return max(0, (next_start - prev_end).days)


def inclusive_gap_days(prev_end: Optional[date], next_start: Optional[date]) -> int:
    if not prev_end or not next_start:
        return 0
    # treat employment dates as inclusive
    return max(0, (next_start - prev_end).days - 1)
