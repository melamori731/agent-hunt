# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

Keep Step 0 coverage in this file. Do not create separate coverage, summary, or overview markdown files for the same requirement mappings.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `hypothesis_withSources_writesPass` | REQ-001 | A hypothesis with one source writes PASS for stage hypothesis. |
| `hypothesis_missingSources_writesRework` | REQ-002 | A missing hypothesis and an empty source list write REWORK and leave the stage file unchanged. |
| `validation_consistentPair_writesPass` | REQ-003 | Support with support, and support with inconclusive, write PASS for stage validation. |
| `validation_contradictionOrMissing_writesRework` | REQ-004 | A missing sandbox result and a support-versus-reject pair write REWORK and leave the stage file unchanged. |
| `rule_submittedWithCitations_writesPass` | REQ-005 | A submitted, non-deployed specification that cites sources and validation results writes PASS. |
| `rule_notEligible_writesRework` | REQ-006 | A missing, unsubmitted, deployed, or uncited specification writes REWORK and leaves the stage file unchanged. |
| `evaluator_sideEffects_writesOnlyEvaluation` | REQ-007 | A check writes only the four evaluation fields and does not launch a process, write a message, or write a faculty report. |
| `evaluation_afterRestart_remainsReadable` | QR-001 | A new reader returns the same evaluation after the writer is discarded. |
| `evaluation_repeat_sameResult` | QR-002 | The same unchanged records produce the same result and trigger on a second check. |

---

## Scenarios (Given-When-Then)

### `hypothesis_withSources_writesPass`

- **Requirements**: REQ-001
- **Given**: hypotheses.json contains one hypothesis id with one non-empty source.
- **When**: The evaluator checks stage hypothesis for that id.
- **Then**: evaluations.json contains hypothesis_id, stage hypothesis, result PASS, and a trigger that states sources are present.

### `hypothesis_missingSources_writesRework`

- **Requirements**: REQ-002
- **Given**: One directory has a hypothesis with an empty source list. Another has no hypothesis record. Both contain a workflow stage file.
- **When**: The evaluator checks stage hypothesis in each directory.
- **Then**: Both evaluations are REWORK and each stage file is byte-for-byte unchanged.

### `validation_consistentPair_writesPass`

- **Requirements**: REQ-003
- **Given**: One directory has dataset support and sandbox support. Another has dataset support and sandbox inconclusive.
- **When**: The evaluator checks stage validation in each directory.
- **Then**: Both evaluations are PASS.

### `validation_contradictionOrMissing_writesRework`

- **Requirements**: REQ-004
- **Given**: One directory has dataset support and no sandbox result. Another has dataset support and sandbox reject. Both contain a workflow stage file.
- **When**: The evaluator checks stage validation in each directory.
- **Then**: Both evaluations are REWORK and each stage file is byte-for-byte unchanged.

### `rule_submittedWithCitations_writesPass`

- **Requirements**: REQ-005
- **Given**: rule_specifications.json has one specification that is submitted, is not deployed, and cites one research source and one validation result.
- **When**: The evaluator checks stage rule_specification.
- **Then**: The evaluation result is PASS.

### `rule_notEligible_writesRework`

- **Requirements**: REQ-006
- **Given**: Five directories, one for each defect: missing specification, submitted false, deployed true, empty research sources, and empty validation results. Each contains a workflow stage file.
- **When**: The evaluator checks stage rule_specification in each directory.
- **Then**: Each evaluation is REWORK and each stage file is byte-for-byte unchanged.

### `evaluator_sideEffects_writesOnlyEvaluation`

- **Requirements**: REQ-007
- **Given**: A sourced hypothesis is stored. Process launch and message writing are observable.
- **When**: The evaluator checks stage hypothesis.
- **Then**: The evaluation contains only hypothesis_id, stage, result, and trigger. No process starts, no agent message file appears, and no faculty report appears.

### `evaluation_afterRestart_remainsReadable`

- **Requirements**: QR-001
- **Given**: One PASS evaluation has been written and the writer object has been discarded.
- **When**: A new evaluator reads the same directory.
- **Then**: The stored hypothesis_id, stage, result, and trigger match the written evaluation.

### `evaluation_repeat_sameResult`

- **Requirements**: QR-002
- **Given**: One sourced hypothesis is stored.
- **When**: The evaluator checks stage hypothesis twice without changing the hypothesis file.
- **Then**: The two appended evaluations have the same result and the same trigger.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `hypothesis_withSources_writesPass` | |
| REQ-002 | `hypothesis_missingSources_writesRework` | |
| REQ-003 | `validation_consistentPair_writesPass` | |
| REQ-004 | `validation_contradictionOrMissing_writesRework` | |
| REQ-005 | `rule_submittedWithCitations_writesPass` | |
| REQ-006 | `rule_notEligible_writesRework` | |
| REQ-007 | `evaluator_sideEffects_writesOnlyEvaluation` | |
| QR-001 | `evaluation_afterRestart_remainsReadable` | |
| QR-002 | `evaluation_repeat_sameResult` | |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 7 | 7 | 0 | 0 |
| QR | 2 | 2 | 0 | 0 |

## Risks and gaps

ASS-002 remains a delivery risk: these scenarios use the local file names. They do not import sibling packages. No contract file is provided.
