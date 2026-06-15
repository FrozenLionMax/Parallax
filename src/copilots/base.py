"""
Parallax — Base Co-Pilot
Abstract base class that all 10 co-pilots inherit from.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
from src.models import Task, Message
from src.config import COPILOT_REGISTRY, MessageType, CONFIDENCE_AUTO_EXECUTE, CONFIDENCE_HOLD_APPROVAL
from src.memory import MemorySystem
from src.message_bus import MessageBus


class BaseCoPilot(ABC):
    """
    Base class for all Parallax co-pilots.

    Every co-pilot has:
    - A unique identity (name, codename, icon, color)
    - Access to the shared memory system
    - Access to the message bus for inter-co-pilot communication
    - A process() method that handles assigned tasks
    - A confidence scoring mechanism
    - Escalation logic for human-in-the-loop decisions
    """

    def __init__(self, copilot_id: str, memory: MemorySystem, message_bus: MessageBus):
        if copilot_id not in COPILOT_REGISTRY:
            raise ValueError(f"Unknown co-pilot: {copilot_id}")

        self.copilot_id = copilot_id
        self.memory = memory
        self.bus = message_bus

        # Load identity from registry
        registry = COPILOT_REGISTRY[copilot_id]
        self.name = registry["name"]
        self.codename = registry["codename"]
        self.icon = registry["icon"]
        self.color = registry["color"]
        self.description = registry["description"]
        self.capabilities = registry["capabilities"]

        # State
        self._active_tasks: list[Task] = []
        self._completed_count: int = 0
        self._escalation_count: int = 0

    # ─────────────────────── CORE INTERFACE ───────────────────────

    @abstractmethod
    def process(self, task: Task) -> dict:
        """
        Process an assigned task and return results.

        Returns:
            dict with keys:
                - "output": The task result
                - "confidence": Float 0.0-1.0
                - "messages": List of Message objects sent during processing
                - "artifacts": List of generated artifacts (files, charts, etc.)
                - "metadata": Any additional metadata
        """
        pass

    # ─────────────────────── MESSAGING ───────────────────────

    def send_message(self, to: str, content: str, msg_type: str = MessageType.RESULT, **kwargs) -> Message:
        """Send a message to another co-pilot."""
        msg = Message(
            sender=self.copilot_id,
            recipient=to,
            msg_type=msg_type,
            content=content,
            payload=kwargs.get("payload", {}),
            confidence=kwargs.get("confidence", 1.0),
            requires_response=kwargs.get("requires_response", False),
        )
        self.bus.send(msg)
        return msg

    def receive_messages(self) -> list[Message]:
        """Check for incoming messages."""
        return self.bus.receive(self.copilot_id)

    def query_copilot(self, to: str, question: str) -> Message:
        """Ask another co-pilot a question."""
        return self.send_message(
            to=to,
            content=question,
            msg_type=MessageType.QUERY,
            requires_response=True,
        )

    def escalate(self, reason: str, options: list[dict], recommendation: str, confidence: float = 0.5) -> dict:
        """
        Escalate a decision to the user (via orchestrator).

        Returns an escalation dict that the orchestrator will present to the user.
        """
        self._escalation_count += 1
        return {
            "type": "escalation",
            "copilot": f"{self.icon} {self.name}",
            "confidence": confidence,
            "reason": reason,
            "options": options,
            "recommendation": recommendation,
        }

    # ─────────────────────── MEMORY ACCESS ───────────────────────

    def remember_short_term(self, key: str, value: Any):
        """Store something in episodic memory (this session only)."""
        self.memory.episodic.store(key, value, source=self.copilot_id)

    def recall_short_term(self, key: str) -> Optional[Any]:
        """Recall from episodic memory."""
        return self.memory.episodic.recall(key)

    def learn_fact(self, key: str, value: Any, confidence: float = 0.9):
        """Store a fact in semantic memory (permanent)."""
        self.memory.semantic.store_fact(key, value, source=self.copilot_id, confidence=confidence)

    def recall_fact(self, key: str) -> Optional[Any]:
        """Recall from semantic memory."""
        return self.memory.semantic.recall_fact(key)

    def get_user_preference(self, key: str) -> Optional[Any]:
        """Check if the user has a preference for something."""
        return self.memory.procedural.get_preference(key)

    # ─────────────────────── CONFIDENCE ───────────────────────

    def determine_action(self, confidence: float) -> str:
        """
        Determine what to do based on confidence score.

        Returns: "auto_execute" | "hold_approval" | "escalate"
        """
        if confidence >= CONFIDENCE_AUTO_EXECUTE:
            return "auto_execute"
        elif confidence >= CONFIDENCE_HOLD_APPROVAL:
            return "hold_approval"
        else:
            return "escalate"

    # ─────────────────────── STATUS ───────────────────────

    def status(self) -> dict:
        """Get co-pilot status."""
        return {
            "copilot_id": self.copilot_id,
            "name": self.name,
            "codename": self.codename,
            "icon": self.icon,
            "active_tasks": len(self._active_tasks),
            "completed_total": self._completed_count,
            "escalations": self._escalation_count,
        }

    def __repr__(self):
        return f"{self.icon} {self.name} ({self.codename})"
