"""
Parallax — Unit Tests
Comprehensive test suite for the multi-agent co-pilot system.

Run with: pytest tests/ -v
"""

import pytest
from src.orchestrator import Orchestrator
from src.models import Task, TaskGraph, Message, Intent, MemoryEntry
from src.memory import MemorySystem, EpisodicMemory, SemanticMemory, ProceduralMemory
from src.message_bus import MessageBus
from src.config import COPILOT_REGISTRY, TaskState, MessageType
from src.copilots.catalyst import CatalystCoPilot


# ═══════════════════════════════════════════════════════════════
#  TEST: CONFIGURATION
# ═══════════════════════════════════════════════════════════════

class TestConfig:
    """Tests for system configuration."""

    def test_all_11_copilots_registered(self):
        """Verify all 11 co-pilots are in the registry."""
        assert len(COPILOT_REGISTRY) == 11
        expected = {
            "research", "analyst", "creator", "action", "quality",
            "communication", "code", "data", "design", "compliance", "catalyst"
        }
        assert set(COPILOT_REGISTRY.keys()) == expected

    def test_copilot_registry_structure(self):
        """Every co-pilot must have name, codename, icon, color, description, capabilities."""
        required_keys = {"name", "codename", "icon", "color", "description", "capabilities"}
        for cid, info in COPILOT_REGISTRY.items():
            for key in required_keys:
                assert key in info, f"Co-pilot '{cid}' missing '{key}'"
            assert len(info["capabilities"]) >= 3, f"Co-pilot '{cid}' needs at least 3 capabilities"

    def test_unique_icons(self):
        """Each co-pilot must have a unique icon."""
        icons = [info["icon"] for info in COPILOT_REGISTRY.values()]
        assert len(icons) == len(set(icons)), "Duplicate icons found"

    def test_unique_codenames(self):
        """Each co-pilot must have a unique codename."""
        codenames = [info["codename"] for info in COPILOT_REGISTRY.values()]
        assert len(codenames) == len(set(codenames)), "Duplicate codenames found"


# ═══════════════════════════════════════════════════════════════
#  TEST: MODELS
# ═══════════════════════════════════════════════════════════════

class TestModels:
    """Tests for core data models."""

    def test_task_creation(self):
        task = Task("T1", "Research competitors", "Find AI tools", "research")
        assert task.task_id == "T1"
        assert task.state == TaskState.PENDING
        assert task.progress == 0.0

    def test_task_completion(self):
        task = Task("T1", "Research", "desc", "research")
        task.complete({"data": "result"}, confidence=0.92)
        assert task.state == TaskState.COMPLETED
        assert task.progress == 1.0
        assert task.confidence == 0.92
        assert task.completed_at is not None

    def test_task_failure(self):
        task = Task("T1", "Research", "desc", "research")
        task.fail("API timeout")
        assert task.state == TaskState.FAILED
        assert "error" in task.result

    def test_task_blocking(self):
        task = Task("T1", "Research", "desc", "research")
        task.block("Need user decision")
        assert task.state == TaskState.BLOCKED

    def test_task_graph_creation(self):
        graph = TaskGraph(user_input="test task")
        t1 = Task("T1", "Research", "desc", "research")
        t2 = Task("T2", "Analyze", "desc", "analyst", dependencies=["T1"])
        graph.add_task(t1)
        graph.add_task(t2)
        assert len(graph.tasks) == 2

    def test_task_graph_ready_tasks(self):
        graph = TaskGraph()
        t1 = Task("T1", "Research", "desc", "research")
        t2 = Task("T2", "Analyze", "desc", "analyst", dependencies=["T1"])
        graph.add_task(t1)
        graph.add_task(t2)

        ready = graph.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].task_id == "T1"

    def test_task_graph_dependency_resolution(self):
        graph = TaskGraph()
        t1 = Task("T1", "Research", "desc", "research")
        t2 = Task("T2", "Analyze", "desc", "analyst", dependencies=["T1"])
        graph.add_task(t1)
        graph.add_task(t2)

        # Complete T1
        t1.complete("done")

        ready = graph.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].task_id == "T2"

    def test_task_graph_progress(self):
        graph = TaskGraph()
        t1 = Task("T1", "A", "d", "research")
        t2 = Task("T2", "B", "d", "analyst")
        graph.add_task(t1)
        graph.add_task(t2)

        assert graph.progress == 0.0
        t1.complete("done")
        assert graph.progress == 0.5
        t2.complete("done")
        assert graph.progress == 1.0
        assert graph.is_complete()

    def test_message_creation(self):
        msg = Message(sender="research", recipient="analyst", msg_type=MessageType.RESULT, content="Data ready")
        assert msg.sender == "research"
        assert msg.recipient == "analyst"
        assert msg.message_id is not None

    def test_intent_creation(self):
        intent = Intent(goal="analyze competitors", domain="AI", audience="Board")
        d = intent.to_dict()
        assert d["Goal"] == "analyze competitors"
        assert d["Domain"] == "AI"


