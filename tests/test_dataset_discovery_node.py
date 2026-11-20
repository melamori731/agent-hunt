"""Unit tests for DatasetDiscoveryNode. INV-003 POL-003 POL-004."""

from __future__ import annotations

from pathlib import Path

import pytest

from dataset_discovery.node import DatasetDiscoveryNode, HumanInputRejected
from dataset_discovery.registry import DatasetRegistry
from tests.helpers import NOW, complete_candidate, write_hypothesis


def test_datasetDiscoveryNode_humanText_writesNothing(tmp_path: Path) -> None:
    # POL-003 REQ-006: human text writes no registry entry.
    write_hypothesis(tmp_path)
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    with pytest.raises(HumanInputRejected):
        node.run(human_text="Find a dataset for Muse")
    assert not (tmp_path / "datasets.json").exists()
    assert node.shopping_agent_started is False


def test_datasetDiscoveryNode_run_startsNoShoppingAgent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # INV-003: DatasetDiscoveryNode does not start a shopping agent.
    calls: list[str] = []

    def refuse(*_args: object, **_kwargs: object) -> None:
        calls.append("called")
        raise AssertionError("shopping agent start")

    monkeypatch.setattr("subprocess.Popen", refuse)
    monkeypatch.setattr("subprocess.run", refuse)
    monkeypatch.setattr("os.system", refuse)
    write_hypothesis(tmp_path)
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    node.run()
    assert calls == []
    assert node.shopping_agent_started is False
    package = Path("dataset_discovery")
    text = "\n".join(path.read_text(encoding="utf-8") for path in package.glob("*.py"))
    assert "subprocess" not in text
    assert "os.system" not in text
    assert "Popen" not in text


def test_datasetDiscoveryNode_run_writesNoHypothesisOrRule(tmp_path: Path) -> None:
    # POL-004 REQ-007: no hypothesis, validation metric, or deployed rule is written.
    write_hypothesis(tmp_path)
    before = (tmp_path / "hypotheses.json").read_text(encoding="utf-8")
    node = DatasetDiscoveryNode(tmp_path, lambda query: [complete_candidate()], now=lambda: NOW)
    node.run()
    assert (tmp_path / "hypotheses.json").read_text(encoding="utf-8") == before
    names = {path.name for path in tmp_path.iterdir()}
    assert names <= {"hypotheses.json", "datasets.json", "discovery_state.json"}
    assert all("validation" not in name and "rule" not in name for name in names)
    records = DatasetRegistry(tmp_path).read()
    assert len(records) == 1
    assert records[0]["suitability"] == "suitable"
