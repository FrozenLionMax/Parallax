# Parallax — User Journey

> **Three real-world scenarios showing how Parallax transforms complex knowledge work**

---

## Scenario 1: Product Manager — Competitive Analysis

### Context
A PM at an AI startup needs a board-ready competitive analysis in 3 days.

---

### 📝 STEP 1 — ASK

**User input:**
> *"Prepare a competitive analysis of AI recruiting tools in India and draft a strategy document for our board meeting next Tuesday. Focus on pricing, key features, market positioning, and where we can differentiate."*

**What Parallax understands (Intent Parser output):**

| Dimension | Extracted |
|---|---|
| **Goal** | Competitive analysis + strategy document |
| **Domain** | AI recruiting tools, India market |
| **Deliverables** | (1) Competitor comparison, (2) Strategy document |
| **Audience** | Board of directors → executive tone, data-driven |
| **Deadline** | Tuesday, June 17 at 9:00 AM IST |
| **Focus areas** | Pricing, features, positioning, differentiation |
| **Implicit needs** | Charts/visuals, executive summary, professional formatting |

---

### 🗺️ STEP 2 — PLAN

**Parallax presents the task graph to the user:**

```
📋 EXECUTION PLAN — Competitive Analysis + Strategy Document
   Estimated time: 25 minutes | 3 Phases | 8 Tasks
   
   PHASE 1: RESEARCH (Parallel — ~8 min)
   ├─ T1 🔍 Research Agent: Identify all AI recruiting tools in India
   ├─ T2 🔍 Research Agent: Gather pricing & feature data per competitor
   └─ T3 🔍 Research Agent: Pull market reports & industry sizing data
   
   PHASE 2: ANALYSIS (Sequential — ~7 min)
   ├─ T4 📊 Analyst Agent: Build feature comparison matrix  [needs T1,T2]
   ├─ T5 📊 Analyst Agent: SWOT analysis per top competitor  [needs T4]
   └─ T6 📊 Analyst Agent: Market sizing & positioning map   [needs T3]
   
   PHASE 3: CREATION (Parallel then sequential — ~10 min)
   ├─ T7 ✍️ Creator Agent: Draft strategy document  [needs T4,T5,T6]
   ├─ T8 ✍️ Creator Agent: Create charts & visuals  [needs T4,T6]
   └─ T9 🛡️ Quality Agent: Final review             [needs T7,T8]
   
   [✅ Approve Plan]  [✏️ Modify]  [❌ Cancel]
```

**User clicks** ✅ Approve Plan.

---

### ⚡ STEP 3 — WATCH

**Live dashboard shows real-time agent progress:**

```
🔍 Research Agent (T1)  ██████████████████░░  90%  "Found 14 competitors"
🔍 Research Agent (T2)  ████████████████░░░░  80%  "Pricing for 11/14 collected"
🔍 Research Agent (T3)  ██████████████████████ 100% ✅ "3 market reports retrieved"
📊 Analyst Agent (T4)   ░░░░░░░░░░░░░░░░░░░░   0%  ⏳ Waiting for T1, T2
📊 Analyst Agent (T5)   ░░░░░░░░░░░░░░░░░░░░   0%  ⏳ Waiting for T4
📊 Analyst Agent (T6)   ████████████░░░░░░░░  60%  "Market sizing in progress"
✍️ Creator Agent (T7)   ░░░░░░░░░░░░░░░░░░░░   0%  ⏳ Waiting for analysis
🛡️ Quality Agent (T9)   ░░░░░░░░░░░░░░░░░░░░   0%  ⏳ Standby

⏱️ Elapsed: 6 min 23 sec | ETA: ~19 min remaining
```

**Inter-agent communication happening in background:**

```
🔍 Research → 📊 Analyst:
   "3 competitors have no public pricing. Found estimates in 2 blog posts 
    but credibility is low (0.4). Flagging for your analysis."

📊 Analyst → 🔍 Research:
   "Market report from Nasscom says ₹2,400 Cr. Blog says ₹4,100 Cr. 
    Can you find a third source to triangulate?"

🔍 Research → 📊 Analyst:
   "Found IMARC Group report: ₹3,200 Cr (2025), projected ₹5,800 Cr 
    by 2028. Source credibility: 0.88. Recommend using IMARC as primary."
```

