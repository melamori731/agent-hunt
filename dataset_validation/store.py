"""JSON persistence for dataset_results.json."""

from __future__ import annotations

import json
from pathlib import Path


class DatasetResultStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def read(self) -> list:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def append(self, record: dict) -> dict:
        rows = self.read()
        rows.append(record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return record
