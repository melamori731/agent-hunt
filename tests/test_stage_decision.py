"""Unit tests for StageDecision. INV-002, POL-001, POL-002, POL-003, POL-004."""

import pytest

from research_orchestrator.stage_decision import StageDecision


def test_stageDecision_missingTrigger_rejected():
    gate = StageDecision()
    with pytest.raises(ValueError):
        gate.record("", "PASS", detail="missing")


def test_stageDecision_pass_advancesOneStage():
    gate = StageDecision()
    record = gate.advance(
        stage="research",
        stages=["research", "validation", "rule_specification"],
        evaluator="PASS",
        checks_passed=True,
    )
    assert record["decision"] == "PASS"
    assert record["stage"] == "validation"
    assert record["trigger"]


def test_stageDecision_reworkUnderLimit_returnsTask():
    gate = StageDecision(rework_limit=2)
    record = gate.rework(rework_count=1, responsible_agent="dataset-validation")
    assert record["decision"] == "REWORK"
    assert record["return_to"] == "dataset-validation"


def test_stageDecision_contradiction_suspends():
    record = StageDecision().contradiction()
    assert record["decision"] == "ESCALATE"
    assert record["suspended"] is True
    assert record["rule_request"] is False


def test_stageDecision_securityViolation_terminates():
    record = StageDecision().security_violation()
    assert record["decision"] == "STOP"
    assert record["terminated"] is True


def test_stageDecision_oneSupport_marksLowerConfidence():
    record = StageDecision().rule_from_partial_support()
    assert record["rule_request"] is True
    assert record["lower_confidence"] is True
