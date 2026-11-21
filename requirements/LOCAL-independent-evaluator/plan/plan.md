# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-independent-evaluator |
| **Requirements base path** | requirements/LOCAL-independent-evaluator/ |
| **Plan base path** | requirements/LOCAL-independent-evaluator/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | Existing repo |
| **Architecture style** | Python package of cohesive classes that append JSON list files |
| **Architecture source** | Inferred from code |
| **Architecture confidence** | Applied style identified from `research_orchestrator/`. Validator confidence is low because no deterministic checks are configured for that label. That does not stop a brownfield plan. |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | ASS-002 |

### Analyst planning anchors

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-001 | critical | yes | A hypothesis without sources must not pass. | Step 3 | `hypothesis_withSources_writesPass` |
| REQ-003 | critical | yes | A consistent validation pair is the only validation PASS. | Step 3 | `validation_consistentPair_writesPass` |
| REQ-005 | critical | yes | A rule passes only when it is submitted, not deployed, and cited. | Step 3 | `rule_submittedWithCitations_writesPass` |
| REQ-002 | critical | yes | Missing hypothesis evidence is REWORK and is not a stage change. | Step 3 | `hypothesis_missingSources_writesRework` |
| INV-001 | critical | yes | This package must not write workflow stage changes. | Step 3 | `independentEvaluator_stageFile_unchanged` |
| POL-003 | high | no | The rule check is the gate before human review. | Step 3 | `independentEvaluator_deployedRule_rework` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | `docs/adr/0001-langchain-langgraph.md` accepts LangChain and LangGraph. No `AGENTS.md` architecture bank. | The ADR names the system framework. Applied modules do not import it. DR-002 records that difference. |
| Existing modules | `research_orchestrator/` | New code lives in `independent_evaluator/` and does not import that package. Classes write JSON lists. |
| Existing tests | `tests/test_boundary.py`, `tests/test_integration_orchestrator.py` | Pytest files under `tests/` use `subject_condition_expectedOutcome`. Boundary tests scan source text for forbidden imports. |
| Contracts / schemas | not provided | Evaluations are JSON objects with the four fields named in the user order. No schema file is part of this package. |

Validator evidence from `architecture-discovery-validator.py` for the applied style label:

```json
{"confidence":"low","evidence":[],"conflicts":["validator-config: no deterministic checks are configured for this architecture label"],"recommendation":"stop"}
```

The applied style is visible in `research_orchestrator/store.py` and `research_orchestrator/orchestrator.py`. Gate 2B for brownfield continues when the applied style is identified.

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
| `independent_evaluator` | Check stored records and append evaluations | Python standard library only |
| `research_orchestrator` and other component packages | Their own records and stage changes | Not imported by `independent_evaluator` |
| `tests` | Boundary, unit, and integration checks | `independent_evaluator` and pytest |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `independent_evaluator_mustNotDependOn_otherComponents` | `independent_evaluator` must not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, `sandbox_validation`, `rule_specification`, or `subprocess` |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Evaluation record

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `EvaluationRecord` | Accept only a four-field PASS or REWORK evaluation | INV-002 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-002 | `EvaluationRecord` | Reject an empty trigger, a result other than PASS or REWORK, or any extra field |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `evaluationRecord_emptyTrigger_rejected` | `EvaluationRecord` | An empty trigger raises |
| `evaluationRecord_otherResult_rejected` | `EvaluationRecord` | ESCALATE and STOP raise |
| `evaluationRecord_extraField_rejected` | `EvaluationRecord` | A mapping with an extra field raises |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Stage evidence check

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `IndependentEvaluator` | Judge one stored stage and append one evaluation without writing any other file | INV-001, POL-001, POL-002, POL-003, POL-004 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `IndependentEvaluator` | Write only `evaluations.json` |
| POL-001 | `IndependentEvaluator` | Hypothesis PASS requires at least one source |
| POL-002 | `IndependentEvaluator` | Validation PASS requires a present pair that is not support with reject |
| POL-003 | `IndependentEvaluator` | Rule PASS requires submitted, not deployed, and both citations |
| POL-004 | `IndependentEvaluator` | An abuse-classification record is REWORK without copying a label, and no process or message is written |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `independentEvaluator_stageFile_unchanged` | `IndependentEvaluator` | A stage file is unchanged after PASS and after REWORK |
| `independentEvaluator_emptySources_rework` | `IndependentEvaluator` | An empty source list is REWORK |
| `independentEvaluator_supportAndInconclusive_pass` | `IndependentEvaluator` | Support with inconclusive is PASS |
| `independentEvaluator_supportAndReject_rework` | `IndependentEvaluator` | Support with reject is REWORK |
| `independentEvaluator_deployedRule_rework` | `IndependentEvaluator` | A deployed specification is REWORK |
| `independentEvaluator_abusePurpose_reworkWithoutLabel` | `IndependentEvaluator` | Abuse classification is REWORK and the trigger has no abuse label |

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
| Functional | REQ-001 | Integration: `hypothesis_withSources_writesPass` |
| Functional | REQ-002 | Integration: `hypothesis_missingSources_writesRework` |
| Functional | REQ-003 | Integration: `validation_consistentPair_writesPass` |
| Functional | REQ-004 | Integration: `validation_contradictionOrMissing_writesRework` |
| Functional | REQ-005 | Integration: `rule_submittedWithCitations_writesPass` |
| Functional | REQ-006 | Integration: `rule_notEligible_writesRework` |
| Functional | REQ-007 | Integration: `evaluator_sideEffects_writesOnlyEvaluation` |
| Quality | QR-001 | Integration: `evaluation_afterRestart_remainsReadable` |
| Quality | QR-002 | Integration: `evaluation_repeat_sameResult` |
| Invariant | INV-001 | Unit: `independentEvaluator_stageFile_unchanged` on `IndependentEvaluator` |
| Invariant | INV-002 | Unit: `evaluationRecord_emptyTrigger_rejected` on `EvaluationRecord` |
| Policy | POL-001 | Unit: `independentEvaluator_emptySources_rework` on `IndependentEvaluator` |
| Policy | POL-002 | Unit: `independentEvaluator_supportAndReject_rework` on `IndependentEvaluator` |
| Policy | POL-003 | Unit: `independentEvaluator_deployedRule_rework` on `IndependentEvaluator` |
| Policy | POL-004 | Unit: `independentEvaluator_abusePurpose_reworkWithoutLabel` on `IndependentEvaluator` |

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
- **Acknowledgement reason**: Input JSON names are local because this package must not import sibling packages that are implemented in parallel. Records that use different names are REWORK until they match.
- **Handoff artifact**: `requirements/LOCAL-independent-evaluator/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-independent-evaluator/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-independent-evaluator/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- DR-001: DD-004 locks `hypotheses.json`, `validations.json`, and `rule_specifications.json`. A parallel writer with other names is REWORK. This is the acknowledgement reason.
- DR-002: The ADR accepts LangChain and LangGraph. Applied modules do not import them, so this package does not register a graph node.
