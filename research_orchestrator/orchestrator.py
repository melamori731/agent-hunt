"""Research orchestrator. Writes assignments and stage changes. Does not research or deploy."""

from __future__ import annotations

from datetime import datetime, timedelta

from research_orchestrator.schedule import StandupSchedule
from research_orchestrator.stage_decision import StageDecision
from research_orchestrator.store import OrchestratorStore

STAGES = ["research", "validation", "rule_specification", "human_review"]
ABUSE_PURPOSE = "abuse_classification"


class ResearchOrchestrator:
    def __init__(self, store: OrchestratorStore, rework_limit: int = 2, interval: timedelta | None = None) -> None:
        self.store = store
        self.decisions = StageDecision(rework_limit)
        self.schedule = StandupSchedule(interval)
        self.stages = list(STAGES)

    def _terminated(self) -> bool:
        return any(row.get("terminated") for row in self.store.all("decisions"))

    def accept_human(self, request: dict) -> dict | None:
        if self._terminated():
            return None
        if request.get("purpose") == ABUSE_PURPOSE:
            return None
        name = request.get("assistant_name")
        if not name:
            raise ValueError("a research request names an assistant")
        return self.store.add(
            "assignments",
            {
                "role": "agent-intelligence",
                "assistant_name": name,
                "writer": "research-orchestrator",
            },
        )

    def assign_waiting(self, hypothesis: dict, *, previous_standup: datetime | None, now: datetime) -> list[dict]:
        if self._terminated():
            return []
        if not self.schedule.is_due(previous_standup, now):
            return []
        if hypothesis.get("status") != "awaiting_validation":
            return []
        written = []
        for role in ("dataset-validation", "sandbox-validation"):
            written.append(
                self.store.add(
                    "assignments",
                    {
                        "role": role,
                        "hypothesis_id": hypothesis["id"],
                        "writer": "research-orchestrator",
                        "starts_shopping_agent": False,
                    },
                )
            )
        return written

    def review_validation(self, hypothesis: dict, dataset: str, sandbox: str, evaluator: str | None, stage: str) -> dict:
        if evaluator != "PASS":
            return {"stage": stage, "advanced": False, "rule_request": False}
        if dataset == "contradict" or sandbox == "contradict" or hypothesis.get("insufficiently_defined"):
            record = self.decisions.contradiction()
            self.store.add("decisions", record)
            self.store.add(
                "returns",
                {"hypothesis_id": hypothesis["id"], "kind": "investigation", "writer": "research-orchestrator"},
            )
            return {"stage": stage, "advanced": False, "rule_request": False, "decision": record}
        other_ok = {"support", "inconclusive", "blocked"}
        one_support = (dataset == "support") ^ (sandbox == "support")
        if one_support and dataset in other_ok and sandbox in other_ok:
            record = self.decisions.rule_from_partial_support()
            self.store.add("decisions", record)
            self.store.add(
                "specifications",
                {
                    "hypothesis_id": hypothesis["id"],
                    "confidence": "lower",
                    "submitted": True,
                    "deployed": False,
                    "writer": "research-orchestrator",
                },
            )
            return {"stage": stage, "advanced": True, "rule_request": True, "decision": record}
        if dataset == "support" and sandbox == "support":
            record = self.decisions.advance(stage=stage, stages=self.stages, evaluator="PASS", checks_passed=True)
            self.store.add("decisions", record)
            self.store.add(
                "specifications",
                {
                    "hypothesis_id": hypothesis["id"],
                    "confidence": "standard",
                    "submitted": True,
                    "deployed": False,
                    "writer": "research-orchestrator",
                },
            )
            return {"stage": record["stage"], "advanced": True, "rule_request": True, "decision": record}
        return {"stage": stage, "advanced": False, "rule_request": False}

    def consider_advance(self, stage: str, evaluator: str | None, checks_passed: bool) -> str:
        if evaluator != "PASS" or not checks_passed:
            return stage
        record = self.decisions.advance(
            stage=stage, stages=self.stages, evaluator=evaluator, checks_passed=checks_passed
        )
        self.store.add("decisions", record)
        return record["stage"]

    def handle_rework(self, rework_count: int, responsible_agent: str) -> dict:
        record = self.decisions.rework(rework_count=rework_count, responsible_agent=responsible_agent)
        self.store.add("decisions", record)
        if record["decision"] == "REWORK":
            self.store.add(
                "assignments",
                {"role": responsible_agent, "kind": "rework", "writer": "research-orchestrator"},
            )
        return record

    def handle_security_violation(self) -> dict:
        record = self.decisions.security_violation()
        self.store.add("decisions", record)
        return record
