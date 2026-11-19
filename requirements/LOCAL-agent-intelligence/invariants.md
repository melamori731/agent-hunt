# Invariants

---

## Data invariants

### INV-001

- **Statement**: Every stored hypothesis cites at least one source.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 4
- **Verification**: Attempt to store a hypothesis with an empty source list and confirm the store rejects it.
- **If violated**: A later rule specification can cite a signal that has no research source.

## Integrity invariants

### INV-003

- **Statement**: Every registry addition has exactly one human-readable report.
- **Source**: User decision 2026-11-19
- **Verification**: Add one registry entry and confirm the report count for that entry is one.
- **If violated**: A human does not see that an assistant was added.

## Business logic invariants

### INV-002

- **Statement**: No stored hypothesis classifies an assistant as abusive, malicious, or legitimate.
- **Source**: User decision 2026-11-19
- **Verification**: Search stored hypotheses for an abuse or legitimacy classification and confirm none exist.
- **If violated**: The agent researches a decision that this build excludes.

## Security invariants

### INV-004

- **Statement**: This agent does not write a deployed detection rule.
- **Source**: `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` section 1, Detection Rule Specification step 6; user decision 2026-11-19
- **Verification**: Finish a research run and confirm the only new records are registry entries, reports, hypotheses, or unresolved investigations.
- **If violated**: An unreviewed rule leaves the research stage.

## Consistency invariants

None.

---

## Summary

- **Total invariants**: 4
