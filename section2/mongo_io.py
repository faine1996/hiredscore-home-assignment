from __future__ import annotations
from typing import List, Dict, Any
from pymongo import MongoClient

def connect(uri: str = "mongodb://localhost:27017") -> MongoClient:
    return MongoClient(uri)

def insert_filtered(db, docs: List[Dict[str, Any]]) -> None:
    coll = db["filtered_candidates"]
    # optional: helpful index
    try:
        coll.create_index("name")
    except Exception:
        pass
    if docs:
        coll.insert_many(docs)
