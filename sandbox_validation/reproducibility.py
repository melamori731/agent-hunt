"""Judge whether a saved sandbox signal is reproducible."""

from __future__ import annotations

SUPPORT = "support"
CONTRADICT = "contradict"
INCONCLUSIVE = "inconclusive"
BLOCKED = "blocked"


class SignalReproducibility:
    """Apply the saved-run reproducibility rule. POL-001 and POL-002."""

    def judge(self, *, evidence_found: bool, evidence: object, hypothesis_id: str) -> str:
        if not evidence_found or not isinstance(evidence, dict):
            return BLOCKED
        recorded = evidence.get("hypothesis_id", evidence.get("id"))
        if recorded is not None and recorded != hypothesis_id:
            return BLOCKED
        runs = evidence.get("runs")
        if not isinstance(runs, list) or not runs:
            return BLOCKED
        observed: list[bool] = []
        for run in runs[:10]:
            if not isinstance(run, dict) or run.get("telemetry_present") is not True:
                return BLOCKED
            observed.append(run.get("signal_observed") is True)
        if len(observed) >= 5:
            for start in range(len(observed) - 4):
                if sum(observed[start : start + 5]) >= 4:
                    return SUPPORT
            if not any(observed):
                return CONTRADICT
        return INCONCLUSIVE