# ═══════════════════════════════════════════════════════════════
#  TEST: MEMORY SYSTEM
# ═══════════════════════════════════════════════════════════════

class TestMemory:
    """Tests for the 3-layer memory system."""

    def test_episodic_store_and_recall(self):
        mem = EpisodicMemory()
        mem.store("key1", "value1", source="test")
        assert mem.recall("key1") == "value1"

    def test_episodic_missing_key(self):
        mem = EpisodicMemory()
        assert mem.recall("nonexistent") is None

    def test_episodic_session_context(self):
        mem = EpisodicMemory()
        mem.store("a", 1)
        mem.store("b", 2)
        ctx = mem.get_session_context()
        assert len(ctx) == 2

    def test_episodic_clear(self):
        mem = EpisodicMemory()
        mem.store("a", 1)
        mem.clear_session()
        assert mem.size == 0

    def test_semantic_entity(self):
        mem = SemanticMemory()
        mem.add_entity("company_x", "competitor", {"name": "X Corp", "revenue": "₹100Cr"})
        entity = mem.get_entity("company_x")
        assert entity is not None
        assert entity["type"] == "competitor"

    def test_semantic_relationship(self):
        mem = SemanticMemory()
        mem.add_entity("a", "company", {})
        mem.add_entity("b", "company", {})
        mem.add_relationship("a", "b", "competes_with")
        rels = mem.get_relationships("a")
        assert len(rels) == 1
        assert rels[0]["relationship"] == "competes_with"

    def test_semantic_fact(self):
        mem = SemanticMemory()
        mem.store_fact("market_size", "₹3200 Cr")
        assert mem.recall_fact("market_size") == "₹3200 Cr"

    def test_semantic_query(self):
        mem = SemanticMemory()
        mem.add_entity("ai_tool", "product", {"name": "AI Recruiter"})
        results = mem.query("AI")
        assert len(results) >= 1

    def test_procedural_preference(self):
        mem = ProceduralMemory()
        mem.store_preference("format", "bullet_points")
        assert mem.get_preference("format") == "bullet_points"

    def test_procedural_template(self):
        mem = ProceduralMemory()
        mem.store_template("comp_analysis", {"steps": ["research", "analyze", "write"]}, 0.9)
        tmpl = mem.get_template("comp_analysis")
        assert tmpl is not None
        assert tmpl["success_score"] == 0.9

    def test_procedural_feedback(self):
        mem = ProceduralMemory()
        mem.record_feedback("task_1", "Too verbose", 0.6)
        assert mem.stats["feedback_entries"] == 1

    def test_unified_memory_system(self):
        mem = MemorySystem()
        mem.episodic.store("test", "value")
        mem.semantic.store_fact("fact", "data")
        mem.procedural.store_preference("pref", "short")
        stats = mem.full_stats()
        assert stats["episodic"]["active_entries"] == 1
        assert stats["semantic"]["facts"] == 1
        assert stats["procedural"]["preferences"] == 1

    def test_memory_consolidation(self):
        mem = MemorySystem()
        mem.episodic.store("entity:company_x", {"name": "X"})
        mem.episodic.store("preference:format", "bullets")
        mem.consolidate_session()
        assert mem.episodic.size == 0  # Cleared after consolidation


