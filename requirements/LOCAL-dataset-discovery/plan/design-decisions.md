# Design Decisions

Material design choices that govern the implementation plan. This file is the single source of truth for planning decisions. Write it with `solution-skeleton-spec.md` before `plan.md`.

---

## Header

| Field | Value |
|-------|-------|
| **Work item ID** | LOCAL-dataset-discovery |
| **Requirements base path** | requirements/LOCAL-dataset-discovery/ |
| **Plan base path** | requirements/LOCAL-dataset-discovery/plan/ |
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
| DD-001 | One LangGraph node in `dataset_discovery` calls one LangChain catalog tool | DECIDED | Step 6 |
| DD-002 | Read `hypotheses.json` and write `datasets.json` with no import of the other agent packages | DECIDED | Step 1, Step 3, Step 4 |
| DD-003 | A registry entry keeps the five handoff fields plus the registry facts used to judge suitability | DECIDED | Step 3 |
| DD-004 | Suitability requires labels, coverage, license, a 730-day verification window, and more than a query match | REQUIRES_ACK | Step 2 |
| DD-005 | Hypothesis id and measurement fields are read from the agreed JSON names, and prose measurements fail coverage | REQUIRES_ACK | Step 4 |
| DD-006 | Search when the 24-hour schedule is due or when no suitable entry exists | DECIDED | Step 5, Step 6 |
| DD-007 | Human text is rejected, and the run writes no hypothesis, validation metric, deployed rule, or shopping-agent start | DECIDED | Step 6 |
| DD-008 | Rank catalog passages in memory and inject the catalog so tests do not call the network | DECIDED | Step 6 |

---

## DD-001 — LangGraph node and LangChain tool

- **Status**: DECIDED
- **Decision**: Package `dataset_discovery` exposes one LangGraph node, `DatasetDiscoveryNode`, and that node calls one LangChain tool, `search_dataset_catalog`.
- **Scope**: Runtime of this ticket.
- **Rationale**: ADR 0001 selects LangChain and LangGraph, and the coordination spec forbids agent chat.
- **Evidence**:
  - CON-001, ASS-ARCH-001, `docs/adr/0001-langchain-langgraph.md`
- **Alternatives considered**:
  - **CrewAI or AutoGen conversation** — the ADR rejects conversational delegation.
- **Consequences**:
  - Tests compile a one-node graph and invoke the tool. No other framework is added.
- **Affected plan steps**: Step 6
- **Supersedes**: None
- **Superseded by**: None

---

## DD-002 — JSON records and package boundary

- **Status**: DECIDED
- **Decision**: The node reads `hypotheses.json` and writes `datasets.json` in a directory passed to it. It does not import `research_orchestrator`, `agent_intelligence`, `dataset_validation`, `sandbox_validation`, `detection_rule_specification`, or `independent_evaluator`.
- **Scope**: Persistence and imports.
- **Rationale**: Agents hand off stored JSON, and this ticket must not call the other roles.
- **Evidence**:
  - CON-002, CON-003, CON-004, user role for LOCAL-dataset-discovery
- **Alternatives considered**:
  - **Importing `HypothesisRecord` from agent intelligence** — that package is a parallel ticket and is forbidden here.
- **Consequences**:
  - A structural test rejects those imports. Dataset validation reads `datasets.json` later and is not started here.
- **Affected plan steps**: Step 1, Step 3, Step 4
- **Supersedes**: None
- **Superseded by**: None

---

## DD-003 — Registry entry fields

- **Status**: DECIDED
- **Decision**: Each `datasets.json` entry stores `datasetName`, `sourceUrl`, `title`, `suitability`, `hypothesisId`, `collectionMethod`, `hasSessionIdentifier`, `hasHumanLabel`, `hasAgentLabel`, `license`, and `verifiedAt`.
- **Scope**: Dataset registry contract.
- **Rationale**: The user role requires the first five fields. The retrieval design says the registry also records collection method, session identifiers, human and agent labels, licensing, and verification date so validation does not repeat the search.
- **Evidence**:
  - REQ-001, INV-001, `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` architecture change
- **Alternatives considered**:
  - **Five fields only** — validation would not see the facts behind `suitability`.
- **Consequences**:
  - Readers must tolerate the extra keys. `suitability` is `suitable` or `unsuitable`.
- **Affected plan steps**: Step 3
- **Supersedes**: None
- **Superseded by**: None

---

## DD-004 — Suitability rule and age window

