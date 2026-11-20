"""JSON persistence for orchestrator assignments and decisions."""

from __future__ import annotations

import json
from pathlib import Path


class OrchestratorStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.root / f"{name}.json"

    def _read(self, name: str) -> list:
        path = self._path(name)
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, name: str, rows: list) -> None:
        self._path(name).write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def add(self, name: str, row: dict) -> dict:
        if name == "decisions" and (not row.get("trigger") or not row.get("decision")):
            raise ValueError("a stage decision requires a trigger and a decision")
        rows = self._read(name)
        rows.append(row)
        self._write(name, rows)
        return row

    def all(self, name: str) -> list:
        return list(self._read(name))
