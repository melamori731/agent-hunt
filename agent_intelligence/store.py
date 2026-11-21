"""JSON files for registry entries, reports, hypotheses, and unresolved investigations."""

from __future__ import annotations

import json
from pathlib import Path


class JsonResearchStore:
    """Read and write research records. This class does not decide which records are valid."""

    REGISTRY_ENTRIES = "registry_entries.json"
    REGISTRY_REPORTS = "registry_reports.json"
    HYPOTHESES = "hypotheses.json"
    UNRESOLVED = "unresolved_investigations.json"

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def write_registry_entry(self, record: dict) -> None:
        self._append(self.REGISTRY_ENTRIES, record)

    def write_registry_report(self, record: dict) -> None:
        self._append(self.REGISTRY_REPORTS, record)

    def write_hypothesis(self, record: dict) -> None:
        self._append(self.HYPOTHESES, record)

    def write_unresolved_investigation(self, record: dict) -> None:
        self._append(self.UNRESOLVED, record)

    def read_registry_entries(self) -> list[dict]:
        return self._read(self.REGISTRY_ENTRIES)

    def read_registry_reports(self) -> list[dict]:
        return self._read(self.REGISTRY_REPORTS)

    def read_hypotheses(self) -> list[dict]:
        return self._read(self.HYPOTHESES)

    def read_unresolved_investigations(self) -> list[dict]:
        return self._read(self.UNRESOLVED)

    def _read(self, filename: str) -> list[dict]:
        path = self.directory / filename
        if not path.is_file():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def _append(self, filename: str, record: dict) -> None:
        records = self._read(filename)
        records.append(record)
        path = self.directory / filename
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
