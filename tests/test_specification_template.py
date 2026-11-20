"""Unit tests for SpecificationTemplate. INV-001, INV-002, INV-003."""

import pytest

from detection_rule_specification.template import SpecificationTemplate


def _record(**overrides):
    record = {
        "hypothesis_id": "H1",
        "submitted": True,
        "deployed": False,
        "confidence": "standard",
        "research_sources": [{"url": "https://example.test/muse", "title": "Muse architecture"}],
        "validation_results": {"dataset_result": "support", "sandbox_result": "support"},
    }
    record.update(overrides)
    return record


def test_specificationTemplate_deployedTrue_rejected():
    """INV-001."""
    template = SpecificationTemplate()
    with pytest.raises(ValueError, match="submitted and not deployed"):
        template.assert_record(_record(deployed=True))
    built = template.build(
        "H1",
        "standard",
        [{"url": "https://example.test/muse", "title": "Muse architecture"}],
        "support",
        "support",
    )
    assert built["submitted"] is True
    assert built["deployed"] is False


def test_specificationTemplate_abuseField_rejected():
    """INV-002."""
    template = SpecificationTemplate()
    with pytest.raises(ValueError, match="abuse or legitimacy"):
        template.assert_record(_record(abuse_classification="abusive"))
    with pytest.raises(ValueError, match="abuse or legitimacy"):
        template.assert_record(_record(legitimacy="legitimate"))


def test_specificationTemplate_missingEvidenceField_rejected():
    """INV-003."""
    template = SpecificationTemplate()
    missing_title = _record(research_sources=[{"url": "https://example.test/muse", "title": ""}])
    with pytest.raises(ValueError, match="url and a title"):
        template.assert_record(missing_title)
    missing_url = _record(research_sources=[{"url": "", "title": "Muse architecture"}])
    with pytest.raises(ValueError, match="url and a title"):
        template.assert_record(missing_url)
    missing_dataset = _record(validation_results={"dataset_result": "", "sandbox_result": "support"})
    with pytest.raises(ValueError, match="dataset result and the sandbox result"):
        template.assert_record(missing_dataset)
    missing_sandbox = _record(validation_results={"dataset_result": "support", "sandbox_result": ""})
    with pytest.raises(ValueError, match="dataset result and the sandbox result"):
        template.assert_record(missing_sandbox)


def test_specificationTemplate_sections_namesResearchSourcesAndValidationResults():
    assert SpecificationTemplate.SECTIONS == ("research_sources", "validation_results")
