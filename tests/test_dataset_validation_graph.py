"""Unit tests for DatasetValidationGraph. POL-003, POL-004."""

from dataset_validation.graph import DatasetValidationGraph
from dataset_validation.store import DatasetResultStore


def test_datasetValidationGraph_chatPayload_storesNothing(tmp_path):
    """POL-003. datasetValidationGraph_chatPayload_storesNothing."""
    results = tmp_path / "dataset_results.json"
    outcome = DatasetValidationGraph().run(
        {"message": "please validate this hypothesis", "results_path": str(results)}
    )
    assert outcome is None
    assert DatasetResultStore(results).read() == []


def test_datasetValidationGraph_forbiddenAction_storesNothing(tmp_path):
    """POL-004. datasetValidationGraph_forbiddenAction_storesNothing."""
    results = tmp_path / "dataset_results.json"
    dataset = tmp_path / "dataset.json"
    dataset.write_text(
        '{"dataset_name":"labelled-sessions","rows":[{"label":"ai","webgl_software_renderer":true},'
        '{"label":"human","webgl_software_renderer":false}]}',
        encoding="utf-8",
    )
    base = {
        "source": "orchestrator",
        "hypothesis_id": "h-1",
        "signal": "webgl_software_renderer",
        "dataset_path": str(dataset),
        "results_path": str(results),
    }
    graph = DatasetValidationGraph()
    assert graph.run({**base, "discover_dataset": True}) is None
    assert graph.run({**base, "launch_shopping_agent": True}) is None
    assert graph.run({**base, "write_rule": True}) is None
    assert graph.run({**base, "purpose": "abuse_classification"}) is None
    assert DatasetResultStore(results).read() == []
