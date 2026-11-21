"""Unit tests for HypothesisReader."""

from __future__ import annotations

import json
from pathlib import Path

from dataset_discovery.hypothesis_reader import HypothesisReader


def test_hypothesisReader_idOrHypothesisId_returnsId(tmp_path: Path) -> None:
    payload = {
        "hypotheses": [
            {"id": "H1", "signal": "webgl"},
            {"hypothesisId": "H2", "signal": "ua"},
            {"signal": "missing id"},
        ]
    }
    (tmp_path / "hypotheses.json").write_text(json.dumps(payload), encoding="utf-8")
    found = HypothesisReader(tmp_path).read()
    assert [item["id"] for item in found] == ["H1", "H2"]


def test_hypothesisReader_listMeasurements_returnsFields(tmp_path: Path) -> None:
    payload = {
        "hypotheses": [
            {"id": "H1", "measurementFields": ["user_agent", "webgl_renderer"]},
            {"hypothesisId": "H2", "measurements": ["client_hint"]},
        ]
    }
    (tmp_path / "hypotheses.json").write_text(json.dumps(payload), encoding="utf-8")
    found = HypothesisReader(tmp_path).read()
    assert found[0]["measurementFields"] == ["user_agent", "webgl_renderer"]
    assert found[1]["measurementFields"] == ["client_hint"]


def test_hypothesisReader_proseMeasurements_returnsNoFields(tmp_path: Path) -> None:
    payload = {
        "hypotheses": [
            {
                "id": "H1",
                "measurements": "Calculate prevalence of the Linux user agent.",
            }
        ]
    }
    (tmp_path / "hypotheses.json").write_text(json.dumps(payload), encoding="utf-8")
    found = HypothesisReader(tmp_path).read()
    assert found[0]["measurementFields"] == []
