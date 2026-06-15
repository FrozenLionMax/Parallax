"""
Parallax — Memory System
Three-layer persistent memory: Episodic, Semantic, Procedural.
"""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Optional
from src.models import MemoryEntry


class EpisodicMemory:
    """
    📌 EPISODIC MEMORY — What's happening NOW.

    Short-term, session-scoped memory for:
    - Current task state and progress
    - Co-pilot intermediate outputs
    - User corrections this session
    - Active context window
    """

    def __init__(self):
        self._store: dict[str, MemoryEntry] = {}
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def store(self, key: str, value: Any, source: str = "system", ttl_minutes: int = 60):
        """Store a short-term memory entry with optional TTL."""
        entry = MemoryEntry(
            key=key,
            value=value,
            source=source,
            entry_type="episodic",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=ttl_minutes),
        )
        self._store[key] = entry

    def recall(self, key: str) -> Optional[Any]:
        """Recall a memory entry. Returns None if expired or not found."""
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry.is_expired():
            del self._store[key]
            return None
        return entry.value

    def get_session_context(self) -> dict:
        """Get all active (non-expired) entries as context."""
        context = {}
        expired_keys = []
        for key, entry in self._store.items():
            if entry.is_expired():
                expired_keys.append(key)
            else:
                context[key] = entry.value
        for key in expired_keys:
            del self._store[key]
        return context

    def clear_session(self):
        """Clear all episodic memory (end of session)."""
        self._store.clear()

    @property
    def size(self) -> int:
        return len(self._store)


class SemanticMemory:
    """
    🧠 SEMANTIC MEMORY — What we KNOW.

    Long-term, persistent memory for:
    - Knowledge graph (entities and relationships)
    - Domain knowledge and expertise models
    - Historical decisions and their outcomes
    - Organization-specific terminology
    """

    def __init__(self):
        self._entities: dict[str, dict] = {}
        self._relationships: list[dict] = []
        self._facts: dict[str, MemoryEntry] = {}

    def add_entity(self, entity_id: str, entity_type: str, properties: dict, source: str = ""):
        """Add an entity to the knowledge graph."""
        self._entities[entity_id] = {
            "type": entity_type,
            "properties": properties,
            "source": source,
            "created_at": datetime.now().isoformat(),
        }

    def add_relationship(self, from_entity: str, to_entity: str, relationship: str, properties: dict = None):
        """Add a relationship between entities."""
        self._relationships.append({
            "from": from_entity,
            "to": to_entity,
            "relationship": relationship,
            "properties": properties or {},
            "created_at": datetime.now().isoformat(),
        })

    def store_fact(self, key: str, value: Any, source: str = "", confidence: float = 1.0):
        """Store a long-term fact."""
        self._facts[key] = MemoryEntry(
            key=key,
            value=value,
            source=source,
            entry_type="fact",
            confidence=confidence,
        )

    def recall_fact(self, key: str) -> Optional[Any]:
        """Recall a stored fact."""
        entry = self._facts.get(key)
        return entry.value if entry else None

    def get_entity(self, entity_id: str) -> Optional[dict]:
        """Get an entity from the knowledge graph."""
        return self._entities.get(entity_id)

    def find_entities(self, entity_type: str) -> list[dict]:
        """Find all entities of a given type."""
        return [
            {"id": eid, **edata}
            for eid, edata in self._entities.items()
            if edata["type"] == entity_type
        ]

    def get_relationships(self, entity_id: str) -> list[dict]:
        """Get all relationships for an entity."""
        return [
            r for r in self._relationships
            if r["from"] == entity_id or r["to"] == entity_id
        ]

    def query(self, query_text: str) -> list[dict]:
        """Simple keyword search across entities and facts."""
        results = []
        query_lower = query_text.lower()

        for eid, edata in self._entities.items():
            props_str = str(edata["properties"]).lower()
            if query_lower in eid.lower() or query_lower in props_str:
                results.append({"type": "entity", "id": eid, "data": edata})

        for key, entry in self._facts.items():
            if query_lower in key.lower() or query_lower in str(entry.value).lower():
                results.append({"type": "fact", "key": key, "value": entry.value})

        return results

    @property
    def stats(self) -> dict:
        return {
            "entities": len(self._entities),
            "relationships": len(self._relationships),
            "facts": len(self._facts),
        }


