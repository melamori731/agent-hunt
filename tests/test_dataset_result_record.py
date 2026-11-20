"""Unit tests for DatasetResultRecord. INV-001, INV-002, POL-001, POL-002."""

import pytest

from dataset_validation.record import DatasetResultRecord


def test_datasetResultRecord_unknownResult_rejected():
    """INV-001. datasetResultRecord_unknownResult_rejected rejects a fifth result."""
    with pytest.raises(ValueError):
        DatasetResultRecord("h-1", "labelled-sessions", "maybe", 1.0, 0.0)


def test_datasetResultRecord_supportWithoutHigherPrevalence_rejected():
    """INV-002. datasetResultRecord_supportWithoutHigherPrevalence_rejected."""
    with pytest.raises(ValueError):
        DatasetResultRecord("h-1", "labelled-sessions", "support", 0.5, 0.5)
    with pytest.raises(ValueError):
        DatasetResultRecord("h-1", "labelled-sessions", "blocked", 0.0, None)


def test_datasetResultRecord_missingFile_recordsBlockedWithNullRates():
    """POL-001. datasetResultRecord_missingFile_recordsBlockedWithNullRates."""
    record = DatasetResultRecord.missing("h-missing", "absent")
    stored = record.to_dict()
    assert stored["result"] == "blocked"
    assert stored["prevalence"] is None
    assert stored["false_positive_rate"] is None


def test_datasetResultRecord_rateComparison_selectsResult():
    """POL-002. datasetResultRecord_rateComparison_selectsResult."""
    support = DatasetResultRecord.from_rates("h-support", "labelled-sessions", 1.0, 0.0)
    contradict = DatasetResultRecord.from_rates("h-contradict", "labelled-sessions", 0.0, 1.0)
    inconclusive = DatasetResultRecord.from_rates("h-equal", "labelled-sessions", 0.5, 0.5)
    assert support.result == "support"
    assert contradict.result == "contradict"
    assert inconclusive.result == "inconclusive"
