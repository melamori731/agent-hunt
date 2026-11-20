# ADR 0001 — LangChain with LangGraph

**Status:** Accepted

**Date:** 2026-11-19 (Europe/Dublin)

## Context

The system is an orchestrated research pipeline that distinguishes AI shopping sessions from human shopping sessions. Specialized roles pass structured records. Execution is mostly sequential, with dataset validation and sandbox validation able to proceed independently, and with retries owned by the orchestrator. Agents do not talk to each other. Agent intelligence uses ReAct and does not use Tree of Thoughts. Each run keeps short-term notes. Hypotheses, validation reports, and rule specifications are versioned records. Tools are web retrieval, dataset access, Python measurement, and sandbox telemetry. A rule is submitted only with research sources and validation results. Unsafe or unsupported work is rejected or escalated.

The sandbox for the MVP is a virtual machine hosting one fixed shopping page. Agents such as Muse are run manually on that machine. Automating those runs is out of scope for the MVP.

## Decision

Use LangChain for agent loops, tools, and retrieval. Use LangGraph for the workflow graph.

LangChain provides the ReAct loop, tool schemas around Python functions, and retrievers. LangGraph holds the stage graph: conditional edges, checkpoints for the current run, and an interrupt before human review of a detection rule. Graph state is the handoff record.

## Comparison

| Framework | What it contributes | Why it is not the orchestrator |
|---|---|---|
| LangChain + LangGraph | ReAct, tool calling, retrieval, explicit state, parallel branches, human interrupt | Selected |
| CrewAI | Role prompts and a manager that delegates to specialists | Delegation is conversational. Acceptance gates, versioned records, and orchestrator-owned retries would sit outside the crew. |
| AutoGen | Multi-agent conversation and critique | The coordination spec requires one-way contracts and no direct agent-to-agent dialogue. |
| LlamaIndex | Ingestion, chunking, and query over documents | Suitable later as a retriever behind LangChain. It does not own the stage graph or the measurement loop. |
| Semantic Kernel | Planner and plugins | The stage graph and feedback loops would be rebuilt beside it. |
| Custom loop | Full control of gates and records | Tool calling, ReAct, retries, and checkpoints would be reimplemented before any research behavior exists. |

## Consequences

Agent code uses LangChain tools and LangGraph nodes. Crew-style chat between roles is out of scope. LlamaIndex remains available for ingestion if the in-memory ranker is not enough. The long-term store of hypotheses and rules stays a versioned record, not only a chat checkpoint. The MVP sandbox does not gain an automated launcher for Muse or similar agents.