# ═══════════════════════════════════════════════════════════════
#  TEST: MESSAGE BUS
# ═══════════════════════════════════════════════════════════════

class TestMessageBus:
    """Tests for inter-co-pilot communication."""

    def test_send_and_receive(self):
        bus = MessageBus()
        msg = Message(sender="research", recipient="analyst", msg_type=MessageType.RESULT, content="Data ready")
        bus.send(msg)
        received = bus.receive("analyst")
        assert len(received) == 1
        assert received[0].content == "Data ready"

    def test_no_pending_messages(self):
        bus = MessageBus()
        received = bus.receive("analyst")
        assert len(received) == 0

    def test_message_history(self):
        bus = MessageBus()
        bus.send(Message(sender="a", recipient="b", msg_type="RESULT", content="msg1"))
        bus.send(Message(sender="b", recipient="a", msg_type="RESULT", content="msg2"))
        history = bus.get_history()
        assert len(history) == 2

    def test_conversation_between_copilots(self):
        bus = MessageBus()
        bus.send(Message(sender="research", recipient="analyst", msg_type="RESULT", content="data"))
        bus.send(Message(sender="analyst", recipient="research", msg_type="QUERY", content="clarify?"))
        bus.send(Message(sender="creator", recipient="quality", msg_type="RESULT", content="draft"))

        conv = bus.get_conversation("research", "analyst")
        assert len(conv) == 2

    def test_bus_summary(self):
        bus = MessageBus()
        bus.send(Message(sender="research", recipient="analyst", msg_type="RESULT", content="1"))
        bus.send(Message(sender="research", recipient="creator", msg_type="RESULT", content="2"))
        summary = bus.summary()
        assert summary["total_messages"] == 2
        assert summary["by_sender"]["research"] == 2


# ═══════════════════════════════════════════════════════════════
#  TEST: ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════

class TestOrchestrator:
    """Tests for the central brain."""

    def test_initialization(self):
        orch = Orchestrator()
        assert len(orch.copilots) == 11

    def test_all_copilots_instantiated(self):
        orch = Orchestrator()
        expected = {
            "research", "analyst", "creator", "action", "quality",
            "communication", "code", "data", "design", "compliance", "catalyst"
        }
        assert set(orch.copilots.keys()) == expected

    def test_intent_parsing(self):
        orch = Orchestrator()
        intent = orch.parse_intent("Analyze AI recruiting tools in India for the board meeting Tuesday")
        assert intent.goal != ""
        assert intent.confidence > 0

    def test_task_decomposition(self):
        orch = Orchestrator()
        intent = orch.parse_intent("Research competitors")
        graph = orch.decompose(intent)
        assert len(graph.tasks) > 0
        assert graph.graph_id is not None

    def test_full_execution(self):
        orch = Orchestrator()
        intent = orch.parse_intent("Prepare competitive analysis for board meeting")
        graph = orch.decompose(intent)
        result = orch.execute(graph)
        assert result["graph_summary"]["completed"] > 0
        assert "results" in result

    def test_learning_from_feedback(self):
        orch = Orchestrator()
        intent = orch.parse_intent("Test task")
        orch.decompose(intent)
        result = orch.learn_from_feedback("Keep summaries shorter", rating=0.9)
        assert result["feedback_stored"] is True

    def test_fleet_status(self):
        orch = Orchestrator()
        status = orch.fleet_status()
        assert len(status) == 11

    def test_copilot_retrieval(self):
        orch = Orchestrator()
        research = orch.get_copilot("research")
        assert research is not None
        assert research.name == "Research Co-Pilot"

    def test_list_copilots(self):
        orch = Orchestrator()
        copilots = orch.list_copilots()
        assert len(copilots) == 11
        assert "catalyst" in copilots


