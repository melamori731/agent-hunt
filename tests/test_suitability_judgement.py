"""Unit tests for SuitabilityJudgement. INV-002 POL-001."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dataset_discovery.suitability import SuitabilityJudgement
from tests.helpers import NOW, complete_candidate, hypothesis

JUDGEMENT = SuitabilityJudgement()


def test_suitabilityJudgement_queryMatchOnly_isUnsuitable() -> None:
    # INV-002: a query-only match is never suitable.
    entry = JUDGEMENT.judge(complete_candidate(queryMatchOnly=True), hypothesis(), NOW)
    assert entry["suitability"] == "unsuitable"
    assert entry["hypothesisId"] == "H1"


def test_suitabilityJudgement_missingLabel_isUnsuitable() -> None:
    # POL-001: a failed label check records unsuitable.
    missing_human = JUDGEMENT.judge(complete_candidate(hasHumanLabel=False), hypothesis(), NOW)
    missing_agent = JUDGEMENT.judge(complete_candidate(hasAgentLabel=False), hypothesis(), NOW)
    assert missing_human["suitability"] == "unsuitable"
    assert missing_agent["suitability"] == "unsuitable"


def test_suitabilityJudgement_staleVerification_isUnsuitable() -> None:
    # POL-001: age uses the 730-day window.
    now = datetime(2026, 11, 20, tzinfo=UTC)
    fresh = JUDGEMENT.judge(
        complete_candidate(verifiedAt="2024-11-20T00:00:00Z"),
        hypothesis(),
        now,
    )
    stale = JUDGEMENT.judge(
        complete_candidate(verifiedAt="2024-11-19T00:00:00Z"),
        hypothesis(),
        now,
    )
    future = JUDGEMENT.judge(
        complete_candidate(verifiedAt="2026-11-21T00:00:00Z"),
        hypothesis(),
        now,
    )
    assert fresh["suitability"] == "suitable"
    assert stale["suitability"] == "unsuitable"
    assert future["suitability"] == "unsuitable"
    assert now - datetime(2024, 11, 20, tzinfo=UTC) == timedelta(days=730)


def test_suitabilityJudgement_missingMeasurementField_isUnsuitable() -> None:
    # POL-001: coverage fails when a measurement field is absent.
    entry = JUDGEMENT.judge(complete_candidate(fields=["user_agent"]), hypothesis(), NOW)
    prose = JUDGEMENT.judge(complete_candidate(), {"id": "H1", "measurementFields": []}, NOW)
    assert entry["suitability"] == "unsuitable"
    assert prose["suitability"] == "unsuitable"


def test_suitabilityJudgement_completeCandidate_isSuitable() -> None:
    entry = JUDGEMENT.judge(complete_candidate(), hypothesis(), NOW)
    assert entry["suitability"] == "suitable"
    assert entry["datasetName"] == "muse-human-sessions"
    assert entry["sourceUrl"] == "https://example.edu/datasets/muse-human"
    assert entry["title"] == "Labelled Muse and human shopping sessions"
    assert entry["hypothesisId"] == "H1"
