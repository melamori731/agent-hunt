"""Structural boundary for sandbox_validation."""

from pathlib import Path


def test_sandbox_validation_mustNotDependOn_otherComponents():
    root = Path(__file__).resolve().parents[1] / "sandbox_validation"
    banned = (
        "research_orchestrator",
        "agent_intelligence",
        "dataset_validation",
        "rule_specification",
        "subprocess",
    )
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in text
            assert f"from {name}" not in text
