# Functional Requirements

Behavior the system must exhibit. Each item must be testable and traceable to a source.

---

## Requirements by area

### Hypothesis evidence

#### REQ-001

- **Statement**: When the stored hypothesis for a hypothesis id contains at least one source, the evaluator writes an evaluation whose hypothesis_id is that id, whose stage is hypothesis, whose result is PASS, and whose trigger states that sources are present.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` sections 4 and 5
- **Verification**: Store one hypothesis with one source, run the hypothesis check, and confirm evaluations.json contains that PASS record.
- **Dependencies**: POL-001, INV-002

#### REQ-002

- **Statement**: When the stored hypothesis is missing or contains no source, the evaluator writes result REWORK for stage hypothesis and leaves every workflow stage file unchanged.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` sections 4 and 5
- **Verification**: Run the hypothesis check with an empty source list and again with no hypothesis record, and confirm both evaluations are REWORK and the stage file bytes are unchanged.
- **Dependencies**: INV-001, POL-001

### Validation evidence

#### REQ-003

- **Statement**: When the stored dataset validation and sandbox validation for a hypothesis id are both present and do not contradict, the evaluator writes result PASS for stage validation.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 5; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 1
- **Verification**: Store support with support, and store support with inconclusive, and confirm both checks write PASS.
- **Dependencies**: POL-002, INV-002

#### REQ-004

- **Statement**: When either validation result is missing, or the dataset outcome is support and the sandbox outcome is reject, or the reverse, the evaluator writes result REWORK for stage validation and leaves every workflow stage file unchanged.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` sections 4 and 5
- **Verification**: Run one missing-sandbox check and one support-versus-reject check, and confirm both evaluations are REWORK and the stage file bytes are unchanged.
- **Dependencies**: INV-001, POL-002

### Rule specification evidence

#### REQ-005

- **Statement**: When the stored rule specification for a hypothesis id is submitted, is not deployed, and cites at least one research source and at least one validation result, the evaluator writes result PASS for stage rule_specification.
- **Source**: User order for LOCAL-independent-evaluator; `docs/adr/0001-langchain-langgraph.md`; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 1
- **Verification**: Store one submitted, non-deployed specification with both citations and confirm the evaluation result is PASS.
- **Dependencies**: POL-003, INV-002

#### REQ-006

- **Statement**: When the rule specification is missing, is not submitted, is deployed, or lacks a research source or a validation result, the evaluator writes result REWORK for stage rule_specification and leaves every workflow stage file unchanged.
- **Source**: User order for LOCAL-independent-evaluator; `docs/specs/Agentic_Threat_Detection_Safety_Intervention_Plan.md` section 7
- **Verification**: Run one check for each of those five defects and confirm each evaluation is REWORK and the stage file bytes are unchanged.
- **Dependencies**: INV-001, POL-003

### Out of scope behavior

#### REQ-007

- **Statement**: An evaluation writes no abuse, malicious, or legitimate label, starts no shopping-agent process, writes no message to another agent, and writes no faculty report.
- **Source**: User order for LOCAL-independent-evaluator; `docs/adr/0001-langchain-langgraph.md`; `docs/specs/Multi_Agent_Coordination_Capstone.md` section 5
- **Verification**: Run one check while process launch and outbound message are observable, and confirm the evaluation has only hypothesis_id, stage, result, and trigger, and that no process, message, or faculty report was written.
- **Dependencies**: POL-004, CON-002, CON-003, CON-004

---

## Summary

| Verified | Total |
|----------|-------|
| 7 | 7 |
