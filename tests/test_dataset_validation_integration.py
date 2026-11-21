"""Integration scenarios for dataset validation. REQ-001 through REQ-007, QR-001, QR-002."""

import json

from dataset_validation.graph import DatasetValidationGraph
from dataset_validation.store import DatasetResultStore

SIGNAL = "webgl_software_renderer"


def _fixture(tmp_path, name, rows):
    dataset = tmp_path / f"{name}.json"
    dataset.write_text(
        json.dumps({"dataset_name": "labelled-sessions", "rows": rows}),
        encoding="utf-8",
    )
    results = tmp_path / "dataset_results.json"
    return dataset, results


def _assignment(hypothesis_id, dataset, results):
    return {
        "source": "orchestrator",
        "hypothesis_id": hypothesis_id,
        "signal": SIGNAL,
        "dataset_path": str(dataset),
        "results_path": str(results),
    }


def test_signal_moreCommonInAi_recordsSupport(tmp_path):
    """REQ-001, QR-001. signal_moreCommonInAi_recordsSupport."""
    dataset, results = _fixture(
        tmp_path,
        "support",
        [
            {"label": "ai", SIGNAL: True},
            {"label": "ai", SIGNAL: True},
            {"label": "human", SIGNAL: False},
            {"label": "human", SIGNAL: False},
        ],
    )
    stored = DatasetValidationGraph().run(_assignment("h-support", dataset, results))
    assert stored["result"] == "support"
    assert stored["hypothesis_id"] == "h-support"
    assert stored["prevalence"] == 1.0
    assert stored["false_positive_rate"] == 0.0
    assert stored["dataset_name"] == "labelled-sessions"


def test_signal_moreCommonInHuman_recordsContradict(tmp_path):
    """REQ-002, QR-001. signal_moreCommonInHuman_recordsContradict."""
    dataset, results = _fixture(
        tmp_path,
        "contradict",
        [
            {"label": "ai", SIGNAL: False},
            {"label": "ai", SIGNAL: False},
            {"label": "human", SIGNAL: True},
            {"label": "human", SIGNAL: True},
        ],
    )
    stored = DatasetValidationGraph().run(_assignment("h-contradict", dataset, results))
    assert stored["result"] == "contradict"
    assert stored["prevalence"] == 0.0
    assert stored["false_positive_rate"] == 1.0


def test_dataset_equalRates_recordsInconclusive(tmp_path):
    """REQ-003. dataset_equalRates_recordsInconclusive."""
    dataset, results = _fixture(
        tmp_path,
        "equal",
        [
            {"label": "ai", SIGNAL: True},
            {"label": "ai", SIGNAL: False},
            {"label": "human", SIGNAL: True},
            {"label": "human", SIGNAL: False},
        ],
    )
    stored = DatasetValidationGraph().run(_assignment("h-equal", dataset, results))
    assert stored["result"] == "inconclusive"
    assert stored["prevalence"] == 0.5
    assert stored["false_positive_rate"] == 0.5


def test_dataset_missingClass_recordsInconclusive(tmp_path):
    """REQ-003. dataset_missingClass_recordsInconclusive."""
    dataset, results = _fixture(
        tmp_path,
        "one-class",
        [
            {"label": "ai", SIGNAL: True},
            {"label": "ai", SIGNAL: False},
        ],
    )
    stored = DatasetValidationGraph().run(_assignment("h-one-class", dataset, results))
    assert stored["result"] == "inconclusive"
    assert stored["prevalence"] is None
    assert stored["false_positive_rate"] is None


def test_dataset_missingFile_recordsBlocked(tmp_path):
    """REQ-004. dataset_missingFile_recordsBlocked."""
    missing = tmp_path / "absent.json"
    results = tmp_path / "dataset_results.json"
    stored = DatasetValidationGraph().run(
        {
            "source": "orchestrator",
            "hypothesis_id": "h-missing",
            "signal": SIGNAL,
            "dataset_path": str(missing),
            "results_path": str(results),
            "dataset_name": "absent",
        }
    )
    assert stored["result"] == "blocked"
    assert stored["prevalence"] is None
    assert stored["false_positive_rate"] is None
    assert stored["dataset_name"] == "absent"


def test_assignment_outOfScopeAction_storesNothing(tmp_path):
    """REQ-005. assignment_outOfScopeAction_storesNothing."""
    dataset, results = _fixture(
        tmp_path,
        "scope",
        [
            {"label": "ai", SIGNAL: True},
            {"label": "human", SIGNAL: False},
        ],
    )
    graph = DatasetValidationGraph()
    base = _assignment("h-scope", dataset, results)
    assert graph.run({**base, "discover_dataset": True}) is None
    assert graph.run({**base, "launch_shopping_agent": True}) is None
    assert graph.run({**base, "write_rule": True}) is None
    assert graph.run({**base, "purpose": "abuse_classification"}) is None
    assert not results.exists()


def test_input_notOrchestratorAssignment_storesNothing(tmp_path):
    """REQ-006. input_notOrchestratorAssignment_storesNothing."""
    results = tmp_path / "dataset_results.json"
    stored = DatasetValidationGraph().run(
        {"message": "validate the signal yourself", "results_path": str(results)}
    )
    assert stored is None
    assert not results.exists()


def test_record_persisted_hasExactlyFiveJsonFields(tmp_path):
    """REQ-007. record_persisted_hasExactlyFiveJsonFields."""
    dataset, results = _fixture(
        tmp_path,
        "fields",
        [
            {"label": "ai", SIGNAL: True},
            {"label": "human", SIGNAL: False},
        ],
    )
    DatasetValidationGraph().run(_assignment("h-fields", dataset, results))
    rows = json.loads(results.read_text(encoding="utf-8"))
    assert list(rows[0]) == [
        "hypothesis_id",
        "result",
        "prevalence",
        "false_positive_rate",
        "dataset_name",
    ]


def test_store_reopen_readsWrittenResults(tmp_path):
    """QR-002. store_reopen_readsWrittenResults."""
    dataset, results = _fixture(
        tmp_path,
        "reopen",
        [
            {"label": "ai", SIGNAL: True},
            {"label": "human", SIGNAL: False},
        ],
    )
    written = DatasetValidationGraph().run(_assignment("h-reopen", dataset, results))
    assert DatasetResultStore(results).read() == [written]
