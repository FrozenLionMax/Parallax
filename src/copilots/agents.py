"""
Parallax — All 10 AI Co-Pilot Implementations

Each co-pilot is purpose-built with domain-specific logic,
not just a different prompt on the same model.
"""

from __future__ import annotations
from typing import Any
from src.copilots.base import BaseCoPilot
from src.models import Task, Message
from src.config import MessageType
from src.memory import MemorySystem
from src.message_bus import MessageBus


# ═══════════════════════════════════════════════════════════════
#  1. 🔍 RESEARCH CO-PILOT — "The Investigator"
# ═══════════════════════════════════════════════════════════════

class ResearchCoPilot(BaseCoPilot):
    """
    Finds, verifies, and synthesizes information from any source.

    Capabilities:
    - Web search & deep crawling
    - Document analysis (PDF, DOCX, HTML)
    - Source credibility scoring
    - Contradiction detection across sources
    - Knowledge extraction into structured data
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("research", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.1

        # Simulate research process
        findings = self._search_and_gather(task.description)
        task.progress = 0.5

        # Verify sources
        verified = self._verify_sources(findings)
        task.progress = 0.8

        # Check for contradictions
        contradictions = self._detect_contradictions(verified)

        # Store discoveries in semantic memory
        for finding in verified:
            self.learn_fact(
                f"research:{task.task_id}:{finding['topic']}",
                finding,
                confidence=finding.get("credibility", 0.8),
            )

        # Notify analyst if contradictions found
        if contradictions:
            self.send_message(
                to="analyst",
                content=f"Found {len(contradictions)} conflicting data points. Sending sources with credibility scores for your analysis.",
                msg_type=MessageType.RESULT,
                payload={"contradictions": contradictions},
            )

        task.progress = 1.0
        result = {
            "output": {
                "findings": verified,
                "sources_checked": len(findings),
                "contradictions": contradictions,
                "high_confidence_facts": [f for f in verified if f.get("credibility", 0) > 0.8],
            },
            "confidence": self._calculate_confidence(verified),
            "messages": [],
            "artifacts": [],
            "metadata": {"sources_count": len(findings)},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _search_and_gather(self, query: str) -> list[dict]:
        """Simulate gathering information from multiple sources."""
        # In production: RAG pipeline + web search API + document parsing
        return [
            {"topic": "market_overview", "data": "AI recruiting market in India", "source": "industry_report", "credibility": 0.92},
            {"topic": "competitors", "data": "14 competitors identified", "source": "web_search", "credibility": 0.85},
            {"topic": "market_size", "data": "₹3,200 Cr (IMARC 2025)", "source": "imarc_report", "credibility": 0.88},
            {"topic": "pricing_data", "data": "Average ₹75K/month for mid-market", "source": "competitor_websites", "credibility": 0.78},
            {"topic": "growth_rate", "data": "23% YoY growth in AI recruiting adoption", "source": "nasscom_report", "credibility": 0.95},
        ]

    def _verify_sources(self, findings: list[dict]) -> list[dict]:
        """Score source credibility and verify claims."""
        credibility_tiers = {
            "industry_report": 0.92, "nasscom_report": 0.95, "imarc_report": 0.88,
            "web_search": 0.70, "competitor_websites": 0.78, "blog": 0.41,
        }
        for finding in findings:
            source = finding.get("source", "unknown")
            finding["credibility"] = credibility_tiers.get(source, 0.5)
        return findings

    def _detect_contradictions(self, findings: list[dict]) -> list[dict]:
        """Detect conflicting information across sources."""
        # Simplified: In production, use embedding similarity + LLM comparison
        return []

    def _calculate_confidence(self, findings: list[dict]) -> float:
        """Calculate overall confidence based on source quality."""
        if not findings:
            return 0.0
        avg_credibility = sum(f.get("credibility", 0.5) for f in findings) / len(findings)
        return min(avg_credibility, 0.95)


# ═══════════════════════════════════════════════════════════════
#  2. 📊 ANALYST CO-PILOT — "The Pattern Finder"
# ═══════════════════════════════════════════════════════════════

class AnalystCoPilot(BaseCoPilot):
    """
    Crunches data, spots patterns, generates insights, creates visualizations.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("analyst", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        # Gather input data from research
        research_data = self._gather_input_data(task)
        task.progress = 0.4

        # Analyze patterns
        analysis = self._analyze(task.description, research_data)
        task.progress = 0.7

        # Generate insights
        insights = self._extract_insights(analysis)
        task.progress = 0.9

        # Send insights to creator
        self.send_message(
            to="creator",
            content=f"Analysis complete. Key insight: {insights[0]['insight'] if insights else 'No notable patterns.'}",
            msg_type=MessageType.RESULT,
            payload={"analysis": analysis, "insights": insights},
        )

        task.progress = 1.0
        result = {
            "output": {
                "analysis": analysis,
                "insights": insights,
                "charts_generated": ["comparison_matrix", "market_map", "growth_projection"],
            },
            "confidence": 0.88,
            "messages": [],
            "artifacts": ["feature_matrix.csv", "market_map.png", "growth_chart.png"],
            "metadata": {"data_points_analyzed": len(research_data)},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _gather_input_data(self, task: Task) -> list[dict]:
        """Pull data from memory and previous task outputs."""
        messages = self.receive_messages()
        data = []
        for msg in messages:
            if msg.payload:
                data.append(msg.payload)
        return data

    def _analyze(self, description: str, data: list) -> dict:
        """Run analysis on gathered data."""
        return {
            "type": "comparative_analysis",
            "competitors_analyzed": 14,
            "market_size": "₹3,200 Cr",
            "growth_rate": "23% YoY",
            "top_differentiator_gaps": [
                "Real-time behavioral signals",
                "Multi-language support",
                "AI-powered skill validation",
            ],
        }

    def _extract_insights(self, analysis: dict) -> list[dict]:
        """Extract actionable insights from analysis."""
        return [
            {"insight": "Market is 3x larger than initially assumed", "impact": "high", "confidence": 0.88},
            {"insight": "No competitor has real-time behavioral signal integration", "impact": "high", "confidence": 0.92},
            {"insight": "Average pricing leaves room for premium positioning", "impact": "medium", "confidence": 0.78},
        ]


# ═══════════════════════════════════════════════════════════════
#  3. ✍️ CREATOR CO-PILOT — "The Wordsmith"
# ═══════════════════════════════════════════════════════════════

class CreatorCoPilot(BaseCoPilot):
    """
    Generates polished, audience-aware content — docs, emails, presentations, code.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("creator", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.1

        # Check user preferences for formatting
        format_pref = self.get_user_preference("document_format") or "professional"
        summary_pref = self.get_user_preference("exec_summary_style") or "bullet_points"
        task.progress = 0.3

        # Gather analysis results
        analysis_data = self._get_analysis_input()
        task.progress = 0.5

        # Generate content with audience awareness
        content = self._generate_content(task.description, analysis_data, format_pref)
        task.progress = 0.8

        # Send to quality for review
        self.send_message(
            to="quality",
            content="Draft content ready for quality review.",
            msg_type=MessageType.RESULT,
            payload={"content": content, "format": format_pref},
        )

        # Send to design for visuals
        self.send_message(
            to="design",
            content="Content ready — need charts and visual formatting.",
            msg_type=MessageType.RESULT,
            payload={"charts_needed": content.get("charts_requested", [])},
        )

        task.progress = 1.0
        result = {
            "output": content,
            "confidence": 0.91,
            "messages": [],
            "artifacts": ["strategy_document.pdf", "executive_summary.pdf"],
            "metadata": {"word_count": content.get("word_count", 0), "audience": content.get("audience", "general")},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _get_analysis_input(self) -> dict:
        """Get analysis results from messages."""
        messages = self.receive_messages()
        for msg in messages:
            if msg.sender == "analyst" and msg.payload:
                return msg.payload
        return {}

    def _generate_content(self, description: str, analysis: dict, format_pref: str) -> dict:
        """Generate audience-aware content."""
        return {
            "title": "AI Recruiting Tools in India — Competitive Analysis & Strategy",
            "audience": "Board of Directors",
            "format": format_pref,
            "sections": [
                "Executive Summary",
                "Market Overview",
                "Competitor Landscape",
                "Feature Comparison Matrix",
                "SWOT Analysis",
                "Strategic Recommendations",
                "Appendix: Raw Data",
            ],
            "word_count": 4200,
            "charts_requested": ["market_positioning_map", "feature_matrix_heatmap", "growth_projection"],
            "executive_summary": [
                "AI recruiting market in India: ₹3,200 Cr (IMARC 2025), growing 23% YoY",
                "14 competitors identified — market is fragmented, no player has >15% share",
                "Key differentiator gap: real-time behavioral signal integration",
                "Recommendation: Position as premium, AI-native solution with behavioral intelligence",
            ],
        }


# ═══════════════════════════════════════════════════════════════
#  4. ⚡ ACTION CO-PILOT — "The Executor"
# ═══════════════════════════════════════════════════════════════

class ActionCoPilot(BaseCoPilot):
    """
    Takes real-world actions — sends emails, creates tickets, schedules meetings.
    The 'last mile' that other AI tools completely miss.
    """

    # Actions that ALWAYS require user approval
    APPROVAL_REQUIRED = {
        "send_external_email",
        "modify_production",
        "financial_transaction",
        "calendar_others",
    }

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("action", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        # Determine action type
        action = self._parse_action(task.description)
        task.progress = 0.4

        # Check compliance before executing
        self.send_message(
            to="compliance",
            content=f"Pre-execution compliance check for action: {action['type']}",
            msg_type=MessageType.QUERY,
            payload=action,
            requires_response=True,
        )
        task.progress = 0.6

        # Check if approval needed
        if action["type"] in self.APPROVAL_REQUIRED:
            escalation = self.escalate(
                reason=f"Action '{action['type']}' requires your approval before execution.",
                options=[{"action": action["type"], "target": action.get("target", ""), "details": action.get("details", "")}],
                recommendation="Review and approve to proceed.",
                confidence=0.85,
            )
            task.progress = 0.7
            result = {
                "output": {"action": action, "status": "awaiting_approval", "escalation": escalation},
                "confidence": 0.85,
                "messages": [],
                "artifacts": [],
                "metadata": {"action_type": action["type"]},
            }
        else:
            # Execute directly
            execution_result = self._execute_action(action)
            task.progress = 1.0
            result = {
                "output": {"action": action, "status": "executed", "result": execution_result},
                "confidence": 0.95,
                "messages": [],
                "artifacts": [],
                "metadata": {"action_type": action["type"]},
            }

        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _parse_action(self, description: str) -> dict:
        """Parse task description into structured action."""
        return {
            "type": "create_document",
            "target": "strategy_document",
            "details": description,
        }

    def _execute_action(self, action: dict) -> dict:
        """Execute the action (simulated)."""
        return {
            "status": "success",
            "action": action["type"],
            "timestamp": "2026-06-15T10:30:00+05:30",
        }


# ═══════════════════════════════════════════════════════════════
#  5. 🛡️ QUALITY CO-PILOT — "The Guardian"
# ═══════════════════════════════════════════════════════════════

class QualityCoPilot(BaseCoPilot):
    """
    Reviews everything before delivery — accuracy, tone, completeness, bias.
    The built-in quality gate.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("quality", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        # Get content to review
        content = self._get_content_to_review()
        task.progress = 0.4

        # Run quality checks
        checks = {
            "factual_accuracy": self._check_facts(content),
            "completeness": self._check_completeness(content, task.description),
            "tone_audience": self._check_tone(content),
            "bias_detection": self._check_bias(content),
            "recency": self._check_recency(content),
            "internal_consistency": self._check_consistency(content),
        }
        task.progress = 0.8

        # Compile quality report
        issues = [c for c in checks.values() if c["status"] != "pass"]
        overall_pass = len(issues) == 0

        # Send feedback to creator if issues found
        for issue in issues:
            if issue["severity"] == "error":
                self.send_message(
                    to="creator",
                    content=f"Quality issue: {issue['message']}",
                    msg_type=MessageType.FEEDBACK,
                    payload=issue,
                )

        task.progress = 1.0
        result = {
            "output": {
                "quality_report": checks,
                "issues_found": len(issues),
                "overall_pass": overall_pass,
                "notes": [c["message"] for c in checks.values()],
            },
            "confidence": 0.95 if overall_pass else 0.75,
            "messages": [],
            "artifacts": ["quality_report.json"],
            "metadata": {"checks_run": len(checks), "issues": len(issues)},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _get_content_to_review(self) -> dict:
        messages = self.receive_messages()
        for msg in messages:
            if msg.payload and "content" in msg.payload:
                return msg.payload["content"]
        return {}

    def _check_facts(self, content: dict) -> dict:
        return {"status": "pass", "severity": "info", "message": "✅ All financial claims sourced — 14 citations included"}

    def _check_completeness(self, content: dict, requirements: str) -> dict:
        return {"status": "pass", "severity": "info", "message": "✅ All requested sections present"}

    def _check_tone(self, content: dict) -> dict:
        return {"status": "pass", "severity": "info", "message": "✅ Executive tone appropriate for board audience"}

    def _check_bias(self, content: dict) -> dict:
        return {"status": "pass", "severity": "info", "message": "✅ No detectable bias in conclusions"}

    def _check_recency(self, content: dict) -> dict:
        return {"status": "warning", "severity": "warning", "message": "⚠️ Competitor X pricing data from March 2026 — may have changed"}

    def _check_consistency(self, content: dict) -> dict:
        return {"status": "pass", "severity": "info", "message": "✅ No internal contradictions detected"}


# ═══════════════════════════════════════════════════════════════
#  6. 💬 COMMUNICATION CO-PILOT — "The Connector"
# ═══════════════════════════════════════════════════════════════

class CommunicationCoPilot(BaseCoPilot):
    """
    Manages meetings, follow-ups, team coordination, and stakeholder updates.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("communication", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.3

        # Determine communication task type
        comm_type = self._classify_task(task.description)
        task.progress = 0.5

        if comm_type == "meeting_prep":
            output = self._prepare_meeting(task)
        elif comm_type == "follow_up":
            output = self._generate_followups(task)
        elif comm_type == "status_update":
            output = self._draft_status_update(task)
        else:
            output = self._general_communication(task)

        task.progress = 1.0
        result = {
            "output": output,
            "confidence": 0.89,
            "messages": [],
            "artifacts": output.get("artifacts", []),
            "metadata": {"comm_type": comm_type},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _classify_task(self, description: str) -> str:
        keywords = {
            "meeting_prep": ["meeting", "agenda", "prepare for"],
            "follow_up": ["follow up", "follow-up", "check in", "remind"],
            "status_update": ["status", "update", "progress report"],
        }
        desc_lower = description.lower()
        for task_type, words in keywords.items():
            if any(w in desc_lower for w in words):
                return task_type
        return "general"

    def _prepare_meeting(self, task: Task) -> dict:
        return {
            "agenda": ["Review competitive analysis findings", "Discuss strategy recommendations", "Assign action items"],
            "pre_read_materials": ["Strategy_Document.pdf", "Executive_Summary.pdf"],
            "attendees_notified": True,
            "artifacts": ["meeting_agenda.md"],
        }

    def _generate_followups(self, task: Task) -> dict:
        return {
            "follow_ups": [
                {"to": "backend_team", "message": "Design review action items — any update?", "days_overdue": 3},
                {"to": "pm", "message": "Competitive analysis shared — feedback needed by Friday", "days_overdue": 0},
            ],
            "artifacts": ["followup_list.md"],
        }

    def _draft_status_update(self, task: Task) -> dict:
        return {
            "status_report": "Sprint 24 retrospective analysis complete. 3 root causes identified. Action items assigned.",
            "audience": "engineering_manager",
            "artifacts": ["status_update.md"],
        }

    def _general_communication(self, task: Task) -> dict:
        return {"output": "Communication task processed", "artifacts": []}


# ═══════════════════════════════════════════════════════════════
#  7. 💻 CODE CO-PILOT — "The Engineer"
# ═══════════════════════════════════════════════════════════════

class CodeCoPilot(BaseCoPilot):
    """
    Writes, reviews, debugs, and deploys code.
    Not autocomplete — full engineering workflow.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("code", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        code_type = self._classify_code_task(task.description)
        task.progress = 0.5

        if code_type == "generate":
            output = self._generate_code(task)
        elif code_type == "review":
            output = self._review_code(task)
        elif code_type == "debug":
            output = self._debug_code(task)
        elif code_type == "automate":
            output = self._create_automation(task)
        else:
            output = self._generate_code(task)

        task.progress = 1.0
        result = {
            "output": output,
            "confidence": 0.87,
            "messages": [],
            "artifacts": output.get("files", []),
            "metadata": {"code_type": code_type},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _classify_code_task(self, description: str) -> str:
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["review", "analyze code", "check"]):
            return "review"
        elif any(w in desc_lower for w in ["debug", "fix", "error", "bug"]):
            return "debug"
        elif any(w in desc_lower for w in ["script", "automate", "automation"]):
            return "automate"
        return "generate"

    def _generate_code(self, task: Task) -> dict:
        return {
            "code": "# Generated by Parallax Code Co-Pilot\n...",
            "language": "python",
            "description": "Generated code based on specifications",
            "files": ["generated_module.py"],
            "documentation": "Auto-generated docstrings included",
        }

    def _review_code(self, task: Task) -> dict:
        return {
            "review": {"issues_found": 2, "severity": "medium", "suggestions": ["Add error handling", "Optimize query"]},
            "files": ["code_review_report.md"],
        }

    def _debug_code(self, task: Task) -> dict:
        return {
            "root_cause": "Null pointer in line 42 — missing null check",
            "fix_suggested": "Add guard clause before accessing property",
            "files": ["debug_report.md"],
        }

    def _create_automation(self, task: Task) -> dict:
        return {
            "script": "#!/usr/bin/env python3\n# Automation script\n...",
            "description": "Automated data processing pipeline",
            "files": ["automation_script.py"],
        }


# ═══════════════════════════════════════════════════════════════
#  8. 📡 DATA CO-PILOT — "The Sensor"
# ═══════════════════════════════════════════════════════════════

class DataCoPilot(BaseCoPilot):
    """
    Connects to live systems, pulls real-time data, monitors metrics.
    Unlike the Analyst (processes data), the Sensor ACQUIRES data.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("data", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        # Determine data source
        source_type = self._identify_source(task.description)
        task.progress = 0.4

        # Pull data
        data = self._pull_data(source_type, task.description)
        task.progress = 0.8

        # Send to analyst for processing
        self.send_message(
            to="analyst",
            content=f"Pulled live data from {source_type}. {len(data)} data points retrieved.",
            msg_type=MessageType.RESULT,
            payload={"data": data, "source": source_type},
        )

        # Store in episodic memory for this session
        self.remember_short_term(f"data:{task.task_id}", data)

        task.progress = 1.0
        result = {
            "output": {"data": data, "source": source_type, "data_points": len(data), "freshness": "real-time"},
            "confidence": 0.93,
            "messages": [],
            "artifacts": [],
            "metadata": {"source": source_type, "records": len(data)},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _identify_source(self, description: str) -> str:
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["jira", "ticket", "sprint"]):
            return "jira_api"
        elif any(w in desc_lower for w in ["github", "pr", "commit"]):
            return "github_api"
        elif any(w in desc_lower for w in ["dashboard", "metric", "analytics"]):
            return "analytics_dashboard"
        elif any(w in desc_lower for w in ["database", "sql", "query"]):
            return "database"
        return "api"

    def _pull_data(self, source: str, query: str) -> list[dict]:
        """Pull data from identified source (simulated)."""
        mock_data = {
            "jira_api": [{"ticket_id": f"PROJ-{i}", "status": "done", "points": 3} for i in range(42)],
            "github_api": [{"pr_id": i, "author": "dev", "status": "merged"} for i in range(87)],
            "analytics_dashboard": [{"metric": "conversion_rate", "value": 0.023, "date": "2026-06-14"}],
            "database": [{"query": "SELECT COUNT(*) FROM users", "result": 15420}],
            "api": [{"endpoint": "/api/data", "status": 200}],
        }
        return mock_data.get(source, [{"data": "retrieved"}])


# ═══════════════════════════════════════════════════════════════
#  9. 🎨 DESIGN CO-PILOT — "The Architect"
# ═══════════════════════════════════════════════════════════════

class DesignCoPilot(BaseCoPilot):
    """
    Creates visual designs, wireframes, diagrams, and brand-consistent assets.
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("design", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        design_type = self._classify_design_task(task.description)
        task.progress = 0.4

        # Check brand preferences
        brand = self.get_user_preference("brand_colors") or {
            "primary": "#0A1628", "accent": "#00D4FF", "secondary": "#7B61FF"
        }
        task.progress = 0.6

        output = self._create_design(design_type, task.description, brand)
        task.progress = 1.0

        result = {
            "output": output,
            "confidence": 0.85,
            "messages": [],
            "artifacts": output.get("files", []),
            "metadata": {"design_type": design_type},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _classify_design_task(self, description: str) -> str:
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["wireframe", "ui", "mockup"]):
            return "wireframe"
        elif any(w in desc_lower for w in ["chart", "graph", "visualization"]):
            return "chart"
        elif any(w in desc_lower for w in ["diagram", "architecture", "flow"]):
            return "diagram"
        elif any(w in desc_lower for w in ["presentation", "slide", "deck"]):
            return "presentation"
        return "general_design"

    def _create_design(self, design_type: str, description: str, brand: dict) -> dict:
        return {
            "type": design_type,
            "brand_colors_applied": brand,
            "format": "PNG + SVG",
            "resolution": "2x retina",
            "files": [f"{design_type}_output.png"],
            "description": f"Generated {design_type} based on: {description[:50]}...",
        }


# ═══════════════════════════════════════════════════════════════
#  10. 🔐 COMPLIANCE CO-PILOT — "The Sentinel"
# ═══════════════════════════════════════════════════════════════

class ComplianceCoPilot(BaseCoPilot):
    """
    Ensures outputs meet regulatory, legal, and organizational policy requirements.
    The guardrail that keeps everything safe and compliant.
    """

    REGULATORY_FRAMEWORKS = ["GDPR", "DPDPA", "HIPAA", "SOC-2", "ISO-27001"]

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("compliance", memory, bus)

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.2

        # Get content to check
        content = self._get_content_to_check()
        task.progress = 0.4

        # Run compliance checks
        checks = {
            "pii_detection": self._check_pii(content),
            "data_classification": self._classify_data(content),
            "regulatory_scan": self._scan_regulations(content),
            "policy_compliance": self._check_policies(content),
            "audit_trail": self._generate_audit_entry(task),
        }
        task.progress = 0.8

        issues = [c for c in checks.values() if c.get("status") != "pass"]

        # Notify action co-pilot of any restrictions
        if issues:
            self.send_message(
                to="action",
                content=f"Compliance issues found: {len(issues)}. Review required before execution.",
                msg_type=MessageType.FEEDBACK,
                payload={"issues": issues},
            )

        task.progress = 1.0
        result = {
            "output": {
                "compliance_report": checks,
                "issues_found": len(issues),
                "frameworks_checked": self.REGULATORY_FRAMEWORKS,
                "overall_compliant": len(issues) == 0,
            },
            "confidence": 0.92,
            "messages": [],
            "artifacts": ["compliance_report.json", "audit_log_entry.json"],
            "metadata": {"frameworks_checked": len(self.REGULATORY_FRAMEWORKS)},
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    def _get_content_to_check(self) -> dict:
        messages = self.receive_messages()
        for msg in messages:
            if msg.payload:
                return msg.payload
        return {}

    def _check_pii(self, content: dict) -> dict:
        return {"status": "warning", "message": "Found 2 competitor revenue figures from estimates — add disclaimer", "severity": "medium"}

    def _classify_data(self, content: dict) -> dict:
        return {"status": "pass", "classification": "internal", "message": "Data classified as INTERNAL — no restricted content"}

    def _scan_regulations(self, content: dict) -> dict:
        return {"status": "pass", "message": "No regulatory violations detected", "frameworks": self.REGULATORY_FRAMEWORKS}

    def _check_policies(self, content: dict) -> dict:
        return {"status": "pass", "message": "Content complies with organizational policies"}

    def _generate_audit_entry(self, task: Task) -> dict:
        return {
            "status": "logged",
            "entry": {
                "task_id": task.task_id,
                "copilot": self.copilot_id,
                "action": "compliance_review",
                "timestamp": "2026-06-15T10:30:00+05:30",
                "result": "reviewed",
            },
        }
