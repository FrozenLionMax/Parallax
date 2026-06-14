<p align="center">
  <img src="assets/aether-logo.png" alt="Aether Logo" width="120" />
</p>

<h1 align="center">Aether</h1>
<p align="center"><strong>The Invisible Intelligence Layer</strong></p>

<p align="center">
  <code>Multi-Agent</code> · <code>Autonomous Orchestration</code> · <code>Knowledge Graph</code> · <code>RLHF</code>
</p>

<p align="center">
  <strong>Team Parallax</strong> · IndiaRuns Hackathon 2026<br/>
  Track 02 — Ideathon · Challenge 1: The AI Systems Architect — Reimagining Work
</p>

---

## 📌 Target Challenge

**Challenge 1: The AI Systems Architect — Reimagining Work**

> *Design a groundbreaking, technical AI system. Think fully self-running "agents," super-smart search, complex AI coordination, or intelligent "co-pilots" that dramatically improve how work gets done.*

---

## 🔥 The Problem

Knowledge workers are drowning — not in work, but in **work about work**.

| The Reality | The Number |
|---|---|
| Average tools used daily per worker | **11+** |
| Daily context switches | **400+** |
| Time spent on coordination, not real work | **62%** *(Asana Work Index)* |
| Hours/week searching for information | **9.3 hrs** *(McKinsey)* |

Today's AI tools — ChatGPT, Copilot, Gemini — are powerful but fundamentally **single-turn and single-task**. You ask a question, you get an answer. But real work isn't a question — it's a **workflow**:

```
Research → Analyze → Draft → Review → Coordinate → Execute → Follow Up
```

This workflow spans multiple tools, requires different skills at each step, and demands judgment about when to proceed and when to pause. Current AI can't handle this. **It can chat, but it can't work.**

---

## 💡 The Solution: Aether

**Aether** is an **Autonomous Multi-Agent Work Intelligence System** — an AI operating system where specialized agents collaborate to handle complex knowledge work from intent to execution.

### What Makes Aether Different

| Capability | ChatGPT / Copilot | Aether |
|---|---|---|
| Multi-step workflows | ❌ Single-turn | ✅ Full workflow DAGs |
| Specialized agents | ❌ One general model | ✅ Purpose-built agents |
| Persistent memory | ❌ Forgets between sessions | ✅ 3-layer memory system |
| Tool integration | ⚠️ Limited plugins | ✅ Deep API integrations |
| Autonomous execution | ❌ Needs constant prompting | ✅ Confidence-based autonomy |
| Quality assurance | ❌ User checks everything | ✅ Built-in Quality Agent |
| Continuous learning | ❌ Static | ✅ RLHF + preference learning |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                           │
│    Natural Language Input  │  Live Dashboard  │  Approval Flows     │
└──────────────────────┬──────────────────────────┬───────────────────┘
                       │                          │
┌──────────────────────▼──────────────────────────▼───────────────────┐
│                   🧠 ORCHESTRATOR (The Brain)                       │
│                                                                     │
│   ┌──────────────┐   ┌───────────────┐   ┌───────────────────────┐ │
│   │ Intent       │   │ Task          │   │ Agent                 │ │
│   │ Parser       │   │ Decomposer    │   │ Coordinator           │ │
│   │              │   │               │   │                       │ │
│   │ Understands  │   │ Builds DAG    │   │ Routes tasks,         │ │
│   │ WHAT + WHY   │   │ of sub-tasks  │   │ monitors progress,    │ │
│   │ + CONTEXT    │   │ with deps     │   │ resolves conflicts    │ │
│   └──────────────┘   └───────────────┘   └───────────────────────┘ │
└────────┬──────────────────┬──────────────────┬──────────────┬──────┘
         │                  │                  │              │
┌────────▼─────┐   ┌───────▼─────┐   ┌────────▼───┐   ┌─────▼──────┐
│ 🔍 RESEARCH  │   │ 📊 ANALYST  │   │ ✍️ CREATOR  │   │ ⚡ EXECUTOR │
│    AGENT     │   │    AGENT    │   │    AGENT   │   │    AGENT   │
│              │   │             │   │            │   │            │
│ RAG + Web    │   │ Code interp │   │ Fine-tuned │   │ Tool-use   │
│ search +     │   │ + stats +   │   │ LLM +      │   │ framework  │
│ knowledge    │   │ viz engine  │   │ templates  │   │ + APIs     │
│ graphs       │   │             │   │            │   │            │
└──────┬───────┘   └──────┬──────┘   └──────┬─────┘   └──────┬─────┘
       │                  │                  │                │
┌──────▼──────────────────▼──────────────────▼────────────────▼──────┐
│              🛡️ QUALITY AGENT (Guardian Layer)                     │
│     Fact-checking · Bias detection · Tone review · Completeness   │
└───────────────────────────────┬────────────────────────────────────┘
                                │
