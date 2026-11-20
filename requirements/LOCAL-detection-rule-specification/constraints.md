# Constraints

---

## Technical constraints

### CON-001

- **Statement**: The component runs as a LangGraph node using LangChain, and this ticket does not replace that framework.
- **Source**: `docs/adr/0001-langchain-langgraph.md`; user instruction 2026-11-20
- **Scope**: Detection rule specification runtime

## Architectural constraints

### CON-002

- **Statement**: Package `detection_rule_specification` does not import other component packages.
- **Source**: User settled scope 2026-11-20
- **Scope**: Package imports

### CON-003

- **Statement**: The component does not launch a shopping agent.
- **Source**: User settled scope 2026-11-20; `docs/adr/0001-langchain-langgraph.md`
- **Scope**: Sandbox and shopping-agent execution

## Data constraints

### CON-004

- **Statement**: The specification record is stored for a human and is not a deployment configuration change.
- **Source**: User settled scope 2026-11-20; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 7
- **Scope**: `rule_specifications.json`

## Performance and capacity constraints

None.

## Deployment and operational constraints

### CON-005

- **Statement**: This component does not research publications, discover datasets, or execute the sandbox.
- **Source**: User settled scope 2026-11-20
- **Scope**: Tools and side effects

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Technical                | 1     |
| Architectural            | 2     |
| Data                     | 1     |
| Performance              | 0     |
| Deployment / operational | 1     |
| **Total**                | **5** |
