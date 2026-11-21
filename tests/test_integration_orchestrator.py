"""Integration scenarios from requirements/LOCAL-research-orchestrator/plan/integration-test-scenarios.md."""

from datetime import datetime, timedelta

from research_orchestrator.orchestrator import ResearchOrchestrator
from research_orchestrator.store import OrchestratorStore


def _orch(tmp_path, **kwargs):
    return ResearchOrchestrator(OrchestratorStore(tmp_path), **kwargs)


def test_human_namedAssistant_storesAssignment(tmp_path):
    """REQ-001."""
    orch = _orch(tmp_path)
    written = orch.accept_human({"assistant_name": "Muse"})
    assert written["assistant_name"] == "Muse"
    assert orch.store.all("hypotheses") == []


def test_human_abuseRequest_storesNoAssignment(tmp_path):
    """REQ-002."""
    orch = _orch(tmp_path)
    before = len(orch.store.all("assignments"))
    assert orch.accept_human({"purpose": "abuse_classification"}) is None
    assert len(orch.store.all("assignments")) == before


def test_standup_waitingHypothesis_assignsBothValidators(tmp_path):
    """REQ-003, QR-001."""
    now = datetime(2026, 11, 20, 18, 0)
    hypothesis = {"id": "H1", "status": "awaiting_validation"}
    first = _orch(tmp_path / "a", interval=timedelta(hours=1)).assign_waiting(
        hypothesis, previous_standup=now - timedelta(hours=1), now=now
    )
    second = _orch(tmp_path / "b", interval=timedelta(hours=1)).assign_waiting(
        hypothesis, previous_standup=now - timedelta(hours=1), now=now
    )
    assert [row["role"] for row in first] == [row["role"] for row in second]
    assert {row["role"] for row in first} == {"dataset-validation", "sandbox-validation"}
    assert all(row["starts_shopping_agent"] is False for row in first)


def test_standup_beforeInterval_assignsNothing(tmp_path):
    """REQ-003."""
    now = datetime(2026, 11, 20, 18, 0)
    rows = _orch(tmp_path, interval=timedelta(hours=1)).assign_waiting(
        {"id": "H1", "status": "awaiting_validation"},
        previous_standup=now - timedelta(minutes=59),
        now=now,
    )
    assert rows == []


def test_standup_oneSupport_requestsLowerConfidenceSpec(tmp_path):
    """REQ-004."""
    orch = _orch(tmp_path)
    result = orch.review_validation({"id": "H1"}, "support", "inconclusive", "PASS", "validation")
    assert result["rule_request"] is True
    spec = orch.store.all("specifications")[0]
    assert spec["confidence"] == "lower"


def test_standup_contradiction_returnsInvestigation(tmp_path):
    """REQ-005."""
    orch = _orch(tmp_path)
    before = len(orch.store.all("specifications"))
    result = orch.review_validation({"id": "H1"}, "support", "contradict", "PASS", "validation")
    assert result["rule_request"] is False
    assert len(orch.store.all("specifications")) == before
    assert orch.store.all("returns")[0]["kind"] == "investigation"


def test_evaluator_missingResult_doesNotAdvance(tmp_path):
    """REQ-006."""
    orch = _orch(tmp_path)
    assert orch.consider_advance("validation", None, True) == "validation"


def test_evaluator_pass_advancesOnce(tmp_path):
    """REQ-006."""
    orch = _orch(tmp_path)
    assert orch.consider_advance("research", "PASS", True) == "validation"


def test_standup_eligibleHypothesis_storesSpecNotDeployedRule(tmp_path):
    """REQ-007."""
    orch = _orch(tmp_path)
    orch.review_validation({"id": "H1"}, "support", "support", "PASS", "validation")
    spec = orch.store.all("specifications")[0]
    assert spec["submitted"] is True
    assert spec["deployed"] is False
    assert all(row.get("deployed") is not True for row in orch.store.all("decisions"))


def test_rework_atLimit_suspendsTask(tmp_path):
    """REQ-008."""
    orch = _orch(tmp_path, rework_limit=2)
    record = orch.handle_rework(2, "dataset-validation")
    assert record["decision"] == "ESCALATE"
    assert record["suspended"] is True
    assert orch.store.all("assignments") == []


def test_decisions_afterRestart_includeTrigger(tmp_path):
    """QR-002."""
    orch = _orch(tmp_path)
    orch.store.add("decisions", {"decision": "PASS", "trigger": "checks passed", "detail": "a"})
    orch.store.add("decisions", {"decision": "REWORK", "trigger": "correctable failure", "detail": "b"})
    orch.store.add("decisions", {"decision": "ESCALATE", "trigger": "contradiction", "detail": "c"})
    orch.store.add("decisions", {"decision": "STOP", "trigger": "security violation", "detail": "d"})
    reopened = OrchestratorStore(tmp_path)
    rows = reopened.all("decisions")
    assert [row["decision"] for row in rows] == ["PASS", "REWORK", "ESCALATE", "STOP"]
    assert all(row["trigger"] for row in rows)
