# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `signal_moreCommonInAi_recordsSupport` | REQ-001, QR-001 | A higher AI rate stores support and the class ratios. |
| `signal_moreCommonInHuman_recordsContradict` | REQ-002, QR-001 | A higher human rate stores contradict and the class ratios. |
| `dataset_equalRates_recordsInconclusive` | REQ-003 | Equal class rates store inconclusive. |
| `dataset_missingClass_recordsInconclusive` | REQ-003 | A fixture that lacks a class stores inconclusive. |
| `dataset_missingFile_recordsBlocked` | REQ-004 | A missing dataset file stores blocked. |
| `assignment_outOfScopeAction_storesNothing` | REQ-005 | Discovery, launch, rule writing, and abuse classification store nothing. |
| `input_notOrchestratorAssignment_storesNothing` | REQ-006 | A chat payload stores nothing. |
| `record_persisted_hasExactlyFiveJsonFields` | REQ-007 | The stored object has the five JSON fields and no others. |
| `store_reopen_readsWrittenResults` | QR-002 | A new store instance reads the written result. |

---

## Scenarios (Given-When-Then)

### `signal_moreCommonInAi_recordsSupport`

- **Requirements**: REQ-001, QR-001
- **Given**: An orchestrator assignment names hypothesis `h-support` and signal `webgl_software_renderer`. The fixture `labelled-sessions` has two AI rows with the signal true and two human rows with the signal false.
- **When**: The dataset validation graph runs the assignment.
- **Then**: `dataset_results.json` contains one record with result support, prevalence 1.0, and false_positive_rate 0.0.

### `signal_moreCommonInHuman_recordsContradict`

- **Requirements**: REQ-002, QR-001
- **Given**: An orchestrator assignment names hypothesis `h-contradict` and the same signal. Both AI rows have the signal false and both human rows have the signal true.
- **When**: The dataset validation graph runs the assignment.
- **Then**: The record result is contradict, prevalence is 0.0, and false_positive_rate is 1.0.

### `dataset_equalRates_recordsInconclusive`

- **Requirements**: REQ-003
- **Given**: An orchestrator assignment names hypothesis `h-equal`. One of two AI rows and one of two human rows have the signal true.
- **When**: The dataset validation graph runs the assignment.
- **Then**: The record result is inconclusive, and prevalence and false_positive_rate are both 0.5.

### `dataset_missingClass_recordsInconclusive`

- **Requirements**: REQ-003
- **Given**: An orchestrator assignment names hypothesis `h-one-class`. The fixture file exists and every row is labelled AI.
- **When**: The dataset validation graph runs the assignment.
- **Then**: The record result is inconclusive, and prevalence and false_positive_rate are null.

### `dataset_missingFile_recordsBlocked`

- **Requirements**: REQ-004
- **Given**: An orchestrator assignment names hypothesis `h-missing` and a dataset path that is not a file.
- **When**: The dataset validation graph runs the assignment.
- **Then**: The record result is blocked, and prevalence and false_positive_rate are null.

### `assignment_outOfScopeAction_storesNothing`

- **Requirements**: REQ-005
- **Given**: Four orchestrator-shaped payloads ask to discover a dataset, launch a shopping agent, write a rule, or classify abuse.
- **When**: The dataset validation graph runs each payload.
- **Then**: No dataset result is stored and no shopping-agent process is started.

### `input_notOrchestratorAssignment_storesNothing`

- **Requirements**: REQ-006
- **Given**: A chat payload has a message and no orchestrator source.
- **When**: The dataset validation graph runs the payload.
- **Then**: `dataset_results.json` is not created.

### `record_persisted_hasExactlyFiveJsonFields`

- **Requirements**: REQ-007
- **Given**: An orchestrator assignment that meets the support fixture.
- **When**: The dataset validation graph runs the assignment.
- **Then**: The stored object keys are `hypothesis_id`, `result`, `prevalence`, `false_positive_rate`, and `dataset_name`.

### `store_reopen_readsWrittenResults`

- **Requirements**: QR-002
- **Given**: One result has been written to `dataset_results.json`.
- **When**: A new store instance opens that path.
- **Then**: The new instance returns the same record.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `signal_moreCommonInAi_recordsSupport` | |
| REQ-002 | `signal_moreCommonInHuman_recordsContradict` | |
| REQ-003 | `dataset_equalRates_recordsInconclusive`, `dataset_missingClass_recordsInconclusive` | |
| REQ-004 | `dataset_missingFile_recordsBlocked` | |
| REQ-005 | `assignment_outOfScopeAction_storesNothing` | |
| REQ-006 | `input_notOrchestratorAssignment_storesNothing` | |
| REQ-007 | `record_persisted_hasExactlyFiveJsonFields` | |
| QR-001 | `signal_moreCommonInAi_recordsSupport`, `signal_moreCommonInHuman_recordsContradict` | |
| QR-002 | `store_reopen_readsWrittenResults` | |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 7 | 7 | 0 | 0 |
| QR | 2 | 2 | 0 | 0 |

## Risks and gaps

ASS-002 is the comparison rule behind support, contradict, and inconclusive. The scenarios use strict inequality and treat equal rates as inconclusive. No contract file is provided.
