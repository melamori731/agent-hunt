"""Read stored hypothesis JSON without importing another agent package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class HypothesisReader:
    """Normalize hypothesis id and measurement fields from hypotheses.json."""

    def __init__(self, store_dir: Path | str) -> None:
        self.path = Path(store_dir) / "hypotheses.json"

    def read(self) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        records = payload.get("hypotheses") if isinstance(payload, dict) else payload
        if not isinstance(records, list):
            return []
        normalized: list[dict[str, Any]] = []
        for record in records:
            if not isinstance(record, dict):
                continue
            hypothesis_id = _hypothesis_id(record)
            if hypothesis_id is None:
                continue
            normalized.append(
                {
                    "id": hypothesis_id,
                    "signal": str(record.get("signal") or ""),
                    "measurementFields": _measurement_fields(record),
                }
            )
        return normalized


def _hypothesis_id(record: dict[str, Any]) -> str | None:
    for key in ("id", "hypothesisId"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _measurement_fields(record: dict[str, Any]) -> list[str]:
    named = record.get("measurementFields")
    if _string_list(named):
        return list(named)
    measurements = record.get("measurements")
    if _string_list(measurements):
        return list(measurements)
    return []


def _string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)
