# Constraints

---

## Technical constraints

### CON-001

- **Statement**: Agent intelligence research uses a ReAct loop and does not use Tree of Thoughts.
- **Source**: `docs/specs/Threat_Intelligence_ReAct_Decision.md`
- **Scope**: Agent-intelligence reasoning

### CON-002

- **Statement**: The agent-intelligence agent calls tools through LangChain, and its stage is a LangGraph node.
- **Source**: User decision 2026-11-19 accepting LangChain with LangGraph; `docs/adr/0001-langchain-langgraph.md`
- **Scope**: This agent's runtime

## Architectural constraints

### CON-003

- **Statement**: The agent does not send messages to other agents; other stages read its stored records.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` opening
- **Scope**: Agent-intelligence outputs

### CON-004

- **Statement**: Shopping-agent execution stays manual on the sandbox virtual machine, and automating those runs is out of scope for the MVP.
- **Source**: User decision 2026-11-19
- **Scope**: Sandbox evidence consumed by research outputs and the end-to-end test

## Data constraints

### CON-005

- **Statement**: Research sources are public documents and measurements, not customer telemetry.
- **Source**: `docs/specs/Agentic_Commerce_Threat_Researcher_Proposal.md` section 5; `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` section 4
- **Scope**: Retrieval inputs

## Performance and capacity constraints

### CON-006

- **Statement**: A research run has no real-time completion deadline.
- **Source**: `docs/specs/Multi_Agent_Coordination_Capstone.md` section 6
- **Scope**: Agent-intelligence runs

## Deployment and operational constraints

### CON-007

- **Statement**: The faculty final report and presentation are out of scope for this work item.
- **Source**: User decision 2026-11-19
- **Scope**: Deliverables of this ticket

### CON-008

- **Statement**: A named-assistant research task reaches this agent only as an orchestrator assignment, and this agent does not take human input directly.
- **Source**: User decision 2026-11-19; `docs/specs/Multi_Agent_Coordination_Capstone.md` sections 1 and 3
- **Scope**: Entry to agent intelligence

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Technical                | 2     |
| Architectural            | 2     |
| Data                     | 1     |
| Performance              | 1     |
| Deployment / operational | 2     |
| **Total**                | **8** |
