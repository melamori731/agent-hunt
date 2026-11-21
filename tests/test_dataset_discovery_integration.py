"""Integration scenarios for dataset discovery."""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

import pytest

from dataset_discovery.node import DatasetDiscoveryNode, HumanInputRejected
from dataset_discovery.registry import DatasetRegistry
from dataset_discovery.suitability import SuitabilityJudgement
from tests.helpers import NOW, complete_candidate, hypothesis, write_hypothesis


def _write_state(store: Path, last_run) -> None:
    text = last_run.strftime("%Y-%m-%dT%H:%M:%SZ")
    (store / "discovery_state.json").write_text(
        json.dumps({"lastRunAt": text}),
        encoding="utf-8",
    )


def test_suitableDataset_writesEntryForHypothesis(tmp_path: Path) -> None:
    # REQ-001: suitable entry stores name, source URL, title, suitability, and hypothesis id.
    write_hypothesis(tmp_path)
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    node.run()
    records = DatasetRegistry(tmp_path).read()
    assert len(records) == 1
    entry = records[0]
    assert entry["datasetName"] == "muse-human-sessions"
    assert entry["sourceUrl"] == "https://example.edu/datasets/muse-human"
    assert entry["title"] == "Labelled Muse and human shopping sessions"
    assert entry["suitability"] == "suitable"
    assert entry["hypothesisId"] == "H1"
    assert entry["hasHumanLabel"] is True
    assert entry["hasAgentLabel"] is True
    assert entry["license"] == "CC-BY-4.0"


def test_queryOnlyDataset_writesUnsuitable(tmp_path: Path) -> None:
    # REQ-002: a query-only candidate is stored as unsuitable.
    write_hypothesis(tmp_path)
    candidate = complete_candidate(queryMatchOnly=True)
    node = DatasetDiscoveryNode(tmp_path, lambda query: [candidate], now=lambda: NOW)
    node.run()
    records = DatasetRegistry(tmp_path).read()
    assert len(records) == 1
    assert records[0]["suitability"] == "unsuitable"
    assert records[0]["hypothesisId"] == "H1"


def test_repeatDiscovery_keepsOneEntry(tmp_path: Path) -> None:
    # REQ-003: repeating discovery leaves one entry for the pair.
    write_hypothesis(tmp_path)
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    node.run()
    node.run()
    records = DatasetRegistry(tmp_path).read()
    assert len(records) == 1
    assert records[0]["datasetName"] == "muse-human-sessions"
    assert records[0]["hypothesisId"] == "H1"


def test_noSuitableCandidate_writesNoSuitableEntry(tmp_path: Path) -> None:
    # REQ-004: failing candidates do not become suitable support.
    write_hypothesis(tmp_path)
    candidates = [
        complete_candidate(datasetName="query-only", queryMatchOnly=True),
        complete_candidate(datasetName="unlabelled", hasHumanLabel=False),
    ]
    node = DatasetDiscoveryNode(tmp_path, lambda query: candidates, now=lambda: NOW)
    node.run()
    records = DatasetRegistry(tmp_path).read()
    assert records
    assert all(item["suitability"] != "suitable" for item in records)
    assert all(item["hypothesisId"] == "H1" for item in records)


def test_scheduleDue_searchesAgain(tmp_path: Path) -> None:
    # REQ-005: the default interval searches again at 24 hours.
    write_hypothesis(tmp_path)
    DatasetRegistry(tmp_path).upsert(
        {
            "datasetName": "muse-human-sessions",
            "sourceUrl": "https://example.edu/datasets/muse-human",
            "title": "Labelled Muse and human shopping sessions",
            "suitability": "suitable",
            "hypothesisId": "H1",
        }
    )
    _write_state(tmp_path, NOW - timedelta(hours=24))
    calls: list[str] = []

    def catalog(query: str) -> list[dict]:
        calls.append(query)
        return [complete_candidate()]

    DatasetDiscoveryNode(tmp_path, catalog, now=lambda: NOW).run()
    assert calls


