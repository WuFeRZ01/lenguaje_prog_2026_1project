from __future__ import annotations

from pathlib import Path

import pytest

import src.tool_lending.storage as storage


@pytest.fixture(autouse=True)
def temp_db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_file = tmp_path / "database.json"
    monkeypatch.setattr(storage, "DB_PATH", db_file)
    return db_file