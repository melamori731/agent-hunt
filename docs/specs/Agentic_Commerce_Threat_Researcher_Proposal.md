# Capstone Project: Autonomous Threat Detection Researcher for Agentic Commerce

## 1. Project Description

The agent will research behavioural signals that can distinguish:

- Human shoppers from AI shopping agents.
- Legitimate AI shopping agents from malicious or abusive agents.

It will analyse browsing activity, identify potential detection signals, formulate hypotheses, and test them against behavioural data.

The intended users are cybersecurity researchers, fraud prevention specialists, and detection engineers working on e-commerce platforms.

## 2. Why a Stand-Alone LLM Is Insufficient

An LLM can suggest potential detection signals but cannot establish their effectiveness without empirical testing.

The agent must access behavioural datasets, execute statistical analyses, evaluate detection accuracy and false-positive rates, and revise hypotheses based on experimental results.

## 3. Environment and Resources

- **Research sources:** Cybersecurity publications and research on AI agents, bot detection, and e-commerce abuse.
- **Behavioural data:** Public datasets of human browsing activity and recorded AI-agent interactions.
- **Experimental environment:** A controlled e-commerce platform (WebArena) for generating legitimate and simulated abusive agent sessions.
- **Analytical tools:** Python-based feature extraction, statistical analysis, and detection evaluation.
- **Research memory:** A database of hypotheses, experiments, results, and previously investigated signals.

## 4. Agent Actions

1. Research existing detection methods and available behavioural data.
2. Identify candidate signals and formulate testable hypotheses.
3. Design experiments to measure their effectiveness.
4. Execute analyses using external tools.
5. Evaluate detection accuracy, false-positive rates, and generalisation across different agents.
6. Refine or reject hypotheses based on results.
7. Produce reports documenting validated signals, supporting evidence, and limitations.

## 5. Feedback and Iteration

Experimental results will determine the agent’s next actions. Inconclusive findings will trigger additional experiments or revised hypotheses.

The agent will retain previous results to avoid repeating unsuccessful investigations. Users will review findings and provide feedback on proposed signals and research priorities.

## Expected Outcome

A research agent that discovers and experimentally evaluates behavioural signals for detecting AI-driven activity and abuse in e-commerce.

The initial version will use public datasets and controlled experiments. A future commercial version could analyse customer-provided telemetry to identify and validate new detection signals.