class ProceduralMemory:
    """
    🔄 PROCEDURAL MEMORY — What we've LEARNED.

    Evolving memory for:
    - User quality preferences
    - Successful workflow templates
    - Tool usage patterns
    - Feedback-driven improvements (RLHF)
    - Calibrated confidence thresholds
    """

    def __init__(self):
        self._preferences: dict[str, MemoryEntry] = {}
        self._templates: dict[str, dict] = {}
        self._feedback_history: list[dict] = []

    def store_preference(self, key: str, value: Any, source: str = "user_feedback"):
        """Store a user preference learned from feedback."""
        self._preferences[key] = MemoryEntry(
            key=key,
            value=value,
            source=source,
            entry_type="preference",
        )

    def get_preference(self, key: str) -> Optional[Any]:
        """Get a stored preference."""
        entry = self._preferences.get(key)
        return entry.value if entry else None

    def get_all_preferences(self) -> dict[str, Any]:
        """Get all stored preferences."""
        return {k: v.value for k, v in self._preferences.items()}

    def store_template(self, name: str, template: dict, success_score: float = 1.0):
        """Store a successful workflow template for reuse."""
        self._templates[name] = {
            "template": template,
            "success_score": success_score,
            "times_used": 0,
            "created_at": datetime.now().isoformat(),
        }

    def get_template(self, name: str) -> Optional[dict]:
        """Get a workflow template."""
        tmpl = self._templates.get(name)
        if tmpl:
            tmpl["times_used"] += 1
        return tmpl

    def find_similar_template(self, task_type: str) -> Optional[dict]:
        """Find the best matching template for a task type."""
        matches = [
            (name, tmpl) for name, tmpl in self._templates.items()
            if task_type.lower() in name.lower()
        ]
        if matches:
            matches.sort(key=lambda x: x[1]["success_score"], reverse=True)
            return matches[0][1]
        return None

    def record_feedback(self, task_id: str, feedback: str, rating: float = 1.0):
        """Record user feedback for RLHF-style learning."""
        self._feedback_history.append({
            "task_id": task_id,
            "feedback": feedback,
            "rating": rating,
            "timestamp": datetime.now().isoformat(),
        })

    @property
    def stats(self) -> dict:
        return {
            "preferences": len(self._preferences),
            "templates": len(self._templates),
            "feedback_entries": len(self._feedback_history),
        }


# ═══════════════════════════════════════════════════════════════
#  UNIFIED MEMORY SYSTEM
# ═══════════════════════════════════════════════════════════════

class MemorySystem:
    """
    The complete 3-layer memory system for Parallax.

    Coordinates across:
    - Episodic: What's happening now
    - Semantic: What we know
    - Procedural: What we've learned
    """

    def __init__(self):
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()

    def consolidate_session(self):
        """
        End-of-session consolidation:
        Move important episodic memories into semantic/procedural storage.
        """
        context = self.episodic.get_session_context()

        # Extract entities from session context
        for key, value in context.items():
            if key.startswith("entity:"):
                entity_id = key.replace("entity:", "")
                self.semantic.add_entity(entity_id, "discovered", {"data": value})

            elif key.startswith("preference:"):
                pref_key = key.replace("preference:", "")
                self.procedural.store_preference(pref_key, value)

        # Clear episodic after consolidation
        self.episodic.clear_session()

    def full_stats(self) -> dict:
        """Get stats across all memory layers."""
        return {
            "episodic": {"active_entries": self.episodic.size},
            "semantic": self.semantic.stats,
            "procedural": self.procedural.stats,
        }