┌───────────────────────────────▼────────────────────────────────────┐
│                   🗄️ SHARED MEMORY LAYER                           │
│                                                                    │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────┐ │
│  │ 📌 Episodic    │  │ 🧠 Semantic    │  │ 🔄 Procedural        │ │
│  │    Memory      │  │    Memory      │  │    Memory            │ │
│  │                │  │                │  │                      │ │
│  │ Current task   │  │ Knowledge      │  │ Learned workflow     │ │
│  │ state, agent   │  │ graph across   │  │ templates, user      │ │
│  │ outputs,       │  │ all sessions,  │  │ preferences,         │ │
│  │ corrections    │  │ domain facts   │  │ RLHF-tuned patterns  │ │
│  └────────────────┘  └────────────────┘  └──────────────────────┘ │
└───────────────────────────────┬────────────────────────────────────┘
                                │
┌───────────────────────────────▼────────────────────────────────────┐
│                   🔌 INTEGRATION LAYER                             │
│  Slack · Notion · JIRA · GitHub · Gmail · Calendar · Drive · APIs │
└────────────────────────────────────────────────────────────────────┘
```

> 📖 **Detailed architecture**: See [docs/architecture.md](docs/architecture.md)

---

## 🗺️ User Journey: How Aether Works

### The 6-Step Flow

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐
│ 1. ASK  │───▶│ 2. PLAN  │───▶│ 3. WATCH │───▶│ 4. GUIDE │───▶│5.REVIEW │───▶│6. LEARN │
│         │    │          │    │          │    │          │    │         │    │         │
│ User    │    │ System   │    │ Agents   │    │ User     │    │ Quality │    │ System  │
│ states  │    │ shows    │    │ work in  │    │ decides  │    │ check + │    │ adapts  │
│ intent  │    │ the plan │    │ real-time│    │ when     │    │ deliver │    │ from    │
│         │    │          │    │          │    │ asked    │    │         │    │ feedback│
└─────────┘    └──────────┘    └──────────┘    └──────────┘    └─────────┘    └─────────┘
```

### Example: Competitive Analysis for a Board Meeting

**User says:**
> *"Prepare a competitive analysis of AI recruiting tools in India and draft a strategy document for our board meeting next Tuesday."*

**Step 1 — ASK**: Aether's Intent Parser identifies:
- **Goal**: Board-ready competitive analysis + strategy document
- **Domain**: AI recruiting tools, India market
- **Audience**: Board of directors (executive-level language)
- **Deadline**: Next Tuesday
- **Implicit needs**: Data-backed, visual-friendly, concise

**Step 2 — PLAN**: The Orchestrator builds a task DAG:
```
Phase 1 (Parallel)          Phase 2 (Sequential)       Phase 3 (Sequential)
├─ Research Agent:          ├─ Analyst Agent:           ├─ Creator Agent:
│  ├─ Identify players     │  ├─ Feature comparison    │  ├─ Draft strategy doc
│  ├─ Gather pricing       │  ├─ SWOT per competitor   │  ├─ Create visuals
│  └─ Find reviews/press   │  └─ Market sizing         │  └─ Format for board
└─ Research Agent:          └─ (depends on Phase 1)     └─ (depends on Phase 2)
   └─ Pull market reports                              
                                                        Phase 4
                                                        └─ Quality Agent: Review
```

**Step 3 — WATCH**: Real-time progress dashboard:
```
🔍 Research Agent    ██████████ 100%  Found 14 competitors, 3 market reports
📊 Analyst Agent     ████████░░  80%  SWOT complete for 8/14 competitors
✍️ Creator Agent     ░░░░░░░░░░   0%  Waiting for analysis...
🛡️ Quality Agent     ░░░░░░░░░░   0%  Standby
```

**Step 4 — GUIDE**: The Analyst Agent escalates a decision:
> 💬 *"I found conflicting market-size data: Report A says ₹2,400 Cr, Report B says ₹4,100 Cr. Report A is from Nasscom (2024), Report B is from a startup blog. I recommend using Nasscom. Should I proceed?"*

User: *"Yes, use Nasscom. Always prefer institutional sources."*
→ Aether stores this preference in **Procedural Memory** for future decisions.

**Step 5 — REVIEW**: Final deliverable presented:
```
📄 Strategy Document (12 pages, board-formatted)
📊 3 embedded charts (market map, feature matrix, growth projection)
📋 Executive summary (1 page)
⚠️ Quality Agent note: "Competitor X's pricing may have changed — data is 
   from March 2026. Recommend verifying before board presentation."
```

**Step 6 — LEARN**: User feedback stored:
> 👍 *"Good analysis, but make executive summaries shorter next time — 3 bullet points max, not paragraphs."*
→ Stored in Procedural Memory. All future executive summaries will be bullet-point format.

> 📖 **More scenarios**: See [docs/user-journey.md](docs/user-journey.md)

---

