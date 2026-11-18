# AI Shopping Agent Detection — Retrieval Design

**Architecture change.** A Dataset Discovery Agent will search for public datasets, check their access conditions and available fields, and maintain a Dataset Registry. Dataset Validation will select candidates from this registry instead of repeating open-ended searches. The registry records collection methods, session-level identifiers, human/agent labels, licensing, source URLs and verification dates.

## 1. Where retrieval is required

The Threat Intelligence Agent needs current documentation and independent measurements to propose signals that distinguish AI shopping agents from human users. The Dataset Discovery Agent needs public dataset descriptions and schema documentation. Dataset Validation reads structured registry entries and inspects candidate datasets before accepting them for a specific hypothesis. A dataset is not treated as suitable merely because its description matches a search query.

## 2. Semantic retrieval mechanism

Both research agents search the public web, fetch candidate pages and extract the main text. A text embedding model represents each passage and the agent query as vectors. Cosine similarity ranks passages by topical match. A second ranking stage considers source authority, publication date and duplication. Retrieved passages retain their URL, title, date and document section. The agent can issue a narrower query when results do not answer its question.

Threat Intelligence retrieves evidence during its ReAct loop. Dataset Discovery runs scheduled searches and responds to targeted requests when the registry has no suitable candidate. The initial implementation can embed and rank passages in memory; persistent vector storage is optional.

## 3. Effect on agent output

**Task:** Propose a testable signal for identifying Meta Muse sessions.

**Without retrieval — sample response:** “AI shopping agents typically run headless browsers, expose automation flags and use data-center IP addresses.” This response provides no source, agent-specific observation or measurement that could justify a detection rule.

**With retrieval — sample response:** “A third-party technical analysis reports a Chromium 154 browser, a Linux x86_64 User-Agent, an ARM architecture Client Hint, SwiftShader/ANGLE/Vulkan WebGL rendering, six logical CPU cores, 8–16 GB device memory, a 1920×1080 screen and navigator.webdriver=false in observed Muse traffic.”

These values are observations to verify, not fixed properties of every Muse session.

**Hypothesis H1:** A combined Linux/Chromium, architecture-hint and software-rendered WebGL fingerprint appears more often in sampled Muse sessions than in comparable human-operated sessions. **Test:** collect those fields from both populations under documented browser versions and collection conditions; calculate prevalence, precision, recall and false-positive rate. **Status:** unvalidated.

**Source to verify:** Arcjet, “How to Detect Meta’s Muse AI Agent” (arcjet.com/learn/how-to-detect-metas-muse-ai-agent). Manufacturer documentation should be checked separately for claims about the underlying browser and virtual-machine architecture.

## 4. Data selection and retrieval settings

| Decision | Requirement |
|---|---|
| Data sources | Public manufacturer documentation, technical measurements and dataset catalogs. |
| Native search | Web search for candidate pages; extract full text where available. |
| Segmentation | Use HTML headings, sections and paragraphs. Preserve the source location. |
| Chunking | Recursive splitting within sections; initially 500–800 tokens with 10% overlap. Keep claims with nearby qualifications. |
| Ranking | Cosine similarity plus claim-specific source priority, freshness checks and MMR to reduce duplicate passages. |
| Retrieval count | Search up to 10 candidate pages per query; send the five highest-ranked passages to the agent. Adjust after evaluation. |
| Iteration | Search again when the evidence is missing, contradictory or limited to one unverified report. |

## 5. Candidate tools

Tavily Search/Extract and Exa Search/Contents are candidates for web discovery and page extraction. LangChain RecursiveCharacterTextSplitter or LlamaIndex ingestion components can split retrieved pages. Embedding models with cosine similarity can rank passages; Cohere Rerank is an optional second-stage ranker. Tool selection depends on full-text access, source metadata, configurable splitting, ranking controls, cost and integration with iterative agent calls.

## 6. Failure mode: relevant but weak evidence

A blog post may match the query more closely than the agent manufacturer’s architecture documentation and therefore rank first by semantic similarity. The agent could repeat speculative fingerprint values as confirmed implementation details. Manufacturer documentation takes priority for declared architecture; independent technical measurements take priority for observed runtime behavior. The agent records disagreements, checks publication dates and requires corroboration before treating a fingerprint as stable. Unsupported claims remain hypotheses, not detection rules.
