"""
Parallax — AI Co-Pilots That See Work From Every Angle
Core configuration and constants.
"""

# ─────────────────────── BRANDING ───────────────────────

APP_NAME = "Parallax"
TAGLINE = "AI Co-Pilots That See Work From Every Angle"
VERSION = "0.1.0"

# ─────────────────────── CO-PILOT REGISTRY ───────────────────────

COPILOT_REGISTRY = {
    "research": {
        "name": "Research Co-Pilot",
        "codename": "The Investigator",
        "icon": "🔍",
        "color": "#00D4FF",
        "description": "Finds, verifies, and synthesizes information from any source.",
        "capabilities": [
            "Web search & deep crawling",
            "Document analysis (PDF, DOCX, HTML)",
            "Source credibility scoring",
            "Contradiction detection",
            "Knowledge extraction",
        ],
    },
    "analyst": {
        "name": "Analyst Co-Pilot",
        "codename": "The Pattern Finder",
        "icon": "📊",
        "color": "#3B82F6",
        "description": "Crunches data, spots patterns, generates insights and visualizations.",
        "capabilities": [
            "Statistical analysis",
            "Comparative analysis (SWOT, matrices)",
            "Data visualization",
            "Root cause analysis",
            "Quantitative forecasting",
        ],
    },
    "creator": {
        "name": "Creator Co-Pilot",
        "codename": "The Wordsmith",
        "icon": "✍️",
        "color": "#8B5CF6",
        "description": "Generates polished, audience-aware content.",
        "capabilities": [
            "Audience-aware writing",
            "Document generation",
            "Email drafting",
            "Presentation content",
            "Code documentation",
        ],
    },
    "action": {
        "name": "Action Co-Pilot",
        "codename": "The Executor",
        "icon": "⚡",
        "color": "#F59E0B",
        "description": "Takes real-world actions — the last mile that other AI misses.",
        "capabilities": [
            "Send emails via API",
            "Create JIRA/Linear tickets",
            "Schedule calendar events",
            "Post to Slack channels",
            "Upload files to Drive/Notion",
        ],
    },
    "quality": {
        "name": "Quality Co-Pilot",
        "codename": "The Guardian",
        "icon": "🛡️",
        "color": "#10B981",
        "description": "Reviews everything before delivery — the built-in quality gate.",
        "capabilities": [
            "Factual accuracy verification",
            "Completeness checks",
            "Tone & audience alignment",
            "Bias detection",
            "Internal consistency review",
        ],
    },
    "communication": {
        "name": "Communication Co-Pilot",
        "codename": "The Connector",
        "icon": "💬",
        "color": "#14B8A6",
        "description": "Manages meetings, follow-ups, and team coordination.",
        "capabilities": [
            "Meeting agenda generation",
            "Note-taking & summarization",
            "Action item tracking",
            "Follow-up automation",
            "Stakeholder updates",
        ],
    },
    "code": {
        "name": "Code Co-Pilot",
        "codename": "The Engineer",
        "icon": "💻",
        "color": "#F97316",
        "description": "Writes, reviews, debugs, and deploys code.",
        "capabilities": [
            "Code generation from specs",
            "Code review & analysis",
            "Debugging & error tracing",
            "Script automation",
            "Documentation generation",
        ],
    },
    "data": {
        "name": "Data Co-Pilot",
        "codename": "The Sensor",
        "icon": "📡",
        "color": "#EF4444",
        "description": "Connects to live systems, pulls real-time data, monitors metrics.",
        "capabilities": [
            "Natural language → SQL/NoSQL",
            "API data retrieval",
            "Dashboard monitoring",
            "Data pipeline health checks",
            "Real-time metric queries",
        ],
    },
    "design": {
        "name": "Design Co-Pilot",
        "codename": "The Architect",
        "icon": "🎨",
        "color": "#EC4899",
        "description": "Creates visual designs, wireframes, diagrams, and brand assets.",
        "capabilities": [
            "UI/UX wireframes",
            "Presentation design",
            "Diagram generation",
            "Brand consistency enforcement",
            "Image & icon creation",
        ],
    },
    "compliance": {
        "name": "Compliance Co-Pilot",
        "codename": "The Sentinel",
        "icon": "🔐",
        "color": "#94A3B8",
        "description": "Ensures outputs meet regulatory, legal, and policy requirements.",
        "capabilities": [
            "Regulatory scanning (GDPR, DPDPA)",
            "Policy enforcement",
            "Contract review",
            "Audit trail maintenance",
            "Data classification",
        ],
    },
}

# ─────────────────────── CONFIDENCE THRESHOLDS ───────────────────────

CONFIDENCE_AUTO_EXECUTE = 0.90    # >90% → do it, notify after
CONFIDENCE_HOLD_APPROVAL = 0.70   # 70-90% → do it, hold for approval
# Below 70% → escalate to user

# ─────────────────────── MESSAGE TYPES ───────────────────────

class MessageType:
    TASK_ASSIGNMENT = "TASK_ASSIGNMENT"
    RESULT = "RESULT"
    QUERY = "QUERY"
    ESCALATION = "ESCALATION"
    FEEDBACK = "FEEDBACK"
    STATUS = "STATUS"
    ERROR = "ERROR"

# ─────────────────────── TASK STATES ───────────────────────

class TaskState:
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
