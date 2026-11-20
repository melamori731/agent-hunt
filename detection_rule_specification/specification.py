"""LangGraph node that writes a submitted detection rule specification."""

from __future__ import annotations

import json
from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import END, StateGraph

from detection_rule_specification.confidence import EvidenceConfidence
from detection_rule_specification.store import RuleSpecificationStore
from detection_rule_specification.template import SpecificationTemplate


class SpecState(TypedDict, total=False):
    hypothesis_id: str
    written: bool
    record: dict | None


class DetectionRuleSpecification:
    """POL-001. The run writes a specification or nothing and sends no agent message."""

    def __init__(self, store: RuleSpecificationStore) -> None:
        self.store = store
        self.confidence = EvidenceConfidence()
        self.template = SpecificationTemplate()
        self.tool = self._assemble_tool()
        self.graph = self._compile()

    def _assemble_tool(self):
        confidence = self.confidence
        template = self.template

        @tool
        def assemble_rule_specification(
            hypothesis_id: str,
            dataset_result: str,
            sandbox_result: str,
            research_sources_json: str,
        ) -> str:
            """Assemble a submitted rule specification from stored evidence."""
            sources = json.loads(research_sources_json)
            level = confidence.level(dataset_result, sandbox_result, sources)
            if level is None:
                return json.dumps({"record": None})
            record = template.build(
                hypothesis_id=hypothesis_id,
                confidence=level,
                research_sources=sources,
                dataset_result=dataset_result,
                sandbox_result=sandbox_result,
            )
            return json.dumps({"record": record})

        return assemble_rule_specification

    def _compile(self):
        graph = StateGraph(SpecState)
        graph.add_node("specify", self._specify)
        graph.set_entry_point("specify")
        graph.add_edge("specify", END)
        return graph.compile()

    def _specify(self, state: SpecState) -> dict:
        hypothesis_id = state["hypothesis_id"]
        hypothesis = self.store.find("hypotheses", hypothesis_id)
        validation = self.store.find("validation_results", hypothesis_id)
        sources = self.store.research_sources(hypothesis) if hypothesis else []
        if validation is None:
            dataset_result, sandbox_result = "", ""
        else:
            dataset_result, sandbox_result = self.store.validation_pair(validation)
        raw = self.tool.invoke(
            {
                "hypothesis_id": hypothesis_id,
                "dataset_result": dataset_result,
                "sandbox_result": sandbox_result,
                "research_sources_json": json.dumps(sources),
            }
        )
        body = json.loads(raw)
        record = body["record"]
        if record is None:
            return {"written": False, "record": None}
        saved = self.store.save_specification(record)
        return {"written": True, "record": saved}

    def run(self, hypothesis_id: str) -> dict:
        self.graph.invoke({"hypothesis_id": hypothesis_id})
        saved = self.store.find("rule_specifications", hypothesis_id)
        return {"hypothesis_id": hypothesis_id, "written": saved is not None, "record": saved}
