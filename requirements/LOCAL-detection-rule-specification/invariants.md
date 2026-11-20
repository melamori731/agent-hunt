# Invariants

---

## Data invariants

### INV-001

- **Statement**: Every stored rule specification has submitted true and deployed false.
- **Source**: User settled scope 2026-11-20; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 7
- **Verification**: Build a specification and confirm those two flags, and reject a record that sets deployed true.
- **If violated**: A detection rule would be treated as deployed.

### INV-003

- **Statement**: Every stored research source has a URL and a title, and every stored specification includes both a dataset result and a sandbox result.
- **Source**: User settled scope 2026-11-20
- **Verification**: Reject a record that omits a source URL, a source title, the dataset result, or the sandbox result.
- **If violated**: The human reviewer would lack the evidence the specification must carry.

## Integrity invariants

None.

## Business logic invariants

### INV-002

- **Statement**: A stored rule specification contains no abuse classification and no legitimacy classification.
- **Source**: User settled scope 2026-11-20; `docs/specs/Agentic_Commerce_Agent_Design_Reasoning_Loops.md` opening scope
- **Verification**: Inspect a written specification and confirm it has no abuse or legitimacy field.
- **If violated**: This component would decide the deferred abuse phase.

## Security invariants

None.

## Consistency invariants

None.

---

## Summary

- **Total invariants**: 3
