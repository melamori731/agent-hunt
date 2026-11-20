"""Unit tests for EvaluationRecord and IndependentEvaluator."""

import json
from pathlib import Path

import pytest

from independent_evaluator.evaluator import EvaluationRecord, IndependentEvaluator


def _write(root: Path, name: str, rows: list) -> None:
    (root / f"{name}.json").write_text(json.dumps(rows), encoding="utf-8")


def test_evaluationRecord_emptyTrigger_rejected():
    # INV-002
    with pytest.raises(ValueError):
        EvaluationRecord("h1", "hypothesis", "PASS", "").as_dict()


def test_evaluationRecord_otherResult_rejected():
    # INV-002
    with pytest.raises(ValueError):
        EvaluationRecord("h1", "hypothesis", "ESCALATE", "suspend").as_dict()
    with pytest.raises(ValueError):
        EvaluationRecord("h1", "hypothesis", "STOP", "terminate").as_dict()


def test_evaluationRecord_extraField_rejected():
    # INV-002
    with pytest.raises(ValueError):
        EvaluationRecord.require(
            {
                "hypothesis_id": "h1",
                "stage": "hypothesis",
                "result": "PASS",
                "trigger": "hypothesis has sources",
                "writer": "independent-evaluator",
            }
        )


def test_independentEvaluator_stageFile_unchanged(tmp_path):
    # INV-001
    stage = {"stage": "research", "writer": "research-orchestrator"}
    _write(tmp_path, "decisions", [stage])
    _write(tmp_path, "hypotheses", [{"hypothesis_id": "h1", "sources": ["https://example.test/a"]}])
    before = (tmp_path / "decisions.json").read_bytes()
    IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    _write(tmp_path, "hypotheses", [{"hypothesis_id": "h1", "sources": []}])
    IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    assert (tmp_path / "decisions.json").read_bytes() == before


def test_independentEvaluator_emptySources_rework(tmp_path):
    # POL-001
    _write(tmp_path, "hypotheses", [{"hypothesis_id": "h1", "sources": ["  "]}])
    row = IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    assert row["result"] == "REWORK"
    assert row["trigger"] == "hypothesis has no sources"


def test_independentEvaluator_supportAndInconclusive_pass(tmp_path):
    # POL-002
    _write(
        tmp_path,
        "validations",
        [
            {"hypothesis_id": "h1", "kind": "dataset", "outcome": "support"},
            {"hypothesis_id": "h1", "kind": "sandbox", "outcome": "inconclusive"},
        ],
    )
    row = IndependentEvaluator(tmp_path).evaluate("h1", "validation")
    assert row["result"] == "PASS"


def test_independentEvaluator_supportAndReject_rework(tmp_path):
    # POL-002
    _write(
        tmp_path,
        "validations",
        [
            {"hypothesis_id": "h1", "kind": "dataset", "outcome": "reject"},
            {"hypothesis_id": "h1", "kind": "sandbox", "outcome": "support"},
        ],
    )
    row = IndependentEvaluator(tmp_path).evaluate("h1", "validation")
    assert row["result"] == "REWORK"
    assert row["trigger"] == "validation pair contradicts"


def test_independentEvaluator_deployedRule_rework(tmp_path):
    # POL-003
    _write(
        tmp_path,
        "rule_specifications",
        [
            {
                "hypothesis_id": "h1",
                "submitted": True,
                "deployed": True,
                "research_sources": ["https://example.test/a"],
                "validation_results": ["dataset support"],
            }
        ],
    )
    row = IndependentEvaluator(tmp_path).evaluate("h1", "rule_specification")
    assert row["result"] == "REWORK"
    assert row["trigger"] == "rule specification is deployed"


def test_independentEvaluator_abusePurpose_reworkWithoutLabel(tmp_path):
    # POL-004
    _write(
        tmp_path,
        "hypotheses",
        [
            {
                "hypothesis_id": "h1",
                "purpose": "abuse_classification",
                "classification": "malicious",
                "sources": ["https://example.test/a"],
            }
        ],
    )
    row = IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    assert row["result"] == "REWORK"
    assert row["trigger"] == "classification is out of scope"
    for label in ("abusive", "malicious", "legitimate"):
        assert label not in row["trigger"]
    assert list(row) == ["hypothesis_id", "stage", "result", "trigger"]
