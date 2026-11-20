# Implementation Plan

Architecture-aware implementation plan with full requirements traceability.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-sandbox-validation |
| **Requirements base path** | requirements/LOCAL-sandbox-validation/ |
| **Plan base path** | requirements/LOCAL-sandbox-validation/plan/ |
| **Design decisions** | [design-decisions.md](./design-decisions.md) |
| **Planning mode** | New repo |
| **Architecture style** | One LangGraph node and a LangChain runnable that write a JSON result |
| **Architecture source** | User-provided |
| **Architecture confidence** | High |
| **Input readiness** | READY_WITH_RISKS |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |
| **Human acknowledgement required** | yes |
| **Risks carried forward** | ASS-002 |

Architecture validator JSON: `{"confidence": "high", "evidence": ["trusted-context: docs/adr/0001-langchain-langgraph.md mentions 'langchain with langgraph'"], "conflicts": [], "recommendation": "proceed"}`.

### Analyst planning anchors

| ID | Priority | Minimum accepted scope | Why it matters | Plan step(s) | Verification |
|----|----------|------------------------|----------------|--------------|--------------|
| REQ-001 | critical | yes | The only output is sandbox_results.json with hypothesis_id, result, and evidence_path. | Step 3 | `evidence_present_writesResultFile` |
| REQ-002 | critical | yes | Missing evidence is blocked and must not start a browser or shopping agent. | Step 3 | `evidence_missing_recordsBlocked` |
| INV-001 | critical | yes | The package must not import subprocess or start a process. | Step 3 | `sandboxValidation_package_doesNotImportSubprocess` |
| POL-001 | critical | yes | Evidence that cannot be read or has no telemetry is blocked. | Step 2 | `signalReproducibility_missingTelemetry_blocked` |
| POL-002 | high | no | Support, contradict, and inconclusive come from the saved-run rule. | Step 2 | `signalReproducibility_fourOfFive_support` |

### Architecture and naming evidence

| Evidence type | Source | Planning implication |
|---------------|--------|----------------------|
| AI context bank / repo guidance | `docs/adr/0001-langchain-langgraph.md` | LangChain runnable plus one LangGraph node. |
| Existing modules | `research_orchestrator/` | Tests live under `tests/`. This package does not import that package. JSON records stay files. |
| Existing tests | `tests/test_boundary.py` | Boundary checks read package source for forbidden imports. |
| Contracts / schemas | not provided | The result fields are the three names in REQ-001. No contract file is added. |

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
| `sandbox_validation` | Load saved evidence and write `sandbox_results.json` | LangGraph, LangChain runnable, local JSON files |
| `research_orchestrator` and other component packages | Their own records | Not imported |
| Shopping-agent launchers | Manual runs on the VM | Not imported and not started |

### Structural boundary test descriptions

| Test name | Rule |
|-----------|------|
| `sandbox_validation_mustNotDependOn_otherComponents` | `sandbox_validation` must not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, `rule_specification`, or `subprocess` |

### Definition of Done

- [ ] Code structure conforms to the planned architectural units and allowed dependencies
- [ ] All planned structural boundary tests are implemented and passing
- [ ] No business invariant or policy enforcement is implemented via structural boundary tests; those checks are covered by unit tests on encapsulating classes

---

## Step 2 — Saved-run judgment

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `SignalReproducibility` | Map saved runs to `support`, `contradict`, `inconclusive`, or `blocked` | POL-001, POL-002 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| POL-001 | `SignalReproducibility` | Missing, unreadable, empty, mismatched, or telemetry-incomplete evidence is `blocked` |
| POL-002 | `SignalReproducibility` | Four of five observations support, a consistent absence contradicts, and the remaining telemetry-complete sets are inconclusive |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `signalReproducibility_missingTelemetry_blocked` | `SignalReproducibility` | A run without telemetry is `blocked` |
| `signalReproducibility_fourOfFive_support` | `SignalReproducibility` | Four positives in five runs are `support` |
| `signalReproducibility_noneOfFive_contradict` | `SignalReproducibility` | Five runs with no signal are `contradict` |
| `signalReproducibility_oneOfFive_inconclusive` | `SignalReproducibility` | One positive in five runs is `inconclusive` |

