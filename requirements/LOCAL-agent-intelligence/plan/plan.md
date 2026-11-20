# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-agent-intelligence |
| **Requirements base path** | requirements/LOCAL-agent-intelligence/ |
| **Plan base path** | requirements/LOCAL-agent-intelligence/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | New repo |
| **Architecture style** | One LangGraph node using a LangChain ReAct loop and LangChain tools, with JSON files as the research record store |
| **Architecture source** | User-provided |
| **Architecture confidence** | High |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | CA-001. Manual sandbox evidence depends on a person running the assistant on the virtual machine. |

### Analyst planning anchors

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-001 | critical | yes | A human-named assistant reaches this agent only as an orchestrator assignment and must become a sourced registry entry. | Step 5 | `assignment_namedAssistant_storesSourcedEntry` |
| REQ-003 | critical | yes | Adding an assistant must be visible to a human. | Step 2 | `discovery_unknownAssistant_addsOneEntryAndReport` |
| REQ-004 | critical | yes | A hypothesis without a signal, observation, sources, and measurements cannot be validated. | Step 3 | `hypothesis_completeSignal_storesRequiredFields` |
| REQ-008 | critical | yes | The system test is the acceptance check from research through a submitted rule specification. | Step 7 | `system_completeRecords_specificationPasses` |
| REQ-010 | critical | yes | Discovery of new assistants and new patterns runs on a configured cadence that defaults to 24 hours. | Step 6 | `discovery_defaultInterval_startsAt24Hours` |
| INV-001 | critical | yes | A hypothesis with no source must not enter the pipeline. | Step 3 | `hypothesisRecord_emptySources_rejected` |
| POL-001 | high | no | Weak sources must stop as an unresolved investigation. | Step 3 | `hypothesisRecord_weakSources_storesUnresolvedOnly` |
| POL-004 | high | no | The end-to-end test must not start a shopping agent. | Step 7 | `systemEndToEndTest_run_startsNoShoppingAgent` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | not found | No existing package layout. New Python modules use `agent_intelligence` and snake_case tests. |
| Existing modules | not applicable | Greenfield. No product modules to extend. |
| Existing tests | not applicable | Tests follow `subject_condition_expectedOutcome` and `className_condition_expectedBehavior`. |
| Contracts / schemas | requirements/LOCAL-agent-intelligence/ | Registry, report, hypothesis, and unresolved records are JSON documents with the fields named in the requirements. |

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

## Step 1 — LangGraph node boundary

### Structure map

