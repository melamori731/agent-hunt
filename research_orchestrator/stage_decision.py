"""Stage transitions for the research orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

DECISIONS = ("PASS", "REWORK", "ESCALATE", "STOP")


@dataclass(frozen=True)
class DecisionRecord:
    trigger: str
    decision: str
    detail: str
    stage: str | None = None
    return_to: str | None = None
    suspended: bool = False
    terminated: bool = False
    rule_request: bool = False
    lower_confidence: bool = False

    def as_dict(self) -> dict:
        if not self.trigger or self.decision not in DECISIONS:
            raise ValueError("a stage decision requires a trigger and a decision")
        return {
            "trigger": self.trigger,
            "decision": self.decision,
            "detail": self.detail,
            "stage": self.stage,
            "return_to": self.return_to,
            "suspended": self.suspended,
            "terminated": self.terminated,
            "rule_request": self.rule_request,
            "lower_confidence": self.lower_confidence,
            "writer": "research-orchestrator",
        }


class StageDecision:
    """Apply PASS, REWORK, ESCALATE, and STOP. INV-002, POL-001 through POL-004."""

    DEFAULT_REWORK_LIMIT = 2

    def __init__(self, rework_limit: int = DEFAULT_REWORK_LIMIT) -> None:
        self.rework_limit = rework_limit

    def record(self, trigger: str, decision: str, **kwargs) -> dict:
        if not trigger or decision not in DECISIONS:
            raise ValueError("a stage decision requires a trigger and a decision")
        return DecisionRecord(trigger=trigger, decision=decision, **kwargs).as_dict()

    def advance(self, *, stage: str, stages: list[str], evaluator: str | None, checks_passed: bool) -> dict:
        if evaluator != "PASS" or not checks_passed:
            raise ValueError("PASS requires an evaluator PASS and passed checks")
        index = stages.index(stage)
        if index + 1 >= len(stages):
            nxt = stage
        else:
            nxt = stages[index + 1]
        return self.record(
            "evaluator PASS and stage checks passed",
            "PASS",
            detail="advance",
            stage=nxt,
        )

    def rework(self, *, rework_count: int, responsible_agent: str) -> dict:
        if rework_count >= self.rework_limit:
            return self.record(
                "rework limit reached",
                "ESCALATE",
                detail="suspend",
                suspended=True,
            )
        return self.record(
            "correctable validation failure",
            "REWORK",
            detail="return",
            return_to=responsible_agent,
        )

    def contradiction(self) -> dict:
        return self.record(
            "validation results contradict",
            "ESCALATE",
            detail="suspend",
            suspended=True,
        )

    def security_violation(self) -> dict:
        return self.record(
            "security violation",
            "STOP",
            detail="terminate",
            terminated=True,
        )

    def verification_impossible(self) -> dict:
        return self.record(
            "verification impossible",
            "STOP",
            detail="terminate",
            terminated=True,
        )

    def rule_from_partial_support(self) -> dict:
        return self.record(
            "one validation supports and the other does not contradict",
            "PASS",
            detail="rule specification at lower confidence",
            rule_request=True,
            lower_confidence=True,
        )