### Definition of Done

- [ ] All planned classes for this unit are implemented with SRP-compliant responsibilities
- [ ] Every `INV-NNN` and `POL-NNN` assigned to this unit is enforced in exactly one implemented class
- [ ] Unit tests for all planned classes in this unit are implemented and passing
- [ ] No dependency violates the planned boundaries for this unit
- [ ] Invariant and policy tests exercise only the designated encapsulating class

---

## Step 3 — Sandbox validation node

### Classes

| Class | Responsibility (SRP) | Encapsulates |
|-------|----------------------|--------------|
| `SandboxValidation` | Run the LangGraph node, load files, and write `sandbox_results.json` | INV-001, INV-002 |

### Invariants and policies

| ID | Encapsulating class | Enforcement summary |
|----|---------------------|---------------------|
| INV-001 | `SandboxValidation` | The package source does not import `subprocess`, and `run` does not start a process |
| INV-002 | `SandboxValidation` | The written object has only `hypothesis_id`, `result`, and `evidence_path` |

### Unit test descriptions

| Test name | Class | Assertion intent |
|-----------|-------|------------------|
| `sandboxValidation_package_doesNotImportSubprocess` | `SandboxValidation` | Parsing the package finds no `subprocess` import |
| `sandboxValidation_run_doesNotStartProcess` | `SandboxValidation` | A validation run emits no process-start audit event |
| `sandboxValidation_resultFile_hasThreeFields` | `SandboxValidation` | The written keys are exactly the three result fields |

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
| Functional | REQ-001 | Integration: `evidence_present_writesResultFile` |
| Functional | REQ-002 | Integration: `evidence_missing_recordsBlocked` |
| Functional | REQ-003 | Integration: `runs_fourOfFive_support` |
| Functional | REQ-004 | Integration: `runs_noneOfFive_contradict` |
| Functional | REQ-005 | Integration: `runs_mixed_inconclusive` |
| Functional | REQ-006 | Integration: `result_file_omitsAbuseAndRule` |
| Quality | QR-001 | Integration: `validation_sameEvidence_writesSameResult` |
| Invariant | INV-001 | Unit: `sandboxValidation_package_doesNotImportSubprocess` on `SandboxValidation` |
| Invariant | INV-002 | Unit: `sandboxValidation_resultFile_hasThreeFields` on `SandboxValidation` |
| Policy | POL-001 | Unit: `signalReproducibility_missingTelemetry_blocked` on `SignalReproducibility` |
| Policy | POL-002 | Unit: `signalReproducibility_fourOfFive_support` on `SignalReproducibility` |

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
- **Acknowledgement reason**: The four-of-five rule is provisional, and the evidence JSON fields are inferred from the reasoning-loop spec.
- **Handoff artifact**: `requirements/LOCAL-sandbox-validation/plan/handoff.json`

### Coding agent instruction

Build the implementation described in `requirements/LOCAL-sandbox-validation/plan/plan.md`.

1. Go through the plan step by step in order.
2. Preserve every analyst planning anchor in the table above, especially `minimumAcceptedScope` and `critical` items.
3. Apply each step's acceptance criteria and Definition of Done before moving to the next step.
4. Implement and run the planned verification for each step, including integration, boundary, and unit tests as specified.
5. Stop and surface a blocker immediately if the codebase, dependencies, or runtime environment conflict with the plan in a way that creates material risk.
6. Implement the active decisions in `requirements/LOCAL-sandbox-validation/plan/design-decisions.md`; stop if implementation evidence invalidates one rather than silently deviating.
7. Apply the Final acceptance and Coverage sign-off sections before considering the work complete.

## Design risks

- ASS-002: saved evidence is judged only when `runs` contain `telemetry_present` and `signal_observed`. A differently shaped file is `blocked`.
