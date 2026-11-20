# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-research-orchestrator |
| **Requirements base path** | requirements/LOCAL-research-orchestrator/ |
| **Plan base path** | requirements/LOCAL-research-orchestrator/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | New repo |
| **Architecture style** | One LangGraph node that writes JSON assignment and stage-decision records |
| **Architecture source** | User-provided |
| **Architecture confidence** | High |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | CA-001. CA-002. |

### Analyst planning anchors

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-001 | critical | yes | Human input must become an agent-intelligence assignment and must not be researched here. | Step 3 | `human_namedAssistant_storesAssignment` |
| REQ-003 | critical | yes | Waiting hypotheses must be assigned to both validators. | Step 3 | `standup_waitingHypothesis_assignsBothValidators` |
| REQ-004 | critical | yes | One supporting result can request a rule specification only with lower confidence. | Step 2 | `standup_oneSupport_requestsLowerConfidenceSpec` |
| REQ-007 | critical | yes | The outcome is a submitted specification, not a deployed rule. | Step 3 | `standup_eligibleHypothesis_storesSpecNotDeployedRule` |
| INV-001 | critical | yes | Only the orchestrator may change workflow stage. | Step 3 | `researchOrchestrator_stageChange_namesOrchestrator` |
| POL-003 | high | no | Contradictions and exhausted rework must stop for a human. | Step 2 | `stageDecision_contradiction_suspends` |
| REQ-008 | high | no | Rework must be finite. | Step 2 | `rework_atLimit_suspendsTask` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | not found | New Python modules use `research_orchestrator`. Tests use `subject_condition_expectedOutcome` and `className_condition_expectedBehavior`. |
| Existing modules | `requirements/LOCAL-agent-intelligence/plan/plan.md` | JSON research records stay file records. This package does not import `agent_intelligence` to perform research. |
| Existing tests | not applicable | No product tests exist yet. |
| Contracts / schemas | requirements/LOCAL-research-orchestrator/ | An assignment names the target role and the subject. A stage decision names the trigger and the decision. |

---

## Step 0 — Integration tests

- [Integration test scenarios](./integration-test-scenarios.md)
- `integration-test-scenarios.md` is the single source of truth for Step 0 scenarios and `REQ-NNN` / `QR-NNN` coverage.

### Definition of Done

- [ ] Integration test scenarios covering every `REQ-NNN` are specified and corresponding test code is implemented
- [ ] Every `QR-NNN` has a specified integration test or manual validation with a path to automation
- [ ] Step 0 tests are runnable and may fail only because the planned production behavior is not implemented yet
- [ ] Acceptance coverage matrix in `integration-test-scenarios.md` shows zero uncovered items and matches the planned verification

---

## Step 1 — Orchestrator package boundary

### Structure map

| Architectural unit | Responsibility | Allowed dependencies |
|--------------------|----------------|----------------------|
| `research_orchestrator` | Human assignment, standup routing, and stage decisions | LangGraph, the local JSON store, saved evaluator results |
| `agent_intelligence` | Research and discovery | Not imported for research. This package only writes an assignment record. |
| Validator and rule packages | Dataset validation, sandbox execution, and rule text | Not imported. Their outputs are saved records. |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `research_orchestrator_mustNotDependOn_researchOrValidators` | `research_orchestrator` must not import agent-intelligence research, dataset validation, sandbox execution, or rule submission |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Stage decision

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `StageDecision` | Apply PASS, REWORK, ESCALATE, and STOP from the evaluator result, validation pair, and rework count | INV-002, POL-001, POL-002, POL-003, POL-004 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-002 | `StageDecision` | Reject a decision record that lacks a trigger or a decision |
| POL-001 | `StageDecision` | PASS plus passed checks advances one stage |
| POL-002 | `StageDecision` | A correctable failure under the configured limit returns the task to the responsible agent |
| POL-003 | `StageDecision` | A contradiction, a high-risk finding, or a rework count at the limit suspends the task |
| POL-004 | `StageDecision` | Impossible verification or a security violation terminates the task and blocks later assignments |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `stageDecision_missingTrigger_rejected` | `StageDecision` | A decision without a trigger is rejected |
| `stageDecision_pass_advancesOneStage` | `StageDecision` | PASS advances exactly one stage |
| `stageDecision_reworkUnderLimit_returnsTask` | `StageDecision` | Rework count 1 with limit 2 returns the task |
| `stageDecision_contradiction_suspends` | `StageDecision` | A contradiction suspends the task and creates no validator assignment |
| `stageDecision_securityViolation_terminates` | `StageDecision` | A security violation terminates the task |
| `stageDecision_oneSupport_marksLowerConfidence` | `StageDecision` | One support and one non-contradicting inconclusive result request a lower-confidence specification |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Research orchestrator node

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `ResearchOrchestrator` | Accept a human assistant name, run one standup, write both validator assignments, and refuse a deployed rule | INV-001, INV-003 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `ResearchOrchestrator` | Stage records written by this class name the orchestrator as the only writer |
| INV-003 | `ResearchOrchestrator` | A finished eligible standup stores a submitted specification and no deployed rule |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `researchOrchestrator_stageChange_namesOrchestrator` | `ResearchOrchestrator` | A stage record names the orchestrator |
| `researchOrchestrator_namedAssistant_writesAssignmentOnly` | `ResearchOrchestrator` | A human name writes one assignment and no hypothesis |
| `researchOrchestrator_abuseRequest_writesNothing` | `ResearchOrchestrator` | An abuse-only request writes no assignment |
| `researchOrchestrator_waitingHypothesis_writesBothAssignments` | `ResearchOrchestrator` | One waiting hypothesis writes dataset and sandbox assignments and starts no shopping agent |
| `researchOrchestrator_eligibleResult_writesNoDeployedRule` | `ResearchOrchestrator` | An eligible result stores a specification and no deployed rule |
| `researchOrchestrator_missingEvaluator_doesNotAdvance` | `ResearchOrchestrator` | A missing evaluator result leaves the stage unchanged |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 4 — JSON assignment store

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `OrchestratorStore` | Read and write assignments, stage decisions, and submitted specifications as JSON files | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `OrchestratorStore` | This class stores records. `StageDecision` decides which transition is legal. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `orchestratorStore_reopen_returnsDecisionsWithTriggers` | `OrchestratorStore` | PASS, REWORK, ESCALATE, and STOP written by one instance are readable from a new instance with their triggers |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 5 — Standup schedule

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `StandupSchedule` | Decide whether a standup is due from the configured interval and the previous standup time | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `StandupSchedule` | The schedule decides timing. `ResearchOrchestrator` writes the assignments. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `standupSchedule_defaultInterval_notDueAt23Hours` | `StandupSchedule` | The default 24-hour interval is not due at 23 hours |
| `standupSchedule_defaultInterval_dueAt24Hours` | `StandupSchedule` | The default interval is due at 24 hours |
| `standupSchedule_oneHour_dueAtOneHour` | `StandupSchedule` | A 1-hour interval is due at 1 hour |
| `standupSchedule_oneHour_notDueAt59Minutes` | `StandupSchedule` | A 1-hour interval is not due at 59 minutes |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Final acceptance

