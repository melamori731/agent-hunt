"""Unit tests for DetectionRuleSpecification. POL-001."""

import json

from detection_rule_specification.specification import DetectionRuleSpecification
from detection_rule_specification.store import RuleSpecificationStore


def _seed(root):
    hypothesis = {
        "hypothesis_id": "H1",
        "research_sources": [{"url": "https://example.test/muse", "title": "Muse architecture"}],
    }
    validation = {"hypothesis_id": "H1", "dataset_result": "support", "sandbox_result": "support"}
    (root / "hypotheses.json").write_text(json.dumps([hypothesis]), encoding="utf-8")
    (root / "validation_results.json").write_text(json.dumps([validation]), encoding="utf-8")


def test_detectionRuleSpecification_result_hasNoAgentMessage(tmp_path):
    """POL-001."""
    _seed(tmp_path)
    result = DetectionRuleSpecification(RuleSpecificationStore(tmp_path)).run("H1")
    assert result["written"] is True
    assert "messages" not in result
    assert "chat" not in result
    assert "agent_message" not in result


def test_detectionRuleSpecification_graph_hasSpecifyNode(tmp_path):
    node = DetectionRuleSpecification(RuleSpecificationStore(tmp_path))
    names = set(node.graph.get_graph().nodes)
    assert "specify" in names
    assert node.tool.name == "assemble_rule_specification"
