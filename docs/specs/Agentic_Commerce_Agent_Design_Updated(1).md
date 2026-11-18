# Autonomous Threat Detection Researcher for Agentic Commerce

Initial scope: Distinguish AI shopping agent sessions from human shopping sessions. Detection of abusive AI agents is deferred. Four specialist agents operate independently; an orchestrator assigns tasks and reads their stored outputs.

## 1. Reasoning loops

### Threat Intelligence & Hypothesis Generation Agent — ReAct + Tree of Thoughts

- **Reason:** Identify gaps in existing hypotheses and select AI shopping technologies to investigate.
- **Act:** Search agent documentation, technical publications, and browser automation research.
- **Observe:** Extract candidate signals, including User-Agent strings, IP ranges, interaction patterns, and fingerprint attributes.
- **Explore:** Generate alternative explanations and compare their technical plausibility.
- **Reason:** Decide whether the signal is observable, testable, and supported by a source. If evidence is insufficient, choose a new search.
- **Act:** Check previous investigations; save a testable hypothesis with sources and validation requirements, or record the unresolved question.

**Decision loop:** Each observation changes the next search or hypothesis. Stop when a testable hypothesis is recorded or relevant sources are exhausted.

### Dataset Validation Agent — Plan-and-Execute + ReAct

- **Plan:** Define required labels, telemetry fields, sample coverage, and evaluation metrics.
- **Act:** Retrieve candidate datasets and inspect schemas, labels, and data quality.
- **Observe and decide:** If no dataset meets the criteria, stop and report the missing requirements; do not substitute unsuitable data.
- **Act:** Select an analysis method and run Python calculations.
- **Observe:** Inspect signal prevalence, discriminative power, false-positive rates, and possible confounders.
- **Reason:** Run additional checks if results are ambiguous; otherwise record the conclusion and limitations.

**Decision loop:** Dataset suitability controls whether analysis starts; measured results determine whether further calculations are justified.

### Sandbox Validation Agent — Reflexion

- **Plan:** Specify the expected signal, controlled scenario, telemetry, reproducibility threshold, and attempt limit.
- **Act:** Run an AI shopping agent in the preconfigured e-commerce sandbox.
- **Observe:** Capture telemetry and compare observed signals with the hypothesis.
- **Reflect:** Compare runs, identify inconsistencies, and distinguish failed execution from a missing signal.
- **Decide:** Repeat valid runs under equivalent conditions; correct invalid experimental setups before retrying.
- **Evaluate:** Calculate reproduction rate and stop when the threshold is met or the attempt limit is reached.

**Provisional criterion:** Signal present in at least four of five independent valid runs; maximum ten attempts. Report blocked or unreproduced results. Reproduction does not establish human-session false-positive rates.

### Detection Rule Specification Agent — Generate–Critique–Revise

- **Generate:** Translate validated signals into telemetry requirements, detection conditions, and thresholds.
- **Critique:** Compare every condition with validation reports, known exceptions, and observed false positives.
- **Reason:** Identify unsupported thresholds, missing fields, or contradictory evidence.
- **Revise:** Modify the specification and assign confidence based on the available validation evidence.
- **Evaluate:** Repeat until each condition has supporting evidence, or report that no defensible rule can be specified.

**Output:** Versioned, machine-readable specification for human review; no automatic deployment.

### Research Orchestrator — Plan-and-Execute

- **Observe:** At scheduled standups, read hypothesis statuses, validation reports, blocked tasks, and rule drafts.
- **Reason:** Identify untested hypotheses, conflicting evidence, and stalled investigations.
- **Plan and act:** Prioritise work and assign hypotheses to independent validators.
- **Evaluate:** Send a hypothesis for rule specification if at least one validator supports it and the other has no contradictory result.
- **Replan:** Return conflicts for investigation, lower evidence confidence when only one method supports a signal, and store next actions.

**Decision loop:** Each standup ends after assignments and statuses are saved; the next standup uses updated evidence.

## 2. Memory

**Short-term:** Each agent retains current sources, intermediate observations, calculations, experiment counts, draft rule conditions, and pending decisions. This context determines the next action within its run.

**Long-term:** Persistent storage holds versioned hypotheses, validation reports, rule specifications, and research status, including blocked and unfinished investigations. Links preserve the evidence supporting each rule.

## 3. External tools

**Retrieval and grounding:** Web search and document access supply verifiable technical evidence. Dataset retrieval supplies labelled session records.

**Computation:** Python measures signal prevalence and false-positive rates.

**Experimental grounding:** Sandbox execution and telemetry collection test observable behaviour; repeated runs measure reproducibility. Persistent storage preserves results across cycles.

**Tool-dependent task:** A proposed fingerprint signal cannot be evaluated for false positives without labelled session data and statistical computation.

## 4. Improvement over prompt-only reasoning

Hypotheses require external sources; rule specifications require dataset evidence or reproducible sandbox observations. Missing data and contradictory findings remain explicit. A single successful validation method permits a lower-confidence specification only when the other method has not contradicted it.

**Failure mode:** An LLM may propose detection rules based on unverified assumptions, leading to false positives.
