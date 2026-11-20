"""Integration checks for stored stage records."""

import json
import os
import subprocess
from pathlib import Path

from independent_evaluator.evaluator import IndependentEvaluator


def _write(root: Path, name: str, rows: list) -> None:
    (root / f"{name}.json").write_text(json.dumps(rows), encoding="utf-8")


def _stage(root: Path) -> bytes:
    payload = [{"stage": "research", "writer": "research-orchestrator"}]
    _write(root, "decisions", payload)
    return (root / "decisions.json").read_bytes()


def test_hypothesis_withSources_writesPass(tmp_path):
    # REQ-001
    _write(
        tmp_path,
        "hypotheses",
        [{"hypothesis_id": "h1", "sources": [{"url": "https://example.test/a", "title": "A"}]}],
    )
    row = IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    assert row == {
        "hypothesis_id": "h1",
        "stage": "hypothesis",
        "result": "PASS",
        "trigger": "hypothesis has sources",
    }


def test_hypothesis_missingSources_writesRework(tmp_path):
    # REQ-002
    empty = tmp_path / "empty"
    missing = tmp_path / "missing"
    empty.mkdir()
    missing.mkdir()
    _write(empty, "hypotheses", [{"hypothesis_id": "h1", "sources": []}])
    before_empty = _stage(empty)
    before_missing = _stage(missing)
    empty_row = IndependentEvaluator(empty).evaluate("h1", "hypothesis")
    missing_row = IndependentEvaluator(missing).evaluate("h1", "hypothesis")
    assert empty_row["result"] == "REWORK"
    assert empty_row["trigger"] == "hypothesis has no sources"
    assert missing_row["result"] == "REWORK"
    assert missing_row["trigger"] == "hypothesis record is missing"
    assert (empty / "decisions.json").read_bytes() == before_empty
    assert (missing / "decisions.json").read_bytes() == before_missing


def test_validation_consistentPair_writesPass(tmp_path):
    # REQ-003
    both = tmp_path / "both"
    partial = tmp_path / "partial"
    both.mkdir()
    partial.mkdir()
    _write(
        both,
        "validations",
        [
            {"hypothesis_id": "h1", "kind": "dataset", "outcome": "support"},
            {"hypothesis_id": "h1", "kind": "sandbox", "outcome": "support"},
        ],
    )
    _write(
        partial,
        "validations",
        [
            {"hypothesis_id": "h1", "kind": "dataset", "outcome": "support"},
            {"hypothesis_id": "h1", "kind": "sandbox", "outcome": "inconclusive"},
        ],
    )
    assert IndependentEvaluator(both).evaluate("h1", "validation")["result"] == "PASS"
    assert IndependentEvaluator(partial).evaluate("h1", "validation")["result"] == "PASS"


def test_validation_contradictionOrMissing_writesRework(tmp_path):
    # REQ-004
    missing = tmp_path / "missing"
    clash = tmp_path / "clash"
    missing.mkdir()
    clash.mkdir()
    _write(
        missing,
        "validations",
        [{"hypothesis_id": "h1", "kind": "dataset", "outcome": "support"}],
    )
    _write(
        clash,
        "validations",
        [
            {"hypothesis_id": "h1", "kind": "dataset", "outcome": "support"},
            {"hypothesis_id": "h1", "kind": "sandbox", "outcome": "reject"},
        ],
    )
    before_missing = _stage(missing)
    before_clash = _stage(clash)
    missing_row = IndependentEvaluator(missing).evaluate("h1", "validation")
    clash_row = IndependentEvaluator(clash).evaluate("h1", "validation")
    assert missing_row["result"] == "REWORK"
    assert missing_row["trigger"] == "validation result is missing"
    assert clash_row["result"] == "REWORK"
    assert clash_row["trigger"] == "validation pair contradicts"
    assert (missing / "decisions.json").read_bytes() == before_missing
    assert (clash / "decisions.json").read_bytes() == before_clash


