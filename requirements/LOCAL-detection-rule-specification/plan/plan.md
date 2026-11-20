# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-detection-rule-specification |
| **Requirements base path** | requirements/LOCAL-detection-rule-specification/ |
| **Plan base path** | requirements/LOCAL-detection-rule-specification/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | Existing repo |
| **Architecture style** | LangChain with LangGraph |
| **Architecture source** | `docs/adr/0001-langchain-langgraph.md` and the package-plus-JSON-store layout in `research_orchestrator/` |
| **Architecture confidence** | High. Validator JSON is recorded below. |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | CA-001, ASS-003 |

Architecture discovery validator:

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
| REQ-001 | critical | yes | Both supporting results must produce a submitted standard-confidence specification. | Step 5 | `specification_bothSupport_writesStandardConfidence` |
| REQ-002 | critical | yes | One supporting result with a non-contradicting inconclusive or blocked result must lower confidence. | Step 3, Step 5 | `specification_oneSupportOtherInconclusive_writesLowerConfidence` |
| REQ-003 | critical | yes | A contradiction or a missing source must produce no specification. | Step 3, Step 5 | `specification_contradiction_writesNothing` |
| INV-001 | critical | yes | A stored specification is submitted for a human and is not deployed. | Step 2 | `specificationTemplate_deployedTrue_rejected` |
| REQ-004 | high | no | This component must not research, discover datasets, or execute the sandbox. | Step 1, Step 5 | `specification_storedInputsOnly_doesNotResearch` |
| POL-001 | high | no | The component must not chat with another agent. | Step 5 | `detectionRuleSpecification_result_hasNoAgentMessage` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | `docs/adr/0001-langchain-langgraph.md` | Use LangChain and LangGraph. Do not replace that decision. |
| Existing modules | `research_orchestrator/` | One package per component, one class per module, JSON list files. Do not import that package. |
| Existing tests | `tests/test_*.py` | Pytest functions named `subject_condition_expectedOutcome`, requirement IDs in docstrings, no quiet flag. |
| Contracts / schemas | not provided | Record shape is the template fields in DD-005. No schema file is part of this package. |

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
| `detection_rule_specification` | Read stored evidence and write one specification | LangChain, LangGraph, the local JSON store |
| Other component packages | Research, dataset discovery, validation, sandbox execution, orchestration | Not imported |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `detection_rule_specification_mustNotDependOn_otherComponents` | `detection_rule_specification` must not import other component packages or subprocess |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Specification template

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `SpecificationTemplate` | Build the submitted record and reject a record outside the two evidence sections | INV-001, INV-002, INV-003 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `SpecificationTemplate` | Reject a record whose submitted flag is not true or whose deployed flag is not false |
| INV-002 | `SpecificationTemplate` | Reject a record that carries an abuse or legitimacy classification field |
| INV-003 | `SpecificationTemplate` | Reject a record that omits a source URL, a source title, the dataset result, or the sandbox result |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `specificationTemplate_deployedTrue_rejected` | `SpecificationTemplate` | A deployed-true record is rejected |
| `specificationTemplate_abuseField_rejected` | `SpecificationTemplate` | An abuse or legitimacy field is rejected |
| `specificationTemplate_missingEvidenceField_rejected` | `SpecificationTemplate` | A missing URL, title, dataset result, or sandbox result is rejected |
| `specificationTemplate_sections_namesResearchSourcesAndValidationResults` | `SpecificationTemplate` | The template sections are research_sources and validation_results |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Evidence confidence

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `EvidenceConfidence` | Choose standard, lower, or no specification from stored results and sources | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `EvidenceConfidence` | REQ-001, REQ-002, and REQ-003 state the outcomes. This class is the only place that chooses the confidence label. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `evidenceConfidence_bothSupport_returnsStandard` | `EvidenceConfidence` | Two support results and a complete source return standard |
| `evidenceConfidence_inconclusiveOther_returnsLower` | `EvidenceConfidence` | One support and one inconclusive result return lower |
| `evidenceConfidence_blockedOther_returnsLower` | `EvidenceConfidence` | One support and one blocked result return lower |
| `evidenceConfidence_contradiction_returnsNone` | `EvidenceConfidence` | A contradict result returns no specification |
| `evidenceConfidence_missingSource_returnsNone` | `EvidenceConfidence` | A missing source or a missing result returns no specification |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 4 — JSON specification store

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `RuleSpecificationStore` | Read `hypotheses.json` and `validation_results.json`, and write one `rule_specifications.json` row per hypothesis | None |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| None | `RuleSpecificationStore` | The store persists records. `SpecificationTemplate` rejects an illegal record before it is written. |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `ruleSpecificationStore_reopen_returnsWrittenSpecification` | `RuleSpecificationStore` | A record written by one instance is readable from a new instance on the same directory |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 5 — Detection rule specification node

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `DetectionRuleSpecification` | Run the LangGraph node, call the LangChain tool, and write the specification or nothing | POL-001 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| POL-001 | `DetectionRuleSpecification` | The run result contains the specification outcome and no message to another agent |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `detectionRuleSpecification_result_hasNoAgentMessage` | `DetectionRuleSpecification` | The run result has no agent message |
| `detectionRuleSpecification_graph_hasSpecifyNode` | `DetectionRuleSpecification` | The compiled graph contains the specify node |

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
| Functional | REQ-001 | Integration: `specification_bothSupport_writesStandardConfidence` |
| Functional | REQ-002 | Integration: `specification_oneSupportOtherInconclusive_writesLowerConfidence`, `specification_oneSupportOtherBlocked_writesLowerConfidence` |
| Functional | REQ-003 | Integration: `specification_contradiction_writesNothing`, `specification_missingSource_writesNothing` |
| Functional | REQ-004 | Integration: `specification_storedInputsOnly_doesNotResearch` |
| Quality | QR-001 | Integration: `specification_repeat_writesEqualRecord` |
| Quality | QR-002 | Integration: `ruleSpecificationStore_reopen_returnsWrittenSpecification` |
| Invariant | INV-001 | Unit: `specificationTemplate_deployedTrue_rejected` on `SpecificationTemplate` |
| Invariant | INV-002 | Unit: `specificationTemplate_abuseField_rejected` on `SpecificationTemplate` |
| Invariant | INV-003 | Unit: `specificationTemplate_missingEvidenceField_rejected` on `SpecificationTemplate` |
| Policy | POL-001 | Unit: `detectionRuleSpecification_result_hasNoAgentMessage` on `DetectionRuleSpecification` |

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
- **Acknowledgement reason**: Input hypothesis and validation file names are a local contract because this package does not import the components that write them.
- **Handoff artifact**: `requirements/LOCAL-detection-rule-specification/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-detection-rule-specification/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-detection-rule-specification/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- CA-001: `hypotheses.json` and `validation_results.json` are the local read contract. Sibling packages are not imported. A different file name from a later writer is outside this ticket until the records use this contract or its `id` and `sources` aliases.
