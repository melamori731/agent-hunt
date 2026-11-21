"""System path from an orchestrator assignment to a submitted rule specification."""

from __future__ import annotations

import json
from pathlib import Path

from agent_intelligence.store import JsonResearchStore


class SystemEndToEndTest:
    """Load saved records and check a submitted specification.

    Encapsulates POL-004. Virtual-machine evidence is read from a file. This
    test does not start a shopping agent and does not deploy a rule.
    """

    def run(self, directory: str | Path) -> dict:
        directory = Path(directory)
        result = {"passed": False, "shoppingAgentStarted": False}
        required = [
            "orchestrator_assignment.json",
            "vm_evidence.json",
            "dataset_validation_results.json",
            "evaluator_results.json",
            "submitted_rule_specification.json",
            JsonResearchStore.REGISTRY_ENTRIES,
            JsonResearchStore.REGISTRY_REPORTS,
            JsonResearchStore.HYPOTHESES,
        ]
        loaded = {}
        for name in required:
            path = directory / name
            if not path.is_file():
                result["missing"] = name
                return result
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))
        unresolved_path = directory / JsonResearchStore.UNRESOLVED
        if unresolved_path.is_file():
            json.loads(unresolved_path.read_text(encoding="utf-8"))
        if not isinstance(loaded["vm_evidence.json"], dict):
            return result
        specification = loaded["submitted_rule_specification.json"]
        result["specification"] = specification
        sources = _research_sources(loaded)
        if isinstance(specification, dict):
            validation = specification.get("validationResults")
        else:
            validation = None
        result["passed"] = _covers_sources(specification, sources) and _has_validation(validation)
        return result


def _research_sources(loaded: dict) -> list[dict]:
    sources = []
    for item in loaded[JsonResearchStore.HYPOTHESES]:
        sources.extend(item.get("sources", []))
    if sources:
        return sources
    for item in loaded[JsonResearchStore.REGISTRY_REPORTS]:
        sources.extend(item.get("sources", []))
    return sources


def _covers_sources(specification: dict, sources: list[dict]) -> bool:
    if not isinstance(specification, dict) or not sources:
        return False
    cited = specification.get("researchSources")
    if not isinstance(cited, list) or not cited:
        return False
    for source in sources:
        if not any(
            item.get("url") == source.get("url") and item.get("title") == source.get("title")
            for item in cited
        ):
            return False
    return True


def _has_validation(validation) -> bool:
    return isinstance(validation, dict) and len(validation) > 0
