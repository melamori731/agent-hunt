# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Submitted specification

#### REQ-001

- **Statement**: When both stored validation results support a hypothesis and every research source has a URL and a title, the component writes one `rule_specifications.json` record for that hypothesis with confidence standard, submitted true, deployed false, those research sources, and the dataset result and sandbox result.
- **Source**: User settled scope 2026-11-20; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Detection Rule Specification step 6
- **Verification**: Run the component on one hypothesis with two support results and two sourced references and confirm that record.
- **Dependencies**: INV-001, INV-003

#### REQ-002

- **Statement**: When one stored validation result supports a hypothesis, the other is inconclusive or blocked and does not contradict, and every research source has a URL and a title, the component writes one `rule_specifications.json` record with confidence lower and the same evidence fields.
- **Source**: User settled scope 2026-11-20; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Orchestrator step 3
- **Verification**: Run once with the other result inconclusive and once with the other result blocked, and confirm both records use confidence lower.
- **Dependencies**: INV-001, INV-003

#### REQ-003

- **Statement**: When either validation result contradicts the other, a research source is missing a URL or a title, the hypothesis has no research source, or a validation result for the hypothesis is absent, the component writes no rule specification.
- **Source**: User settled scope 2026-11-20
- **Verification**: Run each refusing case and confirm `rule_specifications.json` gains no record for that hypothesis.
- **Dependencies**: None

### Stored evidence only

#### REQ-004

- **Statement**: The component reads hypothesis sources and validation results from stored records and does not retrieve publications, discover datasets, or execute the sandbox.
- **Source**: User settled scope 2026-11-20
- **Verification**: Run the component with only the stored input files present and confirm the only added record file is the specification.
- **Dependencies**: REQ-001

---

## Summary

| Verified | Total |
|----------|-------|
| 4 | 4 |
