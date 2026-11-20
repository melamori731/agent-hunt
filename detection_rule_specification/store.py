"""JSON records for hypotheses, validation results, and rule specifications."""

from __future__ import annotations

import json
from pathlib import Path

from detection_rule_specification.template import SpecificationTemplate


class RuleSpecificationStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.template = SpecificationTemplate()

    def _path(self, name: str) -> Path:
        return self.root / f"{name}.json"

    def _read(self, name: str) -> list:
        path = self._path(name)
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, name: str, rows: list) -> None:
        self._path(name).write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def find(self, name: str, hypothesis_id: str) -> dict | None:
        for row in self._read(name):
            row_id = row.get("hypothesis_id", row.get("id"))
            if row_id == hypothesis_id:
                return row
        return None

    def research_sources(self, hypothesis: dict) -> list:
        if "research_sources" in hypothesis:
            return list(hypothesis["research_sources"])
        return list(hypothesis.get("sources") or [])

    def validation_pair(self, row: dict) -> tuple[str, str]:
        dataset = row.get("dataset_result")
        sandbox = row.get("sandbox_result")
        nested = row.get("validation_results")
        if not isinstance(nested, dict):
            nested = {}
        if dataset is None:
            dataset = nested.get("dataset_result")
        if sandbox is None:
            sandbox = nested.get("sandbox_result")
        return str(dataset or ""), str(sandbox or "")

    def specifications(self) -> list:
        return list(self._read("rule_specifications"))

    def save_specification(self, record: dict) -> dict:
        self.template.assert_record(record)
        rows = [row for row in self.specifications() if row.get("hypothesis_id") != record["hypothesis_id"]]
        rows.append(record)
        self._write("rule_specifications", rows)
        return record
