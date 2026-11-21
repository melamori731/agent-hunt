"""System end-to-end: human name to a submitted specification, with no shopping agent."""

import subprocess

from system_e2e.pipeline import run


def _refuse_processes(monkeypatch):
    started = []

    def refuse(*_args, **_kwargs):
        started.append(True)
        raise AssertionError("the system test must not start a process")

    monkeypatch.setattr(subprocess, "Popen", refuse)
    monkeypatch.setattr(subprocess, "run", refuse)
    return started


def test_humanName_submittedSpec_includesSourcesAndValidation(tmp_path, monkeypatch):
    started = _refuse_processes(monkeypatch)

    outcome = run(tmp_path)

    assert started == []
    assert outcome["shopping_agent_started"] is False
    assert outcome["assignment"]["assistant_name"] == "Muse"
    assert outcome["assignment"]["role"] == "agent-intelligence"
    assert outcome["dataset_result"]["result"] == "support"
    assert outcome["sandbox_result"]["result"] == "support"
    specification = outcome["specification"]
    assert specification["submitted"] is True
    assert specification["deployed"] is False
    assert specification["research_sources"]
    assert all(source["url"] and source["title"] for source in specification["research_sources"])
    assert specification["validation_results"]["dataset_result"] == "support"
    assert specification["validation_results"]["sandbox_result"] == "support"
    assert outcome["evaluation"]["result"] == "PASS"
    stored = outcome["orchestrator_specifications"][0]
    assert stored["submitted"] is True
    assert stored["deployed"] is False
    suitable = [row for row in outcome["datasets"] if row["suitability"] == "suitable"]
    assert suitable


def test_contradictingValidation_storesNoSubmittedSpec(tmp_path, monkeypatch):
    started = _refuse_processes(monkeypatch)

    outcome = run(tmp_path, sandbox_signal_observed=False)

    assert started == []
    assert outcome["shopping_agent_started"] is False
    assert outcome["dataset_result"]["result"] == "support"
    assert outcome["sandbox_result"]["result"] == "contradict"
    assert outcome["specification"] is None
    assert outcome["evaluation"]["result"] != "PASS"
    assert outcome["orchestrator_specifications"] == []


def test_abuseRequest_storesNoAssignment(tmp_path, monkeypatch):
    started = _refuse_processes(monkeypatch)

    outcome = run(tmp_path, purpose="abuse_classification")

    assert started == []
    assert outcome["shopping_agent_started"] is False
    assert outcome["assignment"] is None
    assert outcome["hypotheses"] == []
    assert outcome["specification"] is None
    assert outcome["orchestrator_specifications"] == []
