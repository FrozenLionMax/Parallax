"""
Parallax — Core Data Models
Task DAG, Messages, and Memory structures.
"""

from __future__ import annotations
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Optional
from src.config import TaskState, MessageType


# ═══════════════════════════════════════════════════════════════
#  MESSAGES — Inter-Co-Pilot Communication
# ═══════════════════════════════════════════════════════════════

@dataclass
class Message:
    """A message between co-pilots or between co-pilot and orchestrator."""

    sender: str
    recipient: str
    msg_type: str
    content: str
    payload: dict = field(default_factory=dict)
    confidence: float = 1.0
    requires_response: bool = False
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"[{self.sender} → {self.recipient}] {self.content}"


# ═══════════════════════════════════════════════════════════════
#  TASKS — Units of Work in the DAG
# ═══════════════════════════════════════════════════════════════

@dataclass
class Task:
    """A single unit of work assigned to a co-pilot."""

    task_id: str
    name: str
    description: str
    assigned_copilot: str          # Key from COPILOT_REGISTRY
    dependencies: list[str] = field(default_factory=list)  # Task IDs
    state: str = TaskState.PENDING
    result: Any = None
    confidence: float = 0.0
    progress: float = 0.0          # 0.0 to 1.0
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    @property
    def is_ready(self) -> bool:
        """Task is ready when all dependencies are completed."""
        return self.state == TaskState.PENDING

    def complete(self, result: Any, confidence: float = 0.95):
        """Mark task as completed with result."""
        self.state = TaskState.COMPLETED
        self.result = result
        self.confidence = confidence
        self.progress = 1.0
        self.completed_at = datetime.now()

    def fail(self, error: str):
        """Mark task as failed."""
        self.state = TaskState.FAILED
        self.result = {"error": error}

    def block(self, reason: str):
        """Block task pending user decision."""
        self.state = TaskState.BLOCKED
        self.result = {"blocked_reason": reason}


# ═══════════════════════════════════════════════════════════════
#  TASK GRAPH — Directed Acyclic Graph of Tasks
# ═══════════════════════════════════════════════════════════════

@dataclass
class TaskGraph:
    """A DAG of tasks representing a decomposed workflow."""

    graph_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    tasks: list[Task] = field(default_factory=list)
    user_input: str = ""
    intent: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def add_task(self, task: Task) -> None:
        """Add a task to the graph."""
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_ready_tasks(self) -> list[Task]:
        """Get tasks whose dependencies are all completed."""
        completed_ids = {t.task_id for t in self.tasks if t.state == TaskState.COMPLETED}
        ready = []
        for task in self.tasks:
            if task.state == TaskState.PENDING:
                if all(dep in completed_ids for dep in task.dependencies):
                    ready.append(task)
        return ready

    def is_complete(self) -> bool:
        """Check if all tasks are completed."""
        return all(t.state == TaskState.COMPLETED for t in self.tasks)

    @property
    def progress(self) -> float:
        """Overall progress (0.0 to 1.0)."""
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.state == TaskState.COMPLETED)
        return completed / len(self.tasks)

    @property
    def active_copilots(self) -> set[str]:
        """Set of co-pilot keys used in this graph."""
        return {t.assigned_copilot for t in self.tasks}

    def summary(self) -> dict:
        """Get a summary of the task graph state."""
        return {
            "total_tasks": len(self.tasks),
            "completed": sum(1 for t in self.tasks if t.state == TaskState.COMPLETED),
            "running": sum(1 for t in self.tasks if t.state == TaskState.RUNNING),
            "blocked": sum(1 for t in self.tasks if t.state == TaskState.BLOCKED),
            "pending": sum(1 for t in self.tasks if t.state == TaskState.PENDING),
            "failed": sum(1 for t in self.tasks if t.state == TaskState.FAILED),
            "progress": f"{self.progress:.0%}",
            "copilots_active": len(self.active_copilots),
        }


# ═══════════════════════════════════════════════════════════════
#  INTENT — Parsed User Request
# ═══════════════════════════════════════════════════════════════

@dataclass
class Intent:
    """Structured representation of what the user wants."""

    goal: str
    domain: str = ""
    audience: str = ""
    deadline: str = ""
    tone: str = ""
    focus_areas: list[str] = field(default_factory=list)
    implicit_needs: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "Goal": self.goal,
            "Domain": self.domain,
            "Audience": self.audience,
            "Deadline": self.deadline,
            "Tone": self.tone,
            "Focus Areas": ", ".join(self.focus_areas),
            "Implicit Needs": ", ".join(self.implicit_needs),
        }


# ═══════════════════════════════════════════════════════════════
#  MEMORY ENTRIES
# ═══════════════════════════════════════════════════════════════

@dataclass
class MemoryEntry:
    """A single entry in any memory layer."""

    key: str
    value: Any
    source: str = ""                # Which co-pilot created this
    entry_type: str = "fact"        # fact, preference, pattern, entity
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
