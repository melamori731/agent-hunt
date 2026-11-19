# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-threat-intelligence |
| **Requirements base path** | requirements/LOCAL-threat-intelligence/ |
| **Plan base path** | requirements/LOCAL-threat-intelligence/plan/ |
| **Plan** | [plan.md](./plan.md) (written after human approval) |
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
| DD-001 | LangChain ReAct tools inside one LangGraph node | DECIDED | Step 2 |
| DD-002 | JSON files are the research record store | DECIDED | Step 1, Step 3 |
| DD-003 | This node writes records and does not call other agents | DECIDED | Step 2 |
| DD-004 | Sandbox evidence is a saved VM record, with no agent launcher | DECIDED | Step 4 |
| DD-005 | The system end-to-end test asserts a submitted rule specification | DECIDED | Step 4 |
| DD-006 | This node never writes a deployed rule | DECIDED | Step 2 |

---

## DD-001 — LangChain ReAct tools inside one LangGraph node

- **Status**: DECIDED
- **Decision**: Threat intelligence runs as one LangGraph node whose research loop is LangChain ReAct with LangChain tools for search and retrieval.
- **Scope**: Runtime of this agent.
- **Rationale**: The accepted framework decision matches the ReAct loop and the one-way stage graph.
- **Evidence**:
  - CON-001, CON-002, ASS-ARCH-001
  - `docs/adr/0001-langchain-langgraph.md`
  - `docs/specs/Threat_Intelligence_ReAct_Decision.md`
- **Alternatives considered**:
  - **CrewAI** — conversational delegation conflicts with one-way records.
  - **A custom loop** — would rebuild tool calling and checkpoints.
- **Consequences**:
  - Retrieval and hypothesis drafting stay inside this node.
  - Tree of Thoughts is not added.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — JSON files are the research record store

- **Status**: DECIDED
- **Decision**: Registry entries, reports, hypotheses, and unresolved investigations are stored as JSON files that survive the end of a run.
- **Scope**: Persistence for this agent.
- **Rationale**: The MVP needs durable records without operating a separate database. The retrieval note allows in-memory ranking and treats a vector database as optional.
- **Evidence**:
  - QR-002
  - `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 2
  - `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 2
- **Alternatives considered**:
  - **SQLite** — stronger queries, and an extra engine the MVP does not need.
  - **Chat checkpoints only** — they do not keep versioned research records after the run.
- **Consequences**:
  - Other stages read these files. They do not receive messages.
  - A later ticket can replace the file store if query needs grow.
- **Affected plan steps**: Step 1, Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — This node writes records and does not call other agents

- **Status**: DECIDED
- **Decision**: Dataset validation, sandbox validation, the independent evaluator, and rule specification are not invoked by this node.
- **Scope**: Boundary of the threat-intelligence node.
- **Rationale**: Coordination is one-way through stored records.
- **Evidence**:
  - CON-003, ASS-ARCH-002
  - `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Alternatives considered**:
  - **Direct tool calls to the other agents** — that is agent-to-agent dialogue, which the coordination spec excludes.
- **Consequences**:
  - The end-to-end test loads downstream results from records rather than from return values of this node.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — Sandbox evidence is a saved VM record, with no agent launcher

- **Status**: DECIDED
- **Decision**: The MVP sandbox is a virtual machine with one self-hosted shopping page. A person runs assistants such as Muse there. This system stores and reads the evidence file. It does not start those assistants.
- **Scope**: Evidence consumed by the end-to-end test.
- **Rationale**: Muse and similar vendor-hosted assistants cannot be launched by this codebase. The user limited the MVP to manual runs.
- **Evidence**:
  - CON-004, POL-004, ASS-002
  - User decision 2026-11-19
- **Alternatives considered**:
  - **WebArena** — its observations are page content, not the client telemetry under test, and it does not start Muse.
  - **Automating browser-use in the MVP** — the user placed that automation out of scope.
- **Consequences**:
  - A missing evidence file blocks the sandbox portion of the system test.
  - Repeatability depends on the saved file, not on a new manual run.
- **Affected plan steps**: Step 4
- **Supersedes**: None
- **Superseded by**: None

---

## DD-005 — The system end-to-end test asserts a submitted rule specification

- **Status**: DECIDED
- **Decision**: The planned system test is one path: a human names an assistant; the registry entry and report exist; a hypothesis or unresolved investigation is stored; dataset and sandbox results are loaded from saved records, including the manual VM evidence; the independent evaluator outcome is loaded from a saved record; a submitted rule specification passes only when it contains the research sources and the validation results. The test does not deploy a rule and does not start a shopping agent.
- **Scope**: Verification of the pipeline that begins at this agent.
- **Rationale**: The user asked for that outcome and for an end-to-end test of the system. Planning rules require the scenario to be specified before implementation and allow it to fail until the production path exists.
- **Evidence**:
  - REQ-008, QR-003, POL-004, CA-001
  - User decision 2026-11-19
- **Alternatives considered**:
  - **A threat-intelligence-only test with no rule specification** — it would not check the outcome the user set.
  - **A live Muse run inside the test** — automation of those agents is out of scope for the MVP.
- **Consequences**:
  - The scenario is written in `integration-test-scenarios.md` after skeleton approval.
  - The test stays red until the other stage records and the rule specification exist.
  - This delivery dependency is the acknowledgement reason.
- **Affected plan steps**: Step 4
- **Supersedes**: None
- **Superseded by**: None

---

## DD-006 — This node never writes a deployed rule

- **Status**: DECIDED
- **Decision**: Research output is limited to registry entries, reports, hypotheses, and unresolved investigations.
- **Scope**: Writes performed by this node.
- **Rationale**: Deployment is out of scope. The system outcome is a submitted specification.
- **Evidence**:
  - INV-004, REQ-005
  - User decision 2026-11-19
- **Alternatives considered**:
  - **Writing a rule file from this node** — that skips validation and human submission.
- **Consequences**:
  - Rule-template layout beyond research sources and validation results belongs to the rule-specification work item.
- **Affected plan steps**: Step 2
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
