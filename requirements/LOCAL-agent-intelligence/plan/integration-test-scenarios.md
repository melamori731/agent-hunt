# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

Keep Step 0 coverage in this file. Do not create separate coverage, summary, or overview markdown files for the same requirement mappings.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `assignment_namedAssistant_storesSourcedEntry` | REQ-001, QR-001 | An orchestrator assignment creates one sourced registry entry and no direct human entry point is used. |
| `discovery_unknownAssistant_addsOneEntryAndReport` | REQ-002, REQ-003 | A scheduled run adds one new assistant and one report that names scheduled discovery as the origin. |
| `assignment_namedAssistant_reportNamesOrchestratorOrigin` | REQ-003 | The report for an assigned assistant names the orchestrator origin. |
| `hypothesis_completeSignal_storesRequiredFields` | REQ-004, QR-001 | A complete shopping-session signal is stored with sources that have a URL and a title. |
| `hypothesis_abusePurpose_storesNothing` | REQ-005 | An abuse-classification request stores no hypothesis. |
| `hypothesis_sameSignal_doesNotDuplicate` | REQ-006 | Repeating an assistant and signal leaves one hypothesis. |
| `hypothesis_weakSources_storesUnresolvedOnly` | REQ-007 | Sources without a testable signal store an unresolved investigation and no hypothesis. |
| `system_completeRecords_specificationPasses` | REQ-008, QR-003 | The system path from orchestrator input to a submitted specification passes when sources and validation results are present, and a second identical run has the same result. |
| `system_missingValidationResults_specificationFails` | REQ-008 | The same path fails when validation results are removed. |
| `discovery_knownAssistant_storesNewPattern` | REQ-009 | A scheduled run stores one new pattern outcome for an assistant already in the registry. |
| `discovery_defaultInterval_startsAt24Hours` | REQ-010 | The default interval does not start a run at 23 hours and does start one at 24 hours. |
| `discovery_oneHourInterval_startsAtOneHour` | REQ-010 | An interval set to 1 hour starts a run after 1 hour. |
| `store_processRestart_recordsRemain` | QR-002 | Registry, report, hypothesis, and unresolved records are readable after the writing process ends. |

---

## Scenarios (Given-When-Then)

### `assignment_namedAssistant_storesSourcedEntry`

- **Requirements**: REQ-001, QR-001
- **Given**: An orchestrator assignment names one assistant, and a fixture page for that assistant has a URL and a title. No registry entry exists. The agent has no human-request function.
- **When**: The agent runs the assignment.
- **Then**: One registry entry exists and cites that URL and title. No call path accepts the human text except the orchestrator assignment record.
- **Notes**: The fixture page stands in for web retrieval.

### `discovery_unknownAssistant_addsOneEntryAndReport`

- **Requirements**: REQ-002, REQ-003
- **Given**: The registry is empty. A fixture source describes one assistant that is not registered. The discovery interval has elapsed.
- **When**: The scheduled discovery run executes.
- **Then**: Exactly one registry entry exists for that assistant, and exactly one report names the assistant, lists the source, and states scheduled discovery as the origin.

### `assignment_namedAssistant_reportNamesOrchestratorOrigin`

- **Requirements**: REQ-003
- **Given**: An orchestrator assignment names one assistant and a fixture source exists.
- **When**: The agent runs the assignment.
- **Then**: Exactly one report names the assistant, lists the source, and states orchestrator assignment as the origin.

### `hypothesis_completeSignal_storesRequiredFields`

- **Requirements**: REQ-004, QR-001
- **Given**: Sources with a URL and a title describe one observable shopping-session signal, the expected observation, and the measurements validation must perform.
- **When**: The agent finishes that investigation.
- **Then**: One hypothesis stores the signal, the observation, those sources, and the measurements. A record missing any of those four fields is rejected.

### `hypothesis_abusePurpose_storesNothing`

- **Requirements**: REQ-005
- **Given**: The only requested outcome is to classify an assistant as abusive or legitimate.
- **When**: The agent finishes that investigation.
- **Then**: The hypothesis count is unchanged.

### `hypothesis_sameSignal_doesNotDuplicate`

