"""Unit tests for EvidenceConfidence. REQ-001, REQ-002, REQ-003."""

from detection_rule_specification.confidence import EvidenceConfidence

SOURCE = [{"url": "https://example.test/muse", "title": "Muse architecture"}]


def test_evidenceConfidence_bothSupport_returnsStandard():
    """REQ-001."""
    assert EvidenceConfidence().level("support", "support", SOURCE) == "standard"


def test_evidenceConfidence_inconclusiveOther_returnsLower():
    """REQ-002."""
    confidence = EvidenceConfidence()
    assert confidence.level("support", "inconclusive", SOURCE) == "lower"
    assert confidence.level("inconclusive", "support", SOURCE) == "lower"


def test_evidenceConfidence_blockedOther_returnsLower():
    """REQ-002."""
    confidence = EvidenceConfidence()
    assert confidence.level("support", "blocked", SOURCE) == "lower"
    assert confidence.level("blocked", "support", SOURCE) == "lower"


def test_evidenceConfidence_contradiction_returnsNone():
    """REQ-003."""
    confidence = EvidenceConfidence()
    assert confidence.level("support", "contradict", SOURCE) is None
    assert confidence.level("contradict", "support", SOURCE) is None


def test_evidenceConfidence_missingSource_returnsNone():
    """REQ-003."""
    confidence = EvidenceConfidence()
    assert confidence.level("support", "support", []) is None
    assert confidence.level("support", "support", [{"url": "", "title": "Muse architecture"}]) is None
    assert confidence.level("support", "support", [{"url": "https://example.test/muse", "title": ""}]) is None
    assert confidence.level("", "support", SOURCE) is None
    assert confidence.level("support", "", SOURCE) is None
    assert confidence.level("inconclusive", "blocked", SOURCE) is None
