# Parallax — Technical Architecture

> **Deep-dive into the system design of Parallax — AI Co-Pilots That See Work From Every Angle**

---

## 1. System Architecture Overview

Parallax follows a **layered architecture** with clear separation of concerns. Each layer has a specific responsibility and communicates through well-defined interfaces.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: USER INTERFACE                          │
│  Web Dashboard │ CLI │ API │ Slack/Teams Bot │ Mobile (future)      │
├─────────────────────────────────────────────────────────────────────┤
│                    LAYER 2: ORCHESTRATION ENGINE                    │
│  Intent Parser → Task Decomposer → DAG Scheduler → Agent Router    │
├─────────────────────────────────────────────────────────────────────┤
│                    LAYER 3: AI CO-PILOT FLEET (10)                   │
│  🔍 Research │ 📊 Analyst │ ✍️ Creator │ ⚡ Action │ 🛡️ Quality    │
│  💬 Comms    │ 💻 Code    │ 📡 Data    │ 🎨 Design │ 🔐 Compliance │
├─────────────────────────────────────────────────────────────────────┤
│                    LAYER 4: SHARED MEMORY                           │
│  Episodic (Redis) │ Semantic (Neo4j+PG) │ Procedural (Vector DB)   │
├─────────────────────────────────────────────────────────────────────┤
│                    LAYER 5: INTEGRATION & TOOLS                     │
│  APIs │ Web Search │ Code Sandbox │ File System │ External Tools    │
├─────────────────────────────────────────────────────────────────────┤
│                    LAYER 6: INFRASTRUCTURE                          │
│  Auth │ Logging │ Rate Limiting │ Monitoring │ Cost Tracking        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Orchestration Engine — The Brain

The Orchestrator is the central coordination layer. It doesn't do work itself — it **plans, delegates, and monitors**.

### 2.1 Intent Parser

Takes raw user input and extracts structured intent:

```
Input:  "Prepare a competitive analysis of AI tools in India 
         and draft a strategy doc for the board meeting Tuesday"

Output: {
  "goal": "competitive_analysis + strategy_document",
  "domain": "AI tools, India market",
  "audience": "board of directors",
  "tone": "executive, data-driven",
  "deadline": "2026-06-17T09:00:00+05:30",
  "implicit_needs": [
    "data visualization",
    "executive summary",
    "professional formatting"
  ],
  "confidence": 0.92
}
```

**Technology**: LLM with structured output (function calling / JSON mode). Enhanced by Semantic Memory for user-specific context (e.g., "board meeting" → knows the board prefers 1-page summaries because of Procedural Memory).

### 2.2 Task Decomposer

Converts intent into a **Directed Acyclic Graph (DAG)** of tasks:

```
                    ┌─────────────────┐
                    │   ROOT TASK     │
                    │ "Comp Analysis  │
                    │  + Strategy"    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌──────▼─────┐  ┌─────▼──────┐
     │ T1: Find   │  │ T2: Pull   │  │ T3: Get    │
     │ competitors│  │ market     │  │ user       │
     │ (Research) │  │ reports    │  │ reviews    │
     │            │  │ (Research) │  │ (Research) │
     └────────┬───┘  └──────┬─────┘  └─────┬──────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │ T4: Analyze     │
                    │ competitors     │
                    │ (Analyst)       │
                    │ DEPENDS: T1,T2,T3│
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌──────▼─────┐  ┌─────▼──────┐
     │ T5: Draft  │  │ T6: Create │  │ T7: Write  │
     │ strategy   │  │ charts     │  │ exec       │
     │ (Creator)  │  │ (Analyst)  │  │ summary    │
     │ DEP: T4    │  │ DEP: T4    │  │ (Creator)  │
     └────────┬───┘  └──────┬─────┘  │ DEP: T5    │
              │              │        └─────┬──────┘
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │ T8: Quality     │
                    │ review          │
                    │ (Quality Agent) │
                    │ DEP: T5,T6,T7   │
                    └─────────────────┘
```

**Key design decisions:**
- Tasks that CAN run in parallel DO run in parallel (T1, T2, T3)
- Dependencies are explicit — T4 won't start until T1+T2+T3 complete
- Each task is tagged with the best-fit agent
- The DAG is **dynamic** — if T1 discovers something unexpected, the Orchestrator can re-plan

