"""Structural boundary for detection_rule_specification. DD-003."""

from pathlib import Path


def test_detection_rule_specification_mustNotDependOn_otherComponents():
    root = Path(__file__).resolve().parents[1] / "detection_rule_specification"
    banned = (
        "research_orchestrator",
        "agent_intelligence",
        "dataset_validation",
        "dataset_discovery",
        "sandbox_validation",
        "sandbox",
        "shopping",
        "subprocess",
    )
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in text
            assert f"from {name}" not in text
