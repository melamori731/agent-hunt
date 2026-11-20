"""Unit tests for OrchestratorStore. QR-002."""

from research_orchestrator.store import OrchestratorStore


def test_orchestratorStore_reopen_returnsDecisionsWithTriggers(tmp_path):
    first = OrchestratorStore(tmp_path)
    for decision, trigger in (
        ("PASS", "checks passed"),
        ("REWORK", "correctable failure"),
        ("ESCALATE", "contradiction"),
        ("STOP", "security violation"),
    ):
        first.add("decisions", {"decision": decision, "trigger": trigger, "detail": trigger})
    second = OrchestratorStore(tmp_path)
    rows = second.all("decisions")
    assert [row["decision"] for row in rows] == ["PASS", "REWORK", "ESCALATE", "STOP"]
    assert all(row["trigger"] for row in rows)
