# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Agent registry

#### REQ-001

- **Statement**: When the orchestrator assigns a human-named AI assistant, the agent-intelligence agent retrieves external sources about that assistant and stores one registry entry that cites those sources.
- **Source**: User decision 2026-11-19; `docs/specs/Multi_Agent_Coordination_Capstone.md` sections 1 and 3; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1 (Threat Intelligence steps 1–3)
- **Verification**: Deliver one orchestrator assignment that names an assistant and confirm a new registry entry lists at least one retrieved source. Confirm this agent has no separate human entry point.
- **Dependencies**: QR-001, INV-003, POL-003

#### REQ-002

- **Statement**: On each scheduled discovery run, the agent-intelligence agent searches for agents and AI assistants that are not already in the registry and stores one new registry entry for each assistant it adds.
- **Source**: User decision 2026-11-19
- **Verification**: Given a fixture source that describes an assistant absent from the registry, run one scheduled discovery and confirm exactly one new entry for that assistant.
- **Dependencies**: REQ-003, POL-003

#### REQ-003

- **Statement**: Each registry addition produces one human-readable report that names the assistant, lists the cited sources, and states whether the entry came from an orchestrator assignment or from scheduled discovery.
- **Source**: User decision 2026-11-19
- **Verification**: Add one requested entry and one discovered entry, and confirm each addition has one report with those three fields.
- **Dependencies**: INV-003, POL-003

### Hypotheses

#### REQ-004

- **Statement**: The agent stores a hypothesis only when the record names the observable shopping-session signal, the expected observation, the supporting sources, and the measurements validation must perform.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Threat Intelligence step 3; `docs/specs/Threat_Intelligence_ReAct_Decision.md`
- **Verification**: Store one complete hypothesis and reject one record that omits any of those four fields.
- **Dependencies**: INV-001, POL-001

#### REQ-005

- **Statement**: The agent does not store a hypothesis whose purpose is to distinguish abusive or malicious AI agents from legitimate AI agents.
- **Source**: User decision 2026-11-19; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` opening scope
- **Verification**: Submit a research request limited to abusive-versus-legitimate classification and confirm no hypothesis is stored.
- **Dependencies**: INV-002

#### REQ-006

- **Statement**: The agent does not store a second hypothesis for an assistant and signal pair that is already stored.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Threat Intelligence step 4
- **Verification**: Store one hypothesis, repeat the same assistant and signal, and confirm the store still contains one hypothesis.
- **Dependencies**: POL-002

#### REQ-007

- **Statement**: When retrieved sources do not support a testable shopping-session signal, the agent stores an unresolved investigation and does not store a hypothesis.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Threat Intelligence steps 5–6
- **Verification**: Provide only non-evidential sources and confirm an unresolved record exists and no hypothesis was added.
- **Dependencies**: POL-001

### System end-to-end test

#### REQ-008

- **Statement**: An end-to-end test starts from human input accepted by the orchestrator, uses stored research outputs and recorded manual virtual-machine evidence, and passes only when a submitted rule specification contains the research sources and the validation results.
- **Source**: User decisions 2026-11-19 (submitted rule specification; manual VM sandbox; plan a system end-to-end test; human input feeds the orchestrator)
- **Verification**: Run the test once with a complete evidence record and once with the validation results removed, and confirm only the complete record passes.
- **Dependencies**: QR-003, POL-004, INV-004

#### REQ-009

- **Statement**: On each scheduled discovery run, the agent searches for a new observable shopping-session pattern for each assistant already in the registry and stores a hypothesis or an unresolved investigation for each new pattern it finds.
- **Source**: User decision 2026-11-19
- **Verification**: With one registered assistant and no stored hypothesis, provide a fixture source that describes a new signal and confirm the scheduled run stores one hypothesis or one unresolved investigation for that assistant.
- **Dependencies**: REQ-004, REQ-006, REQ-007, POL-002

#### REQ-010

- **Statement**: The agent starts a discovery run when the configured interval since the previous scheduled run has elapsed, and that interval defaults to 24 hours.
- **Source**: User decision 2026-11-19; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 6
- **Verification**: With the default interval, confirm a scheduled run at time T does not start another at T plus 23 hours and does start one at T plus 24 hours. With the interval set to 1 hour, confirm a scheduled run starts at T plus 1 hour.
- **Dependencies**: REQ-002, REQ-009

---

## Summary

| Verified | Total |
|----------|-------|
| 10 | 10 |