# ═══════════════════════════════════════════════════════════════
#  TEST: CATALYST CO-PILOT
# ═══════════════════════════════════════════════════════════════

class TestCatalyst:
    """Tests for the 11th co-pilot — The Accelerator."""

    def setup_method(self):
        self.memory = MemorySystem()
        self.bus = MessageBus()
        self.catalyst = CatalystCoPilot(self.memory, self.bus)

    def test_initialization(self):
        assert self.catalyst.copilot_id == "catalyst"
        assert self.catalyst.codename == "The Accelerator"

    def test_caching(self):
        self.catalyst.cache_result("test_key", {"data": "value"})
        result = self.catalyst.get_cached("test_key")
        assert result == {"data": "value"}

    def test_cache_miss(self):
        result = self.catalyst.get_cached("nonexistent")
        assert result is None

    def test_cache_hit_tracking(self):
        self.catalyst.cache_result("key", "value")
        self.catalyst.get_cached("key")
        self.catalyst.get_cached("key")
        stats = self.catalyst.cache_stats()
        assert stats["total_hits"] == 2

    def test_compression(self):
        large_data = {"text": "x" * 10000, "records": list(range(500))}
        compressed = self.catalyst.compress_for_transfer(large_data)
        assert "summary" in compressed
        assert "entities" in compressed
        assert "metrics" in compressed

    def test_dag_optimization(self):
        tasks = [
            Task("T1", "A", "d", "research"),
            Task("T2", "B", "d", "data"),
            Task("T3", "C", "d", "analyst", dependencies=["T1", "T2", "T3"]),
        ]
        result = self.catalyst.optimize_task_graph(tasks)
        assert len(result["parallelizable_tasks"]) == 2
        assert len(result["bottleneck_tasks"]) == 1

    def test_prefetch(self):
        self.catalyst.prefetch_for_copilot("research", ["market_data", "competitors"])
        stats = self.catalyst.cache_stats()
        assert stats["cache_entries"] == 2

    def test_process_overflow(self):
        task = Task("T1", "Misc task", "Convert CSV", "catalyst")
        result = self.catalyst.process(task)
        assert result["confidence"] > 0
        assert task.state == TaskState.COMPLETED


# ═══════════════════════════════════════════════════════════════
#  TEST: CO-PILOT BASE CLASS
# ═══════════════════════════════════════════════════════════════

class TestCoPilotBase:
    """Tests for base co-pilot functionality."""

    def setup_method(self):
        self.memory = MemorySystem()
        self.bus = MessageBus()
        self.catalyst = CatalystCoPilot(self.memory, self.bus)

    def test_confidence_action_auto_execute(self):
        assert self.catalyst.determine_action(0.95) == "auto_execute"

    def test_confidence_action_hold(self):
        assert self.catalyst.determine_action(0.80) == "hold_approval"

    def test_confidence_action_escalate(self):
        assert self.catalyst.determine_action(0.50) == "escalate"

    def test_send_message(self):
        self.catalyst.send_message("analyst", "Test message")
        received = self.bus.receive("analyst")
        assert len(received) == 1

    def test_memory_access(self):
        self.catalyst.remember_short_term("key", "value")
        assert self.catalyst.recall_short_term("key") == "value"

    def test_learn_fact(self):
        self.catalyst.learn_fact("market_size", "₹3200 Cr")
        assert self.catalyst.recall_fact("market_size") == "₹3200 Cr"

    def test_status(self):
        status = self.catalyst.status()
        assert status["copilot_id"] == "catalyst"
        assert "active_tasks" in status

    def test_repr(self):
        repr_str = repr(self.catalyst)
        assert "Catalyst" in repr_str
        assert "Accelerator" in repr_str
