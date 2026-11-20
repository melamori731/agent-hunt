"""Structural boundary for dataset_discovery. CON-002."""

from __future__ import annotations

import ast
from pathlib import Path

import dataset_discovery

FORBIDDEN = {
    "research_orchestrator",
    "agent_intelligence",
    "dataset_validation",
    "sandbox_validation",
    "detection_rule_specification",
    "independent_evaluator",
}


def test_dataset_discovery_mustNotDependOn_otherAgents() -> None:
    root = Path(dataset_discovery.__file__).resolve().parent
    found: list[str] = []
    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found.extend(
                    alias.name
                    for alias in node.names
                    if alias.name.split(".")[0] in FORBIDDEN
                )
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.split(".")[0] in FORBIDDEN
            ):
                found.append(node.module)
    assert found == []
