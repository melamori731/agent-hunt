# Policies

Software architecture policies: business or operational rules expressed in terms of what the system chooses to do. A policy captures system decision logic, not external process metadata.

---

## Business decision policies

None.

## Operational decision policies

None.

## Routing and classification policies

#### POL-001

- **Statement**: When the evidence file is missing, unreadable, empty, mismatched to the hypothesis, or missing telemetry on a considered run, the result is `blocked`.
- **Source**: User decision 2026-11-20; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` sandbox step 5
- **Verification**: Judge each of those evidence cases and confirm `blocked`.
- **Related requirements**: REQ-002

#### POL-002

- **Statement**: Using at most the first ten runs, five telemetry-complete runs with at least four signal observations yield `support`, five or more telemetry-complete runs with no signal observation yield `contradict`, and every other telemetry-complete set yields `inconclusive`.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` provisional stopping rule
- **Verification**: Judge a four-of-five case, a five-run absence, and a one-of-five case.
- **Related requirements**: REQ-003, REQ-004, REQ-005

## Data handling policies

None.

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
| Business decision        | 0     |
| Operational decision     | 0     |
| Routing / classification | 2     |
| Data handling            | 0     |
| Security behavior        | 0     |
| Fallback / exception     | 0     |
| User experience          | 0     |
| **Total**                | **2** |
