"""Unit tests for DatasetResultStore."""

from dataset_validation.store import DatasetResultStore


def test_datasetResultStore_reopen_returnsWrittenRecord(tmp_path):
    """datasetResultStore_reopen_returnsWrittenRecord."""
    path = tmp_path / "dataset_results.json"
    record = {
        "hypothesis_id": "h-1",
        "result": "support",
        "prevalence": 1.0,
        "false_positive_rate": 0.0,
        "dataset_name": "labelled-sessions",
    }
    DatasetResultStore(path).append(record)
    reopened = DatasetResultStore(path).read()
    assert reopened == [record]