| Architectural unit | Responsibility | Allowed dependencies |
|--------------------|----------------|----------------------|
| `agent_intelligence` | Research loop, registry, hypotheses, schedule, and JSON store | LangChain tools, LangGraph, the local JSON store |
| Orchestrator assignment record | Input that names an assistant | Produced outside this package |
| Downstream stage packages | Dataset validation, sandbox execution, evaluation, and rule submission | Not imported by `agent_intelligence` |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `agent_intelligence_mustNotDependOn_downstreamStages` | `agent_intelligence` must not import dataset validation, sandbox execution, independent evaluation, or rule submission |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Agent registry and addition report

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `AgentRegistry` | Store one assistant entry and exactly one addition report | INV-003, POL-003 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-003 | `AgentRegistry` | Reject an addition that does not create exactly one report |
| POL-003 | `AgentRegistry` | Require assistant name, sources, and origin on both orchestrator-assigned and scheduled-discovery reports |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `agentRegistry_addition_createsOneReport` | `AgentRegistry` | One addition yields one report |
| `agentRegistry_secondReport_rejected` | `AgentRegistry` | A second report for the same addition is rejected |
| `agentRegistry_eitherOrigin_requiresNameSourcesAndOrigin` | `AgentRegistry` | Both origins fail when any of the three report fields is missing |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Hypothesis record

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `HypothesisRecord` | Accept a sourced shopping-session hypothesis or an unresolved investigation, and reject abuse, duplicates, and incomplete signals | INV-001, INV-002, POL-001, POL-002 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `HypothesisRecord` | Reject a hypothesis whose source list is empty |
| INV-002 | `HypothesisRecord` | Reject a hypothesis that classifies an assistant as abusive, malicious, or legitimate |
| POL-001 | `HypothesisRecord` | When sources do not support a testable signal, store an unresolved investigation and no hypothesis |
| POL-002 | `HypothesisRecord` | Reject a second hypothesis for the same assistant and signal |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `hypothesisRecord_emptySources_rejected` | `HypothesisRecord` | A hypothesis with no source is rejected |
| `hypothesisRecord_abuseClassification_rejected` | `HypothesisRecord` | An abuse or legitimacy classification is rejected |
| `hypothesisRecord_weakSources_storesUnresolvedOnly` | `HypothesisRecord` | Weak sources create an unresolved investigation and no hypothesis |
| `hypothesisRecord_duplicateSignal_rejected` | `HypothesisRecord` | The same assistant and signal cannot be stored twice |
| `hypothesisRecord_missingField_rejected` | `HypothesisRecord` | Omitting the signal, observation, sources, or measurements is rejected |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 4 — JSON research store

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `JsonResearchStore` | Read and write registry entries, reports, hypotheses, and unresolved investigations as JSON files that survive the writing process | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `JsonResearchStore` | This class stores records. It does not decide which records are valid. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `jsonResearchStore_reopen_returnsWrittenRecords` | `JsonResearchStore` | Four written record types are readable from a new store instance on the same directory |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 5 — Agent intelligence node

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `AgentIntelligenceNode` | Run LangChain ReAct for one orchestrator assignment, and refuse a direct human call and a deployed-rule write | INV-004 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-004 | `AgentIntelligenceNode` | The node writes only registry entries, reports, hypotheses, and unresolved investigations |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `agentIntelligenceNode_completedRun_writesNoDeployedRule` | `AgentIntelligenceNode` | A finished run adds none of a deployed detection rule |
| `agentIntelligenceNode_directHumanText_rejected` | `AgentIntelligenceNode` | Human text without an orchestrator assignment is rejected |
| `agentIntelligenceNode_assignment_writesRegistryEntry` | `AgentIntelligenceNode` | An assignment naming an assistant writes one sourced registry entry |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 6 — Discovery schedule

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DiscoverySchedule` | Decide whether a discovery run is due from the configured interval and the previous run time | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `DiscoverySchedule` | The schedule decides timing. `HypothesisRecord` and `AgentRegistry` still decide what may be stored. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `discoverySchedule_defaultInterval_notDueAt23Hours` | `DiscoverySchedule` | The default 24-hour interval is not due at 23 hours |
| `discoverySchedule_defaultInterval_dueAt24Hours` | `DiscoverySchedule` | The default interval is due at 24 hours |
| `discoverySchedule_oneHour_dueAtOneHour` | `DiscoverySchedule` | A 1-hour interval is due at 1 hour |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 7 — System end-to-end test

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `SystemEndToEndTest` | Run the path from an orchestrator assignment through a submitted specification using saved records, and refuse to start a shopping agent | POL-004 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| POL-004 | `SystemEndToEndTest` | Load the virtual-machine evidence from a file and do not start a shopping-agent process |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `systemEndToEndTest_run_startsNoShoppingAgent` | `SystemEndToEndTest` | A run performs no shopping-agent process start |
| `systemEndToEndTest_missingValidationResults_fails` | `SystemEndToEndTest` | A specification without validation results fails |
| `systemEndToEndTest_sameRecords_sameResult` | `SystemEndToEndTest` | Two runs on the same records return the same pass or fail result |

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
| Functional | REQ-001 | Integration: `assignment_namedAssistant_storesSourcedEntry` |
| Functional | REQ-002 | Integration: `discovery_unknownAssistant_addsOneEntryAndReport` |
| Functional | REQ-003 | Integration: `discovery_unknownAssistant_addsOneEntryAndReport`, `assignment_namedAssistant_reportNamesOrchestratorOrigin` |
| Functional | REQ-004 | Integration: `hypothesis_completeSignal_storesRequiredFields` |
| Functional | REQ-005 | Integration: `hypothesis_abusePurpose_storesNothing` |
| Functional | REQ-006 | Integration: `hypothesis_sameSignal_doesNotDuplicate` |
| Functional | REQ-007 | Integration: `hypothesis_weakSources_storesUnresolvedOnly` |
| Functional | REQ-008 | Integration: `system_completeRecords_specificationPasses`, `system_missingValidationResults_specificationFails` |
| Functional | REQ-009 | Integration: `discovery_knownAssistant_storesNewPattern` |
| Functional | REQ-010 | Integration: `discovery_defaultInterval_startsAt24Hours`, `discovery_oneHourInterval_startsAtOneHour` |
| Quality | QR-001 | Integration: `assignment_namedAssistant_storesSourcedEntry`, `hypothesis_completeSignal_storesRequiredFields` |
| Quality | QR-002 | Integration: `store_processRestart_recordsRemain` |
| Quality | QR-003 | Integration: `system_completeRecords_specificationPasses` |
| Invariant | INV-001 | Unit: `hypothesisRecord_emptySources_rejected` on `HypothesisRecord` |
| Invariant | INV-002 | Unit: `hypothesisRecord_abuseClassification_rejected` on `HypothesisRecord` |
| Invariant | INV-003 | Unit: `agentRegistry_addition_createsOneReport` on `AgentRegistry` |
| Invariant | INV-004 | Unit: `agentIntelligenceNode_completedRun_writesNoDeployedRule` on `AgentIntelligenceNode` |
| Policy | POL-001 | Unit: `hypothesisRecord_weakSources_storesUnresolvedOnly` on `HypothesisRecord` |
| Policy | POL-002 | Unit: `hypothesisRecord_duplicateSignal_rejected` on `HypothesisRecord` |
| Policy | POL-003 | Unit: `agentRegistry_eitherOrigin_requiresNameSourcesAndOrigin` on `AgentRegistry` |
| Policy | POL-004 | Unit: `systemEndToEndTest_run_startsNoShoppingAgent` on `SystemEndToEndTest` |

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
- **Acknowledgement reason**: The system end-to-end test depends on records from the other work items and on a person running the assistant on the sandbox virtual machine.
- **Handoff artifact**: `requirements/LOCAL-agent-intelligence/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-agent-intelligence/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-agent-intelligence/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- CA-001: dataset validation, sandbox records, independent evaluation, and rule specification are outside this ticket. The system test uses saved fixtures for those records. It does not implement those agents.
- DR-002: manual virtual-machine evidence can omit fields, and discovery can register an assistant that never becomes a shopping-session hypothesis. `HypothesisRecord` blocks a hypothesis when the sources do not support a shopping-session signal.
