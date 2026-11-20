"""Unit tests for RuleSpecificationStore. QR-002."""

from detection_rule_specification.store import RuleSpecificationStore
from detection_rule_specification.template import SpecificationTemplate


def test_ruleSpecificationStore_reopen_returnsWrittenSpecification(tmp_path):
    """QR-002."""
    record = SpecificationTemplate().build(
        "H1",
        "standard",
        [{"url": "https://example.test/muse", "title": "Muse architecture"}],
        "support",
        "support",
    )
    RuleSpecificationStore(tmp_path).save_specification(record)
    reopened = RuleSpecificationStore(tmp_path)
    rows = reopened.specifications()
    assert rows == [record]
    assert (tmp_path / "rule_specifications.json").is_file()
