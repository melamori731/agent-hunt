"""Shared fixtures for agent-intelligence tests."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from agent_intelligence.store import JsonResearchStore

MUSE_SOURCE = {"url": "https://example.test/muse", "title": "Muse shopping assistant notes"}
MUSE_SIGNAL = "navigator.webdriver is true at checkout"
MUSE_OBSERVATION = "The checkout page exposes navigator.webdriver as true."
MUSE_MEASUREMENTS = ["Share of checkout sessions with navigator.webdriver true"]
T0 = datetime(2026, 11, 20, 12, 0, tzinfo=UTC)


def source_page(
    assistant_name: str,
    *,
    url: str,
    title: str,
    supports_testable_signal: bool,
    signal: str | None = None,
    observation: str | None = None,
    measurements: list[str] | None = None,
) -> dict:
    page = {
        "assistantName": assistant_name,
        "url": url,
        "title": title,
        "supportsTestableSignal": supports_testable_signal,
    }
    if signal is not None:
        page["signal"] = signal
    if observation is not None:
        page["observation"] = observation
    if measurements is not None:
        page["measurements"] = measurements
    return page


def muse_page(*, supports_testable_signal: bool = True) -> dict:
    page = source_page(
        "Muse",
        url=MUSE_SOURCE["url"],
        title=MUSE_SOURCE["title"],
        supports_testable_signal=supports_testable_signal,
    )
    if supports_testable_signal:
        page["signal"] = MUSE_SIGNAL
        page["observation"] = MUSE_OBSERVATION
        page["measurements"] = list(MUSE_MEASUREMENTS)
    return page


def orchestrator_assignment(assistant_name: str = "Muse", **extra) -> dict:
    assignment = {
        "kind": "orchestrator_assignment",
        "assistantName": assistant_name,
    }
    assignment.update(extra)
    return assignment


def complete_hypothesis_draft(**overrides) -> dict:
    draft = {
        "assistantName": "Muse",
        "signal": MUSE_SIGNAL,
        "observation": MUSE_OBSERVATION,
        "sources": [
            {
                "url": MUSE_SOURCE["url"],
                "title": MUSE_SOURCE["title"],
                "supportsTestableSignal": True,
            }
        ],
        "measurements": list(MUSE_MEASUREMENTS),
    }
    draft.update(overrides)
    return draft


def hours_after(hours: int) -> datetime:
    return T0 + timedelta(hours=hours)


def write_json(directory: Path, filename: str, payload) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_system_records(directory: Path, *, include_validation_results: bool) -> dict:
    """Saved records for the system test. Downstream stages are fixtures, not agents."""
    sources = [dict(MUSE_SOURCE)]
    validation_results = {
        "dataset": {"outcome": "supported", "measurement": MUSE_MEASUREMENTS[0]},
        "sandbox": {"outcome": "reproduced", "evidenceFile": "vm_evidence.json"},
    }
    specification = {
        "researchSources": sources,
        "status": "submitted",
    }
    if include_validation_results:
        specification["validationResults"] = validation_results
    write_json(
        directory,
        "orchestrator_assignment.json",
        {"assistantName": "Muse", "humanText": "Investigate Muse checkout signals."},
    )
    write_json(
        directory,
        JsonResearchStore.REGISTRY_ENTRIES,
        [{"recordType": "registry_entry", "assistantName": "Muse", "sources": sources}],
    )
    write_json(
        directory,
        JsonResearchStore.REGISTRY_REPORTS,
        [
            {
                "recordType": "registry_report",
                "assistantName": "Muse",
                "sources": sources,
                "origin": "orchestrator assignment",
                "summary": "Added Muse from orchestrator assignment.",
            }
        ],
    )
    write_json(
        directory,
        JsonResearchStore.HYPOTHESES,
        [
            {
                "recordType": "hypothesis",
                "assistantName": "Muse",
                "signal": MUSE_SIGNAL,
                "observation": MUSE_OBSERVATION,
                "sources": sources,
                "measurements": list(MUSE_MEASUREMENTS),
            }
        ],
    )
    write_json(directory, JsonResearchStore.UNRESOLVED, [])
    write_json(
        directory,
        "vm_evidence.json",
        {"assistantName": "Muse", "checkoutObserved": True},
    )
    write_json(directory, "dataset_validation_results.json", validation_results["dataset"])
    write_json(directory, "evaluator_results.json", {"independent": True, "contradiction": False})
    write_json(directory, "submitted_rule_specification.json", specification)
    return specification
