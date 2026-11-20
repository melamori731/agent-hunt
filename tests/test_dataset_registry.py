"""Unit tests for DatasetRegistry. INV-001 POL-002."""

from __future__ import annotations

from pathlib import Path

import pytest

from dataset_discovery.registry import DatasetRegistry


def _entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "datasetName": "muse-human-sessions",
        "sourceUrl": "https://example.edu/datasets/muse-human",
        "title": "Labelled Muse and human shopping sessions",
        "suitability": "suitable",
        "hypothesisId": "H1",
        "collectionMethod": "browser telemetry",
        "hasSessionIdentifier": True,
        "hasHumanLabel": True,
        "hasAgentLabel": True,
        "license": "CC-BY-4.0",
        "verifiedAt": "2026-06-01T00:00:00Z",
    }
    entry.update(overrides)
    return entry


def test_datasetRegistry_missingName_rejected(tmp_path: Path) -> None:
    # INV-001: identity fields are required on DatasetRegistry.
    registry = DatasetRegistry(tmp_path)
    for field in ("datasetName", "title", "hypothesisId"):
        broken = _entry()
        broken[field] = "  "
        with pytest.raises(ValueError):
            registry.upsert(broken)
    broken = _entry(suitability="maybe")
    with pytest.raises(ValueError):
        registry.upsert(broken)
    assert registry.read() == []


def test_datasetRegistry_badUrl_rejected(tmp_path: Path) -> None:
    # INV-001: the source URL is http or https.
    registry = DatasetRegistry(tmp_path)
    with pytest.raises(ValueError):
        registry.upsert(_entry(sourceUrl="ftp://example.edu/data"))
    assert registry.read() == []


def test_datasetRegistry_repeatPair_keepsOneEntry(tmp_path: Path) -> None:
    # POL-002: one entry per dataset name and hypothesis id.
    registry = DatasetRegistry(tmp_path)
    registry.upsert(_entry(suitability="unsuitable"))
    registry.upsert(_entry(suitability="suitable", title="Updated title"))
    registry.upsert(_entry(hypothesisId="H2"))
    records = registry.read()
    pair = [item for item in records if item["hypothesisId"] == "H1"]
    assert len(pair) == 1
    assert pair[0]["suitability"] == "suitable"
    assert pair[0]["title"] == "Updated title"
    assert len(records) == 2
