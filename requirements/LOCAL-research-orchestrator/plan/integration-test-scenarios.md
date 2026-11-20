# Integration Test Scenarios

End-to-end scenarios that verify functional and quality requirements. Each scenario must link to at least one `REQ-NNN` or `QR-NNN`.

Keep Step 0 coverage in this file. Do not create separate coverage, summary, or overview markdown files for the same requirement mappings.

---

## Summary table

| Test name | Requirements | Scenario |
|-----------|--------------|----------|
| `human_namedAssistant_storesAssignment` | REQ-001 | A human assistant name becomes one agent-intelligence assignment and no hypothesis. |
| `human_abuseRequest_storesNoAssignment` | REQ-002 | An abuse-classification request creates no assignment. |
| `standup_waitingHypothesis_assignsBothValidators` | REQ-003, QR-001 | A due standup assigns one waiting hypothesis to both validators, and a repeat writes the same records. |
| `standup_beforeInterval_assignsNothing` | REQ-003 | A standup before the interval writes no validator assignments. |
| `standup_oneSupport_requestsLowerConfidenceSpec` | REQ-004 | One supporting result and one inconclusive result request a lower-confidence specification. |
| `standup_contradiction_returnsInvestigation` | REQ-005 | Contradicting results return the hypothesis and request no specification. |
| `evaluator_missingResult_doesNotAdvance` | REQ-006 | A missing evaluator result leaves the stage unchanged. |
| `evaluator_pass_advancesOnce` | REQ-006 | A PASS result advances the stage once. |
| `standup_eligibleHypothesis_storesSpecNotDeployedRule` | REQ-007 | An eligible result stores a submitted specification and no deployed rule. |
| `rework_atLimit_suspendsTask` | REQ-008 | The next correctable failure at the configured limit suspends the task. |
| `decisions_afterRestart_includeTrigger` | QR-002 | PASS, REWORK, ESCALATE, and STOP remain readable with their triggers after the process exits. |

---

## Scenarios (Given-When-Then)

### `human_namedAssistant_storesAssignment`

- **Requirements**: REQ-001
- **Given**: No assignment exists for assistant "Muse".
- **When**: A human submits the name "Muse".
- **Then**: One assignment for agent intelligence contains "Muse". The orchestrator stores no hypothesis and no retrieved source.

### `human_abuseRequest_storesNoAssignment`

- **Requirements**: REQ-002
- **Given**: The assignment store has a known count.
- **When**: A human asks only to distinguish an abusive agent from a legitimate agent.
- **Then**: The assignment count is unchanged.

### `standup_waitingHypothesis_assignsBothValidators`

- **Requirements**: REQ-003, QR-001
- **Given**: The standup interval is 1 hour and has elapsed. One hypothesis is awaiting validation. No validation reports exist.
- **When**: The standup runs twice without changing the store.
- **Then**: Both runs write one dataset-validation assignment and one sandbox-validation assignment for that hypothesis, and the two runs write the same records. Neither run starts a shopping agent.

### `standup_beforeInterval_assignsNothing`

- **Requirements**: REQ-003
- **Given**: The standup interval is 1 hour. The previous standup was 59 minutes ago. One hypothesis is awaiting validation.
- **When**: The scheduler is checked.
- **Then**: No dataset-validation assignment and no sandbox-validation assignment are written.

### `standup_oneSupport_requestsLowerConfidenceSpec`

- **Requirements**: REQ-004
- **Given**: Dataset validation supports a hypothesis. Sandbox validation is inconclusive and does not contradict it. The evaluator result is PASS.
- **When**: The standup reviews that hypothesis.
- **Then**: One rule-specification request is stored and its evidence confidence is lower.

### `standup_contradiction_returnsInvestigation`

- **Requirements**: REQ-005
- **Given**: Dataset validation supports a hypothesis and sandbox validation contradicts it.
- **When**: The standup reviews that hypothesis.
- **Then**: One investigation return is stored. The rule-specification request count is unchanged.

### `evaluator_missingResult_doesNotAdvance`

- **Requirements**: REQ-006
- **Given**: A task has passed its stage checks and has no independent evaluator result.
- **When**: The orchestrator considers advancing it.
- **Then**: The task stage is unchanged.

### `evaluator_pass_advancesOnce`

- **Requirements**: REQ-006
- **Given**: A task has passed its stage checks and the independent evaluator result is PASS.
- **When**: The orchestrator considers advancing it.
- **Then**: The task advances one stage.

### `standup_eligibleHypothesis_storesSpecNotDeployedRule`

- **Requirements**: REQ-007
- **Given**: A hypothesis is eligible for a rule specification and the specification text is available.
- **When**: The standup completes that request.
- **Then**: A submitted specification is stored for human review. No deployed-rule record exists.

### `rework_atLimit_suspendsTask`

- **Requirements**: REQ-008
- **Given**: The rework limit is 2. A task already has two REWORK returns. A new correctable validation failure arrives.
- **When**: The orchestrator handles that failure.
- **Then**: The task is suspended for human review and is not assigned again.

### `decisions_afterRestart_includeTrigger`

- **Requirements**: QR-002
- **Given**: One standup has stored one PASS, one REWORK, one ESCALATE, and one STOP, each with a trigger, and that process has exited.
- **When**: A new process opens the store.
- **Then**: All four records are readable and each contains its trigger and its decision.

---

## Acceptance coverage matrix

| ID | Covered by | Notes |
|----|------------|-------|
| REQ-001 | `human_namedAssistant_storesAssignment` | |
| REQ-002 | `human_abuseRequest_storesNoAssignment` | |
| REQ-003 | `standup_waitingHypothesis_assignsBothValidators`, `standup_beforeInterval_assignsNothing` | Due and not due |
| REQ-004 | `standup_oneSupport_requestsLowerConfidenceSpec` | |
| REQ-005 | `standup_contradiction_returnsInvestigation` | |
| REQ-006 | `evaluator_missingResult_doesNotAdvance`, `evaluator_pass_advancesOnce` | |
| REQ-007 | `standup_eligibleHypothesis_storesSpecNotDeployedRule` | |
| REQ-008 | `rework_atLimit_suspendsTask` | |
| QR-001 | `standup_waitingHypothesis_assignsBothValidators` | Two identical runs |
| QR-002 | `decisions_afterRestart_includeTrigger` | |

### Coverage summary

| Type | Total | Covered by IT | Manual validation | Uncovered |
|------|-------|---------------|-------------------|-----------|
| REQ | 8 | 8 | 0 | 0 |
| QR | 2 | 2 | 0 | 0 |

## Risks and gaps

Dataset validation, sandbox validation, and rule specification are represented by saved records. This ticket does not execute those agents. The sandbox assignment does not start a shopping agent.