- **Requirements**: REQ-006
- **Given**: One hypothesis is already stored for an assistant and a signal.
- **When**: The same assistant and signal are investigated again.
- **Then**: The store still contains one hypothesis for that pair.

### `hypothesis_weakSources_storesUnresolvedOnly`

- **Requirements**: REQ-007
- **Given**: The only sources do not describe a testable shopping-session signal.
- **When**: The agent finishes that investigation.
- **Then**: One unresolved investigation is stored and the hypothesis count is unchanged.

### `system_completeRecords_specificationPasses`

- **Requirements**: REQ-008, QR-003
- **Given**: Human input is stored as an orchestrator assignment. Research records, a saved virtual-machine evidence file, dataset results, evaluator results, and a submitted rule specification all contain the research sources and the validation results. No shopping-agent process is available to the test.
- **When**: The system test runs twice without changing those records.
- **Then**: Both runs pass. The inspected specification contains the research sources and the validation results. The test starts no shopping-agent process.

### `system_missingValidationResults_specificationFails`

- **Requirements**: REQ-008
- **Given**: The same records as the passing system test, except the submitted specification has no validation results.
- **When**: The system test runs.
- **Then**: The run fails.

### `discovery_knownAssistant_storesNewPattern`

- **Requirements**: REQ-009
- **Given**: One assistant is in the registry and has no hypothesis. A fixture source describes a new shopping-session signal for that assistant. The discovery interval has elapsed.
- **When**: The scheduled discovery run executes.
- **Then**: One hypothesis or one unresolved investigation is stored for that assistant, and no second hypothesis is stored for a signal that was already present.

### `discovery_defaultInterval_startsAt24Hours`

- **Requirements**: REQ-010
- **Given**: The interval is the default 24 hours. The previous scheduled run completed at time T.
- **When**: The clock is T plus 23 hours, then T plus 24 hours.
- **Then**: No scheduled run starts at T plus 23 hours. One scheduled run starts at T plus 24 hours.

### `discovery_oneHourInterval_startsAtOneHour`

- **Requirements**: REQ-010
- **Given**: The configured interval is 1 hour. The previous scheduled run completed at time T.
- **When**: The clock is T plus 1 hour.
- **Then**: One scheduled run starts.

### `store_processRestart_recordsRemain`

- **Requirements**: QR-002
- **Given**: One run has written one registry entry, one report, one hypothesis, and one unresolved investigation, and that process has exited.
- **When**: A new process opens the JSON store.
- **Then**: All four records are readable and match what the first run wrote.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `assignment_namedAssistant_storesSourcedEntry` | |
| REQ-002 | `discovery_unknownAssistant_addsOneEntryAndReport` | |
| REQ-003 | `discovery_unknownAssistant_addsOneEntryAndReport`, `assignment_namedAssistant_reportNamesOrchestratorOrigin` | Both origins |
| REQ-004 | `hypothesis_completeSignal_storesRequiredFields` | |
| REQ-005 | `hypothesis_abusePurpose_storesNothing` | |
| REQ-006 | `hypothesis_sameSignal_doesNotDuplicate` | |
| REQ-007 | `hypothesis_weakSources_storesUnresolvedOnly` | |
| REQ-008 | `system_completeRecords_specificationPasses`, `system_missingValidationResults_specificationFails` | |
| REQ-009 | `discovery_knownAssistant_storesNewPattern` | |
| REQ-010 | `discovery_defaultInterval_startsAt24Hours`, `discovery_oneHourInterval_startsAtOneHour` | |
| QR-001 | `assignment_namedAssistant_storesSourcedEntry`, `hypothesis_completeSignal_storesRequiredFields` | URL and title |
| QR-002 | `store_processRestart_recordsRemain` | |
| QR-003 | `system_completeRecords_specificationPasses` | Two identical runs |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 10 | 10 | 0 | 0 |
| QR | 3 | 3 | 0 | 0 |

## Risks and gaps

Downstream dataset, sandbox, evaluator, and rule-specification behavior is supplied as saved records in `system_completeRecords_specificationPasses`. Those records are fixtures for this ticket. They do not prove the other agents produce them. The virtual-machine file is a saved manual run, not a live assistant launch.
