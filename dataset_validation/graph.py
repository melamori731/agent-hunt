"""LangGraph node that tests one hypothesis against one labelled fixture."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph

from dataset_validation.counting import count_labelled_signal
from dataset_validation.record import DatasetResultRecord
from dataset_validation.store import DatasetResultStore


class ValidationState(TypedDict, total=False):
    assignment: dict
    record: dict | None


class DatasetValidationGraph:
    """POL-003 and POL-004. One node stores a result or nothing."""

    def __init__(self) -> None:
        graph = StateGraph(ValidationState)
        graph.add_node("dataset_validation", self._node)
        graph.set_entry_point("dataset_validation")
        graph.add_edge("dataset_validation", END)
        self._compiled = graph.compile()

    def run(self, assignment: dict) -> dict | None:
        outcome = self._compiled.invoke({"assignment": assignment})
        return outcome.get("record")

    def _node(self, state: ValidationState) -> dict:
        return {"record": self._measure(state["assignment"])}

    def _measure(self, assignment: dict) -> dict | None:
        if not isinstance(assignment, dict):
            return None
        if assignment.get("purpose") == "abuse_classification":
            return None
        forbidden = (
            assignment.get("discover_dataset")
            or assignment.get("launch_shopping_agent")
            or assignment.get("write_rule")
        )
        if forbidden:
            return None
        if assignment.get("source") != "orchestrator":
            return None
        hypothesis_id = assignment.get("hypothesis_id")
        signal = assignment.get("signal")
        dataset_path = assignment.get("dataset_path")
        if not hypothesis_id or not signal or not dataset_path:
            return None
        path = Path(dataset_path)
        dataset_name = assignment.get("dataset_name") or path.stem
        if not path.is_file():
            record = DatasetResultRecord.missing(str(hypothesis_id), str(dataset_name))
        else:
            record = self._from_file(path, str(hypothesis_id), str(signal), str(dataset_name))
        results_path = assignment.get("results_path") or str(path.with_name("dataset_results.json"))
        stored = record.to_dict()
        DatasetResultStore(Path(results_path)).append(stored)
        return stored

    def _from_file(self, path: Path, hypothesis_id: str, signal: str, dataset_name: str) -> DatasetResultRecord:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return DatasetResultRecord.from_rates(hypothesis_id, dataset_name, None, None)
        if isinstance(payload, dict) and payload.get("dataset_name"):
            dataset_name = str(payload["dataset_name"])
        rows = payload.get("rows", []) if isinstance(payload, dict) else []
        counted = json.loads(
            count_labelled_signal.invoke({"rows_json": json.dumps(rows), "signal": signal})
        )
        prevalence, false_positive_rate = _rates(counted)
        return DatasetResultRecord.from_rates(
            hypothesis_id, dataset_name, prevalence, false_positive_rate
        )


def _rates(counted: dict) -> tuple[float | None, float | None]:
    if counted["ai_total"] == 0 or counted["human_total"] == 0:
        return None, None
    prevalence = counted["ai_present"] / counted["ai_total"]
    false_positive_rate = counted["human_present"] / counted["human_total"]
    return prevalence, false_positive_rate
