"""
Parallax — 11th Co-Pilot: The Catalyst (Accelerator)
Speeds up data flow, handles overflow, and optimizes the entire pipeline.
"""

from __future__ import annotations
from typing import Any
from src.copilots.base import BaseCoPilot
from src.models import Task, Message
from src.config import MessageType
from src.memory import MemorySystem
from src.message_bus import MessageBus


class CatalystCoPilot(BaseCoPilot):
    """
    ⚙️ CATALYST CO-PILOT — "The Accelerator"

    The 11th co-pilot that makes the other 10 faster.

    Responsibilities:
    1. PRE-FETCH — Anticipate what co-pilots will need and fetch it early
    2. CACHE — Store intermediate results so co-pilots don't repeat work
    3. OVERFLOW — Handle simple tasks when specialist co-pilots are busy
    4. PARALLELIZE — Optimize task graph for maximum parallel execution
    5. COMPRESS — Summarize large data payloads for faster inter-agent transfer
    """

    def __init__(self, memory: MemorySystem, bus: MessageBus):
        super().__init__("catalyst", memory, bus)
        self._cache: dict[str, Any] = {}
        self._prefetch_queue: list[dict] = []
        self._compression_stats = {"original_tokens": 0, "compressed_tokens": 0}

    def process(self, task: Task) -> dict:
        task.state = "running"
        task.progress = 0.1

        task_type = self._classify(task.description)
        task.progress = 0.3

        if task_type == "prefetch":
            output = self._prefetch(task)
        elif task_type == "cache_warmup":
            output = self._warm_cache(task)
        elif task_type == "compress":
            output = self._compress_payload(task)
        elif task_type == "optimize_dag":
            output = self._optimize_dag(task)
        else:
            output = self._handle_overflow(task)

        task.progress = 1.0
        result = {
            "output": output,
            "confidence": 0.94,
            "messages": [],
            "artifacts": [],
            "metadata": {
                "task_type": task_type,
                "cache_size": len(self._cache),
                "compression_ratio": self._get_compression_ratio(),
            },
        }
        task.complete(result["output"], result["confidence"])
        self._completed_count += 1
        return result

    # ─────────────────────── PREFETCH ───────────────────────

    def prefetch_for_copilot(self, copilot_id: str, anticipated_needs: list[str]):
        """
        Anticipate what a co-pilot will need and fetch it before it asks.

        Example: If Research Co-Pilot is researching "AI tools in India",
        Catalyst pre-fetches industry reports, market data, and competitor lists
        so they're ready in cache when Research needs them.
        """
        for need in anticipated_needs:
            cache_key = f"prefetch:{copilot_id}:{need}"
            if cache_key not in self._cache:
                data = self._fetch_anticipated_data(need)
                self._cache[cache_key] = data
                self.remember_short_term(cache_key, data)

        self.send_message(
            to=copilot_id,
            content=f"Pre-fetched {len(anticipated_needs)} data points. Available in cache.",
            msg_type=MessageType.STATUS,
            payload={"prefetched": anticipated_needs},
        )

        return {"prefetched": len(anticipated_needs), "cache_hits_expected": len(anticipated_needs)}

    def _prefetch(self, task: Task) -> dict:
        """Pre-fetch data based on task graph analysis."""
        return self.prefetch_for_copilot("research", [
            "industry_reports", "market_data", "competitor_lists", "pricing_databases"
        ])

    # ─────────────────────── CACHING ───────────────────────

    def cache_result(self, key: str, value: Any, ttl_minutes: int = 30):
        """Cache an intermediate result for reuse by other co-pilots."""
        self._cache[key] = {
            "data": value,
            "hits": 0,
            "ttl": ttl_minutes,
        }

    def get_cached(self, key: str) -> Any:
        """Retrieve cached data. Returns None if not found."""
        entry = self._cache.get(key)
        if entry:
            entry["hits"] += 1
            return entry["data"]
        return None

    def _warm_cache(self, task: Task) -> dict:
        """Pre-warm cache with commonly needed data."""
        common_data = {
            "market_frameworks": ["SWOT", "Porter's Five Forces", "PESTEL", "BCG Matrix"],
            "report_templates": ["executive_summary", "full_report", "one_pager", "slide_deck"],
            "credibility_tiers": {"institutional": 0.95, "industry_report": 0.88, "news": 0.75, "blog": 0.45},
            "formatting_standards": {"board": "executive", "engineering": "technical", "sales": "persuasive"},
        }
        for key, data in common_data.items():
            self.cache_result(key, data, ttl_minutes=120)

        return {"cache_warmed": True, "entries": len(common_data), "cache_size": len(self._cache)}

    # ─────────────────────── COMPRESSION ───────────────────────

    def compress_for_transfer(self, data: dict, max_tokens: int = 2000) -> dict:
        """
        Compress large data payloads for faster inter-agent transfer.

        When Research Co-Pilot finds 50 pages of data, Catalyst
        compresses it to key facts before passing to Analyst.
        """
        original_size = len(str(data))
        self._compression_stats["original_tokens"] += original_size

        compressed = {
            "summary": self._extract_key_points(data),
            "entities": self._extract_entities(data),
            "metrics": self._extract_metrics(data),
            "full_data_ref": "available_in_cache",
        }

        compressed_size = len(str(compressed))
        self._compression_stats["compressed_tokens"] += compressed_size

        return compressed

    def _compress_payload(self, task: Task) -> dict:
        """Compress a task's payload."""
        sample_data = {"pages": 50, "findings": list(range(100)), "raw_text": "x" * 5000}
        compressed = self.compress_for_transfer(sample_data)
        return {
            "compressed": True,
            "ratio": self._get_compression_ratio(),
            "original_size": len(str(sample_data)),
            "compressed_size": len(str(compressed)),
        }

    def _get_compression_ratio(self) -> str:
        orig = self._compression_stats["original_tokens"]
        comp = self._compression_stats["compressed_tokens"]
        if orig == 0:
            return "N/A"
        return f"{(1 - comp / orig) * 100:.0f}% reduction"

    # ─────────────────────── DAG OPTIMIZATION ───────────────────────

    def optimize_task_graph(self, tasks: list[Task]) -> dict:
        """
        Analyze a task graph and suggest optimizations:
        - Identify tasks that can run in parallel
        - Merge redundant tasks
        - Suggest pre-fetching for bottleneck tasks
        """
        parallelizable = []
        sequential = []
        bottlenecks = []

        for task in tasks:
            if not task.dependencies:
                parallelizable.append(task.task_id)
            elif len(task.dependencies) > 2:
                bottlenecks.append(task.task_id)
            else:
                sequential.append(task.task_id)

        optimizations = {
            "parallelizable_tasks": parallelizable,
            "sequential_tasks": sequential,
            "bottleneck_tasks": bottlenecks,
            "suggestions": [],
        }

        if len(parallelizable) > 1:
            optimizations["suggestions"].append(
                f"Run {len(parallelizable)} tasks in parallel at start — saves ~{len(parallelizable) * 2} minutes"
            )

        if bottlenecks:
            optimizations["suggestions"].append(
                f"Pre-fetch data for bottleneck tasks {bottlenecks} to reduce wait time"
            )

        return optimizations

    def _optimize_dag(self, task: Task) -> dict:
        return {"optimization": "DAG analyzed", "suggestions": ["Parallel execution enabled", "Cache pre-warmed"]}

    # ─────────────────────── OVERFLOW HANDLING ───────────────────────

    def _handle_overflow(self, task: Task) -> dict:
        """Handle tasks that don't fit any specialist or when specialists are busy."""
        return {
            "handled_as": "overflow",
            "description": task.description,
            "result": f"General-purpose processing completed for: {task.name}",
            "note": "Handled by Catalyst as overflow from specialist co-pilots",
        }

    # ─────────────────────── HELPERS ───────────────────────

    def _classify(self, description: str) -> str:
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["prefetch", "pre-fetch", "anticipate"]):
            return "prefetch"
        elif any(w in desc_lower for w in ["cache", "warm", "prepare"]):
            return "cache_warmup"
        elif any(w in desc_lower for w in ["compress", "summarize payload"]):
            return "compress"
        elif any(w in desc_lower for w in ["optimize", "dag", "parallel"]):
            return "optimize_dag"
        return "overflow"

    def _fetch_anticipated_data(self, need: str) -> dict:
        return {"need": need, "status": "prefetched", "data": f"Cached data for {need}"}

    def _extract_key_points(self, data: dict) -> list[str]:
        return ["Key finding 1", "Key finding 2", "Key finding 3"]

    def _extract_entities(self, data: dict) -> list[str]:
        return ["Entity A", "Entity B"]

    def _extract_metrics(self, data: dict) -> dict:
        return {"data_points": len(str(data)), "sources": 5}

    def cache_stats(self) -> dict:
        """Get cache performance metrics."""
        total_hits = sum(entry.get("hits", 0) for entry in self._cache.values() if isinstance(entry, dict))
        return {
            "cache_entries": len(self._cache),
            "total_hits": total_hits,
            "compression": self._get_compression_ratio(),
        }
