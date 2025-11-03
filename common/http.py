from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json
from typing import Any

DEFAULT_TIMEOUT = 20.0

def fetch_json(url: str, timeout: float = DEFAULT_TIMEOUT) -> Any:
    req = Request(url, headers={"user-agent": "python-urllib/3.11"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except HTTPError as e:
        raise RuntimeError(f"hTTP error {e.code} when fetching {url}") from e
    except URLError as e:
        raise RuntimeError(f"network error when fetching {url}: {e.reason}") from e

    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"invalid jSON from {url}") from e