from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DB_PATH = Path("data/database.json")


def load_db() -> dict[str, Any]:
    """Load the JSON database from disk.

    Returns:
        A dictionary with keys: tools, members, loans.
    """
    if not DB_PATH.exists():
        return {"tools": [], "members": [], "loans": []}

    with DB_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Be defensive if file exists but is incomplete
    data.setdefault("tools", [])
    data.setdefault("members", [])
    data.setdefault("loans", [])
    return data


def save_db(db: dict[str, Any]) -> None:
    """Save the in-memory database to disk.

    Args:
        db: database dictionary.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)