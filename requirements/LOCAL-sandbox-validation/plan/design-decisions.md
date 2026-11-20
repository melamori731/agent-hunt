# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-sandbox-validation |
| **Requirements base path** | requirements/LOCAL-sandbox-validation/ |
| **Plan base path** | requirements/LOCAL-sandbox-validation/plan/ |
| **Plan** | [plan.md](./plan.md) |
| **Implementation readiness** | READY_FOR_IMPLEMENTATION_WITH_ACK |

## Status definitions

- `DECIDED`: selected for implementation and supported by sufficient evidence.
- `REQUIRES_ACK`: selected provisionally, but material risk requires human acknowledgement before implementation.
- `BLOCKED`: unresolved choice prevents safe implementation.
- `SUPERSEDED`: replaced by another decision; preserve the entry and link its replacement.

---

## Decision index

| ID | Decision | Status | Affected plan step(s) |
|----|----------|--------|-----------------------|
| DD-001 | One LangGraph node in `sandbox_validation` loads files through a LangChain runnable | DECIDED | Step 1, Step 3 |
| DD-002 | Missing or unusable evidence writes `blocked` and starts no browser | DECIDED | Step 2, Step 3 |
| DD-003 | Saved runs use the provisional four-of-five rule on `telemetry_present` and `signal_observed` | REQUIRES_ACK | Step 2 |
| DD-004 | The package does not import another component package | DECIDED | Step 1 |
| DD-005 | `sandbox_results.json` has only `hypothesis_id`, `result`, and `evidence_path` | DECIDED | Step 3 |
| DD-006 | No abuse classification, deployed rule, faculty report, or agent chat | DECIDED | Step 3 |

---

## DD-001 — LangGraph node

- **Status**: DECIDED
- **Decision**: `SandboxValidation` compiles one LangGraph node. The node calls a LangChain `RunnableLambda` to load the hypothesis and the evidence file.
- **Scope**: Package `sandbox_validation`.
- **Rationale**: ADR 0001 selects LangChain for tool and runnable calls and LangGraph for the stage graph. This component is one stage.
- **Evidence**:
  - `docs/adr/0001-langchain-langgraph.md`
  - ASS-ARCH-001
  - Architecture validator: confidence high, conflicts empty, recommendation proceed
- **Alternatives considered**:
  - **Plain function with no graph** — Matches `research_orchestrator` today, and it drops the accepted framework for this new package.
- **Consequences**:
  - The environment must provide `langgraph` and `langchain-core`.
  - The node does not add a checkpointer and does not write checkpoint files.
- **Affected plan steps**: Step 1, Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — Missing evidence is blocked

- **Status**: DECIDED
- **Decision**: A missing, unreadable, empty, hypothesis-mismatched, or telemetry-incomplete evidence file writes `result` `blocked`. The run does not open a browser.
- **Scope**: Result selection.
- **Rationale**: The user required missing evidence to be blocked rather than a launched browser. The reasoning loop reports blocked when telemetry cannot be collected.
- **Evidence**:
  - REQ-002, POL-001, CON-006
  - User decision 2026-11-20
- **Alternatives considered**:
  - **Launch WebArena when the file is missing** — The ADR and the user forbid automating shopping-agent runs.
- **Consequences**:
  - A person must place the evidence file before a non-blocked result is possible.
- **Affected plan steps**: Step 2, Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — Four-of-five saved runs

- **Status**: REQUIRES_ACK
- **Decision**: Consider at most the first ten `runs`. Each considered run needs `telemetry_present` true. A window of five runs with at least four `signal_observed` true values is `support`. Five or more runs with none observed is `contradict`. Any other telemetry-complete set is `inconclusive`.
- **Scope**: `SignalReproducibility`.
- **Rationale**: The reasoning-loop spec states this stopping rule as provisional. The user asked the package to record whether the saved signal is reproducible and did not publish a different threshold.
- **Evidence**:
  - POL-002, REQ-003, REQ-004, REQ-005
  - `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` provisional stopping rule
  - ASS-002
- **Alternatives considered**:
  - **Copy a `result` field from the evidence file** — Skips the reproducibility rule the spec assigns to this agent.
  - **Require ten runs before any judgment** — The spec stops when the threshold is met, including at five runs.
- **Consequences**:
  - A human evidence file that uses different field names is `blocked`.
  - Acknowledgement is required before this rule is implemented.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — No other component imports

- **Status**: DECIDED
- **Decision**: `sandbox_validation` does not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, or `rule_specification`.
- **Scope**: Package boundary.
- **Rationale**: The user forbade imports of other component packages. Agents do not talk to each other.
- **Evidence**:
  - CON-003, CON-004
  - User decision 2026-11-20
- **Alternatives considered**:
  - **Call the orchestrator to fetch the hypothesis** — Couples this package to another component.
- **Consequences**:
  - Callers pass file paths. This package does not discover hypotheses itself.
- **Affected plan steps**: Step 1
- **Supersedes**: None
- **Superseded by**: None

---

## DD-005 — Result fields

- **Status**: DECIDED
- **Decision**: Write `sandbox_results.json` in the caller-supplied directory with exactly `hypothesis_id`, `result`, and `evidence_path`. `hypothesis_id` comes from the hypothesis file (`hypothesis_id`, otherwise `id`). `evidence_path` is the path string the caller passed.
- **Scope**: Result file.
- **Rationale**: The user named those three fields and no others.
- **Evidence**:
  - REQ-001, INV-002, CON-005
- **Alternatives considered**:
  - **Embed the runs in the result file** — Adds fields the user did not request. The evidence path keeps the runs traceable.
- **Consequences**:
  - A second run overwrites the same file name.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-006 — Out of scope records

- **Status**: DECIDED
- **Decision**: Do not write an abuse classification, a deployed detection rule, a faculty report, or a message to another agent.
- **Scope**: Outputs of `SandboxValidation`.
- **Rationale**: The user excluded those outcomes. The initial research scope defers abuse classification, and rules are not deployed by this stage.
- **Evidence**:
  - REQ-006, CON-004, CON-007
  - User decision 2026-11-20
- **Alternatives considered**:
  - **Add an abuse label when the hypothesis mentions abuse** — That is the deferred classification this ticket must not perform.
- **Consequences**:
  - The directory written by one run contains only `sandbox_results.json`.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## Decision completeness

- [x] Every material architecture, boundary, dependency, contract, persistence, policy-placement, and consequential technology choice has a `DD-NNN` entry
- [x] Every active decision cites concrete evidence
- [x] Every active decision records alternatives and consequences
- [x] Every active decision maps to the plan step(s) it governs
- [x] Every `REQUIRES_ACK` decision is reflected in a `READY_FOR_IMPLEMENTATION_WITH_ACK` handoff
- [x] Every `BLOCKED` decision is reflected in a blocked handoff
- [x] Superseded decisions are preserved and linked to their replacements
