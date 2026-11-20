"""LangGraph node that writes sandbox_results.json from saved evidence."""

from __future__ import annotations

import json
from pathlib import Path

from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, START, StateGraph

from sandbox_validation.reproducibility import SignalReproducibility


class SandboxValidation:
    """Load a hypothesis and saved evidence, then write the result file. INV-001 and INV-002."""

    def __init__(self) -> None:
        self._judge = SignalReproducibility()
        self._loader = RunnableLambda(self._read_json)
        self._graph = self._compile()

    def run(self, hypothesis_path: str, evidence_path: str, output_dir: str) -> dict:
        state = self._graph.invoke(
            {
                "hypothesis_path": hypothesis_path,
                "evidence_path": evidence_path,
                "output_dir": output_dir,
            }
        )
        return state["record"]

    def _compile(self):
        graph = StateGraph(dict)
        graph.add_node("validate", self._node)
        graph.add_edge(START, "validate")
        graph.add_edge("validate", END)
        return graph.compile()

    def _node(self, state: dict) -> dict:
        hypothesis_id = self._hypothesis_id(state["hypothesis_path"])
        evidence_path = state["evidence_path"]
        found, payload = self._load_evidence(evidence_path)
        result = self._judge.judge(
            evidence_found=found,
            evidence=payload,
            hypothesis_id=hypothesis_id,
        )
        record = {
            "hypothesis_id": hypothesis_id,
            "result": result,
            "evidence_path": evidence_path,
        }
        destination = Path(state["output_dir"])
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "sandbox_results.json").write_text(
            json.dumps(record, indent=2) + "\n",
            encoding="utf-8",
        )
        return {"record": record}

    def _hypothesis_id(self, path: str) -> str:
        data = self._loader.invoke(path)
        if not isinstance(data, dict):
            raise TypeError("hypothesis file must be a JSON object")
        hypothesis_id = data.get("hypothesis_id", data.get("id"))
        if not isinstance(hypothesis_id, str) or not hypothesis_id:
            raise ValueError("hypothesis_id is required")
        return hypothesis_id

    def _load_evidence(self, path: str) -> tuple[bool, object]:
        evidence = Path(path)
        if not evidence.is_file():
            return False, None
        try:
            payload = self._loader.invoke(path)
        except (OSError, json.JSONDecodeError, ValueError):
            return False, None
        return True, payload

    @staticmethod
    def _read_json(path: str) -> object:
        return json.loads(Path(path).read_text(encoding="utf-8"))
