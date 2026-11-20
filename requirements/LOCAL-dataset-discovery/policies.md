# Policies

---

## Business decision policies

### POL-001

- **Statement**: When any suitability check fails, the recorded suitability is `unsuitable`.
- **Source**: `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` dataset suitability stage
- **Verification**: Fail one check at a time for labels, coverage, age, license, and query-only match, and confirm each judgment is `unsuitable`.
- **Related requirements**: REQ-002, REQ-004

### POL-002

- **Statement**: The registry stores at most one entry for a dataset name and hypothesis id pair.
- **Source**: `docs/specs/shopping_agent_retrieval_checkpoint_polished(1).md` architecture change
- **Verification**: Store the same pair twice and confirm one entry remains.
- **Related requirements**: REQ-003

## Operational decision policies

## Routing and classification policies

## Data handling policies

### POL-003

- **Statement**: When the caller supplies human text, the agent writes no registry entry.
- **Source**: User decision 2026-11-20
- **Verification**: Pass non-empty human text into discovery and confirm `datasets.json` is unchanged.
- **Related requirements**: REQ-006

### POL-004

- **Statement**: Dataset discovery writes dataset registry records and does not write hypothesis records, validation metrics, or deployed rules.
- **Source**: User decision 2026-11-20; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: Run discovery and confirm the only new research record is a dataset registry entry.
- **Related requirements**: REQ-007

## Security behavior policies

## Fallback and exception policies

## User experience policies

---

## Summary

| Category                 | Count |
| ------------------------ | ----- |
| Business decision        | 2     |
| Operational decision     | 0     |
| Routing / classification | 0     |
| Data handling            | 2     |
| Security behavior        | 0     |
| Fallback / exception     | 0     |
| User experience          | 0     |
| **Total**                | **4** |
