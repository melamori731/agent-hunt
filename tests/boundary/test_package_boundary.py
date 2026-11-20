"""Structural boundary for the agent_intelligence package."""

import ast
from pathlib import Path

FORBIDDEN_MODULES = {
    "dataset_validation",
    "sandbox_execution",
    "independent_evaluation",
    "independent_evaluator",
    "rule_submission",
    "rule_specification",
}


def agent_intelligence_mustNotDependOn_downstreamStages():
    """agent_intelligence must not import downstream stage packages."""
    root = Path(__file__).resolve().parents[2] / "agent_intelligence"
    offenders = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            for module in modules:
                top = module.split(".")[0]
                if top in FORBIDDEN_MODULES or module in FORBIDDEN_MODULES:
                    offenders.append(f"{path.name}: {module}")
    assert offenders == []