- **Status**: REQUIRES_ACK
- **Decision**: `SuitabilityJudgement` sets `suitable` only when the dataset name, title, and http(s) source URL are non-empty, human and agent labels and a session identifier are present, the license is non-empty, `verifiedAt` is not after the judgment time and not more than 730 days before it, the candidate fields cover every hypothesis measurement field, and the candidate is not flagged as a query-only match. Any other candidate is `unsuitable` and is still stored.
- **Scope**: Suitability outcome.
- **Rationale**: The safety plan requires relevance, coverage, and age. The retrieval note says a query match is not enough. The sources do not state the day count, so 730 days is the planning choice in ASS-003.
- **Evidence**:
  - REQ-002, REQ-004, INV-002, POL-001, CA-001, ASS-003
- **Alternatives considered**:
  - **Title overlap counts as suitable** — contradicted by the retrieval note.
  - **Dropping unsuitable rows** — a later reader could not see the rejection.
- **Consequences**:
  - Tests cover a 730-day date and a 731-day date. Changing the window changes those tests.
- **Affected plan steps**: Step 2
- **Supersedes**: None
- **Superseded by**: None

---

## DD-005 — Hypothesis JSON names

- **Status**: REQUIRES_ACK
- **Decision**: `HypothesisReader` accepts hypothesis id from `id` or `hypothesisId`. Measurement fields come from `measurementFields` when it is a list of strings, otherwise from `measurements` when that value is a list of strings. Prose `measurements` yield no measurement fields, and coverage then fails.
- **Scope**: Read contract for stored hypotheses.
- **Rationale**: Agent intelligence requires signal, observation, sources, and measurements, and it does not publish a frozen field list on this branch. Reading both id names avoids a hard break, and failing closed avoids inventing columns.
- **Evidence**:
  - REQ-001, CA-002, ASS-002, `requirements/LOCAL-agent-intelligence/functional.md` REQ-004
- **Alternatives considered**:
  - **Waiting to import the other package** — forbidden by DD-002.
- **Consequences**:
  - A hypothesis file that uses a different id key is skipped. Prose measurements cannot make a dataset suitable.
- **Affected plan steps**: Step 4
- **Supersedes**: None
- **Superseded by**: None

---

## DD-006 — Schedule and targeted search

- **Status**: DECIDED
- **Decision**: `DiscoverySchedule` defaults to 24 hours. The node searches a hypothesis when the schedule is due or when that hypothesis has no `suitable` entry. A scheduled run stores `lastRunAt` in `discovery_state.json`. A targeted run does not change `lastRunAt`.
- **Scope**: When catalog search runs.
- **Rationale**: The retrieval design runs scheduled searches and also answers a gap when the registry has no suitable candidate. The coordination spec accepts high latency, and the sibling discovery default is 24 hours.
- **Evidence**:
  - REQ-005, `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 2, `docs/specs/Multi_Agent_Coordination_Capstone.md` section 6
- **Alternatives considered**:
  - **Search on every call** — ignores the configured interval once a suitable entry exists.
- **Consequences**:
  - Tests set a 1-hour interval. The first run has no `lastRunAt` and is due.
- **Affected plan steps**: Step 5, Step 6
- **Supersedes**: None
- **Superseded by**: None

---

## DD-007 — Human input, shopping agents, and foreign records

- **Status**: DECIDED
- **Decision**: Non-empty human text raises before any write. The node does not start a shopping agent. The run does not add a hypothesis, a validation metric, or a deployed rule.
- **Scope**: Input and side effects.
- **Rationale**: Human input enters only through the research orchestrator. This ticket discovers datasets and does not research, validate, or deploy.
- **Evidence**:
  - REQ-006, REQ-007, INV-003, POL-003, POL-004, CON-007, CON-008, CON-009
- **Alternatives considered**:
  - **Accepting a free-text research prompt** — would create a second human entry point.
- **Consequences**:
  - Tests patch process launch and compare the store before and after a run.
- **Affected plan steps**: Step 6
- **Supersedes**: None
- **Superseded by**: None

---

## DD-008 — In-memory ranking and injected catalog

- **Status**: DECIDED
- **Decision**: The node ranks catalog passages with in-memory token vectors and cosine similarity, keeps the five highest, and does not open a vector database. The catalog callable is injected.
- **Scope**: Retrieval inside this node.
- **Rationale**: The retrieval design allows in-memory ranking and makes persistent vectors optional. Tests must not depend on a search API key.
- **Evidence**:
  - ASS-004, `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` sections 2 and 4
- **Alternatives considered**:
  - **Live Tavily or Exa calls** — no credential is in scope, and results would not be repeatable.
- **Consequences**:
  - Ranking quality is lexical. Suitability remains a separate check from rank.
- **Affected plan steps**: Step 6
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