def test_scheduleNotDue_skipsSearchWhenSuitableExists(tmp_path: Path) -> None:
    # REQ-005: a suitable entry is not searched again at 23 hours.
    write_hypothesis(tmp_path)
    DatasetRegistry(tmp_path).upsert(
        {
            "datasetName": "muse-human-sessions",
            "sourceUrl": "https://example.edu/datasets/muse-human",
            "title": "Labelled Muse and human shopping sessions",
            "suitability": "suitable",
            "hypothesisId": "H1",
        }
    )
    _write_state(tmp_path, NOW - timedelta(hours=23))
    calls: list[str] = []
    DatasetDiscoveryNode(tmp_path, lambda query: calls.append(query) or [], now=lambda: NOW).run()
    assert calls == []


def test_missingSuitable_searchesBeforeInterval(tmp_path: Path) -> None:
    # REQ-005: a hypothesis with no suitable entry is searched before the interval elapses.
    write_hypothesis(tmp_path)
    previous = NOW - timedelta(minutes=1)
    _write_state(tmp_path, previous)
    calls: list[str] = []

    def catalog(query: str) -> list[dict]:
        calls.append(query)
        return [complete_candidate(hasHumanLabel=False)]

    DatasetDiscoveryNode(tmp_path, catalog, now=lambda: NOW).run()
    assert calls
    stored = json.loads((tmp_path / "discovery_state.json").read_text(encoding="utf-8"))
    assert stored["lastRunAt"] == previous.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_humanText_writesNothing(tmp_path: Path) -> None:
    # REQ-006: human text does not read as a research prompt.
    write_hypothesis(tmp_path)
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    with pytest.raises(HumanInputRejected):
        node.run(human_text="Please discover datasets")
    assert not (tmp_path / "datasets.json").exists()
    assert (tmp_path / "hypotheses.json").is_file()


def test_discoveryRun_startsNoShoppingAgentAndWritesNoRule(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # REQ-007: no shopping agent, hypothesis write, validation metric, or deployed rule.
    calls: list[str] = []

    def refuse(*_args: object, **_kwargs: object) -> None:
        calls.append("called")
        raise AssertionError("shopping agent start")

    monkeypatch.setattr("subprocess.Popen", refuse)
    monkeypatch.setattr("subprocess.run", refuse)
    monkeypatch.setattr("os.system", refuse)
    write_hypothesis(tmp_path)
    before = (tmp_path / "hypotheses.json").read_text(encoding="utf-8")
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    node.run()
    assert calls == []
    assert node.shopping_agent_started is False
    assert (tmp_path / "hypotheses.json").read_text(encoding="utf-8") == before
    names = {path.name for path in tmp_path.iterdir()}
    assert all("validation" not in name and "rule" not in name for name in names)


def test_reopenRegistry_returnsSameEntry(tmp_path: Path) -> None:
    # QR-001: a later process reads the written entry.
    registry = DatasetRegistry(tmp_path)
    registry.upsert(
        {
            "datasetName": "muse-human-sessions",
            "sourceUrl": "https://example.edu/datasets/muse-human",
            "title": "Labelled Muse and human shopping sessions",
            "suitability": "suitable",
            "hypothesisId": "H1",
        }
    )
    reopened = DatasetRegistry(tmp_path).read()
    assert reopened[0]["datasetName"] == "muse-human-sessions"
    assert reopened[0]["hypothesisId"] == "H1"


def test_sameCandidate_sameSuitability() -> None:
    # QR-002: the same inputs return the same suitability.
    judgement = SuitabilityJudgement()
    first = judgement.judge(complete_candidate(), hypothesis(), NOW)
    second = judgement.judge(complete_candidate(), hypothesis(), NOW)
    assert first["suitability"] == second["suitability"] == "suitable"
