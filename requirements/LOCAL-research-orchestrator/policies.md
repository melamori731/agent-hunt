# Policies

---

## Business decision policies

### POL-001

- **Statement**: When the independent evaluator result is PASS and the stage checks pass, the orchestrator advances the task to the next stage.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Verification**: Provide a PASS result for a task whose checks pass and confirm the stage advances once.
- **Related requirements**: REQ-006

## Operational decision policies

### POL-002

- **Statement**: When a validation failure is correctable and the rework count is below the configured limit, the orchestrator returns the task to the responsible agent.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Verification**: With the limit set to 2 and the rework count at 1, submit one correctable failure and confirm one return assignment.
- **Related requirements**: REQ-005, REQ-008

### POL-003

- **Statement**: When results contradict, rework has reached the configured limit, or the finding is marked high-risk, the orchestrator suspends the task for human review.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Orchestrator step 4
- **Verification**: Submit one contradiction and confirm the task is suspended and has no new validator assignment.
- **Related requirements**: REQ-005, REQ-008

## Routing and classification policies

None.

## Data handling policies

None.

## Security behavior policies

### POL-004

- **Statement**: When verification is impossible or the task records a security violation, the orchestrator terminates that task and does not assign further work for it.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 4
- **Verification**: Submit one security-violation record and confirm the task is terminated and receives no later assignment.
- **Related requirements**: REQ-006

## Fallback and exception policies

None.

## User experience policies

None.

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Business decision        | 1     |
| Operational decision     | 2     |
| Routing / classification | 0     |
| Data handling            | 0     |
| Security behavior        | 1     |
| Fallback / exception     | 0     |
| User experience          | 0     |
| **Total**                | **4** |
