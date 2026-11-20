"""Structural boundary: research_orchestrator must not import downstream research or validators."""

from pathlib import Path


def test_research_orchestrator_mustNotDependOn_researchOrValidators():
    root = Path(__file__).resolve().parents[1] / "research_orchestrator"
    banned = ("agent_intelligence", "dataset_validation", "sandbox", "rule_specification", "subprocess")
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in banned:
            assert f"import {name}" not in text
            assert f"from {name}" not in text
