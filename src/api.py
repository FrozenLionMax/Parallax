"""
Parallax — REST API
FastAPI backend exposing co-pilot orchestration as a production-ready API.

Endpoints:
    POST /ask              — Submit a task in natural language
    GET  /status/{id}      — Get task graph execution status
    GET  /copilots          — List all 11 co-pilots and their status
    GET  /copilots/{id}     — Get details for a specific co-pilot
    POST /feedback          — Submit feedback for learning
    GET  /memory/stats      — Get memory system statistics
    GET  /cost/{id}         — Get cost breakdown for a task
    GET  /health            — Health check
"""

from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from src.orchestrator import Orchestrator
from src.config import COPILOT_REGISTRY, APP_NAME, TAGLINE, VERSION


# ═══════════════════════════════════════════════════════════════
#  APP SETUP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title=f"⬡ {APP_NAME} API",
    description=f"{TAGLINE} — RESTful API for orchestrating 11 AI co-pilots.",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator (single instance for demo)
orchestrator = Orchestrator()

# Store active task graphs by ID
active_tasks: dict[str, dict] = {}


# ═══════════════════════════════════════════════════════════════
#  REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════

class AskRequest(BaseModel):
    """Submit a task to Parallax."""
    task: str = Field(..., description="Natural language task description", min_length=5)
    priority: str = Field(default="normal", description="Task priority: low, normal, high, urgent")
    audience: Optional[str] = Field(default=None, description="Target audience for the output")
    deadline: Optional[str] = Field(default=None, description="Deadline for the task")

    class Config:
        json_schema_extra = {
            "example": {
                "task": "Prepare a competitive analysis of AI recruiting tools in India for our board meeting Tuesday",
                "priority": "high",
                "audience": "Board of Directors",
                "deadline": "Tuesday"
            }
        }


class AskResponse(BaseModel):
    graph_id: str
    status: str
    intent: dict
    task_plan: list[dict]
    copilots_assigned: list[str]
    estimated_time: str


class FeedbackRequest(BaseModel):
    """Submit feedback for a completed task."""
    graph_id: str = Field(..., description="The task graph ID to provide feedback for")
    feedback: str = Field(..., description="Natural language feedback")
    rating: float = Field(default=1.0, ge=0.0, le=1.0, description="Rating from 0.0 to 1.0")

    class Config:
        json_schema_extra = {
            "example": {
                "graph_id": "abc123",
                "feedback": "Executive summary was too long — keep it to 4 bullet points max",
                "rating": 0.85
            }
        }


class CostBreakdown(BaseModel):
    """Per-task cost breakdown."""
    copilot: str
    model_used: str
    tokens: int
    cost_inr: float


# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """System health check."""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": VERSION,
        "copilots_active": len(orchestrator.copilots),
        "memory": orchestrator.memory.full_stats(),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """
    Submit a task to Parallax.

    The orchestrator will:
    1. Parse your intent
    2. Decompose into a task DAG
    3. Assign co-pilots
    4. Execute the workflow
    5. Return results

    This endpoint returns immediately with the execution plan.
    Use GET /status/{graph_id} to check progress.
    """
    # Step 1: Parse intent
    intent = orchestrator.parse_intent(request.task)

    # Step 2: Decompose into task graph
    graph = orchestrator.decompose(intent)

    # Step 3: Execute
    execution = orchestrator.execute(graph)

    # Store for status checks
    active_tasks[graph.graph_id] = {
        "graph": graph,
        "intent": intent,
        "execution": execution,
        "created_at": datetime.now().isoformat(),
    }

    # Build response
    task_plan = []
    for task in graph.tasks:
        cp_info = COPILOT_REGISTRY.get(task.assigned_copilot, {})
        task_plan.append({
            "task_id": task.task_id,
            "name": task.name,
            "copilot": f"{cp_info.get('icon', '❓')} {cp_info.get('name', task.assigned_copilot)}",
            "status": task.state,
            "dependencies": task.dependencies,
            "confidence": task.confidence,
        })

    return AskResponse(
        graph_id=graph.graph_id,
        status="completed",
        intent=intent.to_dict(),
        task_plan=task_plan,
        copilots_assigned=list(graph.active_copilots),
        estimated_time="25 minutes",
    )