## 🔬 Technical Innovation — 5 Pillars

### 1. Hierarchical Task Decomposition Engine
Not just a to-do list — a full **Directed Acyclic Graph (DAG)** of tasks with dependencies, parallelism, and checkpoints. The orchestrator reasons about task ordering, identifies parallelizable work, and dynamically re-plans when agents encounter blockers.

### 2. Specialized Agent Architecture
Each agent is purpose-built with domain-specific tools, not a generic LLM wrapper:
| Agent | Core Tech Stack | Specialization |
|---|---|---|
| Orchestrator | Planning LLM + DAG scheduler | Task decomposition, dependency management |
| Research | RAG + Web crawl + Knowledge graph | Information gathering with source verification |
| Analyst | Code interpreter + Statistical tools | Data analysis, pattern finding, visualization |
| Creator | Fine-tuned LLM + Document templates | Content generation tailored to audience & format |
| Executor | Tool-use framework + API connectors | Real-world actions: email, tickets, scheduling |
| Quality | Critique LLM + Fact-checker + Bias detector | Output review before delivery |

### 3. Three-Layer Shared Memory
The breakthrough: agents share a **persistent memory system** that makes the entire system smarter over time.
- **Episodic** (Redis): What's happening right now — task state, intermediate results
- **Semantic** (Neo4j + PostgreSQL): What we know — knowledge graph, entities, relationships
- **Procedural** (Vector DB): What we've learned — workflow patterns, user preferences, quality standards

### 4. Confidence-Based Human-in-the-Loop
```
Confidence > 90%  →  Auto-execute, notify after completion
Confidence 70-90% →  Execute, but hold for approval before delivery
Confidence < 70%  →  Pause, present options, ask user to decide
Agent stuck        →  Escalate with full context + recommendations
```
Trust is **earned progressively** — the system starts cautious and earns autonomy over time.

### 5. Inter-Agent Communication Protocol
Agents aren't isolated — they collaborate through a structured message bus:
```
Research → Analyst:  "Found conflicting data on market size. 
                      Here are 3 sources with credibility scores."

Analyst → Creator:   "Key insight: market is 3x larger than assumed. 
                      Flag this prominently in the executive summary."

Quality → Creator:   "Paragraph 3 cites 2024 data but calls it 'latest.' 
                      Recommend adding the date explicitly."
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Orchestration** | LangGraph / Custom DAG scheduler | Native support for stateful agent graphs |
| **LLMs** | GPT-4o / Claude 3.5 / Llama 3 (swappable) | Best-in-class reasoning, swappable to avoid lock-in |
| **Knowledge Graph** | Neo4j | Industry standard for entity-relationship modeling |
| **Vector Store** | FAISS / Qdrant | Fast similarity search for RAG and memory retrieval |
| **Episodic Memory** | Redis | Sub-millisecond reads for real-time task state |
| **Semantic Memory** | PostgreSQL + pgvector | Durable long-term storage with vector search |
| **Message Bus** | Redis Streams | Lightweight, ordered inter-agent messaging |
| **Backend** | FastAPI (Python) | Async-native, fast, excellent for AI workloads |
| **Frontend** | React + WebSockets | Real-time agent progress updates |
| **Auth & Security** | Supabase / Auth0 | Enterprise-grade identity management |

---

## 🗓️ Roadmap

```
Phase 1 (0-3 months)                Phase 2 (3-6 months)              Phase 3 (6-12 months)
━━━━━━━━━━━━━━━━━━━━               ━━━━━━━━━━━━━━━━━━━━━             ━━━━━━━━━━━━━━━━━━━━━
✅ Core Orchestrator                 🔧 Agent Marketplace              🚀 Self-improving RLHF
✅ 3 Base Agents                     🔧 Custom agent creation          🚀 Industry agent packs
   (Research, Analyst, Creator)      🔧 Enterprise SSO + RBAC          🚀 Multi-user collaboration
✅ Shared Memory MVP                 🔧 15+ tool integrations          🚀 On-premise deployment
✅ 5 tool integrations               🔧 Team workspaces                🚀 API for third-party agents
✅ Single-user deployment            🔧 Advanced analytics             🚀 Voice + mobile interface
```

---

## 📊 Market Opportunity

| Metric | Number |
|---|---|
| India's knowledge workforce | **~100 million** workers |
| Time lost to "work about work" | **62%** of workday |
| Global productivity software market | **$102B** by 2027 |
| India enterprise SaaS market | **$15B** by 2027 |
| Productivity saved per worker (2 hrs/day) | **~₹3L/year** per worker |

---

## 👥 Team Parallax

| | |
|---|---|
| **Team Name** | Parallax |
| **Hackathon** | IndiaRuns Hackathon 2026 |
| **Track** | Ideathon — Challenge 1 |
| **System** | Aether — The Invisible Intelligence Layer |

---

## 📄 License

MIT License — see [LICENSE](LICENSE)
