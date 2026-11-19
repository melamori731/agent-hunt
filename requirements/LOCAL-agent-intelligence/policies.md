# Policies

---

## Business decision policies

### POL-001

- **Statement**: When retrieved sources do not support a testable shopping-session signal, the agent stores an unresolved investigation and does not store a hypothesis.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Threat Intelligence steps 5–6
- **Verification**: Run one investigation whose sources omit the signal and confirm the unresolved record exists and the hypothesis count is unchanged.
- **Related requirements**: REQ-007, INV-001

## Operational decision policies

### POL-004

- **Statement**: The system end-to-end test loads manual virtual-machine evidence from a saved record and does not start a shopping agent.
- **Source**: User decision 2026-11-19
- **Verification**: Run the end-to-end test and confirm it performs no shopping-agent process start.
- **Related requirements**: REQ-008

## Routing and classification policies

None.

## Data handling policies

### POL-002

- **Statement**: When a hypothesis for the same assistant and the same signal is already stored, the agent does not store another hypothesis.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Threat Intelligence step 4
- **Verification**: Repeat one stored assistant and signal and confirm the hypothesis count stays the same.
- **Related requirements**: REQ-006

### POL-003

- **Statement**: An orchestrator-assigned registry addition and a scheduled-discovery registry addition both produce a report with the assistant name, the cited sources, and the entry origin.
- **Source**: User decision 2026-11-19
- **Verification**: Create one entry of each origin and confirm both reports contain those three items.
- **Related requirements**: REQ-001, REQ-002, REQ-003

## Security behavior policies

None.

## Fallback and exception policies

None.

## User experience policies

None.

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Business decision        | 1     |
| Operational decision     | 1     |
| Routing / classification | 0     |
| Data handling            | 2     |
| Security behavior        | 0     |
| Fallback / exception     | 0     |
| User experience          | 0     |
| **Total**                | **4** |