### 2.3 DAG Scheduler

Manages task execution lifecycle:

```python
class TaskState(Enum):
    PENDING = "pending"         # Waiting for dependencies
    READY = "ready"             # Dependencies met, queued for execution
    RUNNING = "running"         # Agent is working on it
    BLOCKED = "blocked"         # Agent needs human input
    COMPLETED = "completed"     # Done, output in shared memory
    FAILED = "failed"           # Error, needs re-planning

class DAGScheduler:
    def tick(self):
        for task in self.dag.tasks:
            if task.state == PENDING and task.dependencies_met():
                task.state = READY
                self.dispatch_to_agent(task)
            elif task.state == FAILED:
                self.replan_or_escalate(task)
```

### 2.4 Agent Router

Assigns tasks to the best-fit agent based on:
1. **Task type** → Primary routing (research tasks → Research Agent)
2. **Agent load** → Load balancing across multiple agent instances
3. **Specialization history** → If an agent has done similar tasks well before, prefer it
4. **Urgency** → Priority queue for deadline-sensitive tasks

---

## 3. Agent Specifications

### 3.1 Research Agent

| Property | Detail |
|---|---|
| **Role** | Information gathering, source verification, knowledge extraction |
| **Core Tech** | RAG pipeline + Web search API + Knowledge graph queries |
| **Input** | Research query + scope constraints + quality requirements |
| **Output** | Structured findings with sources, confidence scores, and summaries |

**Capabilities:**
- Web search with result ranking and deduplication
- Document parsing (PDF, DOCX, HTML → structured text)
- Knowledge graph queries for entity relationships
- Source credibility scoring (institutional > blog > social media)
- Contradiction detection across sources

**Example behavior:**
```
Input:  "Find all AI recruiting tools operating in India with 
         pricing information"

Output: {
  "findings": [
    {
      "entity": "Redrob AI",
      "category": "AI-native talent platform",
      "pricing": "Enterprise custom, est. ₹50K-2L/month",
      "source": "https://redrob.ai/pricing",
      "credibility": 0.95,
      "last_verified": "2026-06-10"
    },
    // ... more results
  ],
  "gaps": ["3 competitors found without public pricing"],
  "confidence": 0.87
}
```

**Failure modes & recovery:**
- Rate-limited by search API → Switch to cached results + notify
- Conflicting data → Flag to Analyst Agent for resolution
- No results found → Broaden search scope + report to Orchestrator

---

### 3.2 Analyst Agent

| Property | Detail |
|---|---|
| **Role** | Data analysis, pattern recognition, insight extraction, visualization |
| **Core Tech** | Python code interpreter + Pandas/NumPy + Matplotlib/Plotly |
| **Input** | Structured data from Research Agent + analysis objectives |
| **Output** | Insights, statistical summaries, charts, comparison matrices |

**Capabilities:**
- Statistical analysis (trends, correlations, outliers)
- Comparative analysis (feature matrices, SWOT, scoring models)
- Data visualization (charts, graphs, heat maps)
- Anomaly detection in datasets
- Quantitative forecasting (simple models)

**Example behavior:**
```
Input:  Research data on 14 AI recruiting tools

Output: {
  "insights": [
    "Market is fragmented — no player has >15% share",
    "Average pricing: ₹75K/month for mid-market",
    "3 competitors launched in last 6 months — market accelerating"
  ],
  "artifacts": [
    "feature_comparison_matrix.csv",
    "market_map_chart.png",
    "pricing_distribution.png"
  ],
  "confidence": 0.91
}
```

---

### 3.3 Creator Agent

| Property | Detail |
|---|---|
| **Role** | Content generation — documents, emails, code, presentations |
| **Core Tech** | Fine-tuned LLM + Document templates + Style adapters |
| **Input** | Content brief + source material + audience + format requirements |
| **Output** | Polished content ready for review |

**Key innovation — Audience-Aware Generation:**
```
Same content, different audiences:

Board audience  → "Market opportunity: ₹4,100 Cr (Nasscom 2024). 
                    3x growth projected by 2028."

Engineering team → "14 competitors identified. Key differentiator 
                    opportunity: none have real-time behavioral 
                    signal integration. Tech feasibility: HIGH."

Sales team      → "Top 3 competitors to watch: [X], [Y], [Z]. 
                    Our edge: [specific talking points]."
```

