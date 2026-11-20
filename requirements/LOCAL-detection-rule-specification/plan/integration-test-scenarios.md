# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `specification_bothSupport_writesStandardConfidence` | REQ-001 | Two support results and complete sources write one standard submitted specification. |
| `specification_oneSupportOtherInconclusive_writesLowerConfidence` | REQ-002 | One support result and one inconclusive result write lower confidence. |
| `specification_oneSupportOtherBlocked_writesLowerConfidence` | REQ-002 | One support result and one blocked result write lower confidence. |
| `specification_contradiction_writesNothing` | REQ-003 | A contradicting result writes no specification. |
| `specification_missingSource_writesNothing` | REQ-003 | A missing source or a missing validation result writes no specification. |
| `specification_storedInputsOnly_doesNotResearch` | REQ-004 | The run adds only the specification file. |
| `specification_repeat_writesEqualRecord` | QR-001 | A second run leaves the same specification record. |

---

## Scenarios (Given-When-Then)

### `specification_bothSupport_writesStandardConfidence`

- **Requirements**: REQ-001
- **Given**: `hypotheses.json` has hypothesis `H1` with one research source that has a URL and a title. `validation_results.json` has dataset result support and sandbox result support for `H1`.
- **When**: The specification node runs for `H1`.
- **Then**: `rule_specifications.json` has one record with hypothesis_id `H1`, confidence standard, submitted true, deployed false, that research source, and both validation results.

### `specification_oneSupportOtherInconclusive_writesLowerConfidence`

- **Requirements**: REQ-002
- **Given**: Hypothesis `H1` has a complete research source. The dataset result is support and the sandbox result is inconclusive.
- **When**: The specification node runs for `H1`.
- **Then**: One record is stored with confidence lower and both results.

### `specification_oneSupportOtherBlocked_writesLowerConfidence`

- **Requirements**: REQ-002
- **Given**: Hypothesis `H1` has a complete research source. The dataset result is blocked and the sandbox result is support.
- **When**: The specification node runs for `H1`.
- **Then**: One record is stored with confidence lower and both results.

### `specification_contradiction_writesNothing`

- **Requirements**: REQ-003
- **Given**: Hypothesis `H1` has a complete research source. One validation result is support and the other is contradict.
- **When**: The specification node runs for `H1` in both directions.
- **Then**: `rule_specifications.json` has no record for `H1`.

### `specification_missingSource_writesNothing`

- **Requirements**: REQ-003
- **Given**: Separate cases omit the research source, omit the source URL, omit the source title, or omit the validation record.
- **When**: The specification node runs for each case.
- **Then**: No specification record is written for that hypothesis.

### `specification_storedInputsOnly_doesNotResearch`

- **Requirements**: REQ-004
- **Given**: The directory contains only `hypotheses.json` and `validation_results.json` for a qualifying hypothesis.
- **When**: The specification node runs.
- **Then**: The only added file is `rule_specifications.json`.

### `specification_repeat_writesEqualRecord`

- **Requirements**: QR-001
- **Given**: One qualifying hypothesis and its validation results are stored.
- **When**: The specification node runs twice without changing the inputs.
- **Then**: The two written records are equal, and the file still has one row for that hypothesis.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `specification_bothSupport_writesStandardConfidence` | |
| REQ-002 | `specification_oneSupportOtherInconclusive_writesLowerConfidence`, `specification_oneSupportOtherBlocked_writesLowerConfidence` | |
| REQ-003 | `specification_contradiction_writesNothing`, `specification_missingSource_writesNothing` | |
| REQ-004 | `specification_storedInputsOnly_doesNotResearch` | |
| QR-001 | `specification_repeat_writesEqualRecord` | |
| QR-002 | `ruleSpecificationStore_reopen_returnsWrittenSpecification` | Unit reopen of the same directory. |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 4 | 4 | 0 | 0 |
| QR | 2 | 2 | 0 | 0 |

## Risks and gaps

CA-001: the input files are fixtures of the local contract. This component does not run sibling writers, a shopping agent, or the sandbox.
