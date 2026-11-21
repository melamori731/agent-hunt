# Conflicts and Ambiguities

---

## Blocking

| ID | Description | Source | Severity |
|----|-------------|--------|----------|

## Risky

| ID | Description | Source | Severity |
|----|-------------|--------|----------|
| CA-001 | The safety plan names age as a suitability check for REQ-002 and POL-001, and no source states the number of days that makes a verification date too old. | `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` dataset suitability stage | risky |
| CA-002 | REQ-001 reads a hypothesis id and measurement fields from JSON, and the parallel agent-intelligence ticket owns that record shape, which is not implemented on this branch. | `requirements/LOCAL-agent-intelligence/functional.md` REQ-004; user role for LOCAL-dataset-discovery | risky |

## Informational

| ID | Description | Source | Severity |
|----|-------------|--------|----------|

---

## Summary

| Type | Blocking | Risky | Informational | Total |
|------|----------|-------|---------------|-------|
| Conflicts | 0 | 0 | 0 | 0 |
| Ambiguities | 0 | 2 | 0 | 2 |
| **Total** | **0** | **2** | **0** | **2** |
