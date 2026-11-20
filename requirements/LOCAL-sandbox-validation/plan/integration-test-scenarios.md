# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `evidence_present_writesResultFile` | REQ-001 | A saved evidence file writes the three result fields. |
| `evidence_missing_recordsBlocked` | REQ-002 | A missing evidence file is `blocked` and starts no process. |
| `runs_fourOfFive_support` | REQ-003 | Four positive observations in five runs support the hypothesis. |
| `runs_noneOfFive_contradict` | REQ-004 | Five telemetry-complete runs with no signal contradict the hypothesis. |
| `runs_mixed_inconclusive` | REQ-005 | One positive observation in five runs is inconclusive. |
| `result_file_omitsAbuseAndRule` | REQ-006 | The result file has no abuse label and no deployed rule. |
| `validation_sameEvidence_writesSameResult` | QR-001 | A second run writes the same result bytes. |

---

## Scenarios (Given-When-Then)

### `evidence_present_writesResultFile`

- **Requirements**: REQ-001
- **Given**: A hypothesis file with `hypothesis_id` `H-1` and a saved evidence file with five telemetry-complete runs, four of which observe the signal.
- **When**: `SandboxValidation` runs against those paths.
- **Then**: `sandbox_results.json` contains `hypothesis_id` `H-1`, `result` `support`, and `evidence_path` equal to the supplied evidence path.

### `evidence_missing_recordsBlocked`

- **Requirements**: REQ-002
- **Given**: A hypothesis file and an evidence path that does not exist.
- **When**: `SandboxValidation` runs.
- **Then**: `result` is `blocked`, `evidence_path` is that missing path, and the run starts no process.

### `runs_fourOfFive_support`

- **Requirements**: REQ-003
- **Given**: Saved evidence with five runs, `telemetry_present` true, and four `signal_observed` true values.
- **When**: `SandboxValidation` runs.
- **Then**: `result` is `support`.

### `runs_noneOfFive_contradict`

- **Requirements**: REQ-004
- **Given**: Saved evidence with five telemetry-complete runs and `signal_observed` false on each.
- **When**: `SandboxValidation` runs.
- **Then**: `result` is `contradict`.

### `runs_mixed_inconclusive`

- **Requirements**: REQ-005
- **Given**: Saved evidence with five telemetry-complete runs and one `signal_observed` true value.
- **When**: `SandboxValidation` runs.
- **Then**: `result` is `inconclusive`.

### `result_file_omitsAbuseAndRule`

- **Requirements**: REQ-006
- **Given**: A hypothesis whose text mentions abuse, plus saved supporting evidence.
- **When**: `SandboxValidation` runs.
- **Then**: The result keys are only `hypothesis_id`, `result`, and `evidence_path`, and the output directory contains only `sandbox_results.json`.

### `validation_sameEvidence_writesSameResult`

- **Requirements**: QR-001
- **Given**: One hypothesis file and one saved evidence file.
- **When**: `SandboxValidation` runs twice.
- **Then**: The two `sandbox_results.json` writes are byte-identical.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `evidence_present_writesResultFile` | |
| REQ-002 | `evidence_missing_recordsBlocked` | |
| REQ-003 | `runs_fourOfFive_support` | |
| REQ-004 | `runs_noneOfFive_contradict` | |
| REQ-005 | `runs_mixed_inconclusive` | |
| REQ-006 | `result_file_omitsAbuseAndRule` | |
| QR-001 | `validation_sameEvidence_writesSameResult` | |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 6 | 6 | 0 | 0 |
| QR | 1 | 1 | 0 | 0 |

## Risks and gaps

ASS-002: evidence that does not use `runs`, `telemetry_present`, and `signal_observed` is `blocked`. No separate contract file is part of this package.