---

### 💬 STEP 4 — GUIDE

**Confidence-based escalation — Analyst Agent asks the user:**

> 🤔 **Decision needed** (confidence: 0.65)
>
> I found conflicting market size data:
> | Source | Market Size | Year | Credibility |
> |---|---|---|---|
> | Nasscom | ₹2,400 Cr | 2024 | 0.92 |
> | IMARC Group | ₹3,200 Cr | 2025 | 0.88 |
> | TechBlog.in | ₹4,100 Cr | 2026 | 0.41 |
>
> **My recommendation**: Use IMARC Group (₹3,200 Cr, 2025) as the primary figure — it's the most recent credible source. Mention Nasscom as supporting data.
>
> [✅ Use recommendation] [🔄 Use Nasscom instead] [📝 Use custom approach]

**User clicks** ✅ Use recommendation.

**Parallax stores this preference in Procedural Memory:**
> *"User prefers: for market data, prioritize recent institutional reports over older ones. Avoid blog sources for quantitative claims."*

---

### ✅ STEP 5 — REVIEW

**Quality Agent completes final review. Deliverable presented:**

```
📦 DELIVERABLE READY — Competitive Analysis + Strategy

📄 Documents:
   ├── Strategy_Document.pdf (14 pages, board-formatted)
   ├── Executive_Summary.pdf (1 page)
   └── Appendix_Raw_Data.xlsx

📊 Embedded Visuals:
   ├── Market Positioning Map (bubble chart)
   ├── Feature Comparison Matrix (heat map)
   └── Market Growth Projection (line chart, 2024-2028)

🛡️ Quality Agent Notes:
   ⚠️ "Competitor X announced new pricing on June 10 — verify before 
       board meeting as our data is from May."
   ✅ "All financial claims sourced. 14 citations included."
   ✅ "Executive summary: 4 bullet points (within user preference)."

   [📥 Download All]  [✏️ Request Changes]  [📧 Send to Board]
```

---

### 🧠 STEP 6 — LEARN

**User provides feedback:**

> 👍 *"Great analysis. Two notes for next time: (1) Always include a 'So What?' section at the end of each competitor profile — what it means for us specifically. (2) The exec summary was perfect at 4 bullets — keep that length."*

**Parallax stores in Procedural Memory:**
- Competitive analyses should include a "So What?" section per competitor
- Executive summaries: 4 bullet points is the ideal length for this user
- Board documents: 14 pages is acceptable length

**Knowledge graph updated (Semantic Memory):**
- 14 new competitor entities with relationships
- Market size data points with source references
- User's company positioning relative to competitors

---

## Scenario 2: Software Engineer — Sprint Retrospective

### Context
An engineering lead needs to understand why the team missed their sprint deadline.

---

### 📝 STEP 1 — ASK

**User input:**
> *"Analyze our team's last sprint — pull the JIRA data, identify why we missed the deadline, find the blockers, and prepare a sprint retro document with action items."*

---

### 🗺️ STEP 2 — PLAN

```
📋 EXECUTION PLAN — Sprint Retrospective Analysis
   Estimated time: 15 minutes | 4 Phases | 7 Tasks
   
   PHASE 1: DATA COLLECTION (Parallel — ~4 min)
   ├─ T1 🔍 Research Agent: Pull JIRA sprint data via API
   │      (stories, bugs, story points, status, assignees)
   ├─ T2 🔍 Research Agent: Pull GitHub PR/commit data for the sprint
   └─ T3 🔍 Research Agent: Check Slack #engineering for blocker discussions
   
   PHASE 2: ANALYSIS (Sequential — ~5 min)
   ├─ T4 📊 Analyst Agent: Sprint velocity analysis  [needs T1]
   │      (planned vs delivered, burndown, per-developer breakdown)
   └─ T5 📊 Analyst Agent: Blocker identification    [needs T1,T2,T3]
         (root cause analysis, dependency mapping)
   
   PHASE 3: CREATION (~5 min)
   ├─ T6 ✍️ Creator Agent: Draft retro document      [needs T4,T5]
   └─ T7 ✍️ Creator Agent: Generate action items     [needs T5]
   
   PHASE 4: REVIEW (~1 min)
   └─ T8 🛡️ Quality Agent: Review for sensitivity   [needs T6,T7]
         (ensure no blame-oriented language)
```

