# Constraints

---

## Technical constraints

### CON-001

- **Statement**: The research orchestrator is one LangGraph node and does not use a conversational multi-agent framework.
- **Source**: User decision 2026-11-19; `docs/adr/0001-langchain-langgraph.md`
- **Scope**: Orchestrator runtime

## Architectural constraints

### CON-002

- **Statement**: The orchestrator assigns work by storing records and does not send messages to other agents.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Scope**: Assignments and returns

### CON-003

- **Statement**: The orchestrator does not launch a shopping agent. Sandbox runs stay manual on the virtual machine.
- **Source**: User decision 2026-11-19
- **Scope**: Sandbox assignments

## Data constraints

### CON-004

- **Statement**: Standup decisions are stored with the research records they cite.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 2
- **Scope**: Standup output

## Performance and capacity constraints

### CON-005

- **Statement**: A standup has no real-time completion deadline.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 6
- **Scope**: Standup runs

## Deployment and operational constraints

### CON-006

- **Statement**: The faculty final report and presentation are out of scope for this work item.
- **Source**: User decision 2026-11-19
- **Scope**: Deliverables of this ticket

### CON-007

- **Statement**: Production deployment of a detection rule is out of scope. The safety diagram's deployment step is not implemented.
- **Source**: User decision 2026-11-19; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 5
- **Scope**: Rule outcome

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Technical                | 1     |
| Architectural            | 2     |
| Data                     | 1     |
| Performance              | 1     |
| Deployment / operational | 2     |
| **Total**                | **7** |
