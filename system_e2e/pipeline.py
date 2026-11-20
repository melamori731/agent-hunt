"""Run each stored-record agent once, from a human name to a submitted specification."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from agent_intelligence.node import AgentIntelligenceNode
from agent_intelligence.store import JsonResearchStore
from dataset_discovery.node import DatasetDiscoveryNode
from dataset_validation.graph import DatasetValidationGraph
from detection_rule_specification.specification import DetectionRuleSpecification
from detection_rule_specification.store import RuleSpecificationStore
from independent_evaluator.evaluator import IndependentEvaluator
from research_orchestrator.orchestrator import ResearchOrchestrator
from research_orchestrator.store import OrchestratorStore
from sandbox_validation.validation import SandboxValidation


def run(
    root: Path,
    *,
    assistant_name: str = "Muse",
    purpose: str | None = None,
    sandbox_signal_observed: bool = True,
) -> dict:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    orchestrator = ResearchOrchestrator(OrchestratorStore(root), interval=timedelta(hours=1))
    request = {"assistant_name": assistant_name}
    if purpose == "abuse_classification":
        request = {"purpose": purpose}
    assignment = orchestrator.accept_human(request)
    if assignment is None:
        return {
            "assignment": None,
            "hypotheses": [],
            "specification": None,
            "orchestrator_specifications": orchestrator.store.all("specifications"),
            "shopping_agent_started": False,
        }
    research = AgentIntelligenceNode(
        JsonResearchStore(root),
        source_catalog=[_source_page(assistant_name)],
    )
    research.run_assignment(
        {
            "kind": "orchestrator_assignment",
            "assistantName": assignment["assistant_name"],
        }
    )
    hypothesis = _stamp_hypothesis_id(root)
    hypothesis_id = hypothesis["hypothesis_id"]
    discovery = DatasetDiscoveryNode(
        root,
        lambda _query: [_dataset_passage(hypothesis["signal"])],
        now=lambda: datetime(2026, 11, 20, tzinfo=UTC),
    )
    discovery.run()
    dataset = DatasetValidationGraph().run(
        {
            "source": "orchestrator",
            "hypothesis_id": hypothesis_id,
            "signal": hypothesis["signal"],
            "dataset_path": str(_write_labelled_rows(root, hypothesis["signal"])),
            "dataset_name": "session-hints",
            "results_path": str(root / "dataset_results.json"),
        }
    )
    evidence_path = _write_saved_evidence(root, hypothesis_id, sandbox_signal_observed)
    hypothesis_path = _write_hypothesis_file(root, hypothesis)
    sandbox = SandboxValidation().run(str(hypothesis_path), str(evidence_path), str(root))
    _write_validation_results(root, hypothesis_id, dataset["result"], sandbox["result"])
    specification = DetectionRuleSpecification(RuleSpecificationStore(root)).run(hypothesis_id)
    _write_evaluator_validations(root, hypothesis_id, dataset["result"], sandbox["result"])
    evaluation = IndependentEvaluator(root).evaluate(hypothesis_id, "rule_specification")
    orchestrator.review_validation(
        {"id": hypothesis_id},
        dataset["result"],
        sandbox["result"],
        evaluation["result"],
        "validation",
    )
    return {
        "assignment": assignment,
        "hypothesis": hypothesis,
        "datasets": json.loads((root / "datasets.json").read_text(encoding="utf-8"))["datasets"],
        "dataset_result": dataset,
        "sandbox_result": sandbox,
        "specification": specification["record"],
        "evaluation": evaluation,
        "orchestrator_specifications": orchestrator.store.all("specifications"),
        "shopping_agent_started": discovery.shopping_agent_started,
    }


def _source_page(assistant_name: str) -> dict:
    return {
        "assistantName": assistant_name,
        "url": "https://example.edu/muse-shopping-session",
        "title": "Muse shopping session notes",
        "supportsTestableSignal": True,
        "signal": "client_hint",
        "observation": "The shopping session sends a client hint header.",
        "measurements": ["client_hint"],
    }


def _stamp_hypothesis_id(root: Path) -> dict:
    path = root / "hypotheses.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    hypothesis = rows[-1]
    hypothesis_id = f"{hypothesis['assistantName']}-{hypothesis['signal']}"
    hypothesis["id"] = hypothesis_id
    hypothesis["hypothesis_id"] = hypothesis_id
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return hypothesis


def _dataset_passage(signal: str) -> dict:
    return {
        "datasetName": "session-hints",
        "sourceUrl": "https://example.edu/datasets/session-hints",
        "title": f"{signal} labelled sessions",
        "text": f"{signal} shopping sessions with human and agent labels",
        "collectionMethod": "manual-vm",
        "hasSessionIdentifier": True,
        "hasHumanLabel": True,
        "hasAgentLabel": True,
        "license": "CC-BY-4.0",
        "verifiedAt": "2026-11-01T00:00:00+00:00",
        "fields": [signal],
    }


def _write_labelled_rows(root: Path, signal: str) -> Path:
    path = root / "labelled.json"
    rows = [
        {"label": "ai", signal: True},
        {"label": "ai", signal: True},
        {"label": "human", signal: False},
        {"label": "human", signal: False},
    ]
    path.write_text(json.dumps({"dataset_name": "session-hints", "rows": rows}), encoding="utf-8")
    return path


def _write_saved_evidence(root: Path, hypothesis_id: str, signal_observed: bool) -> Path:
    path = root / "vm_evidence.json"
    runs = [{"telemetry_present": True, "signal_observed": signal_observed} for _ in range(5)]
    path.write_text(
        json.dumps({"hypothesis_id": hypothesis_id, "runs": runs}),
        encoding="utf-8",
    )
    return path


def _write_hypothesis_file(root: Path, hypothesis: dict) -> Path:
    path = root / "hypothesis.json"
    path.write_text(json.dumps(hypothesis), encoding="utf-8")
    return path


def _write_validation_results(root: Path, hypothesis_id: str, dataset_result: str, sandbox_result: str) -> None:
    row = {
        "hypothesis_id": hypothesis_id,
        "dataset_result": dataset_result,
        "sandbox_result": sandbox_result,
    }
    (root / "validation_results.json").write_text(json.dumps([row], indent=2) + "\n", encoding="utf-8")


def _write_evaluator_validations(root: Path, hypothesis_id: str, dataset_result: str, sandbox_result: str) -> None:
    rows = [
        {"hypothesis_id": hypothesis_id, "kind": "dataset", "outcome": dataset_result},
        {"hypothesis_id": hypothesis_id, "kind": "sandbox", "outcome": sandbox_result},
    ]
    (root / "validations.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