---

### ⚡ STEP 3 — WATCH

```
🔍 Research Agent (T1)   ██████████████████████ 100% ✅ "42 tickets pulled"
🔍 Research Agent (T2)   ██████████████████████ 100% ✅ "87 PRs, 234 commits"
🔍 Research Agent (T3)   ██████████████████████ 100% ✅ "15 blocker threads found"
📊 Analyst Agent (T4)    ████████████████░░░░░░  75%  "Burndown chart generated"
📊 Analyst Agent (T5)    ████████████░░░░░░░░░░  55%  "3 root causes identified"
```

**Agent communication:**
```
📊 Analyst → 🔍 Research:
   "The JIRA data shows 12 story points were added mid-sprint. 
    Can you check who added them and find the Slack discussion?"

🔍 Research → 📊 Analyst:
   "Found it. Product manager added 3 stories on Day 5 after 
    client call. Slack thread: #product-updates, June 8."

📊 Analyst → ✍️ Creator:
   "Root cause #1: Scope creep (12 points added mid-sprint, 
    30% of total capacity). Frame diplomatically — focus on 
    process improvement, not blame."
```

---

### 💬 STEP 4 — GUIDE

> 🤔 **Sensitive content flag** (Quality Agent, confidence: 0.58)
>
> The analysis shows that **one developer** completed only 20% of assigned story points. Including individual performance data in a team retro document could be counterproductive.
>
> **Options:**
> 1. Include aggregate data only (team-level metrics)
> 2. Include individual breakdown but frame constructively
> 3. Create two versions: team retro + private manager report
>
> [1️⃣ Aggregate only] [2️⃣ Individual + constructive] [3️⃣ Two versions]

**User selects** 3️⃣ Two versions.

---

### ✅ STEP 5 — REVIEW

```
📦 DELIVERABLE READY — Sprint Retrospective

📄 Documents:
   ├── Sprint_24_Retro.pdf (Team version, 6 pages)
   ├── Sprint_24_Manager_Report.pdf (Private, individual metrics)
   └── Action_Items.md (5 action items with owners & deadlines)

📊 Key Findings:
   🔴 Root Cause 1: Mid-sprint scope creep (+12 story points, +30%)
   🟡 Root Cause 2: CI/CD pipeline failures (8 hrs blocked across team)
   🟡 Root Cause 3: External API dependency delayed 2 stories

📋 Top Action Items:
   1. Implement sprint scope-lock after Day 2 (Owner: PM)
   2. Migrate CI/CD to dedicated runners (Owner: DevOps)
   3. Add circuit breaker for external API dependency (Owner: Backend)

🛡️ Quality Notes:
   ✅ "No blame-oriented language in team version"
   ✅ "All data sourced from JIRA + GitHub"
```

---

### 🧠 STEP 6 — LEARN

> 👍 *"Perfect. Always create two versions for retros — team and manager. Never include individual metrics in the team version."*

**Stored**: Sprint retro = always two versions (team + private).

---

## Scenario 3: Startup Founder — Investor Outreach

### Context
A founder needs to identify the best VC matches for their AI startup's Series A.

---

### 📝 STEP 1 — ASK

**User input:**
> *"Research the top 20 VCs investing in AI in India, find their recent investments, identify the best 5 fits for our Series A, and draft personalized outreach emails for each."*

---

### 🗺️ STEP 2 — PLAN

```
📋 EXECUTION PLAN — VC Research + Outreach
   Estimated time: 30 minutes | 4 Phases | 9 Tasks
   
   PHASE 1: RESEARCH (Parallel — ~10 min)
   ├─ T1 🔍 Research: Identify top 20 AI-focused VCs in India
   ├─ T2 🔍 Research: Find recent investments per VC (last 18 months)
   ├─ T3 🔍 Research: Find partner profiles & investment thesis
   └─ T4 🔍 Research: Check for existing portfolio conflicts
   
   PHASE 2: ANALYSIS (~8 min)
   ├─ T5 📊 Analyst: Score & rank VCs by fit  [needs T1-T4]
   │      (stage match, sector focus, check size, thesis alignment)
   └─ T6 📊 Analyst: Identify connection paths  [needs T3]
         (mutual connections, events, warm intros)
   
   PHASE 3: CREATION (~10 min)
   ├─ T7 ✍️ Creator: Draft 5 personalized emails  [needs T5,T6]
   └─ T8 ✍️ Creator: Create VC comparison one-pager  [needs T5]
   
   PHASE 4: REVIEW (~2 min)
   └─ T9 🛡️ Quality: Review emails for tone & personalization
```