### Build and static analysis

- [ ] Project compiles without errors
- [ ] No linter or static analysis errors introduced

### Test suite

- [ ] All structural boundary tests pass
- [ ] All unit tests pass (including invariant and policy encapsulation tests)
- [ ] All integration tests pass (all scenarios in `integration-test-scenarios.md`)

### Traceability

- [ ] All items in the Coverage sign-off below are green
- [ ] Every active `DD-NNN` in `design-decisions.md` is reflected in the affected implementation steps

---

## Coverage sign-off

| ID type | ID | Verification |
|---------|-----|--------------|
| Functional | REQ-001 | Integration: `human_namedAssistant_storesAssignment` |
| Functional | REQ-002 | Integration: `human_abuseRequest_storesNoAssignment` |
| Functional | REQ-003 | Integration: `standup_waitingHypothesis_assignsBothValidators`, `standup_beforeInterval_assignsNothing` |
| Functional | REQ-004 | Integration: `standup_oneSupport_requestsLowerConfidenceSpec` |
| Functional | REQ-005 | Integration: `standup_contradiction_returnsInvestigation` |
| Functional | REQ-006 | Integration: `evaluator_missingResult_doesNotAdvance`, `evaluator_pass_advancesOnce` |
| Functional | REQ-007 | Integration: `standup_eligibleHypothesis_storesSpecNotDeployedRule` |
| Functional | REQ-008 | Integration: `rework_atLimit_suspendsTask` |
| Quality | QR-001 | Integration: `standup_waitingHypothesis_assignsBothValidators` |
| Quality | QR-002 | Integration: `decisions_afterRestart_includeTrigger` |
| Invariant | INV-001 | Unit: `researchOrchestrator_stageChange_namesOrchestrator` on `ResearchOrchestrator` |
| Invariant | INV-002 | Unit: `stageDecision_missingTrigger_rejected` on `StageDecision` |
| Invariant | INV-003 | Unit: `researchOrchestrator_eligibleResult_writesNoDeployedRule` on `ResearchOrchestrator` |
| Policy | POL-001 | Unit: `stageDecision_pass_advancesOneStage` on `StageDecision` |
| Policy | POL-002 | Unit: `stageDecision_reworkUnderLimit_returnsTask` on `StageDecision` |
| Policy | POL-003 | Unit: `stageDecision_contradiction_suspends` on `StageDecision` |
| Policy | POL-004 | Unit: `stageDecision_securityViolation_terminates` on `StageDecision` |

### Sign-off checklist

- [ ] Every `REQ-NNN` → integration test(s)
- [ ] Every `INV-NNN` → unit test(s) on encapsulating class
- [ ] Every `POL-NNN` → unit test(s) on encapsulating class
- [ ] Every `QR-NNN` → integration test(s) or manual validation note
- [ ] No invariant or policy split across multiple classes
- [ ] Every `minimumAcceptedScope` ID is mapped to a plan step and verification
- [ ] Every `critical` priority item is mapped to a plan step and verification
- [ ] All mapped verifications are implemented and passing

---

## Coding agent handoff

- **Automatic start**: no
- **Acknowledgement reason**: The standup interval and rework limit defaults are planning choices, and the validators and rule specification are outside this ticket.
- **Handoff artifact**: `requirements/LOCAL-research-orchestrator/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-research-orchestrator/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-research-orchestrator/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- CA-001: dataset validation, sandbox validation, and rule specification are outside this ticket. Assignments are stored records. This plan does not implement those agents or start a shopping agent.
- CA-002: the standup interval defaults to 24 hours and the rework limit defaults to 2. Both are configuration, and tests set them explicitly.