---

### 3.4 Executor Agent

| Property | Detail |
|---|---|
| **Role** | Real-world actions — API calls, emails, ticket creation, scheduling |
| **Core Tech** | Tool-use framework + OAuth-based API connectors |
| **Input** | Action specification + parameters + approval status |
| **Output** | Execution confirmation + result |

**Supported actions:**
- Send emails via Gmail/Outlook API
- Create JIRA/Linear tickets
- Schedule calendar events
- Post to Slack channels
- Upload files to Drive/Notion
- Trigger webhooks

**Safety model:** Executor Agent **always** requires explicit approval for:
- Sending external communications
- Modifying production systems
- Financial transactions
- Actions affecting other people's calendars

---

### 3.5 Quality Agent

| Property | Detail |
|---|---|
| **Role** | Review all outputs before delivery — accuracy, tone, completeness |
| **Core Tech** | Critique LLM + Fact-checking pipeline + Bias detector |
| **Input** | Any agent output + original task requirements |
| **Output** | Approval / revision requests with specific feedback |

**Quality checks performed:**
1. **Factual accuracy** — Cross-reference claims against sources
2. **Completeness** — Does the output address all requirements?
3. **Tone & audience** — Is the language appropriate for the target audience?
4. **Bias detection** — Flag potentially biased conclusions
5. **Recency** — Flag data that may be outdated
6. **Internal consistency** — Do different sections contradict each other?

---

### 3.6 Communication Co-Pilot — "The Connector"

| Property | Detail |
|---|---|
| **Role** | Meeting management, follow-ups, team coordination, stakeholder updates |
| **Core Tech** | Calendar APIs + Meeting transcription + NLU |
| **Input** | Project context + meeting metadata + team structure |
| **Output** | Agendas, meeting notes, action items, status reports, follow-up reminders |

**Capabilities:**
- Auto-generate meeting agendas from project context
- Extract decisions and action items from meeting transcripts
- Track action item completion and send reminders
- Draft audience-tailored status updates (PM vs Engineering Manager vs Board)
- Detect overdue commitments: "Backend team hasn't responded in 3 days — ping them?"

**Example behavior:**
```
Input:  Board meeting in 2 hours. Strategy document just completed.

Output: {
  "agenda": [
    "Review competitive landscape findings",
    "Discuss strategic recommendations",
    "Decide on resource allocation",
    "Assign action items"
  ],
  "pre_read_sent_to": ["cfo@company.com", "cto@company.com"],
  "attachments": ["Strategy_Document.pdf", "Executive_Summary.pdf"],
  "estimated_duration": "45 min"
}
```

---

### 3.7 Code Co-Pilot — "The Engineer"

| Property | Detail |
|---|---|
| **Role** | Code generation, review, debugging, automation — full engineering workflow |
| **Core Tech** | Code LLM + AST analysis + Docker sandbox + Git integration |
| **Input** | Natural language specs OR existing codebase + task |
| **Output** | Code, reviews, bug fixes, documentation, automation scripts |

**Capabilities:**
- Generate full functions/modules from natural language specifications
- Review pull requests for bugs, security vulnerabilities, performance issues
- Debug errors with root cause analysis and suggested fixes
- Create automation scripts ("Write a script that cleans our CSV data")
- Auto-generate documentation (docstrings, READMEs, API docs)

**How it differs from GitHub Copilot:**
```
GitHub Copilot:  Autocompletes lines of code in your IDE.
                 Scope: current file, maybe adjacent files.

Parallax Code:   Understands the FULL PROJECT CONTEXT —
                 architecture, dependencies, team conventions.
                 Works at the feature level, not line level.
                 Can review entire PRs, not just autocomplete.
```

**Safety:** All generated code runs in a Docker sandbox. No access to production systems without explicit approval.

---

### 3.8 Data Co-Pilot — "The Sensor"

| Property | Detail |
|---|---|
| **Role** | Live data acquisition from databases, APIs, dashboards |
| **Core Tech** | SQL/NoSQL query generation + REST/GraphQL clients + Data connectors |
| **Input** | Natural language data request + authorized data sources |
| **Output** | Structured data, real-time metrics, data health reports |