@app.get("/status/{graph_id}")
async def get_status(graph_id: str):
    """Get the execution status of a task graph."""
    entry = active_tasks.get(graph_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Task graph {graph_id} not found")

    graph = entry["graph"]
    return {
        "graph_id": graph_id,
        "summary": graph.summary(),
        "tasks": [
            {
                "task_id": t.task_id,
                "name": t.name,
                "copilot": t.assigned_copilot,
                "state": t.state,
                "progress": t.progress,
                "confidence": t.confidence,
            }
            for t in graph.tasks
        ],
        "messages": [str(m) for m in entry["execution"].get("messages", [])],
        "created_at": entry["created_at"],
    }


@app.get("/copilots")
async def list_copilots():
    """List all 11 co-pilots with their capabilities and status."""
    fleet = []
    for cid, info in COPILOT_REGISTRY.items():
        copilot = orchestrator.copilots.get(cid)
        status = copilot.status() if copilot else {}
        fleet.append({
            "id": cid,
            "name": info["name"],
            "codename": info["codename"],
            "icon": info["icon"],
            "color": info["color"],
            "description": info["description"],
            "capabilities": info["capabilities"],
            "tasks_completed": status.get("completed_total", 0),
            "escalations": status.get("escalations", 0),
        })
    return {"total_copilots": len(fleet), "fleet": fleet}


@app.get("/copilots/{copilot_id}")
async def get_copilot(copilot_id: str):
    """Get detailed information about a specific co-pilot."""
    if copilot_id not in COPILOT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Co-pilot '{copilot_id}' not found")

    info = COPILOT_REGISTRY[copilot_id]
    copilot = orchestrator.copilots.get(copilot_id)
    status = copilot.status() if copilot else {}

    return {
        "id": copilot_id,
        **info,
        "status": status,
    }


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback for a completed task.

    This feeds into the Procedural Memory (RLHF-style learning).
    Preferences extracted from feedback are stored for future tasks.
    """
    result = orchestrator.learn_from_feedback(request.feedback, request.rating)
    return {
        "feedback_stored": True,
        "graph_id": request.graph_id,
        "preferences_learned": result.get("preferences_extracted", {}),
        "template_saved": result.get("template_saved", False),
        "memory_stats": result.get("memory_stats", {}),
    }


@app.get("/memory/stats")
async def memory_stats():
    """Get statistics for all three memory layers."""
    return {
        "memory_system": orchestrator.memory.full_stats(),
        "description": {
            "episodic": "Short-term session memory — what's happening now",
            "semantic": "Long-term knowledge graph — entities, facts, relationships",
            "procedural": "Learned preferences — user style, templates, RLHF feedback",
        },
    }


@app.get("/cost/{graph_id}")
async def get_cost(graph_id: str):
    """Get cost breakdown for a task execution."""
    entry = active_tasks.get(graph_id)
    if not entry:
        raise HTTPException(status_code=404, detail=f"Task graph {graph_id} not found")

    # Simulated cost model (in production: actual token counting)
    cost_model = {
        "research": {"model": "GPT-4o", "tokens": 12400, "cost_inr": 3.20},
        "data": {"model": "GPT-4o-mini", "tokens": 4200, "cost_inr": 0.45},
        "analyst": {"model": "Claude 3.5 Sonnet", "tokens": 8100, "cost_inr": 2.10},
        "creator": {"model": "GPT-4o", "tokens": 15600, "cost_inr": 4.00},
        "design": {"model": "DALL-E 3", "tokens": 0, "cost_inr": 2.50},
        "compliance": {"model": "Llama 3 70B", "tokens": 3800, "cost_inr": 0.00},
        "quality": {"model": "Llama 3 70B", "tokens": 4200, "cost_inr": 0.00},
        "catalyst": {"model": "GPT-4o-mini", "tokens": 1200, "cost_inr": 0.12},
        "communication": {"model": "GPT-4o-mini", "tokens": 2100, "cost_inr": 0.22},
        "action": {"model": "GPT-4o-mini", "tokens": 800, "cost_inr": 0.08},
        "code": {"model": "Claude 3.5 Sonnet", "tokens": 6500, "cost_inr": 1.70},
    }

    graph = entry["graph"]
    breakdown = []
    total_tokens = 0
    total_cost = 0.0

    for task in graph.tasks:
        cost = cost_model.get(task.assigned_copilot, {"model": "GPT-4o-mini", "tokens": 1000, "cost_inr": 0.10})
        cp_info = COPILOT_REGISTRY.get(task.assigned_copilot, {})
        breakdown.append({
            "copilot": f"{cp_info.get('icon', '')} {cp_info.get('name', task.assigned_copilot)}",
            "task": task.name,
            "model": cost["model"],
            "tokens": cost["tokens"],
            "cost_inr": cost["cost_inr"],
        })
        total_tokens += cost["tokens"]
        total_cost += cost["cost_inr"]

    # Calculate ROI
    manual_hours = 24  # Estimated manual time in hours
    avg_hourly_cost = 625  # ₹12L/year ÷ 1920 hrs
    manual_cost = manual_hours * avg_hourly_cost

    return {
        "graph_id": graph_id,
        "breakdown": breakdown,
        "total_tokens": total_tokens,
        "total_cost_inr": round(total_cost, 2),
        "roi": {
            "parallax_cost": f"₹{total_cost:.2f}",
            "manual_cost": f"₹{manual_cost:,.0f}",
            "savings": f"₹{manual_cost - total_cost:,.0f}",
            "roi_multiplier": f"{manual_cost / total_cost:.0f}x" if total_cost > 0 else "∞",
            "time_saved": f"{manual_hours} hours → 25 minutes",
        },
    }


# ═══════════════════════════════════════════════════════════════
#  STARTUP
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    """Warm up the system on startup."""
    print(f"\n  {APP_NAME} API v{VERSION}")
    print(f"  {TAGLINE}")
    print(f"  {len(orchestrator.copilots)} co-pilots ready\n")
