# Capstone: Assignment Requirements → Document Mapping

Project: **Autonomous Threat Detection Researcher for Agentic Commerce**

## Authority and scope

The official assignment is [Capstone Project Option - Research Assistant (1).pdf](<Capstone Project Option - Research Assistant (1).pdf>). It defines six competency areas, not a numbered checkpoint schedule. The mapping below uses those areas as logical checkpoints. **Documented** means a design/specification exists, not that implementation or demonstrations are complete.

| Assignment competency | Formal requirement / success criterion | Supporting documents | Evidence status / outstanding proof |
|---|---|---|---|
| 1. Tool Calling | Agent calls tools/functions and understands their outputs | [Agentic_Commerce_Agent_Design_Updated(1).pdf](<Agentic_Commerce_Agent_Design_Updated(1).pdf>); [Agentic_Commerce_Threat_Researcher_Proposal.pdf](Agentic_Commerce_Threat_Researcher_Proposal.pdf); [shopping_agent_retrieval_checkpoint_final.docx](shopping_agent_retrieval_checkpoint_final.docx) | Design documented. Demonstrate actual tool calls, outputs, and decisions. |
| 2. Reasoning Architectures and Chain of Thought | Basic reasoning loop (e.g. ReAct), environment interaction, recovery from mistakes | [Agentic_Commerce_Agent_Design_Reasoning_Loops.pdf](Agentic_Commerce_Agent_Design_Reasoning_Loops.pdf); [Agentic_Commerce_Agent_Design_Updated(1).pdf](<Agentic_Commerce_Agent_Design_Updated(1).pdf>) | Design documented. Demonstrate recovery after an inconclusive/failed step. |
| 3. Knowledge and Memory | Retrieval-based memory/RAG or another store; recall past executions or knowledge | [Agentic_Commerce_Agent_Design_Updated(1).pdf](<Agentic_Commerce_Agent_Design_Updated(1).pdf>); [shopping_agent_retrieval_checkpoint_final.docx](shopping_agent_retrieval_checkpoint_final.docx); [shopping_agent_retrieval_checkpoint_polished(1).pdf](<shopping_agent_retrieval_checkpoint_polished(1).pdf>) | Design documented. Demonstrate persistent recall and avoidance of duplicate work. |
| 4. Further Reasoning | Extend the reasoning loop (ToT given as an example); explain reasoning architecture/process | [Threat_Intelligence_ReAct_Decision.pdf](Threat_Intelligence_ReAct_Decision.pdf); [Agentic_Commerce_Agent_Design_Reasoning_Loops.pdf](Agentic_Commerce_Agent_Design_Reasoning_Loops.pdf) | Partially documented. Explicitly justify the alternative to ToT and demonstrate its value. |
| 5. Multi-agent Coordination | Specialized agents, parallelism, demonstration of task execution by at least one agent | [Multi_Agent_Coordination_Capstone.pdf](Multi_Agent_Coordination_Capstone.pdf); [Agentic_Commerce_Agent_Design_Updated(1).pdf](<Agentic_Commerce_Agent_Design_Updated(1).pdf>) | Design documented. Demonstrate a specialized agent and orchestrated handoff. |
| 6. Safety | Identify unintended actions and preventive guardrails | [Agentic_Threat_Detection_Safety_Intervention_Plan.pdf](Agentic_Threat_Detection_Safety_Intervention_Plan.pdf) | Design documented. Demonstrate rejection/escalation of unsupported or unsafe work. |

## Additional design documents

- [Agentic_Commerce_Threat_Researcher_Proposal.pdf](Agentic_Commerce_Threat_Researcher_Proposal.pdf): initial project scope, users, research approach and expected outcome.
- [shopping_agent_retrieval_checkpoint_final.docx](shopping_agent_retrieval_checkpoint_final.docx): separate retrieval checkpoint artifact; retrieval supports the official Knowledge and Memory competency but is not separately enumerated in the official assignment.
- [shopping_agent_retrieval_checkpoint_polished(1).pdf](<shopping_agent_retrieval_checkpoint_polished(1).pdf>): additional saved retrieval checkpoint presentation; compare with DOCX if editing.
- [Threat_Intelligence_ReAct_Decision.pdf](Threat_Intelligence_ReAct_Decision.pdf): later decision to use ReAct without Tree of Thoughts. This supersedes the earlier ToT proposal in [Agentic_Commerce_Agent_Design_Updated(1).pdf](<Agentic_Commerce_Agent_Design_Updated(1).pdf>).
- [Multi_Agent_Coordination_Capstone.pdf](Multi_Agent_Coordination_Capstone.pdf): six-agent architecture; earlier agent-design documents may describe fewer roles.

## Formal final deliverables

1. **Final Report** — comprehensive problem, methodology, results and conclusions.
2. **Presentation** — formal presentation for faculty and peers.

Neither deliverable is established as complete by the source documents in this archive.

## Document manifest

| File | Role |
|---|---|
| [Capstone Project Option - Research Assistant (1).pdf](<Capstone Project Option - Research Assistant (1).pdf>) | Official assignment / requirements |
| [Agentic_Commerce_Threat_Researcher_Proposal.pdf](Agentic_Commerce_Threat_Researcher_Proposal.pdf) | Project proposal |
| [Agentic_Commerce_Agent_Design_Updated(1).pdf](<Agentic_Commerce_Agent_Design_Updated(1).pdf>) | Agent design, reasoning, memory, tools (earlier ToT design) |
| [Agentic_Commerce_Agent_Design_Reasoning_Loops.pdf](Agentic_Commerce_Agent_Design_Reasoning_Loops.pdf) | Detailed agent reasoning loops |
| [Threat_Intelligence_ReAct_Decision.pdf](Threat_Intelligence_ReAct_Decision.pdf) | Later reasoning architecture decision |
| [shopping_agent_retrieval_checkpoint_final.docx](shopping_agent_retrieval_checkpoint_final.docx) | Retrieval design checkpoint |
| [shopping_agent_retrieval_checkpoint_polished(1).pdf](<shopping_agent_retrieval_checkpoint_polished(1).pdf>) | Retrieval design PDF |
| [Multi_Agent_Coordination_Capstone.pdf](Multi_Agent_Coordination_Capstone.pdf) | Multi-agent coordination specification |
| [Agentic_Threat_Detection_Safety_Intervention_Plan.pdf](Agentic_Threat_Detection_Safety_Intervention_Plan.pdf) | Safety and intervention specification |

## Limits

This archive includes the located core assignment and checkpoint documents, not every historical revision. Design artifacts do not prove that software has been implemented or evaluated. Later discussion-only designs (such as rule reliability validation and sample-based spot checks) have not been reconstructed as files.
