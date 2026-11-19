# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Agent registry

#### REQ-001

- **Statement**: When a human names an AI assistant, the agent-intelligence agent retrieves external sources about that assistant and stores one registry entry that cites those sources.
- **Source**: User decision 2026-11-19; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1 (Threat Intelligence steps 1–3)
- **Verification**: Submit one named assistant and confirm a new registry entry lists at least one retrieved source for it.
- **Dependencies**: QR-001, INV-003, POL-003

#### REQ-002

- **Statement**: The agent-intelligence agent searches for AI assistants that are not already in the registry and stores one new registry entry for each assistant it adds.
- **Source**: User decision 2026-11-19
- **Verification**: Given a fixture source that describes an assistant absent from the registry, run discovery and confirm exactly one new entry for that assistant.
- **Dependencies**: REQ-003, POL-003

#### REQ-003

- **Statement**: Each registry addition produces one human-readable report that names the assistant, lists the cited sources, and states whether a human requested the entry or the agent discovered it.
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

- **Statement**: An end-to-end test starts from a human request to research a named assistant, uses stored research outputs and recorded manual virtual-machine evidence, and passes only when a submitted rule specification contains the research sources and the validation results.
- **Source**: User decisions 2026-11-19 (submitted rule specification; manual VM sandbox; plan a system end-to-end test)
- **Verification**: Run the test once with a complete evidence record and once with the validation results removed, and confirm only the complete record passes.
- **Dependencies**: QR-003, POL-004, INV-004

---

## Summary

| Verified | Total |
|----------|-------|
| 8 | 8 |
