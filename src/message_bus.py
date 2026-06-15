"""
Parallax — Message Bus
Inter-co-pilot communication system.
"""

from __future__ import annotations
from collections import defaultdict
from datetime import datetime
from typing import Callable, Optional
from src.models import Message
from src.config import MessageType


class MessageBus:
    """
    Central message bus for inter-co-pilot communication.

    Co-pilots don't talk directly — they publish messages to the bus,
    and the bus routes them to the right recipient. This enables:
    - Decoupled communication
    - Message logging for audit trails
    - Broadcast messages to all co-pilots
    - Priority-based message routing
    """

    def __init__(self):
        self._messages: list[Message] = []
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._pending: dict[str, list[Message]] = defaultdict(list)

    def send(self, message: Message) -> None:
        """Send a message from one co-pilot to another."""
        self._messages.append(message)
        self._pending[message.recipient].append(message)

        # Notify subscribers
        for callback in self._subscribers.get(message.recipient, []):
            callback(message)

    def receive(self, recipient: str) -> list[Message]:
        """Receive all pending messages for a co-pilot."""
        messages = self._pending.pop(recipient, [])
        return messages

    def subscribe(self, copilot_id: str, callback: Callable) -> None:
        """Subscribe a co-pilot to receive real-time messages."""
        self._subscribers[copilot_id].append(callback)

    def broadcast(self, sender: str, content: str, msg_type: str = MessageType.STATUS) -> None:
        """Broadcast a message to all co-pilots."""
        from src.config import COPILOT_REGISTRY
        for copilot_id in COPILOT_REGISTRY:
            if copilot_id != sender:
                self.send(Message(
                    sender=sender,
                    recipient=copilot_id,
                    msg_type=msg_type,
                    content=content,
                ))

    def get_conversation(self, copilot_a: str, copilot_b: str) -> list[Message]:
        """Get all messages between two co-pilots."""
        return [
            m for m in self._messages
            if (m.sender == copilot_a and m.recipient == copilot_b)
            or (m.sender == copilot_b and m.recipient == copilot_a)
        ]

    def get_history(self, limit: int = 50) -> list[Message]:
        """Get recent message history."""
        return self._messages[-limit:]

    @property
    def total_messages(self) -> int:
        return len(self._messages)

    def summary(self) -> dict:
        """Get message bus statistics."""
        senders = defaultdict(int)
        types = defaultdict(int)
        for msg in self._messages:
            senders[msg.sender] += 1
            types[msg.msg_type] += 1
        return {
            "total_messages": len(self._messages),
            "by_sender": dict(senders),
            "by_type": dict(types),
        }
