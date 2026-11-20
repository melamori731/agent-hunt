"""Integration scenarios from integration-test-scenarios.md.

REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008,
REQ-009, REQ-010, QR-001, QR-002, QR-003.
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import pytest

from agent_intelligence import (
    AgentIntelligenceNode,
    DirectHumanInputRejected,
    HypothesisRecord,
    HypothesisRejection,
    JsonResearchStore,
)
from agent_intelligence.system_test import SystemEndToEndTest
from tests.support import (
    MUSE_MEASUREMENTS,
    MUSE_OBSERVATION,
    MUSE_SIGNAL,
    MUSE_SOURCE,
    T0,
    hours_after,
    muse_page,
    orchestrator_assignment,
    source_page,
    write_system_records,
)


def assignment_namedAssistant_storesSourcedEntry(tmp_path):
    """REQ-001, QR-001. An assignment stores one sourced registry entry."""
    store = JsonResearchStore(tmp_path)
    node = AgentIntelligenceNode(store, source_catalog=[muse_page()])
    node.run_assignment(orchestrator_assignment())
    entries = store.read_registry_entries()
    assert len(entries) == 1
    assert entries[0]["assistantName"] == "Muse"
    assert entries[0]["sources"] == [MUSE_SOURCE]
    assert entries[0]["sources"][0]["url"]
    assert entries[0]["sources"][0]["title"]
    with pytest.raises(DirectHumanInputRejected):
        node.run_assignment({"humanText": "Please research Muse."})
    assert not hasattr(node, "accept_human_text")


def discovery_unknownAssistant_addsOneEntryAndReport(tmp_path):
    """REQ-002, REQ-003. Scheduled discovery adds one assistant and one report."""
    store = JsonResearchStore(tmp_path)
    page = source_page(
        "NewBot",
        url="https://example.test/newbot",
        title="NewBot product notes",
        supports_testable_signal=False,
    )
    node = AgentIntelligenceNode(store, source_catalog=[page])
    node.run_discovery(previous_run=T0, now=hours_after(24))
    entries = store.read_registry_entries()
    reports = store.read_registry_reports()
    assert len(entries) == 1
    assert entries[0]["assistantName"] == "NewBot"
    assert entries[0]["sources"] == [{"url": page["url"], "title": page["title"]}]
    assert len(reports) == 1
    assert reports[0]["assistantName"] == "NewBot"
    assert reports[0]["sources"] == [{"url": page["url"], "title": page["title"]}]
    assert reports[0]["origin"] == "scheduled discovery"


def assignment_namedAssistant_reportNamesOrchestratorOrigin(tmp_path):
    """REQ-003. The assignment report names the orchestrator origin."""
    store = JsonResearchStore(tmp_path)
    node = AgentIntelligenceNode(store, source_catalog=[muse_page()])
    node.run_assignment(orchestrator_assignment())
    reports = store.read_registry_reports()
    assert len(reports) == 1
    assert reports[0]["assistantName"] == "Muse"
    assert reports[0]["sources"] == [MUSE_SOURCE]
    assert reports[0]["origin"] == "orchestrator assignment"


def hypothesis_completeSignal_storesRequiredFields(tmp_path):
    """REQ-004, QR-001. A complete signal is stored, and a partial record is rejected."""
    store = JsonResearchStore(tmp_path)
    node = AgentIntelligenceNode(store, source_catalog=[muse_page()])
    node.run_assignment(orchestrator_assignment())
    hypotheses = store.read_hypotheses()
    assert len(hypotheses) == 1
    stored = hypotheses[0]
    assert stored["signal"] == MUSE_SIGNAL
    assert stored["observation"] == MUSE_OBSERVATION
    assert stored["sources"] == [MUSE_SOURCE]
    assert stored["sources"][0]["url"] and stored["sources"][0]["title"]
    assert stored["measurements"] == MUSE_MEASUREMENTS
    record = HypothesisRecord(store)
    for field in ("signal", "observation", "sources", "measurements"):
        draft = {
            "assistantName": "Other",
            "signal": MUSE_SIGNAL,
            "observation": MUSE_OBSERVATION,
            "sources": [{**MUSE_SOURCE, "supportsTestableSignal": True}],
            "measurements": list(MUSE_MEASUREMENTS),
        }
        draft.pop(field)
        with pytest.raises(HypothesisRejection):
            record.submit(draft)


def hypothesis_abusePurpose_storesNothing(tmp_path):
    """REQ-005. An abuse-classification request stores no hypothesis."""
    store = JsonResearchStore(tmp_path)
    node = AgentIntelligenceNode(store, source_catalog=[muse_page()])
    before = len(store.read_hypotheses())
    with pytest.raises(HypothesisRejection):
        node.run_assignment(
            orchestrator_assignment(purpose="abuse_classification", classification="abusive")
        )
    assert len(store.read_hypotheses()) == before
    assert store.read_unresolved_investigations() == []


def hypothesis_sameSignal_doesNotDuplicate(tmp_path):
    """REQ-006. The same assistant and signal stay a single hypothesis."""
    store = JsonResearchStore(tmp_path)
    node = AgentIntelligenceNode(store, source_catalog=[muse_page()])
    node.run_assignment(orchestrator_assignment())
    with pytest.raises(HypothesisRejection):
        node.run_assignment(orchestrator_assignment())
    matching = [
        item
        for item in store.read_hypotheses()
        if item["assistantName"] == "Muse" and item["signal"] == MUSE_SIGNAL
    ]
    assert len(matching) == 1


def hypothesis_weakSources_storesUnresolvedOnly(tmp_path):
    """REQ-007. Non-evidential sources store an unresolved investigation only."""
    store = JsonResearchStore(tmp_path)
    before = len(store.read_hypotheses())
    node = AgentIntelligenceNode(
        store, source_catalog=[muse_page(supports_testable_signal=False)]
    )
    node.run_assignment(orchestrator_assignment())
    assert len(store.read_hypotheses()) == before
    unresolved = store.read_unresolved_investigations()
    assert len(unresolved) == 1
    assert unresolved[0]["assistantName"] == "Muse"
    assert unresolved[0]["sources"] == [MUSE_SOURCE]


def system_completeRecords_specificationPasses(tmp_path):
    """REQ-008, QR-003. Complete saved records pass twice and start no shopping agent."""
    write_system_records(tmp_path, include_validation_results=True)
    first = SystemEndToEndTest().run(tmp_path)
    second = SystemEndToEndTest().run(tmp_path)
    assert first["passed"] is True
    assert second["passed"] is True
    assert first == second
    specification = first["specification"]
    assert specification["researchSources"] == [MUSE_SOURCE]
    assert specification["validationResults"]["dataset"]["outcome"] == "supported"
    assert specification["validationResults"]["sandbox"]["outcome"] == "reproduced"
    assert first["shoppingAgentStarted"] is False
    assert second["shoppingAgentStarted"] is False


def system_missingValidationResults_specificationFails(tmp_path):
    """REQ-008. A specification without validation results fails."""
    write_system_records(tmp_path, include_validation_results=False)
    result = SystemEndToEndTest().run(tmp_path)
    assert result["passed"] is False
    assert result["shoppingAgentStarted"] is False


def discovery_knownAssistant_storesNewPattern(tmp_path):
    """REQ-009. Discovery stores one new pattern and does not duplicate a known signal."""
    store = JsonResearchStore(tmp_path)
    known = muse_page()
    AgentIntelligenceNode(store, source_catalog=[known]).run_assignment(orchestrator_assignment())
    assert len(store.read_hypotheses()) == 1
    new_signal = source_page(
        "Muse",
        url="https://example.test/muse-pointer",
        title="Muse pointer cadence notes",
        supports_testable_signal=True,
        signal="pointer cadence stays constant through checkout",
        observation="Pointer moves at a fixed interval on the checkout page.",
        measurements=["Distribution of pointer intervals on checkout"],
    )
    node = AgentIntelligenceNode(store, source_catalog=[known, new_signal])
    node.run_discovery(previous_run=T0, now=hours_after(24))
    hypotheses = store.read_hypotheses()
    signals = [item["signal"] for item in hypotheses if item["assistantName"] == "Muse"]
    assert signals.count(MUSE_SIGNAL) == 1
    assert "pointer cadence stays constant through checkout" in signals
    assert len(signals) == 2
    assert len(store.read_registry_reports()) == 1


def discovery_defaultInterval_startsAt24Hours(tmp_path):
    """REQ-010. The default interval waits 24 hours before another discovery run."""
    store = JsonResearchStore(tmp_path)
    page = source_page(
        "NewBot",
        url="https://example.test/newbot",
        title="NewBot product notes",
        supports_testable_signal=False,
    )
    node = AgentIntelligenceNode(store, source_catalog=[page])
    early = node.run_discovery(previous_run=T0, now=hours_after(23))
    assert early["started"] is False
    assert store.read_registry_entries() == []
    due = node.run_discovery(previous_run=T0, now=hours_after(24))
    assert due["started"] is True
    assert len(store.read_registry_entries()) == 1


def discovery_oneHourInterval_startsAtOneHour(tmp_path):
    """REQ-010. A one-hour interval starts discovery after one hour."""
    store = JsonResearchStore(tmp_path)
    page = source_page(
        "NewBot",
        url="https://example.test/newbot",
        title="NewBot product notes",
        supports_testable_signal=False,
    )
    node = AgentIntelligenceNode(store, source_catalog=[page], interval=timedelta(hours=1))
    result = node.run_discovery(previous_run=T0, now=hours_after(1))
    assert result["started"] is True
    assert len(store.read_registry_entries()) == 1


def store_processRestart_recordsRemain(tmp_path):
    """QR-002. Records written by one process remain readable in a new process."""
    writer = """
