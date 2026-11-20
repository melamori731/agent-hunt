"""Shared fixtures for dataset discovery tests."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

NOW = datetime(2026, 11, 20, tzinfo=UTC)


def write_hypothesis(store: Path, hypothesis_id: str = "H1", fields: list[str] | None = None) -> None:
    store.mkdir(parents=True, exist_ok=True)
    payload = {
        "hypotheses": [
            {
                "id": hypothesis_id,
                "signal": "linux chromium webgl",
                "observation": "The fingerprint appears more often in Muse sessions.",
                "sources": [
                    {
                        "url": "https://example.edu/notes/muse",
                        "title": "Muse session notes",
                    }
                ],
                "measurementFields": fields if fields is not None else ["user_agent", "webgl_renderer"],
            }
        ]
    }
    (store / "hypotheses.json").write_text(json.dumps(payload), encoding="utf-8")


def complete_candidate(**overrides: Any) -> dict[str, Any]:
    candidate = {
        "datasetName": "muse-human-sessions",
        "sourceUrl": "https://example.edu/datasets/muse-human",
        "title": "Labelled Muse and human shopping sessions",
        "text": "linux chromium webgl user agent sessions",
        "queryMatchOnly": False,
        "hasHumanLabel": True,
        "hasAgentLabel": True,
        "hasSessionIdentifier": True,
        "license": "CC-BY-4.0",
        "verifiedAt": "2026-06-01T00:00:00Z",
        "fields": ["user_agent", "webgl_renderer"],
        "collectionMethod": "browser telemetry",
    }
    candidate.update(overrides)
    return candidate


def hypothesis() -> dict[str, Any]:
    return {"id": "H1", "signal": "linux chromium webgl", "measurementFields": ["user_agent", "webgl_renderer"]}