---

### ⚡ STEP 3 — WATCH

```
🔍 Research (T1)  ██████████████████████ 100% ✅ "23 VCs identified"
🔍 Research (T2)  ██████████████████░░░░  85%  "Portfolios for 19/23 VCs"
🔍 Research (T3)  ████████████████░░░░░░  75%  "14 partner profiles found"
🔍 Research (T4)  ██████████████████████ 100% ✅ "2 portfolio conflicts found"
📊 Analyst (T5)   ░░░░░░░░░░░░░░░░░░░░░   0%  ⏳ Waiting for research
```

---

### 💬 STEP 4 — GUIDE

> 🤔 **Decision needed** (confidence: 0.72)
>
> Two of your top-5 VCs have **potential portfolio conflicts**:
>
> | VC | Conflict | Risk Level |
> |---|---|---|
> | Peak XV | Invested in CompetitorX (similar space) | 🟡 Medium |
> | Lightspeed India | Portfolio company pivoting toward your space | 🟠 Moderate |
>
> **Options:**
> 1. Keep both — portfolio overlap isn't always a blocker
> 2. Replace Peak XV with next-best: Kalaari Capital
> 3. Replace both — move to Kalaari + Blume Ventures
> 4. Keep both but acknowledge overlap in outreach emails
>
> [1️⃣ Keep both] [2️⃣ Replace Peak XV] [3️⃣ Replace both] [4️⃣ Acknowledge]

**User selects** 4️⃣ Acknowledge — *"Good catch. Keep them but mention in the email that we see the overlap and explain our differentiation."*

---

### ✅ STEP 5 — REVIEW

```
📦 DELIVERABLE READY — VC Outreach Package

📄 Documents:
   ├── VC_Comparison_OnePager.pdf (Top 5 ranked with scores)
   └── Outreach_Strategy.md (approach plan per VC)

📧 Draft Emails (5):
   ├── accel_india_outreach.md — Personalized: references their 
   │   investment in SimilarCompanyY, our 3x growth rate
   ├── peak_xv_outreach.md — Addresses portfolio overlap directly,
   │   highlights differentiation vs CompetitorX
   ├── lightspeed_outreach.md — Acknowledges pivot risk, positions 
   │   us as strategic acquisition target for their portfolio co
   ├── elevation_capital_outreach.md — References partner's blog 
   │   post on "AI-first hiring," quotes their thesis
   └── matrix_partners_outreach.md — Leads with India market data, 
       aligns with their India-focus fund

🛡️ Quality Notes:
   ✅ "Each email references specific VC activities — not generic"
   ✅ "Portfolio conflicts acknowledged professionally"
   ⚠️ "Elevation partner's blog post is from Jan 2025 — thesis may 
       have evolved. Consider verifying."
```

---

### 🧠 STEP 6 — LEARN

> 👍 *"Excellent personalization. For investor emails, always lead with a specific reference to their recent activity — it shows we did our homework. Also, always flag portfolio conflicts proactively."*

**Stored**:
- Investor emails: always lead with specific reference to VC's recent activity
- Always proactively flag portfolio conflicts
- Preferred tone for investor outreach: confident but not salesy

---

## Key Takeaways Across All Scenarios

| Principle | How Parallax Delivers |
|---|---|
| **Complex work, simple input** | Natural language → full workflow execution |
| **Parallel efficiency** | Multiple agents work simultaneously |
| **Intelligent escalation** | Only bothers the user when genuinely needed |
| **Domain adaptation** | Same system works for PM, engineering, and business tasks |
| **Progressive trust** | System earns autonomy through consistent quality |
| **Continuous improvement** | Every interaction makes Parallax smarter |

---

*Team Parallax · IndiaRuns Hackathon 2026*

