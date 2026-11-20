"""Signal evaluation helpers for sandbox scenario reports."""

from __future__ import annotations

import re
from typing import Any


def _dig(data: dict[str, Any], path: str) -> Any:
    cur: Any = data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def match_condition(fingerprint: dict[str, Any], condition: dict[str, Any]) -> bool:
    """Evaluate one condition against a fingerprint dict.

    Supported ops: eq, ne, contains, regex, exists, in, gte, lte.
    """
    field = condition["field"]
    op = condition.get("op", "eq")
    expected = condition.get("value")
    actual = _dig(fingerprint, field)

    if op == "exists":
        return actual is not None
    if op == "eq":
        return actual == expected
    if op == "ne":
        return actual != expected
    if op == "in":
        return actual in (expected or [])
    if op == "contains":
        return isinstance(actual, str) and expected in actual
    if op == "regex":
        return isinstance(actual, str) and re.search(expected, actual) is not None
    if op == "gte":
        return actual is not None and actual >= expected
    if op == "lte":
        return actual is not None and actual <= expected
    raise ValueError(f"Unsupported op: {op}")


def signal_present(fingerprint: dict[str, Any], signal: dict[str, Any]) -> bool:
    mode = signal.get("mode", "all")
    conditions = signal.get("conditions", [])
    if not conditions:
        return False
    results = [match_condition(fingerprint, c) for c in conditions]
    if mode == "any":
        return any(results)
    return all(results)


def summarize_runs(
    runs: list[dict[str, Any]],
    *,
    threshold_positives: int,
    threshold_window: int,
    max_attempts: int,
) -> dict[str, Any]:
    valid = [r for r in runs if r.get("status") == "ok"]
    positives = [r for r in valid if r.get("signal_observed")]
    blocked = [r for r in runs if r.get("status") == "blocked"]
    reproduction_rate = (len(positives) / len(valid)) if valid else 0.0

    # Provisional stopping rule from the design docs: >= threshold_positives
    # positive observations in threshold_window independent runs; <= max_attempts.
    window = valid[:threshold_window]
    window_positives = sum(1 for r in window if r.get("signal_observed"))
    window_complete = len(window) >= threshold_window
    met_threshold = window_complete and window_positives >= threshold_positives
    # A full evaluation window that misses the positive count is enough to reject
    # reproduction. max_attempts mainly covers blocked/invalid retries.
    exhausted = (not met_threshold) and (
        window_complete or len(runs) >= max_attempts
    )

    if blocked and not valid:
        conclusion = "blocked"
    elif met_threshold:
        conclusion = "reproduced"
    elif exhausted:
        conclusion = "not_reproduced"
    else:
        conclusion = "inconclusive"

    return {
        "attempts": len(runs),
        "valid_runs": len(valid),
        "positive_runs": len(positives),
        "blocked_runs": len(blocked),
        "reproduction_rate": round(reproduction_rate, 4),
        "threshold": {
            "positives": threshold_positives,
            "window": threshold_window,
            "max_attempts": max_attempts,
        },
        "window_positives": window_positives,
        "met_threshold": met_threshold,
        "conclusion": conclusion,
    }
