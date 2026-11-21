# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-dataset-discovery |
| **Requirements base path** | requirements/LOCAL-dataset-discovery/ |
| **Plan base path** | requirements/LOCAL-dataset-discovery/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | New repo |
| **Architecture style** | LangChain plus LangGraph: one node, one tool, JSON records |
| **Architecture source** | User-provided |
| **Architecture confidence** | Low; carried as DR-003 because the validator has no checks for this label. The accepted ADR matches the user-provided style and does not contradict it. |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | CA-001, CA-002, DR-003 |

### Analyst planning anchors

These fields come from `requirements/LOCAL-dataset-discovery/handoff.json`. The plan must preserve every minimum-scope item and map every critical item to a step and verification.

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-001 | critical | yes | A suitable dataset must be stored with the name, source URL, title, suitability, and hypothesis id. | Step 6 | `suitableDataset_writesEntryForHypothesis` |
| REQ-002 | critical | yes | A query match or an incomplete dataset must not be recorded as suitable. | Step 2, Step 6 | `queryOnlyDataset_writesUnsuitable` |
| INV-002 | critical | yes | Description match alone must never become a suitable registry entry. | Step 2 | `suitabilityJudgement_queryMatchOnly_isUnsuitable` |
| POL-001 | critical | yes | Any failed suitability check must record unsuitable. | Step 2 | `suitabilityJudgement_missingLabel_isUnsuitable` |
| REQ-004 | high | no | An unsuitable dataset must not be substituted as support for a hypothesis. | Step 6 | `noSuitableCandidate_writesNoSuitableEntry` |
| REQ-006 | high | no | Human text must not enter this agent. | Step 6 | `humanText_writesNothing` |
| INV-001 | high | no | A registry entry without identity fields cannot be traced to a hypothesis. | Step 3 | `datasetRegistry_missingName_rejected` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | `docs/adr/0001-langchain-langgraph.md` | Use a LangGraph node and a LangChain tool. Do not add a conversational crew. |
| Existing modules | not applicable | No product package exists yet. Package name is `dataset_discovery`. |
| Existing tests | not applicable | Tests live under `tests/` and use `subject_condition_expectedOutcome`. |
| Contracts / schemas | not provided | Registry entries are JSON objects. No schema file is part of this package. |

Validator command: `python3 /home/ubuntu/.cursor/skills/planner/scripts/architecture-discovery-validator.py /agent/repos/agent-hunt "LangChain plus LangGraph"`

```json
{
  "confidence": "low",
  "evidence": [],
  "conflicts": [
    "validator-config: no deterministic checks are configured for this architecture label"
  ],
  "recommendation": "stop"
}
```

The user-provided style is the governing style because `docs/adr/0001-langchain-langgraph.md` selects the same frameworks. The validator stop is a missing checker, recorded as DR-003, not a contradiction with the ADR.

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

## Step 1 — Architectural structure and boundaries

### Structure map

| Architectural unit | Responsibility | Allowed dependencies |
|--------------------|----------------|----------------------|
| `dataset_discovery` | Discover datasets for stored hypotheses and write the registry | LangChain, LangGraph, and the Python standard library |
| Hypothesis JSON | Read-only input | Local `hypotheses.json` |
| Dataset registry | Written output | Local `datasets.json` and `discovery_state.json` |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `dataset_discovery_mustNotDependOn_otherAgents` | `dataset_discovery` must not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, `sandbox_validation`, `detection_rule_specification`, or `independent_evaluator` |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Suitability judgement

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `SuitabilityJudgement` | Decide suitable or unsuitable for one candidate and one hypothesis | INV-002, POL-001 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-002 | `SuitabilityJudgement` | A query-only candidate is unsuitable |
| POL-001 | `SuitabilityJudgement` | Any failed check yields unsuitable |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `suitabilityJudgement_queryMatchOnly_isUnsuitable` | `SuitabilityJudgement` | A query-only candidate is unsuitable |
| `suitabilityJudgement_missingLabel_isUnsuitable` | `SuitabilityJudgement` | A missing human or agent label is unsuitable |
| `suitabilityJudgement_staleVerification_isUnsuitable` | `SuitabilityJudgement` | A verification date 731 days old is unsuitable and 730 days old passes the age check |
| `suitabilityJudgement_missingMeasurementField_isUnsuitable` | `SuitabilityJudgement` | A missing measurement field is unsuitable |
| `suitabilityJudgement_completeCandidate_isSuitable` | `SuitabilityJudgement` | A complete candidate is suitable |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Dataset registry

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DatasetRegistry` | Store and reload `datasets.json`, and keep one entry per dataset name and hypothesis id | INV-001, POL-002 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `DatasetRegistry` | Reject an entry missing the name, http(s) URL, title, suitability, or hypothesis id |
| POL-002 | `DatasetRegistry` | A repeated pair replaces the previous entry instead of adding a second one |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `datasetRegistry_missingName_rejected` | `DatasetRegistry` | An entry without a dataset name is rejected |
| `datasetRegistry_badUrl_rejected` | `DatasetRegistry` | A non-http source URL is rejected |
| `datasetRegistry_repeatPair_keepsOneEntry` | `DatasetRegistry` | The same dataset name and hypothesis id stay one entry |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 4 — Hypothesis reader

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `HypothesisReader` | Read hypothesis id and measurement fields from stored JSON | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `HypothesisReader` | This class reads records. It does not judge datasets or write the registry. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `hypothesisReader_idOrHypothesisId_returnsId` | `HypothesisReader` | Either id field is returned |
| `hypothesisReader_listMeasurements_returnsFields` | `HypothesisReader` | A list of measurement names is returned |
| `hypothesisReader_proseMeasurements_returnsNoFields` | `HypothesisReader` | Prose measurements yield no field list |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 5 — Discovery schedule

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DiscoverySchedule` | Decide whether a scheduled search is due | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `DiscoverySchedule` | The schedule decides timing. It does not search or judge. |

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

