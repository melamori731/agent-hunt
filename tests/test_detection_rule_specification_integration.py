"""Integration scenarios for detection rule specification."""

import json

from detection_rule_specification.specification import DetectionRuleSpecification
from detection_rule_specification.store import RuleSpecificationStore

SOURCE = {"url": "https://example.test/muse", "title": "Muse architecture"}


def _prepare(root, hypothesis_id, sources, dataset_result, sandbox_result, *, validation=True, id_key="hypothesis_id"):
    hypothesis = {id_key: hypothesis_id, "research_sources": sources}
    (root / "hypotheses.json").write_text(json.dumps([hypothesis]), encoding="utf-8")
    if validation:
        row = {id_key: hypothesis_id, "dataset_result": dataset_result, "sandbox_result": sandbox_result}
        (root / "validation_results.json").write_text(json.dumps([row]), encoding="utf-8")
    return DetectionRuleSpecification(RuleSpecificationStore(root))


def test_specification_bothSupport_writesStandardConfidence(tmp_path):
    """REQ-001."""
    node = _prepare(tmp_path, "H1", [SOURCE], "support", "support")
    result = node.run("H1")
    assert result["written"] is True
    record = result["record"]
    assert record["hypothesis_id"] == "H1"
    assert record["confidence"] == "standard"
    assert record["submitted"] is True
    assert record["deployed"] is False
    assert record["research_sources"] == [SOURCE]
    assert record["validation_results"] == {"dataset_result": "support", "sandbox_result": "support"}
    assert "abuse" not in record
    assert "legitimacy" not in record


def test_specification_oneSupportOtherInconclusive_writesLowerConfidence(tmp_path):
    """REQ-002."""
    node = _prepare(tmp_path, "H1", [SOURCE], "support", "inconclusive")
    record = node.run("H1")["record"]
    assert record["confidence"] == "lower"
    assert record["submitted"] is True
    assert record["deployed"] is False
    assert record["validation_results"]["dataset_result"] == "support"
    assert record["validation_results"]["sandbox_result"] == "inconclusive"
    assert record["research_sources"][0]["url"] == SOURCE["url"]
    assert record["research_sources"][0]["title"] == SOURCE["title"]


def test_specification_oneSupportOtherBlocked_writesLowerConfidence(tmp_path):
    """REQ-002."""
    node = _prepare(tmp_path, "H1", [SOURCE], "blocked", "support")
    record = node.run("H1")["record"]
    assert record["confidence"] == "lower"
    assert record["validation_results"] == {"dataset_result": "blocked", "sandbox_result": "support"}


def test_specification_contradiction_writesNothing(tmp_path):
    """REQ-003."""
    for dataset_result, sandbox_result in (("support", "contradict"), ("contradict", "support")):
        case = tmp_path / f"{dataset_result}-{sandbox_result}"
        case.mkdir()
        node = _prepare(case, "H1", [SOURCE], dataset_result, sandbox_result)
        result = node.run("H1")
        assert result["written"] is False
        assert result["record"] is None
        assert not (case / "rule_specifications.json").exists()


def test_specification_missingSource_writesNothing(tmp_path):
    """REQ-003."""
    cases = [
        ("empty", [], "support", "support", True),
        ("no-url", [{"url": "", "title": "Muse architecture"}], "support", "support", True),
        ("no-title", [{"url": "https://example.test/muse", "title": ""}], "support", "support", True),
        ("no-validation", [SOURCE], "support", "support", False),
    ]
    for name, sources, dataset_result, sandbox_result, validation in cases:
        case = tmp_path / name
        case.mkdir()
        node = _prepare(case, "H1", sources, dataset_result, sandbox_result, validation=validation)
        result = node.run("H1")
        assert result["written"] is False
        assert result["record"] is None


def test_specification_storedInputsOnly_doesNotResearch(tmp_path):
    """REQ-004."""
    node = _prepare(tmp_path, "H1", [SOURCE], "support", "support")
    before = {path.name for path in tmp_path.iterdir()}
    node.run("H1")
    added = {path.name for path in tmp_path.iterdir()} - before
    assert added == {"rule_specifications.json"}


def test_specification_repeat_writesEqualRecord(tmp_path):
    """QR-001."""
    node = _prepare(tmp_path, "H1", [SOURCE], "support", "support")
    first = node.run("H1")["record"]
    second = node.run("H1")["record"]
    assert first == second
    rows = json.loads((tmp_path / "rule_specifications.json").read_text(encoding="utf-8"))
    assert rows == [first]


def test_specification_aliasKeys_readsIdAndSources(tmp_path):
    """REQ-001. DD-002 aliases."""
    hypothesis = {"id": "H1", "sources": [SOURCE]}
    validation = {
        "hypothesis_id": "H1",
        "validation_results": {"dataset_result": "support", "sandbox_result": "support"},
    }
    (tmp_path / "hypotheses.json").write_text(json.dumps([hypothesis]), encoding="utf-8")
    (tmp_path / "validation_results.json").write_text(json.dumps([validation]), encoding="utf-8")
    record = DetectionRuleSpecification(RuleSpecificationStore(tmp_path)).run("H1")["record"]
    assert record["confidence"] == "standard"
    assert record["research_sources"] == [SOURCE]
