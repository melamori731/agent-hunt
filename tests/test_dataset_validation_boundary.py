"""Structural boundary: dataset_validation must not import other component packages."""

from pathlib import Path


def test_dataset_validation_mustNotDependOn_otherComponents():
    """dataset_validation_mustNotDependOn_otherComponents."""
    root = Path(__file__).resolve().parents[1] / "dataset_validation"
    banned = (
        "research_orchestrator",
        "agent_intelligence",
        "dataset_discovery",
        "sandbox_validation",
        "rule_specification",
        "subprocess",
    )
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in text
            assert f"from {name}" not in text