## Step 6 — Dataset discovery node

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DatasetDiscoveryNode` | Run the LangGraph node, call the catalog tool, and refuse human text, shopping-agent starts, and foreign records | INV-003, POL-003, POL-004 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-003 | `DatasetDiscoveryNode` | A run does not start a shopping-agent process |
| POL-003 | `DatasetDiscoveryNode` | Human text writes nothing |
| POL-004 | `DatasetDiscoveryNode` | The run writes registry state only and does not write a hypothesis, validation metric, or deployed rule |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `datasetDiscoveryNode_humanText_writesNothing` | `DatasetDiscoveryNode` | Human text writes no registry entry |
| `datasetDiscoveryNode_run_startsNoShoppingAgent` | `DatasetDiscoveryNode` | A run performs no shopping-agent process start |
| `datasetDiscoveryNode_run_writesNoHypothesisOrRule` | `DatasetDiscoveryNode` | A run leaves hypotheses unchanged and adds no metric or deployed rule |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Final acceptance

Overall acceptance criteria for the planned code changes. All items must pass before the implementation is considered complete.

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

Final traceability check before implementation.

| ID type | ID | Verification |
|---------|-----|--------------|
| Functional | REQ-001 | Integration: `suitableDataset_writesEntryForHypothesis` |
| Functional | REQ-002 | Integration: `queryOnlyDataset_writesUnsuitable` |
| Functional | REQ-003 | Integration: `repeatDiscovery_keepsOneEntry` |
| Functional | REQ-004 | Integration: `noSuitableCandidate_writesNoSuitableEntry` |
| Functional | REQ-005 | Integration: `scheduleDue_searchesAgain` |
| Functional | REQ-006 | Integration: `humanText_writesNothing` |
| Functional | REQ-007 | Integration: `discoveryRun_startsNoShoppingAgentAndWritesNoRule` |
| Quality | QR-001 | Integration: `reopenRegistry_returnsSameEntry` |
| Quality | QR-002 | Integration: `sameCandidate_sameSuitability` |
| Invariant | INV-001 | Unit: `datasetRegistry_missingName_rejected` on `DatasetRegistry` |
| Invariant | INV-002 | Unit: `suitabilityJudgement_queryMatchOnly_isUnsuitable` on `SuitabilityJudgement` |
| Invariant | INV-003 | Unit: `datasetDiscoveryNode_run_startsNoShoppingAgent` on `DatasetDiscoveryNode` |
| Policy | POL-001 | Unit: `suitabilityJudgement_missingLabel_isUnsuitable` on `SuitabilityJudgement` |
| Policy | POL-002 | Unit: `datasetRegistry_repeatPair_keepsOneEntry` on `DatasetRegistry` |
| Policy | POL-003 | Unit: `datasetDiscoveryNode_humanText_writesNothing` on `DatasetDiscoveryNode` |
| Policy | POL-004 | Unit: `datasetDiscoveryNode_run_writesNoHypothesisOrRule` on `DatasetDiscoveryNode` |

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
- **Acknowledgement reason**: The 730-day verification window and the hypothesis JSON field names are planning choices because the sources do not state them.
- **Handoff artifact**: `requirements/LOCAL-dataset-discovery/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-dataset-discovery/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-dataset-discovery/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- CA-001: the 730-day verification window is a planning choice. `SuitabilityJudgement` keeps it as one constant.
- CA-002: hypothesis JSON names may differ in the parallel agent-intelligence ticket. `HypothesisReader` accepts the names in DD-005 and fails coverage closed for prose.
- DR-003: the architecture validator returned low confidence because it has no checker for LangChain plus LangGraph. The ADR is the trusted record for that style.
