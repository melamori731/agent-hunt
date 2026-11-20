"""LangGraph node that discovers datasets for stored hypotheses."""

from __future__ import annotations

import json
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from dataset_discovery.hypothesis_reader import HypothesisReader
from dataset_discovery.ranking import rank_passages
from dataset_discovery.registry import DatasetRegistry
from dataset_discovery.schedule import DiscoverySchedule
from dataset_discovery.suitability import SuitabilityJudgement


class HumanInputRejected(Exception):
    """Human text is not an input to dataset discovery."""


class DiscoveryState(TypedDict):
    searched: list[str]


Catalog = Callable[[str], list[dict[str, Any]]]


class DatasetDiscoveryNode:
    """Search a catalog and write datasets.json. Do not start a shopping agent."""

    def __init__(
        self,
        store_dir: Path | str,
        catalog: Catalog,
        *,
        now: Callable[[], datetime] | None = None,
        interval: timedelta | None = None,
    ) -> None:
        self.store_dir = Path(store_dir)
        self.catalog = catalog
        self.now = now or (lambda: datetime.now(UTC))
        self.schedule = DiscoverySchedule(interval)
        self.shopping_agent_started = False
        self.tool = self._build_tool()
        self.graph = self._compile()

    def run(self, *, human_text: str | None = None) -> dict[str, Any]:
        if human_text is not None and str(human_text).strip():
            raise HumanInputRejected(
                "Human input enters only through the research orchestrator"
            )
        self.shopping_agent_started = False
        return self.graph.invoke({"searched": []})

    def _build_tool(self):
        catalog = self.catalog

        @tool
        def search_dataset_catalog(query: str) -> str:
            """Search the dataset catalog and return JSON passages."""
            return json.dumps(catalog(query))

        return search_dataset_catalog

    def _compile(self):
        graph = StateGraph(DiscoveryState)
        graph.add_node("discover", self._discover)
        graph.add_edge(START, "discover")
        graph.add_edge("discover", END)
        return graph.compile()

    def _discover(self, state: DiscoveryState) -> DiscoveryState:
        del state
        moment = _aware(self.now())
        reader = HypothesisReader(self.store_dir)
        registry = DatasetRegistry(self.store_dir)
        last_run_at = _read_last_run(self.store_dir)
        due = self.schedule.is_due(last_run_at, moment)
        searched: list[str] = []
        judgement = SuitabilityJudgement()
        for hypothesis in reader.read():
            if not due and registry.has_suitable(hypothesis["id"]):
                continue
            raw = self.tool.invoke({"query": hypothesis["signal"] or hypothesis["id"]})
            ranked = rank_passages(json.loads(raw), hypothesis["signal"] or hypothesis["id"])
            for passage in ranked:
                registry.upsert(judgement.judge(passage, hypothesis, moment))
            searched.append(hypothesis["id"])
        if due:
            _write_last_run(self.store_dir, moment)
        return {"searched": searched}


def _aware(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def _read_last_run(store_dir: Path) -> datetime | None:
    path = store_dir / "discovery_state.json"
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload.get("lastRunAt") if isinstance(payload, dict) else None
    if not isinstance(raw, str) or not raw.strip():
        return None
    parsed = datetime.fromisoformat(raw.strip())
    return _aware(parsed)


def _write_last_run(store_dir: Path, moment: datetime) -> None:
    store_dir.mkdir(parents=True, exist_ok=True)
    text = _aware(moment).strftime("%Y-%m-%dT%H:%M:%SZ")
    path = store_dir / "discovery_state.json"
    path.write_text(json.dumps({"lastRunAt": text}, indent=2) + "\n", encoding="utf-8")