**Key distinction from Analyst Co-Pilot:**
```
Data Co-Pilot (Sensor):   ACQUIRES data from live production systems.
                          "What's our MRR today?" → queries the database.

Analyst Co-Pilot (Pattern Finder):   PROCESSES data already acquired.
                                     "What does this MRR trend mean?" → analysis.
```

**Capabilities:**
- Natural language → SQL/NoSQL query generation
- REST/GraphQL API data retrieval with pagination
- Dashboard monitoring with alerting ("Alert me if conversion drops below 2%")
- Data pipeline health checks ("Is yesterday's ETL healthy?")
- Real-time metric queries with caching

**Supported integrations:**
- **Databases:** PostgreSQL, MySQL, MongoDB, BigQuery
- **APIs:** Any REST/GraphQL endpoint with OAuth
- **Tools:** JIRA, GitHub, Slack, Notion, Google Analytics
- **Dashboards:** Grafana, Metabase, Amplitude

---

### 3.9 Design Co-Pilot — "The Architect"

| Property | Detail |
|---|---|
| **Role** | Visual design — wireframes, charts, diagrams, brand-consistent assets |
| **Core Tech** | Image generation models + Figma API + Chart libraries + Brand engine |
| **Input** | Design brief + content data + brand guidelines |
| **Output** | PNG/SVG visuals, chart images, wireframes, presentation layouts |

**Capabilities:**
- Generate UI/UX wireframes from natural language descriptions
- Create publication-quality charts from data (bar, line, pie, radar, heatmap)
- Architecture diagrams and flowcharts from system descriptions
- Enforce brand consistency (colors, typography, logo placement)
- Generate custom icons and illustrations

**Example behavior:**
```
Input:  "Create a market positioning bubble chart for 14 competitors.
         X-axis: pricing, Y-axis: feature completeness, 
         bubble size: market share. Use brand colors."

Output: {
  "file": "market_positioning_chart.png",
  "format": "PNG, 2x retina",
  "brand_colors_applied": true,
  "data_points_plotted": 14,
  "labels": "auto-positioned to avoid overlap"
}
```

---

### 3.10 Compliance Co-Pilot — "The Sentinel"

| Property | Detail |
|---|---|
| **Role** | Regulatory compliance, policy enforcement, audit trail |
| **Core Tech** | Legal NLP models + Regulatory databases + Policy engine |
| **Input** | Any co-pilot output + applicable regulatory frameworks |
| **Output** | Compliance report, flagged issues, audit log entries |

**Regulatory frameworks supported:**
- 🇮🇳 DPDPA (Digital Personal Data Protection Act, India)
- 🇪🇺 GDPR (General Data Protection Regulation)
- 🏥 HIPAA (Health Insurance Portability — healthcare)
- 🔒 SOC-2 / ISO 27001 (security frameworks)

**Capabilities:**
- **PII Detection:** Scans all outputs for personal identifiable information
- **Data Classification:** Auto-labels content as Public / Internal / Confidential / Restricted
- **Policy Enforcement:** "This email contains customer PII — mask before sending"
- **Contract Review:** Flags risky clauses, missing terms, non-standard language
- **Audit Trail:** Immutable log of every co-pilot action for compliance audits

**Example behavior:**
```
Input:  Review outreach email to VC investor.

Output: {
  "compliant": true,
  "checks_passed": [
    "No confidential financial data exposed",
    "No customer PII included",
    "Forward-looking statements properly qualified"
  ],
  "warnings": [
    "Revenue figure is an estimate — add disclaimer"
  ],
  "audit_entry_logged": true
}
```

**Critical rule:** Compliance Co-Pilot has **veto power** — it can block the Action Co-Pilot from executing any action that fails compliance checks.

---

## 4. Shared Memory Architecture

### 4.1 Three-Layer Design

