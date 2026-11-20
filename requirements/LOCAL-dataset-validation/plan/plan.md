# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-dataset-validation |
| **Requirements base path** | requirements/LOCAL-dataset-validation/ |
| **Plan base path** | requirements/LOCAL-dataset-validation/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | Existing repo |
| **Architecture style** | LangChain with LangGraph: one node, one counting tool, and a JSON result file |
| **Architecture source** | User-provided |
| **Architecture confidence** | High |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | ASS-002. DR-001: `research_orchestrator` does not import LangGraph. |

Architecture validator JSON for `LangChain with LangGraph`:

```json
{
  "confidence": "high",
  "evidence": [
    "trusted-context: docs/adr/0001-langchain-langgraph.md mentions 'langchain with langgraph'"
  ],
  "conflicts": [],
  "recommendation": "proceed"
}
```

### Analyst planning anchors

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-001 | critical | yes | Support is the outcome that says the signal is present at a measured rate. | Step 4 | `signal_moreCommonInAi_recordsSupport` |
| REQ-002 | critical | yes | Contradict is the outcome that says the labels refute the signal. | Step 4 | `signal_moreCommonInHuman_recordsContradict` |
| REQ-004 | critical | yes | A missing dataset must be blocked rather than filled in. | Step 4 | `dataset_missingFile_recordsBlocked` |
| REQ-007 | critical | yes | Downstream readers depend on the five JSON fields. | Step 3 | `record_persisted_hasExactlyFiveJsonFields` |
| INV-001 | critical | yes | A result outside the four allowed values cannot be coordinated. | Step 2 | `datasetResultRecord_unknownResult_rejected` |
| POL-002 | critical | no | The rate comparison is what makes support, contradict, and inconclusive exclusive. | Step 2 | `datasetResultRecord_rateComparison_selectsResult` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | `docs/adr/0001-langchain-langgraph.md` | Use a LangChain tool and a LangGraph node. Do not reopen the framework choice. |
| Existing modules | `research_orchestrator/` | Keep a package of cohesive classes and a JSON list store. Do not import that package. |
| Existing tests | `tests/test_*.py` | Put tests under `tests/` and name them `subject_condition_expectedOutcome` or `className_condition_expectedBehavior`. |
| Contracts / schemas | not provided | The five JSON fields are stated in REQ-007. No schema file is part of this package. |

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

## Step 1 — Package boundary

### Structure map

| Architectural unit | Responsibility | Allowed dependencies |
|--------------------|----------------|----------------------|
| `dataset_validation` | Measure one labelled fixture and store one dataset result | LangChain, LangGraph, the local JSON store |
| Orchestrator assignment | Names the hypothesis, the signal, and the dataset path | Produced outside this package |
| Other component packages | Research, discovery, sandbox, and rule specification | Not imported by `dataset_validation` |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `dataset_validation_mustNotDependOn_otherComponents` | `dataset_validation` must not import `research_orchestrator`, `agent_intelligence`, `dataset_discovery`, `sandbox_validation`, `rule_specification`, or `subprocess` |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Dataset result record

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DatasetResultRecord` | Select one of the four results and reject a record whose rates disagree with that result | INV-001, INV-002, POL-001, POL-002 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `DatasetResultRecord` | Reject a result outside support, contradict, inconclusive, and blocked |
| INV-002 | `DatasetResultRecord` | Reject support unless prevalence is strictly greater than the false-positive rate, and reject blocked when a rate is a number |
| POL-001 | `DatasetResultRecord` | A missing file becomes blocked with both rates null |
| POL-002 | `DatasetResultRecord` | Numeric rates become support, contradict, or inconclusive by strict comparison |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `datasetResultRecord_unknownResult_rejected` | `DatasetResultRecord` | A result other than the four allowed values is rejected |
| `datasetResultRecord_supportWithoutHigherPrevalence_rejected` | `DatasetResultRecord` | Support requires prevalence strictly greater than the false-positive rate, and blocked rejects a numeric rate |
| `datasetResultRecord_missingFile_recordsBlockedWithNullRates` | `DatasetResultRecord` | A missing dataset becomes blocked with null rates |
| `datasetResultRecord_rateComparison_selectsResult` | `DatasetResultRecord` | Higher AI rate, higher human rate, and equal rates select support, contradict, and inconclusive |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Dataset result store

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DatasetResultStore` | Append and read `dataset_results.json` | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `DatasetResultStore` | This class stores records. It does not choose the result. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `datasetResultStore_reopen_returnsWrittenRecord` | `DatasetResultStore` | A new store on the same path returns the appended record |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 4 — Dataset validation graph

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DatasetValidationGraph` | Run one LangGraph node for an orchestrator assignment, call `count_labelled_signal`, and store one result or nothing | POL-003, POL-004 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| POL-003 | `DatasetValidationGraph` | A payload without orchestrator source, hypothesis id, signal, and dataset path stores nothing |
| POL-004 | `DatasetValidationGraph` | Discovery, shopping-agent launch, rule writing, and abuse classification store nothing |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `datasetValidationGraph_chatPayload_storesNothing` | `DatasetValidationGraph` | A chat payload does not append a record |
| `datasetValidationGraph_forbiddenAction_storesNothing` | `DatasetValidationGraph` | Each forbidden action leaves the result file unchanged |

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
| Functional | REQ-001 | Integration: `signal_moreCommonInAi_recordsSupport` |
| Functional | REQ-002 | Integration: `signal_moreCommonInHuman_recordsContradict` |
| Functional | REQ-003 | Integration: `dataset_equalRates_recordsInconclusive` |
| Functional | REQ-004 | Integration: `dataset_missingFile_recordsBlocked` |
| Functional | REQ-005 | Integration: `assignment_outOfScopeAction_storesNothing` |
| Functional | REQ-006 | Integration: `input_notOrchestratorAssignment_storesNothing` |
| Functional | REQ-007 | Integration: `record_persisted_hasExactlyFiveJsonFields` |
| Quality | QR-001 | Integration: `signal_moreCommonInAi_recordsSupport` |
| Quality | QR-002 | Integration: `store_reopen_readsWrittenResults` |
| Invariant | INV-001 | Unit: `datasetResultRecord_unknownResult_rejected` on `DatasetResultRecord` |
| Invariant | INV-002 | Unit: `datasetResultRecord_supportWithoutHigherPrevalence_rejected` on `DatasetResultRecord` |
| Policy | POL-001 | Unit: `datasetResultRecord_missingFile_recordsBlockedWithNullRates` on `DatasetResultRecord` |
| Policy | POL-002 | Unit: `datasetResultRecord_rateComparison_selectsResult` on `DatasetResultRecord` |
| Policy | POL-003 | Unit: `datasetValidationGraph_chatPayload_storesNothing` on `DatasetValidationGraph` |
| Policy | POL-004 | Unit: `datasetValidationGraph_forbiddenAction_storesNothing` on `DatasetValidationGraph` |

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
- **Acknowledgement reason**: Support and contradict use a strict comparison of AI prevalence and the human false-positive rate, which the sources do not state as a number, and this package adds a LangGraph node while `research_orchestrator` does not import LangGraph.
- **Handoff artifact**: `requirements/LOCAL-dataset-validation/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-dataset-validation/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-dataset-validation/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- ASS-002: equal rates store inconclusive. DD-003 requires acknowledgement.
- DR-001: `research_orchestrator` does not import LangGraph. This package follows the ADR and does not import that package.
