"""One LangGraph node whose research loop is LangChain ReAct."""

from __future__ import annotations

import json
from datetime import timedelta
from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph

from agent_intelligence.hypothesis import HypothesisRecord, HypothesisRejection
from agent_intelligence.registry import DISCOVERY_ORIGIN, ORCHESTRATOR_ORIGIN, AgentRegistry
from agent_intelligence.schedule import DiscoverySchedule
from agent_intelligence.store import JsonResearchStore


class DirectHumanInputRejected(ValueError):
    """Human text is accepted only as an orchestrator assignment."""


class DeployedRuleRejected(ValueError):
    """This node does not write a deployed detection rule."""


class ResearchState(TypedDict, total=False):
    mode: str
    assignment: dict
    started: bool
    reactTrace: str


class AgentIntelligenceNode:
    """Run one orchestrator assignment or one scheduled discovery pass.

    Encapsulates INV-004. The node writes registry entries, reports, hypotheses,
    and unresolved investigations. It does not accept a direct human call and it
    does not write a deployed rule.
    """

    def __init__(
        self,
        store: JsonResearchStore,
        source_catalog: list[dict] | None = None,
        interval: timedelta | None = None,
    ):
        self.store = store
        self.registry = AgentRegistry(store)
        self.hypotheses = HypothesisRecord(store)
        self.schedule = DiscoverySchedule(interval)
        self.source_catalog = list(source_catalog or [])
        self._graph = self._compile_graph()

    def run_assignment(self, assignment) -> dict:
        if not isinstance(assignment, dict) or assignment.get("kind") != "orchestrator_assignment":
            raise DirectHumanInputRejected(
                "Human input reaches this agent only as an orchestrator assignment."
            )
        if not assignment.get("assistantName"):
            raise DirectHumanInputRejected(
                "An orchestrator assignment must name an assistant."
            )
        return self._graph.invoke(
            {
                "mode": "assignment",
                "assignment": assignment,
                "started": True,
            }
        )

    def run_discovery(self, *, previous_run, now) -> dict:
        if not self.schedule.is_due(previous_run, now):
            return {"started": False, "reactTrace": ""}
        state = self._graph.invoke(
            {
                "mode": "discovery",
                "assignment": {},
                "started": True,
            }
        )
        state["started"] = True
        return state

    def write_deployed_rule(self, rule: dict) -> None:
        raise DeployedRuleRejected(
            "This agent does not write a deployed detection rule."
        )

    def _compile_graph(self):
        builder = StateGraph(ResearchState)
        builder.add_node("agent_intelligence", self._research)
        builder.add_edge(START, "agent_intelligence")
        builder.add_edge("agent_intelligence", END)
        return builder.compile()

    def _research(self, state: ResearchState) -> ResearchState:
        trace = self._react(state)
        return {
            "mode": state.get("mode", ""),
            "assignment": state.get("assignment") or {},
            "started": True,
            "reactTrace": trace,
        }

    def _react(self, state: ResearchState) -> str:
        tools = self._build_tools(state)
        scratchpad = ""
        for _ in range(4):
            message = self._next_message(scratchpad, state)
            scratchpad += message
            if "Final Answer:" in message:
                return scratchpad
            action_name = _action_name(message)
            observation = tools[action_name].invoke(_action_input(message))
            if not isinstance(observation, str):
                observation = json.dumps(observation)
            scratchpad += f"Observation: {observation}\n"
        raise RuntimeError("The ReAct loop did not finish.")

    def _next_message(self, scratchpad: str, state: ResearchState) -> str:
        if "Action: search_public_sources" not in scratchpad:
            if state.get("mode") == "assignment":
                assistant_name = state["assignment"]["assistantName"]
            else:
                assistant_name = "*"
            payload = json.dumps({"assistant_name": assistant_name})
            return (
                "Thought: I need public sources before storing a registry entry or hypothesis.\n"
                "Action: search_public_sources\n"
                f"Action Input: {payload}\n"
            )
        if "Action: store_research_records" not in scratchpad:
            observation = scratchpad.rsplit("Observation: ", 1)[1].strip()
            payload = json.dumps({"observation_json": observation})
            return (
                "Thought: I will store the registry report and apply the hypothesis gate.\n"
                "Action: store_research_records\n"
                f"Action Input: {payload}\n"
            )
        return "Thought: The research records are stored.\nFinal Answer: records stored\n"

    def _build_tools(self, state: ResearchState):
        catalog = self.source_catalog
        node = self

        @tool
        def search_public_sources(assistant_name: str) -> str:
            """Retrieve public documents for one assistant, or * for the whole catalog."""
            if assistant_name == "*":
                matches = catalog
            else:
                matches = [
                    page for page in catalog if page.get("assistantName") == assistant_name
                ]
            return json.dumps(matches)

        @tool
        def store_research_records(observation_json: str) -> str:
            """Store registry and hypothesis records from a search observation."""
            pages = json.loads(observation_json)
            origin = (
                ORCHESTRATOR_ORIGIN
                if state.get("mode") == "assignment"
                else DISCOVERY_ORIGIN
            )
            raise_on_duplicate = state.get("mode") == "assignment"
            node._store_pages(pages, origin, state.get("assignment") or {}, raise_on_duplicate)
            return json.dumps({"stored": True, "pages": len(pages)})

        return {
            "search_public_sources": search_public_sources,
            "store_research_records": store_research_records,
        }

    def _store_pages(self, pages, origin: str, assignment: dict, raise_on_duplicate: bool) -> None:
        if not pages and assignment:
            raise LookupError(
                f"No public sources were retrieved for {assignment.get('assistantName')}."
            )
        for page in pages:
            draft = _draft_from_page(page, assignment)
            if _is_abuse(draft):
                self.hypotheses.submit(draft)
            assistant_name = page["assistantName"]
            if not any(entry["assistantName"] == assistant_name for entry in self.registry.entries):
                self.registry.add(assistant_name, _registry_sources(page), origin)
            try:
                self.hypotheses.submit(draft)
            except HypothesisRejection as error:
                if error.duplicate and not raise_on_duplicate:
                    continue
                raise


def _is_abuse(draft: dict) -> bool:
    classification = str(draft.get("classification") or "").strip().lower()
    purpose = str(draft.get("purpose") or "").strip().lower()
    return classification in {"abusive", "malicious", "legitimate"} or purpose in {
        "abuse_classification",
        "abusive_versus_legitimate",
    }


def _registry_sources(page: dict) -> list[dict]:
    return [{"url": page["url"], "title": page["title"]}]


def _draft_from_page(page: dict, assignment: dict) -> dict:
    draft = {
        "assistantName": page["assistantName"],
        "sources": [
            {
                "url": page["url"],
                "title": page["title"],
                "supportsTestableSignal": page.get("supportsTestableSignal") is True,
            }
        ],
    }
    if page.get("signal"):
        draft["signal"] = page["signal"]
    if page.get("observation"):
        draft["observation"] = page["observation"]
    if page.get("measurements") is not None:
        draft["measurements"] = page["measurements"]
    if assignment.get("purpose"):
        draft["purpose"] = assignment["purpose"]
    if assignment.get("classification"):
        draft["classification"] = assignment["classification"]
    return draft


def _action_name(message: str) -> str:
    for line in message.splitlines():
        if line.startswith("Action: "):
            return line.removeprefix("Action: ").strip()
    raise RuntimeError("ReAct message has no action.")


def _action_input(message: str) -> dict:
    for line in message.splitlines():
        if line.startswith("Action Input: "):
            return json.loads(line.removeprefix("Action Input: "))
    return {}