```
┌─────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ LAYER 1: EPISODIC MEMORY (Redis)                │   │
│  │ TTL: Session-scoped                             │   │
│  │                                                 │   │
│  │ • Current task DAG state                        │   │
│  │ • Agent intermediate outputs                    │   │
│  │ • User corrections this session                 │   │
│  │ • Active context window                         │   │
│  │ • Real-time progress metrics                    │   │
│  │                                                 │   │
│  │ Access pattern: Write-heavy, sub-ms reads       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ LAYER 2: SEMANTIC MEMORY (Neo4j + PostgreSQL)   │   │
│  │ TTL: Permanent                                  │   │
│  │                                                 │   │
│  │ • Knowledge graph: entities, relationships      │   │
│  │ • User's domain expertise model                 │   │
│  │ • Historical decisions & their outcomes         │   │
│  │ • Organization-specific terminology             │   │
│  │ • Cross-session context                         │   │
│  │                                                 │   │
│  │ Access pattern: Read-heavy, graph traversals    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ LAYER 3: PROCEDURAL MEMORY (Vector DB)          │   │
│  │ TTL: Permanent, evolving                        │   │
│  │                                                 │   │
│  │ • Successful workflow templates                 │   │
│  │ • User quality preferences                      │   │
│  │ • Tool usage patterns                           │   │
│  │ • Feedback-driven improvements                  │   │
│  │ • Calibrated confidence thresholds              │   │
│  │                                                 │   │
│  │ Access pattern: Similarity search on embeddings │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Memory Access Patterns

| Operation | Layer | Example |
|---|---|---|
| "What's the current task status?" | Episodic | Real-time DAG state check |
| "What do we know about Company X?" | Semantic | Knowledge graph traversal |
| "How does this user prefer executive summaries?" | Procedural | Similarity search on past feedback |
| "What happened in last Tuesday's analysis?" | Semantic | Historical task retrieval |
| "What's the best approach for SWOT analysis?" | Procedural | Template matching from past successes |

### 4.3 Memory Lifecycle

```
User Interaction
       │
       ▼
  ┌─────────┐    Write immediately    ┌──────────┐
  │ Session  │ ──────────────────────▶ │ Episodic │
  │ Events   │                         │ Memory   │
  └─────────┘                         └────┬─────┘
                                           │
                                    On session end
                                           │
                                    ┌──────▼──────┐
                                    │ Consolidate  │
                                    │ & Extract    │
                                    └──────┬──────┘
                                           │
                              ┌────────────┼────────────┐
                              │            │            │
                        ┌─────▼────┐ ┌─────▼────┐ ┌────▼─────┐
                        │ Entities │ │ Patterns │ │ Feedback │
                        │ & Facts  │ │ & Prefs  │ │ & Scores │
                        └─────┬────┘ └─────┬────┘ └────┬─────┘
                              │            │            │
                        ┌─────▼────┐ ┌─────▼────┐ ┌────▼─────┐
                        │ Semantic │ │Procedural│ │ RLHF     │
                        │ Memory   │ │ Memory   │ │ Training │
                        └──────────┘ └──────────┘ └──────────┘
```

---

## 5. Inter-Agent Communication Protocol

### 5.1 Message Format

```json
{
  "message_id": "msg_a1b2c3",
  "timestamp": "2026-06-15T10:30:00Z",
  "sender": "research_agent_01",
  "recipient": "analyst_agent_01",
  "type": "RESULT",
  "task_id": "task_004",
  "payload": {
    "data": { ... },
    "confidence": 0.87,
    "sources": ["url1", "url2"],
    "warnings": ["Pricing data may be 3 months old"]
  },
  "requires_response": false
}
```

### 5.2 Message Types

| Type | When Used | Example |
|---|---|---|
| `TASK_ASSIGNMENT` | Orchestrator → Agent | "Research AI tools in India" |
| `RESULT` | Agent → Orchestrator/Agent | "Found 14 competitors" |
| `QUERY` | Agent → Agent | "Is this source reliable?" |
| `ESCALATION` | Agent → Orchestrator → User | "Need human decision" |
| `FEEDBACK` | Quality Agent → Any Agent | "Fix factual error in para 3" |
| `STATUS` | Agent → Orchestrator | "80% complete, ETA 2 min" |

### 5.3 Communication Flow Example

```
Time ──────────────────────────────────────────────────────────▶