import sys
from pathlib import Path
from agent_intelligence import JsonResearchStore

directory = Path(sys.argv[1])
store = JsonResearchStore(directory)
source = {
    "url": "https://example.test/muse",
    "title": "Muse shopping assistant notes",
}
store.write_registry_entry({
    "recordType": "registry_entry",
    "assistantName": "Muse",
    "sources": [source],
})
store.write_registry_report({
    "recordType": "registry_report",
    "assistantName": "Muse",
    "sources": [source],
    "origin": "orchestrator assignment",
})
store.write_hypothesis({
    "recordType": "hypothesis",
    "assistantName": "Muse",
    "signal": "navigator.webdriver is true at checkout",
    "observation": "The checkout page exposes navigator.webdriver as true.",
    "sources": [source],
    "measurements": ["Share of checkout sessions with navigator.webdriver true"],
})
store.write_unresolved_investigation({
    "recordType": "unresolved_investigation",
    "assistantName": "Other",
    "sources": [{"url": "https://example.test/other", "title": "Other notes"}],
    "reason": (
        "Retrieved sources do not support a testable shopping-session signal."
    ),
})
"""
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    completed = subprocess.run(
        [sys.executable, "-c", writer, str(tmp_path)],
        cwd=repo_root,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    store = JsonResearchStore(tmp_path)
    assert store.read_registry_entries()[0]["assistantName"] == "Muse"
    assert store.read_registry_reports()[0]["origin"] == "orchestrator assignment"
    assert store.read_hypotheses()[0]["signal"] == MUSE_SIGNAL
    assert store.read_unresolved_investigations()[0]["assistantName"] == "Other"
