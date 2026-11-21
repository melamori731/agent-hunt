"""Unit tests for ResearchOrchestrator. INV-001, INV-003, REQ-001, REQ-002, REQ-003, REQ-006, REQ-007."""

from datetime import datetime, timedelta

from research_orchestrator.orchestrator import ResearchOrchestrator
from research_orchestrator.store import OrchestratorStore


def _orch(tmp_path, **kwargs):
    return ResearchOrchestrator(OrchestratorStore(tmp_path), **kwargs)


def test_researchOrchestrator_stageChange_namesOrchestrator(tmp_path):
    orch = _orch(tmp_path)
    stage = orch.consider_advance("research", "PASS", True)
    assert stage == "validation"
    assert orch.store.all("decisions")[0]["writer"] == "research-orchestrator"


def test_researchOrchestrator_namedAssistant_writesAssignmentOnly(tmp_path):
    orch = _orch(tmp_path)
    written = orch.accept_human({"assistant_name": "Muse"})
    assert written["assistant_name"] == "Muse"
    assert written["role"] == "agent-intelligence"
    assert orch.store.all("hypotheses") == []


def test_researchOrchestrator_abuseRequest_writesNothing(tmp_path):
    orch = _orch(tmp_path)
    assert orch.accept_human({"purpose": "abuse_classification"}) is None
    assert orch.store.all("assignments") == []


def test_researchOrchestrator_waitingHypothesis_writesBothAssignments(tmp_path):
    orch = _orch(tmp_path, interval=timedelta(hours=1))
    now = datetime(2026, 11, 20, 18, 0)
    rows = orch.assign_waiting(
        {"id": "H1", "status": "awaiting_validation"},
        previous_standup=now - timedelta(hours=1),
        now=now,
    )
    roles = {row["role"] for row in rows}
    assert roles == {"dataset-validation", "sandbox-validation"}
    assert all(row["starts_shopping_agent"] is False for row in rows)


def test_researchOrchestrator_eligibleResult_writesNoDeployedRule(tmp_path):
    orch = _orch(tmp_path)
    result = orch.review_validation(
        {"id": "H1"},
        "support",
        "support",
        "PASS",
        "validation",
    )
    assert result["rule_request"] is True
    spec = orch.store.all("specifications")[0]
    assert spec["submitted"] is True
    assert spec["deployed"] is False


def test_researchOrchestrator_missingEvaluator_doesNotAdvance(tmp_path):
    orch = _orch(tmp_path)
    assert orch.consider_advance("validation", None, True) == "validation"
    assert orch.store.all("decisions") == []