def test_rule_submittedWithCitations_writesPass(tmp_path):
    # REQ-005
    _write(
        tmp_path,
        "rule_specifications",
        [
            {
                "hypothesis_id": "h1",
                "submitted": True,
                "deployed": False,
                "research_sources": [{"title": "Source"}],
                "validation_results": ["dataset support"],
            }
        ],
    )
    row = IndependentEvaluator(tmp_path).evaluate("h1", "rule_specification")
    assert row["result"] == "PASS"
    assert row["trigger"] == "rule specification is submitted with citations"
    assert row["stage"] == "rule_specification"


def test_rule_notEligible_writesRework(tmp_path):
    # REQ-006
    cases = {
        "missing": None,
        "unsubmitted": {
            "hypothesis_id": "h1",
            "submitted": False,
            "deployed": False,
            "research_sources": ["s"],
            "validation_results": ["v"],
        },
        "deployed": {
            "hypothesis_id": "h1",
            "submitted": True,
            "deployed": True,
            "research_sources": ["s"],
            "validation_results": ["v"],
        },
        "no_sources": {
            "hypothesis_id": "h1",
            "submitted": True,
            "deployed": False,
            "research_sources": [],
            "validation_results": ["v"],
        },
        "no_results": {
            "hypothesis_id": "h1",
            "submitted": True,
            "deployed": False,
            "research_sources": ["s"],
            "validation_results": [""],
        },
    }
    expected = {
        "missing": "rule specification is missing",
        "unsubmitted": "rule specification is not submitted",
        "deployed": "rule specification is deployed",
        "no_sources": "rule specification lacks research sources",
        "no_results": "rule specification lacks validation results",
    }
    for name, row in cases.items():
        root = tmp_path / name
        root.mkdir()
        if row is not None:
            _write(root, "rule_specifications", [row])
        before = _stage(root)
        result = IndependentEvaluator(root).evaluate("h1", "rule_specification")
        assert result["result"] == "REWORK"
        assert result["trigger"] == expected[name]
        assert (root / "decisions.json").read_bytes() == before


def test_evaluator_sideEffects_writesOnlyEvaluation(tmp_path, monkeypatch):
    # REQ-007
    launched = []
    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: launched.append(args))
    monkeypatch.setattr(os, "system", lambda *args, **kwargs: launched.append(args))
    _write(tmp_path, "hypotheses", [{"hypothesis_id": "h1", "sources": ["https://example.test/a"]}])
    row = IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    assert list(row) == ["hypothesis_id", "stage", "result", "trigger"]
    assert launched == []
    names = {path.name for path in tmp_path.iterdir()}
    assert "faculty_report.json" not in names
    assert "messages.json" not in names
    assert names == {"hypotheses.json", "evaluations.json"}


def test_evaluation_afterRestart_remainsReadable(tmp_path):
    # QR-001
    _write(tmp_path, "hypotheses", [{"hypothesis_id": "h1", "sources": ["https://example.test/a"]}])
    written = IndependentEvaluator(tmp_path).evaluate("h1", "hypothesis")
    del written
    stored = IndependentEvaluator(tmp_path).read_evaluations()
    assert stored == [
        {
            "hypothesis_id": "h1",
            "stage": "hypothesis",
            "result": "PASS",
            "trigger": "hypothesis has sources",
        }
    ]


def test_evaluation_repeat_sameResult(tmp_path):
    # QR-002
    _write(tmp_path, "hypotheses", [{"hypothesis_id": "h1", "sources": ["https://example.test/a"]}])
    evaluator = IndependentEvaluator(tmp_path)
    first = evaluator.evaluate("h1", "hypothesis")
    second = evaluator.evaluate("h1", "hypothesis")
    assert first["result"] == second["result"]
    assert first["trigger"] == second["trigger"]
    assert len(evaluator.read_evaluations()) == 2
