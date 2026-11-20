"""Structural boundary for independent_evaluator."""

from pathlib import Path


def test_independent_evaluator_mustNotDependOn_otherComponents():
    root = Path(__file__).resolve().parents[1] / "independent_evaluator"
    banned = (
        "research_orchestrator",
        "agent_intelligence",
        "dataset_validation",
        "sandbox_validation",
        "rule_specification",
        "subprocess",
    )
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in text
            assert f"from {name}" not in text