Orchestrator ──TASK──▶ Research    ──RESULT──▶ Analyst
                      Agent                   Agent
                        │                       │
                        │                       │──QUERY──▶ Research
                        │                       │           Agent
                        │                       │◀─RESULT──
                        │                       │
                        │                       │──RESULT──▶ Creator
                        │                       │            Agent
                        │                       │              │
                        │                       │              │──RESULT──▶ Quality
                        │                       │              │            Agent
                        │                       │              │              │
                        │                       │              │◀─FEEDBACK──
                        │                       │              │
                        │                       │              │──RESULT──▶ Orchestrator
                        │                       │              │            ──▶ USER
```

---

## 6. Human-in-the-Loop Trust Model

### 6.1 Confidence Scoring

Every agent output carries a confidence score (0.0 - 1.0) based on:

| Factor | Weight | Description |
|---|---|---|
| Source reliability | 30% | How trustworthy are the underlying data sources? |
| Task familiarity | 25% | Has the system done similar tasks before? |
| Internal consistency | 20% | Do different parts of the output agree? |
| Completeness | 15% | Were all requirements addressed? |
| Recency | 10% | How current is the data? |

### 6.2 Escalation Thresholds

```
Confidence ≥ 0.90  ──▶  AUTO-EXECUTE
                        Agent proceeds autonomously.
                        User notified after completion.
                        "✅ Competitive analysis complete. View results."

Confidence 0.70-0.89 ──▶  APPROVE-BEFORE-DELIVERY
                          Agent completes work but holds delivery.
                          "📋 Strategy document ready. Review before sending?"

Confidence < 0.70  ──▶  ESCALATE-TO-USER
                        Agent pauses and presents options.
                        "🤔 Found conflicting data. Which source should I use?"

Agent STUCK        ──▶  FULL ESCALATION
                        Orchestrator packages full context for user.
                        "⚠️ Research Agent couldn't find pricing for 3 
                         competitors. How should I proceed?"
```

### 6.3 Trust Calibration

The thresholds are **not static** — they evolve:
- User overrides AUTO-EXECUTE frequently → Lower the threshold (be more cautious)
- User always approves APPROVE-BEFORE-DELIVERY → Raise threshold (earn more autonomy)
- Calibration is per-task-type (e.g., user trusts research more than email drafting)

---

## 7. Security & Privacy

### 7.1 Data Isolation
- Each organization gets a **dedicated memory partition**
- No cross-organization data leakage in shared infrastructure
- Agent sandboxing: agents cannot access data outside their assigned task scope

### 7.2 Audit Logging
```json
{
  "timestamp": "2026-06-15T10:35:00Z",
  "agent": "executor_agent",
  "action": "SEND_EMAIL",
  "target": "cfo@company.com",
  "approval_status": "USER_APPROVED",
  "approved_by": "user_001",
  "content_hash": "sha256:abc123..."
}
```
Every agent action is logged immutably. Enterprise admins can audit exactly what Parallax did, when, and who approved it.

### 7.3 Co-Pilot Sandboxing
- 🔍 Research Co-Pilot: read-only web access, no file writes
- 📊 Analyst Co-Pilot: sandboxed code execution (no network, no filesystem)
- ✍️ Creator Co-Pilot: output-only, no external actions
- ⚡ Action Co-Pilot: explicit action whitelist per organization
- 🛡️ Quality Co-Pilot: read-only access to all co-pilot outputs
- 💬 Communication Co-Pilot: read/write calendar, Slack — no external emails without approval
- 💻 Code Co-Pilot: Docker sandbox — no production access, no network
- 📡 Data Co-Pilot: read-only database access — no writes, no schema changes
- 🎨 Design Co-Pilot: output-only — generates assets, cannot modify external systems
- 🔐 Compliance Co-Pilot: read-only + **veto power** — can block Action Co-Pilot

---

## 8. Scalability Design

### 8.1 Horizontal Scaling

```
                    Load Balancer
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │ Orchestr. │  │ Orchestr. │  │ Orchestr. │
    │ Instance 1│  │ Instance 2│  │ Instance 3│
    └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
                   AI CO-PILOT POOL
              (Auto-scaled per type)
```

### 8.2 Cost Management
- Per-task cost tracking (LLM tokens, API calls, compute time)
- Budget limits per user/organization
- Agent-level cost optimization (use cheaper models for low-complexity tasks)
- Caching layer to avoid redundant LLM calls

---

*This architecture document is maintained by Team Parallax for the IndiaRuns Hackathon 2026.*

