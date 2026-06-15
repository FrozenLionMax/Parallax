"""
Parallax — AI Co-Pilots That See Work From Every Angle
Interactive Prototype | Team Parallax

This Streamlit app demonstrates the Parallax 6-step user journey
with 3 pre-built scenarios showing 10 AI co-pilots in action.
"""

import streamlit as st
import time
import json

# ─────────────────────────── PAGE CONFIG ───────────────────────────

st.set_page_config(
    page_title="Parallax — AI Co-Pilots",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────── CUSTOM CSS ───────────────────────────

st.markdown("""
<style>
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0A1628 0%, #0F1D32 50%, #0A1628 100%);
        color: #E2E8F0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    code, .stCode {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Hero title */
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4FF, #7B61FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        line-height: 1.1;
    }

    .hero-subtitle {
        font-size: 1.4rem;
        color: #94A3B8;
        text-align: center;
        font-weight: 300;
        margin-top: 0.5rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px 4px;
        letter-spacing: 0.5px;
    }

    .badge-cyan { background: rgba(0, 212, 255, 0.15); color: #00D4FF; border: 1px solid rgba(0, 212, 255, 0.3); }
    .badge-violet { background: rgba(123, 97, 255, 0.15); color: #7B61FF; border: 1px solid rgba(123, 97, 255, 0.3); }
    .badge-green { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }

    /* Glassmorphism cards */
    .glass-card {
        background: rgba(15, 29, 50, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(0, 212, 255, 0.3);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.1);
    }

    .glass-card-accent {
        background: rgba(15, 29, 50, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(123, 97, 255, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
    }

    /* Co-pilot tags */
    .copilot-tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }

    .tag-research { background: rgba(0, 212, 255, 0.15); color: #00D4FF; }
    .tag-analyst { background: rgba(59, 130, 246, 0.15); color: #3B82F6; }
    .tag-creator { background: rgba(139, 92, 246, 0.15); color: #8B5CF6; }
    .tag-action { background: rgba(245, 158, 11, 0.15); color: #F59E0B; }
    .tag-quality { background: rgba(16, 185, 129, 0.15); color: #10B981; }
    .tag-comms { background: rgba(20, 184, 166, 0.15); color: #14B8A6; }
    .tag-code { background: rgba(249, 115, 22, 0.15); color: #F97316; }
    .tag-data { background: rgba(239, 68, 68, 0.15); color: #EF4444; }
    .tag-design { background: rgba(236, 72, 153, 0.15); color: #EC4899; }
    .tag-compliance { background: rgba(148, 163, 184, 0.15); color: #94A3B8; }

    /* Step indicators */
    .step-indicator {
        display: inline-block;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        text-align: center;
        line-height: 36px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-right: 8px;
    }

    .step-active { background: linear-gradient(135deg, #00D4FF, #7B61FF); color: white; }
    .step-done { background: #10B981; color: white; }
    .step-pending { background: rgba(255,255,255,0.1); color: #64748B; }

    /* Progress animations */
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.6); }
    }

    .pulse { animation: pulse-glow 2s ease-in-out infinite; }

    /* Escalation card */
    .escalation-card {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    }

    /* Chat messages */
    .agent-msg {
        background: rgba(15, 29, 50, 0.8);
        border-left: 3px solid;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.9rem;
    }

    .msg-research { border-color: #00D4FF; }
    .msg-analyst { border-color: #3B82F6; }
    .msg-creator { border-color: #8B5CF6; }
    .msg-quality { border-color: #10B981; }
    .msg-compliance { border-color: #94A3B8; }
    .msg-data { border-color: #EF4444; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF, #7B61FF);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
        transform: translateY(-2px);
    }

    /* Section divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
        margin: 2rem 0;
    }

    /* Stats */
    .stat-number {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4FF, #7B61FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── SCENARIOS ───────────────────────────

SCENARIOS = {
    "Competitive Analysis for Board Meeting": {
        "input": "Prepare a competitive analysis of AI recruiting tools in India and draft a strategy document for our board meeting next Tuesday.",
        "intent": {
            "Goal": "Competitive analysis + strategy document",
            "Domain": "AI recruiting tools, India market",
            "Audience": "Board of directors (executive tone)",
            "Deadline": "Tuesday, June 17 at 9:00 AM",
            "Focus": "Pricing, features, positioning, differentiation",
        },
        "tasks": [
            {"id": "T1", "name": "Identify AI recruiting tools in India", "copilot": "🔍 Research", "color": "cyan", "duration": 3},
            {"id": "T2", "name": "Gather pricing & feature data", "copilot": "🔍 Research", "color": "cyan", "duration": 4},
            {"id": "T3", "name": "Pull live market metrics", "copilot": "📡 Data", "color": "red", "duration": 2},
            {"id": "T4", "name": "Build feature comparison matrix", "copilot": "📊 Analyst", "color": "blue", "duration": 3},
            {"id": "T5", "name": "SWOT analysis per competitor", "copilot": "📊 Analyst", "color": "blue", "duration": 3},
            {"id": "T6", "name": "Draft strategy document", "copilot": "✍️ Creator", "color": "violet", "duration": 4},
            {"id": "T7", "name": "Design charts & visuals", "copilot": "🎨 Design", "color": "pink", "duration": 3},
            {"id": "T8", "name": "Compliance review", "copilot": "🔐 Compliance", "color": "grey", "duration": 1},
            {"id": "T9", "name": "Quality review & fact-check", "copilot": "🛡️ Quality", "color": "green", "duration": 2},
        ],
        "escalation": {
            "copilot": "📊 Analyst Co-Pilot",
            "confidence": 0.65,
            "message": "I found conflicting market size data from different sources:",
            "options": [
                {"source": "Nasscom Report", "value": "₹2,400 Cr", "year": "2024", "credibility": "0.92"},
                {"source": "IMARC Group", "value": "₹3,200 Cr", "year": "2025", "credibility": "0.88"},
                {"source": "TechBlog.in", "value": "₹4,100 Cr", "year": "2026", "credibility": "0.41"},
            ],
            "recommendation": "Use IMARC Group (₹3,200 Cr, 2025) — most recent credible source. Mention Nasscom as supporting data.",
        },
        "agent_comms": [
            {"from": "🔍 Research", "to": "📊 Analyst", "msg": "Found 14 competitors. 3 have no public pricing — found estimates in blog posts but credibility is low (0.41). Flagging for your analysis.", "cls": "msg-research"},
            {"from": "📡 Data", "to": "📊 Analyst", "msg": "Pulled live market metrics from 3 industry dashboards. Conversion data shows 23% YoY growth in AI recruiting adoption.", "cls": "msg-data"},
            {"from": "📊 Analyst", "to": "✍️ Creator", "msg": "Key insight: market is 3x larger than assumed. Flag this prominently — it changes the strategy recommendation.", "cls": "msg-analyst"},
            {"from": "🛡️ Quality", "to": "✍️ Creator", "msg": "Paragraph 3 says 'latest data' but source is from March 2026. Add the date explicitly to avoid misleading the board.", "cls": "msg-quality"},
            {"from": "🔐 Compliance", "to": "⚡ Action", "msg": "Document contains 2 competitor revenue figures sourced from estimates. Add disclaimer: 'Revenue figures are estimates from public sources.'", "cls": "msg-compliance"},
        ],
        "output": {
            "documents": [
                "📄 Strategy_Document.pdf — 14 pages, board-formatted",
                "📋 Executive_Summary.pdf — 1 page, 4 bullet points",
                "📊 Appendix_Raw_Data.xlsx — Full competitor data",
            ],
            "visuals": [
                "📈 Market Positioning Map (bubble chart)",
                "🗂️ Feature Comparison Matrix (heat map)",
                "📉 Market Growth Projection (2024-2028 line chart)",
            ],
            "quality_notes": [
                "✅ All financial claims sourced — 14 citations included",
                "✅ Executive summary: 4 bullet points (optimal length)",
                "⚠️ Competitor X announced new pricing on June 10 — verify before board meeting",
                "✅ Compliance: Revenue disclaimer added to estimated figures",
            ],
            "time_saved": "3-4 days → 25 minutes",
        },
    },
    "Sprint Retrospective Analysis": {
        "input": "Analyze our team's last sprint — pull the JIRA data, identify why we missed the deadline, find the blockers, and prepare a sprint retro document with action items.",
        "intent": {
            "Goal": "Sprint retrospective with root cause analysis",
            "Data Sources": "JIRA, GitHub, Slack",
            "Audience": "Engineering team + Engineering Manager",
            "Sensitivity": "Individual performance data — handle carefully",
            "Deliverable": "Retro doc + action items with owners",
        },
        "tasks": [
            {"id": "T1", "name": "Pull JIRA sprint data", "copilot": "📡 Data", "color": "red", "duration": 2},
            {"id": "T2", "name": "Pull GitHub PR/commit data", "copilot": "📡 Data", "color": "red", "duration": 2},
            {"id": "T3", "name": "Scan Slack for blocker discussions", "copilot": "🔍 Research", "color": "cyan", "duration": 3},
            {"id": "T4", "name": "Sprint velocity analysis", "copilot": "📊 Analyst", "color": "blue", "duration": 3},
            {"id": "T5", "name": "Root cause identification", "copilot": "📊 Analyst", "color": "blue", "duration": 3},
            {"id": "T6", "name": "Draft retro document", "copilot": "✍️ Creator", "color": "violet", "duration": 3},
            {"id": "T7", "name": "Generate action items", "copilot": "✍️ Creator", "color": "violet", "duration": 2},
            {"id": "T8", "name": "Sensitivity review", "copilot": "🛡️ Quality", "color": "green", "duration": 2},
        ],
        "escalation": {
            "copilot": "🛡️ Quality Co-Pilot",
            "confidence": 0.58,
            "message": "The analysis shows one developer completed only 20% of assigned story points. Including individual performance data in a team retro could be counterproductive.",
            "options": [
                {"source": "Option A", "value": "Aggregate only", "year": "Team-level metrics", "credibility": "Safe"},
                {"source": "Option B", "value": "Individual + constructive framing", "year": "Detailed but diplomatic", "credibility": "Medium risk"},
                {"source": "Option C", "value": "Two versions: Team + Private Manager report", "year": "Best of both worlds", "credibility": "Recommended"},
            ],
            "recommendation": "Create two versions — team retro (aggregate) + private manager report (individual). This is the safest and most professional approach.",
        },
        "agent_comms": [
            {"from": "📡 Data", "to": "📊 Analyst", "msg": "Pulled 42 JIRA tickets and 87 PRs. 12 story points were added mid-sprint on Day 5.", "cls": "msg-data"},
            {"from": "📊 Analyst", "to": "🔍 Research", "msg": "12 points added mid-sprint is suspicious. Can you find the Slack discussion about why?", "cls": "msg-analyst"},
            {"from": "🔍 Research", "to": "📊 Analyst", "msg": "Found it. PM added 3 stories after client call. Slack thread: #product-updates, June 8.", "cls": "msg-research"},
            {"from": "📊 Analyst", "to": "✍️ Creator", "msg": "Root cause #1: Scope creep (12 pts added mid-sprint = 30% of capacity). Frame diplomatically.", "cls": "msg-analyst"},
        ],
        "output": {
            "documents": [
                "📄 Sprint_24_Retro.pdf — Team version, 6 pages",
                "📄 Sprint_24_Manager_Report.pdf — Private, individual metrics",
                "📋 Action_Items.md — 5 items with owners & deadlines",
            ],
            "visuals": [
                "📉 Sprint Burndown Chart",
                "📊 Velocity Trend (last 6 sprints)",
                "🗂️ Blocker Dependency Map",
            ],
            "quality_notes": [
                "✅ No blame-oriented language in team version",
                "✅ Individual metrics only in private manager report",
                "✅ All data sourced from JIRA + GitHub — verifiable",
                "🔴 Root Cause 1: Mid-sprint scope creep (+12 pts, +30%)",
                "🟡 Root Cause 2: CI/CD pipeline failures (8 hrs blocked)",
                "🟡 Root Cause 3: External API dependency delayed 2 stories",
            ],
            "time_saved": "1-2 days → 18 minutes",
        },
    },
    "Investor Outreach Campaign": {
        "input": "Research the top 20 VCs investing in AI in India, find their recent investments, identify the best 5 fits for our Series A, and draft personalized outreach emails for each.",
        "intent": {
            "Goal": "VC research + ranked shortlist + personalized outreach",
            "Domain": "AI venture capital, India",
            "Stage": "Series A fundraising",
            "Deliverable": "VC comparison + 5 personalized emails",
            "Tone": "Confident but not salesy",
        },
        "tasks": [
            {"id": "T1", "name": "Identify top 20 AI-focused VCs in India", "copilot": "🔍 Research", "color": "cyan", "duration": 4},
            {"id": "T2", "name": "Find recent investments per VC", "copilot": "🔍 Research", "color": "cyan", "duration": 4},
            {"id": "T3", "name": "Pull partner profiles & thesis", "copilot": "🔍 Research", "color": "cyan", "duration": 3},
            {"id": "T4", "name": "Check portfolio conflicts", "copilot": "🔍 Research", "color": "cyan", "duration": 2},
            {"id": "T5", "name": "Score & rank VCs by fit", "copilot": "📊 Analyst", "color": "blue", "duration": 3},
            {"id": "T6", "name": "Identify connection paths", "copilot": "📊 Analyst", "color": "blue", "duration": 2},
            {"id": "T7", "name": "Draft 5 personalized emails", "copilot": "✍️ Creator", "color": "violet", "duration": 5},
            {"id": "T8", "name": "Compliance check on outreach", "copilot": "🔐 Compliance", "color": "grey", "duration": 1},
            {"id": "T9", "name": "Review tone & personalization", "copilot": "🛡️ Quality", "color": "green", "duration": 2},
        ],
        "escalation": {
            "copilot": "📊 Analyst Co-Pilot",
            "confidence": 0.72,
            "message": "Two of your top-5 VCs have potential portfolio conflicts:",
            "options": [
                {"source": "Peak XV Partners", "value": "Invested in CompetitorX", "year": "Similar space", "credibility": "🟡 Medium risk"},
                {"source": "Lightspeed India", "value": "Portfolio co pivoting", "year": "Toward your space", "credibility": "🟠 Moderate risk"},
                {"source": "Keep both", "value": "Acknowledge overlap in emails", "year": "Transparent approach", "credibility": "✅ Recommended"},
            ],
            "recommendation": "Keep both VCs but acknowledge the overlap directly in outreach emails. Transparency builds trust with investors.",
        },
        "agent_comms": [
            {"from": "🔍 Research", "to": "📊 Analyst", "msg": "Found 23 VCs matching criteria. 2 have potential portfolio conflicts with our space.", "cls": "msg-research"},
            {"from": "📊 Analyst", "to": "✍️ Creator", "msg": "Top 5 ranked. #1 Accel India (98% fit), #2 Elevation (92%), #3 Peak XV (87% but conflict), #4 Lightspeed (85% but pivot risk), #5 Matrix (83%).", "cls": "msg-analyst"},
            {"from": "✍️ Creator", "to": "🛡️ Quality", "msg": "5 emails drafted. Each references specific VC activity — blog posts, recent investments, partner interviews.", "cls": "msg-creator"},
            {"from": "🛡️ Quality", "to": "✍️ Creator", "msg": "Elevation partner's blog post referenced is from Jan 2025 — thesis may have evolved. Recommend verifying.", "cls": "msg-quality"},
        ],
        "output": {
            "documents": [
                "📄 VC_Comparison_OnePager.pdf — Top 5 ranked with fit scores",
                "📋 Outreach_Strategy.md — Approach plan per VC",
                "📧 5 personalized outreach emails (each references specific VC activity)",
            ],
            "visuals": [
                "📊 VC Fit Score Matrix (radar chart)",
                "🗂️ Portfolio Overlap Analysis",
                "📈 Connection Path Map",
            ],
            "quality_notes": [
                "✅ Each email references specific VC activities — not generic",
                "✅ Portfolio conflicts acknowledged professionally",
                "⚠️ Elevation partner's blog post is from Jan 2025 — verify thesis",
                "✅ Compliance: No confidential data in outreach emails",
            ],
            "time_saved": "2-3 days → 30 minutes",
        },
    },
}

# ─────────────────────────── SESSION STATE ───────────────────────────

if "step" not in st.session_state:
    st.session_state.step = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "escalation_choice" not in st.session_state:
    st.session_state.escalation_choice = None

def go_to_step(step):
    st.session_state.step = step

def select_scenario(name):
    st.session_state.scenario = name
    st.session_state.step = 1
    st.session_state.escalation_choice = None

# ─────────────────────────── STEP 0: LANDING ───────────────────────────

def render_landing():
    st.markdown("")
    st.markdown("")

    st.markdown('<p class="hero-title">⬡ Parallax</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">AI Co-Pilots That See Work From Every Angle</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0;">
        <span class="hero-badge badge-cyan">10 AI Co-Pilots</span>
        <span class="hero-badge badge-violet">Multi-Agent Orchestration</span>
        <span class="hero-badge badge-green">Adaptive Memory</span>
        <span class="hero-badge badge-cyan">Confidence-Based Trust</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Co-pilot fleet
    st.markdown("### 🤖 Meet the 10 Co-Pilots")

    col1, col2, col3, col4, col5 = st.columns(5)
    copilots_row1 = [
        ("🔍", "Research", "The Investigator", "tag-research"),
        ("📊", "Analyst", "The Pattern Finder", "tag-analyst"),
        ("✍️", "Creator", "The Wordsmith", "tag-creator"),
        ("⚡", "Action", "The Executor", "tag-action"),
        ("🛡️", "Quality", "The Guardian", "tag-quality"),
    ]
    for col, (icon, name, title, cls) in zip([col1, col2, col3, col4, col5], copilots_row1):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding: 16px;">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: 700; margin: 4px 0;">{name}</div>
                <div style="font-size: 0.75rem; color: #64748B;">{title}</div>
            </div>
            """, unsafe_allow_html=True)

    col6, col7, col8, col9, col10 = st.columns(5)
    copilots_row2 = [
        ("💬", "Comms", "The Connector", "tag-comms"),
        ("💻", "Code", "The Engineer", "tag-code"),
        ("📡", "Data", "The Sensor", "tag-data"),
        ("🎨", "Design", "The Architect", "tag-design"),
        ("🔐", "Compliance", "The Sentinel", "tag-compliance"),
    ]
    for col, (icon, name, title, cls) in zip([col6, col7, col8, col9, col10], copilots_row2):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding: 16px;">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: 700; margin: 4px 0;">{name}</div>
                <div style="font-size: 0.75rem; color: #64748B;">{title}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Scenario selection
    st.markdown("### 🚀 Try a Scenario")
    st.markdown("*Select a real-world scenario to see Parallax in action:*")

    col1, col2, col3 = st.columns(3)
    scenarios = list(SCENARIOS.keys())

    with col1:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 1.5rem;">📊</div>
            <div style="font-weight: 700; margin: 8px 0;">Competitive Analysis</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Product Manager preparing a board-ready competitive analysis</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Run Scenario", key="s1"):
            select_scenario(scenarios[0])
            st.rerun()

    with col2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 1.5rem;">🔧</div>
            <div style="font-weight: 700; margin: 8px 0;">Sprint Retrospective</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Engineering lead analyzing why the team missed a sprint deadline</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Run Scenario", key="s2"):
            select_scenario(scenarios[1])
            st.rerun()

    with col3:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 1.5rem;">💰</div>
            <div style="font-weight: 700; margin: 8px 0;">Investor Outreach</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Startup founder researching VCs and drafting personalized emails</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ Run Scenario", key="s3"):
            select_scenario(scenarios[2])
            st.rerun()

    # Footer
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #475569; font-size: 0.85rem;">
        Team Parallax · AI Co-Pilots That See Work From Every Angle
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────── STEP 1: ASK ───────────────────────────

def render_ask():
    scenario = SCENARIOS[st.session_state.scenario]

    render_step_header(1, "ASK", "You tell Parallax what you need")

    st.markdown(f"""
    <div class="glass-card-accent">
        <div style="font-size: 0.8rem; color: #7B61FF; font-weight: 600; margin-bottom: 8px;">YOUR INPUT</div>
        <div style="font-size: 1.1rem; font-style: italic; color: #E2E8F0;">"{scenario['input']}"</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🧠 Parallax Intent Parser Output")

    for key, value in scenario["intent"].items():
        st.markdown(f"""
        <div style="display: flex; margin: 6px 0;">
            <div style="min-width: 140px; color: #64748B; font-weight: 600; font-size: 0.85rem;">{key}</div>
            <div style="color: #E2E8F0; font-size: 0.85rem;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("✅ Looks good — show me the plan →", key="to_plan"):
        go_to_step(2)
        st.rerun()


# ─────────────────────────── STEP 2: PLAN ───────────────────────────

def render_plan():
    scenario = SCENARIOS[st.session_state.scenario]
    tasks = scenario["tasks"]

    render_step_header(2, "PLAN", "Parallax shows the task graph and co-pilots assigned")

    total_time = sum(t["duration"] for t in tasks)
    copilots_used = len(set(t["copilot"] for t in tasks))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div style="text-align:center;"><span class="stat-number">{len(tasks)}</span><br><span class="stat-label">Tasks</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="text-align:center;"><span class="stat-number">{copilots_used}</span><br><span class="stat-label">Co-Pilots</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="text-align:center;"><span class="stat-number">~{total_time}</span><br><span class="stat-label">Est. Minutes</span></div>', unsafe_allow_html=True)

    st.markdown("#### 📋 Execution Plan")

    for task in tasks:
        color_map = {"cyan": "#00D4FF", "blue": "#3B82F6", "violet": "#8B5CF6", "red": "#EF4444", "green": "#10B981", "pink": "#EC4899", "grey": "#94A3B8"}
        color = color_map.get(task["color"], "#64748B")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 6px 0; padding: 10px 16px; border-radius: 8px; background: rgba(255,255,255,0.03); border-left: 3px solid {color};">
            <div style="min-width: 40px; font-weight: 700; color: #64748B;">{task['id']}</div>
            <div style="flex: 1; color: #E2E8F0;">{task['name']}</div>
            <div style="color: {color}; font-weight: 600; font-size: 0.85rem;">{task['copilot']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("✅ Approve Plan — Start Co-Pilots →", key="to_watch"):
        go_to_step(3)
        st.rerun()


# ─────────────────────────── STEP 3: WATCH ───────────────────────────

def render_watch():
    scenario = SCENARIOS[st.session_state.scenario]
    tasks = scenario["tasks"]

    render_step_header(3, "WATCH", "Co-pilots are working — watch live progress")

    # Simulate progress
    progress_container = st.container()

    with progress_container:
        # Group tasks by co-pilot
        copilot_tasks = {}
        for task in tasks:
            cp = task["copilot"]
            if cp not in copilot_tasks:
                copilot_tasks[cp] = []
            copilot_tasks[cp].append(task)

        progress_bars = {}
        for cp, cp_tasks in copilot_tasks.items():
            color_map = {"🔍 Research": "#00D4FF", "📊 Analyst": "#3B82F6", "✍️ Creator": "#8B5CF6",
                        "⚡ Action": "#F59E0B", "🛡️ Quality": "#10B981", "💬 Comms": "#14B8A6",
                        "💻 Code": "#F97316", "📡 Data": "#EF4444", "🎨 Design": "#EC4899",
                        "🔐 Compliance": "#94A3B8"}
            color = color_map.get(cp, "#64748B")

            task_names = ", ".join(t["name"] for t in cp_tasks)
            st.markdown(f"""
            <div style="margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 600; color: {color};">{cp}</span>
                    <span style="color: #64748B; font-size: 0.8rem;">{task_names}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            progress_bars[cp] = st.progress(0)

    # Animate progress
    for pct in range(0, 101, 5):
        for cp, bar in progress_bars.items():
            # Different co-pilots progress at different rates
            adjusted = min(100, pct + hash(cp) % 20 - 10)
            adjusted = max(0, adjusted)
            bar.progress(min(adjusted, 100))
        time.sleep(0.08)

    # Set all to 100%
    for bar in progress_bars.values():
        bar.progress(100)

    # Show agent communications
    st.markdown("#### 💬 Co-Pilot Communications")
    for comm in scenario["agent_comms"]:
        st.markdown(f"""
        <div class="agent-msg {comm['cls']}">
            <div style="font-weight: 600; font-size: 0.8rem; color: #94A3B8; margin-bottom: 4px;">
                {comm['from']} → {comm['to']}
            </div>
            <div>{comm['msg']}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.3)

    st.markdown("")
    if st.button("⚠️ Decision needed — Continue →", key="to_guide"):
        go_to_step(4)
        st.rerun()


# ─────────────────────────── STEP 4: GUIDE ───────────────────────────

def render_guide():
    scenario = SCENARIOS[st.session_state.scenario]
    esc = scenario["escalation"]

    render_step_header(4, "GUIDE", "A co-pilot needs your decision")

    st.markdown(f"""
    <div class="escalation-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-weight: 700; font-size: 1.1rem;">🤔 Decision Needed</span>
            <span style="background: rgba(245,158,11,0.2); color: #F59E0B; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                Confidence: {esc['confidence']:.0%}
            </span>
        </div>
        <div style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 8px;">From: {esc['copilot']}</div>
        <div style="color: #E2E8F0; margin-bottom: 16px;">{esc['message']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Options table
    for opt in esc["options"]:
        st.markdown(f"""
        <div style="display: flex; padding: 10px 16px; margin: 4px 0; background: rgba(255,255,255,0.03); border-radius: 8px;">
            <div style="min-width: 160px; font-weight: 600; color: #E2E8F0;">{opt['source']}</div>
            <div style="min-width: 120px; color: #00D4FF;">{opt['value']}</div>
            <div style="min-width: 120px; color: #64748B;">{opt['year']}</div>
            <div style="color: #94A3B8;">{opt['credibility']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top: 16px; padding: 12px 16px; background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: 8px;">
        <span style="font-weight: 600; color: #10B981;">💡 Recommendation:</span>
        <span style="color: #E2E8F0;"> {esc['recommendation']}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("✅ Use Recommendation — Continue →", key="to_review"):
        st.session_state.escalation_choice = "recommendation"
        go_to_step(5)
        st.rerun()


# ─────────────────────────── STEP 5: REVIEW ───────────────────────────

def render_review():
    scenario = SCENARIOS[st.session_state.scenario]
    output = scenario["output"]

    render_step_header(5, "REVIEW", "Quality-checked deliverables ready for you")

    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <span class="stat-number" style="font-size: 1.8rem;">{output['time_saved']}</span><br>
        <span class="stat-label">Time Saved</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📄 Documents")
        for doc in output["documents"]:
            st.markdown(f"""
            <div style="padding: 8px 12px; margin: 4px 0; background: rgba(255,255,255,0.03); border-radius: 6px; font-size: 0.9rem;">
                {doc}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### 📊 Visuals")
        for viz in output["visuals"]:
            st.markdown(f"""
            <div style="padding: 8px 12px; margin: 4px 0; background: rgba(255,255,255,0.03); border-radius: 6px; font-size: 0.9rem;">
                {viz}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🛡️ Quality Co-Pilot Notes")
        for note in output["quality_notes"]:
            if note.startswith("✅"):
                color = "#10B981"
            elif note.startswith("⚠️"):
                color = "#F59E0B"
            elif note.startswith("🔴"):
                color = "#EF4444"
            elif note.startswith("🟡"):
                color = "#F59E0B"
            else:
                color = "#94A3B8"

            st.markdown(f"""
            <div style="padding: 8px 12px; margin: 4px 0; background: rgba(255,255,255,0.03); border-radius: 6px; font-size: 0.9rem; border-left: 3px solid {color};">
                {note}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("👍 Looks great — Give feedback →", key="to_learn"):
        go_to_step(6)
        st.rerun()


# ─────────────────────────── STEP 6: LEARN ───────────────────────────

def render_learn():
    render_step_header(6, "LEARN", "Your feedback makes Parallax smarter")

    st.markdown("""
    <div class="glass-card-accent">
        <div style="font-size: 0.8rem; color: #7B61FF; font-weight: 600; margin-bottom: 12px;">FEEDBACK</div>
        <div style="color: #E2E8F0;">How was this output? Your feedback is stored in Parallax's Procedural Memory and improves all future tasks.</div>
    </div>
    """, unsafe_allow_html=True)

    feedback = st.text_area(
        "Your feedback (optional):",
        placeholder="e.g., 'Make executive summaries shorter — bullet points only, max 4 items'",
        height=100,
    )

    if st.button("✅ Submit Feedback", key="submit_feedback"):
        if feedback:
            st.success(f"**Preference stored in Procedural Memory:**")
            st.info(f'"{feedback}"')
            st.markdown("""
            <div class="glass-card" style="margin-top: 16px;">
                <div style="font-weight: 700; color: #10B981; margin-bottom: 8px;">🧠 Memory Updated</div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    This preference will be applied to all future tasks. Parallax now knows your style better.
                    Over time, it will need fewer decisions from you as it learns your patterns.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**No feedback — task complete!**")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #E2E8F0;">That's Parallax.</div>
            <div style="color: #94A3B8; margin-top: 8px; font-size: 1rem;">
                10 AI co-pilots. One task at a time. Smarter every day.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try Another Scenario", key="restart"):
                st.session_state.step = 0
                st.session_state.scenario = None
                st.session_state.escalation_choice = None
                st.rerun()
        with col2:
            if st.button("📖 View Architecture", key="arch"):
                st.markdown("[View full architecture on GitHub →](https://github.com/FrozenLionMax/Parallax)")


# ─────────────────────────── HELPERS ───────────────────────────

def render_step_header(step_num, step_name, description):
    """Render the step progress bar and header."""
    steps = ["ASK", "PLAN", "WATCH", "GUIDE", "REVIEW", "LEARN"]

    # Progress dots
    dots_html = ""
    for i, s in enumerate(steps, 1):
        if i < step_num:
            dots_html += f'<span class="step-indicator step-done">{i}</span>'
        elif i == step_num:
            dots_html += f'<span class="step-indicator step-active">{i}</span>'
        else:
            dots_html += f'<span class="step-indicator step-pending">{i}</span>'

    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0 0.5rem 0;">
        {dots_html}
    </div>
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <div style="font-size: 0.8rem; color: #7B61FF; font-weight: 600; letter-spacing: 2px;">STEP {step_num}</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #E2E8F0;">{step_name}</div>
        <div style="font-size: 0.95rem; color: #94A3B8;">{description}</div>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if step_num > 1:
        if st.button("← Back", key=f"back_{step_num}"):
            go_to_step(step_num - 1)
            st.rerun()


# ─────────────────────────── MAIN ───────────────────────────

def main():
    step = st.session_state.step

    if step == 0:
        render_landing()
    elif step == 1:
        render_ask()
    elif step == 2:
        render_plan()
    elif step == 3:
        render_watch()
    elif step == 4:
        render_guide()
    elif step == 5:
        render_review()
    elif step == 6:
        render_learn()

if __name__ == "__main__":
    main()
