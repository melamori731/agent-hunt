"""Persist dataset registry entries in datasets.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DatasetRegistry:
    """Keep one datasets.json entry for each dataset name and hypothesis id."""

    def __init__(self, store_dir: Path | str) -> None:
        self.store_dir = Path(store_dir)
        self.path = self.store_dir / "datasets.json"

    def read(self) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        datasets = payload.get("datasets") if isinstance(payload, dict) else None
        if not isinstance(datasets, list):
            return []
        return [item for item in datasets if isinstance(item, dict)]

    def upsert(self, entry: dict[str, Any]) -> None:
        self._validate(entry)
        records = self.read()
        key = (entry["datasetName"], entry["hypothesisId"])
        replaced = False
        updated: list[dict[str, Any]] = []
        for existing in records:
            if (existing.get("datasetName"), existing.get("hypothesisId")) == key:
                updated.append(dict(entry))
                replaced = True
            else:
                updated.append(existing)
        if not replaced:
            updated.append(dict(entry))
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"datasets": updated}, indent=2) + "\n",
            encoding="utf-8",
        )

    def has_suitable(self, hypothesis_id: str) -> bool:
        return any(
            item.get("hypothesisId") == hypothesis_id and item.get("suitability") == "suitable"
            for item in self.read()
        )

    def _validate(self, entry: dict[str, Any]) -> None:
        name = str(entry.get("datasetName") or "").strip()
        title = str(entry.get("title") or "").strip()
        hypothesis_id = str(entry.get("hypothesisId") or "").strip()
        source_url = str(entry.get("sourceUrl") or "").strip()
        suitability = entry.get("suitability")
        if not name or not title or not hypothesis_id:
            raise ValueError("registry entry is missing an identity field")
        if not source_url.startswith("https://") and not source_url.startswith("http://"):
            raise ValueError("registry entry source URL must be http or https")
        if suitability not in {"suitable", "unsuitable"}:
            raise ValueError("registry entry suitability is invalid")
