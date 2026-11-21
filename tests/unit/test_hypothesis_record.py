"""Unit tests for HypothesisRecord. INV-001, INV-002, POL-001, POL-002."""

import pytest

from agent_intelligence import HypothesisRecord, HypothesisRejection
from tests.support import MUSE_SOURCE, complete_hypothesis_draft


def hypothesisRecord_emptySources_rejected():
    """INV-001. A hypothesis with no source is rejected."""
    record = HypothesisRecord()
    with pytest.raises(HypothesisRejection):
        record.submit(complete_hypothesis_draft(sources=[]))
    assert record.hypotheses == []
    assert record.unresolved_investigations == []


def hypothesisRecord_abuseClassification_rejected():
    """INV-002. An abuse or legitimacy classification is rejected."""
    record = HypothesisRecord()
    for classification in ("abusive", "malicious", "legitimate"):
        with pytest.raises(HypothesisRejection):
            record.submit(complete_hypothesis_draft(classification=classification))
    with pytest.raises(HypothesisRejection):
        record.submit(complete_hypothesis_draft(purpose="abuse_classification"))
    assert record.hypotheses == []
    assert record.unresolved_investigations == []


def hypothesisRecord_weakSources_storesUnresolvedOnly():
    """POL-001. Weak sources create an unresolved investigation and no hypothesis."""
    record = HypothesisRecord()
    weak = complete_hypothesis_draft(
        sources=[{**MUSE_SOURCE, "supportsTestableSignal": False}]
    )
    result = record.submit(weak)
    assert result["outcome"] == "unresolved"
    assert record.hypotheses == []
    assert len(record.unresolved_investigations) == 1
    stored = record.unresolved_investigations[0]
    assert stored["sources"] == [MUSE_SOURCE]
    assert stored["recordType"] == "unresolved_investigation"
    assert "signal" not in stored


def hypothesisRecord_duplicateSignal_rejected():
    """POL-002. The same assistant and signal cannot be stored twice."""
    record = HypothesisRecord()
    record.submit(complete_hypothesis_draft())
    with pytest.raises(HypothesisRejection) as caught:
        record.submit(complete_hypothesis_draft())
    assert caught.value.duplicate is True
    assert len(record.hypotheses) == 1


def hypothesisRecord_missingField_rejected():
    """REQ-004. Omitting the signal, observation, sources, or measurements is rejected."""
    for field in ("signal", "observation", "sources", "measurements"):
        record = HypothesisRecord()
        draft = complete_hypothesis_draft()
        draft.pop(field)
        with pytest.raises(HypothesisRejection):
            record.submit(draft)
        assert record.hypotheses == []
