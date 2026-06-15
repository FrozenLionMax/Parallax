"""
Parallax — The Orchestrator
The brain that understands intent, decomposes tasks, and coordinates 10 co-pilots.
"""

from __future__ import annotations
from typing import Optional
from src.config import COPILOT_REGISTRY, TaskState
from src.models import Task, TaskGraph, Intent, Message
from src.memory import MemorySystem
from src.message_bus import MessageBus
from src.copilots.base import BaseCoPilot
from src.copilots.agents import (
    ResearchCoPilot, AnalystCoPilot, CreatorCoPilot, ActionCoPilot,
    QualityCoPilot, CommunicationCoPilot, CodeCoPilot,
    DataCoPilot, DesignCoPilot, ComplianceCoPilot,
)
from src.copilots.catalyst import CatalystCoPilot


class Orchestrator:
    """
    🧠 The Orchestrator — Parallax's Central Brain

    Responsibilities:
    1. UNDERSTAND — Parse user intent from natural language
    2. DECOMPOSE — Break complex tasks into a DAG of sub-tasks
    3. ROUTE — Assign each sub-task to the best co-pilot
    4. COORDINATE — Manage execution, dependencies, and inter-agent comms
    5. ESCALATE — Surface decisions to the user when confidence is low
    6. DELIVER — Compile final output from all co-pilots
    7. LEARN — Store feedback and improve for next time
    """

    def __init__(self):
        # Initialize shared systems
        self.memory = MemorySystem()
        self.bus = MessageBus()

        # Initialize all 10 co-pilots
        self.copilots: dict[str, BaseCoPilot] = {
            "research": ResearchCoPilot(self.memory, self.bus),
            "analyst": AnalystCoPilot(self.memory, self.bus),
            "creator": CreatorCoPilot(self.memory, self.bus),
            "action": ActionCoPilot(self.memory, self.bus),
            "quality": QualityCoPilot(self.memory, self.bus),
            "communication": CommunicationCoPilot(self.memory, self.bus),
            "code": CodeCoPilot(self.memory, self.bus),
            "data": DataCoPilot(self.memory, self.bus),
            "design": DesignCoPilot(self.memory, self.bus),
            "compliance": ComplianceCoPilot(self.memory, self.bus),
            "catalyst": CatalystCoPilot(self.memory, self.bus),
        }

        # Cost tracking
        self._cost_log: list[dict] = []

        # Execution state
        self._active_graph: Optional[TaskGraph] = None
        self._results: dict[str, dict] = {}
        self._escalations: list[dict] = []

    # ─────────────────────── STEP 1: UNDERSTAND ───────────────────────

    def parse_intent(self, user_input: str) -> Intent:
        """
        Parse natural language input into structured intent.

        In production: LLM with structured output (function calling / JSON mode).
        Enhanced by Semantic Memory for user-specific context.
        """
        # Check procedural memory for user preferences
        format_pref = self.memory.procedural.get_preference("preferred_format")
        audience_pref = self.memory.procedural.get_preference("default_audience")

        intent = Intent(
            goal=self._extract_goal(user_input),
            domain=self._extract_domain(user_input),
            audience=audience_pref or self._extract_audience(user_input),
            deadline=self._extract_deadline(user_input),
            tone=self._determine_tone(user_input),
            focus_areas=self._extract_focus(user_input),
            implicit_needs=self._infer_implicit_needs(user_input),
            confidence=0.92,
        )

        # Store in episodic memory
        self.memory.episodic.store("current_intent", intent.to_dict(), source="orchestrator")

        return intent

    # ─────────────────────── STEP 2: DECOMPOSE ───────────────────────

    def decompose(self, intent: Intent) -> TaskGraph:
        """
        Break the intent into a DAG of tasks with dependencies.

        The decomposer reasons about:
        - Which co-pilots are needed
        - Task ordering and dependencies
        - Parallelizable vs sequential work
        - Estimated time per task
        """
        graph = TaskGraph(user_input=intent.goal, intent=intent.to_dict())

        # Check if we have a template for this type of task
        template = self.memory.procedural.find_similar_template(intent.goal)

        if template:
            # Use existing template (learned from past success)
            graph = self._apply_template(template, intent)
        else:
            # Build new task graph based on intent analysis
            graph = self._build_task_graph(intent)

        self._active_graph = graph
        return graph

    def _build_task_graph(self, intent: Intent) -> TaskGraph:
        """Build a task graph from intent analysis."""
        graph = TaskGraph(user_input=intent.goal, intent=intent.to_dict())

        # Phase 1: Research & Data Collection (parallel)
        t1 = Task("T1", "Research & gather information", intent.goal, "research")
        t2 = Task("T2", "Pull live data & metrics", f"Get real-time data for {intent.domain}", "data")
        graph.add_task(t1)
        graph.add_task(t2)

        # Phase 2: Analysis (depends on research + data)
        t3 = Task("T3", "Analyze findings & identify patterns",
                   f"Analyze data for {intent.goal}", "analyst", dependencies=["T1", "T2"])
        graph.add_task(t3)

        # Phase 3: Creation (depends on analysis)
        t4 = Task("T4", "Generate content & documents",
                   f"Create deliverables for {intent.audience}", "creator", dependencies=["T3"])
        t5 = Task("T5", "Create visuals & charts",
                   f"Design visualizations for {intent.goal}", "design", dependencies=["T3"])
        graph.add_task(t4)
        graph.add_task(t5)

        # Phase 4: Review (depends on creation)
        t6 = Task("T6", "Compliance check",
                   "Verify regulatory and policy compliance", "compliance", dependencies=["T4"])
        t7 = Task("T7", "Quality review & fact-check",
                   "Final quality assurance pass", "quality", dependencies=["T4", "T5", "T6"])
        graph.add_task(t6)
        graph.add_task(t7)

        return graph

    # ─────────────────────── STEP 3: EXECUTE ───────────────────────

    def execute(self, graph: Optional[TaskGraph] = None) -> dict:
        """
        Execute the task graph — coordinate co-pilots, handle dependencies.

        Returns execution summary with all results.
        """
        if graph is None:
            graph = self._active_graph
        if graph is None:
            raise ValueError("No task graph to execute. Call decompose() first.")

        results = {}
        escalations = []

        # Execute tasks in dependency order
        while not graph.is_complete():
            ready_tasks = graph.get_ready_tasks()

            if not ready_tasks:
                # Check for blocked or failed tasks
                blocked = [t for t in graph.tasks if t.state == TaskState.BLOCKED]
                failed = [t for t in graph.tasks if t.state == TaskState.FAILED]
                if blocked or failed:
                    break
                break

            # Execute ready tasks (in production: parallel execution)
            for task in ready_tasks:
                copilot = self.copilots.get(task.assigned_copilot)
                if copilot is None:
                    task.fail(f"No co-pilot found for: {task.assigned_copilot}")
                    continue

                task.state = TaskState.RUNNING
                result = copilot.process(task)
                results[task.task_id] = result

                # Check for escalations
                if result.get("output", {}).get("escalation"):
                    escalations.append(result["output"]["escalation"])

        self._results = results
        self._escalations = escalations

        return {
            "graph_summary": graph.summary(),
            "results": {tid: r.get("output", {}) for tid, r in results.items()},
            "escalations": escalations,
            "messages": self.bus.get_history(),
            "memory_stats": self.memory.full_stats(),
        }

    # ─────────────────────── STEP 4: LEARN ───────────────────────

    def learn_from_feedback(self, feedback: str, rating: float = 1.0):
        """
        Store user feedback for continuous improvement.

        Feedback flows into:
        1. Procedural Memory — preferences for future tasks
        2. Confidence calibration — adjust trust thresholds
        3. Template storage — save successful workflows for reuse
        """
        graph_id = self._active_graph.graph_id if self._active_graph else "unknown"

        # Store feedback
        self.memory.procedural.record_feedback(graph_id, feedback, rating)

        # Extract preferences from feedback
        preferences = self._extract_preferences(feedback)
        for key, value in preferences.items():
            self.memory.procedural.store_preference(key, value, source="user_feedback")

        # If task was successful, save as template
        if rating >= 0.8 and self._active_graph:
            self.memory.procedural.store_template(
                name=self._active_graph.intent.get("Goal", "unknown"),
                template={"tasks": [t.name for t in self._active_graph.tasks]},
                success_score=rating,
            )

        # Consolidate session memories
        self.memory.consolidate_session()

        return {
            "feedback_stored": True,
            "preferences_extracted": preferences,
            "template_saved": rating >= 0.8,
            "memory_stats": self.memory.full_stats(),
        }

    # ─────────────────────── HELPERS ───────────────────────

    def _extract_goal(self, text: str) -> str:
        return text.strip()

    def _extract_domain(self, text: str) -> str:
        domains = ["AI", "recruiting", "software", "finance", "healthcare", "education"]
        text_lower = text.lower()
        found = [d for d in domains if d.lower() in text_lower]
        return ", ".join(found) if found else "general"

    def _extract_audience(self, text: str) -> str:
        audiences = {
            "board": "Board of Directors", "team": "Team Members",
            "investor": "Investors", "client": "Clients", "manager": "Management",
        }
        text_lower = text.lower()
        for key, value in audiences.items():
            if key in text_lower:
                return value
        return "General"

    def _extract_deadline(self, text: str) -> str:
        time_words = ["today", "tomorrow", "tuesday", "wednesday", "thursday", "friday", "monday",
                       "next week", "this week", "eod", "end of day", "asap"]
        text_lower = text.lower()
        for word in time_words:
            if word in text_lower:
                return word.title()
        return "No specific deadline"

    def _determine_tone(self, text: str) -> str:
        if any(w in text.lower() for w in ["board", "executive", "investor"]):
            return "executive"
        elif any(w in text.lower() for w in ["team", "sprint", "engineering"]):
            return "technical"
        return "professional"

    def _extract_focus(self, text: str) -> list[str]:
        focus_keywords = ["pricing", "features", "market", "competitors", "strategy",
                          "blockers", "performance", "growth", "risks"]
        return [k for k in focus_keywords if k in text.lower()]

    def _infer_implicit_needs(self, text: str) -> list[str]:
        needs = []
        if any(w in text.lower() for w in ["board", "executive", "presentation"]):
            needs.extend(["executive summary", "data visualizations", "professional formatting"])
        if any(w in text.lower() for w in ["analysis", "compare", "competitive"]):
            needs.extend(["comparison matrix", "market positioning"])
        if any(w in text.lower() for w in ["email", "outreach", "send"]):
            needs.extend(["personalization", "tone calibration"])
        return needs

    def _extract_preferences(self, feedback: str) -> dict:
        """Extract actionable preferences from natural language feedback."""
        prefs = {}
        feedback_lower = feedback.lower()

        if "shorter" in feedback_lower or "concise" in feedback_lower:
            prefs["exec_summary_style"] = "concise_bullet_points"
        if "bullet" in feedback_lower:
            prefs["preferred_format"] = "bullet_points"
        if "institutional" in feedback_lower or "credible" in feedback_lower:
            prefs["source_preference"] = "institutional_sources_first"
        if "no paragraph" in feedback_lower:
            prefs["writing_style"] = "no_paragraphs"

        return prefs

    def _apply_template(self, template: dict, intent: Intent) -> TaskGraph:
        """Apply a saved template to create a task graph."""
        return self._build_task_graph(intent)

    # ─────────────────────── STATUS ───────────────────────

    def fleet_status(self) -> dict:
        """Get status of all 10 co-pilots."""
        return {cid: cp.status() for cid, cp in self.copilots.items()}

    def get_copilot(self, copilot_id: str) -> Optional[BaseCoPilot]:
        """Get a specific co-pilot by ID."""
        return self.copilots.get(copilot_id)

    def list_copilots(self) -> list[str]:
        """List all available co-pilot IDs."""
        return list(self.copilots.keys())
