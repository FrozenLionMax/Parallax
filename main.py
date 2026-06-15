"""
⬡ Parallax — AI Co-Pilots That See Work From Every Angle
═══════════════════════════════════════════════════════════

Interactive demo runner showing the full 6-step co-pilot experience:
  ASK → PLAN → WATCH → GUIDE → REVIEW → LEARN

Team Parallax · IndiaRuns Hackathon 2026
Challenge 1: The AI Systems Architect — Reimagining Work
"""

import time
import sys
import os

# Fix Windows encoding for Unicode output
if sys.platform == "win32":
    os.system("")  # Enable ANSI escape sequences on Windows
    sys.stdout.reconfigure(encoding="utf-8")

from src.orchestrator import Orchestrator
from src.config import COPILOT_REGISTRY


# ─────────────────────── PRETTY PRINTING ───────────────────────

class Colors:
    CYAN = "\033[96m"
    VIOLET = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              ⬡  P A R A L L A X                              ║
    ║                                                              ║
    ║        AI Co-Pilots That See Work From Every Angle            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}    Team Parallax · IndiaRuns Hackathon 2026 · Challenge 1{Colors.RESET}
"""
    print(banner)


def print_step(step_num: int, step_name: str, description: str):
    colors = {1: Colors.CYAN, 2: Colors.BLUE, 3: Colors.VIOLET, 4: Colors.YELLOW, 5: Colors.GREEN, 6: Colors.VIOLET}
    color = colors.get(step_num, Colors.WHITE)
    print(f"\n{color}{Colors.BOLD}{'═' * 60}")
    print(f"  STEP {step_num} — {step_name}")
    print(f"{'═' * 60}{Colors.RESET}")
    print(f"  {Colors.DIM}{description}{Colors.RESET}\n")


def print_copilot_fleet():
    print(f"\n{Colors.BOLD}  🤖 Co-Pilot Fleet (10 Active){Colors.RESET}\n")
    for i, (cid, info) in enumerate(COPILOT_REGISTRY.items(), 1):
        print(f"  {info['icon']}  {info['name']:<28} {Colors.DIM}— {info['codename']}{Colors.RESET}")
    print()


def print_task_graph(graph):
    print(f"  {Colors.BOLD}📋 Execution Plan{Colors.RESET}")
    print(f"  {Colors.DIM}{'─' * 50}{Colors.RESET}")
    for task in graph.tasks:
        copilot_info = COPILOT_REGISTRY.get(task.assigned_copilot, {})
        icon = copilot_info.get("icon", "❓")
        name = copilot_info.get("name", task.assigned_copilot)
        deps = f" (depends: {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"  {task.task_id}  {task.name:<40} {icon} {name}{Colors.DIM}{deps}{Colors.RESET}")
    print(f"  {Colors.DIM}{'─' * 50}{Colors.RESET}")
    print(f"  {Colors.CYAN}{len(graph.tasks)} tasks · {len(graph.active_copilots)} co-pilots{Colors.RESET}\n")


def simulate_progress(graph):
    """Animate co-pilot progress bars."""
    copilots_in_use = {}
    for task in graph.tasks:
        cp = task.assigned_copilot
        if cp not in copilots_in_use:
            copilots_in_use[cp] = {"tasks": [], "icon": COPILOT_REGISTRY[cp]["icon"], "name": COPILOT_REGISTRY[cp]["name"]}
        copilots_in_use[cp]["tasks"].append(task.task_id)

    for step in range(0, 21):
        pct = step * 5
        sys.stdout.write("\033[F" * (len(copilots_in_use) + 1))  # Move cursor up

        for cp_id, cp_info in copilots_in_use.items():
            filled = int(pct / 5)
            bar = "█" * filled + "░" * (20 - filled)

            if pct >= 100:
                status = f"{Colors.GREEN}✅ Done{Colors.RESET}"
            elif pct >= 50:
                status = f"{Colors.CYAN}⏳ Working...{Colors.RESET}"
            else:
                status = f"{Colors.DIM}⏳ Starting...{Colors.RESET}"

            print(f"  {cp_info['icon']} {cp_info['name']:<22} [{bar}] {pct:>3}% {status}")

        print()  # Extra line for cursor positioning
        time.sleep(0.12)


def print_messages(messages):
    print(f"\n  {Colors.BOLD}💬 Co-Pilot Communications{Colors.RESET}\n")
    colors_map = {
        "research": Colors.CYAN, "analyst": Colors.BLUE, "creator": Colors.VIOLET,
        "quality": Colors.GREEN, "data": Colors.RED, "compliance": Colors.DIM,
        "action": Colors.YELLOW, "design": Colors.VIOLET, "communication": Colors.CYAN,
        "code": Colors.YELLOW,
    }
    for msg in messages[-8:]:  # Show last 8 messages
        color = colors_map.get(msg.sender, Colors.WHITE)
        sender_info = COPILOT_REGISTRY.get(msg.sender, {})
        recip_info = COPILOT_REGISTRY.get(msg.recipient, {})
        s_icon = sender_info.get("icon", "❓")
        r_icon = recip_info.get("icon", "❓")
        print(f"  {color}  {s_icon} → {r_icon}  {msg.content[:80]}{Colors.RESET}")
        time.sleep(0.3)
    print()


def print_results(execution_result):
    summary = execution_result["graph_summary"]
    print(f"  {Colors.GREEN}{Colors.BOLD}✅ All tasks completed{Colors.RESET}\n")
    print(f"  Tasks: {summary['total_tasks']} total, {summary['completed']} completed")
    print(f"  Co-pilots used: {summary['copilots_active']}")
    print(f"  Progress: {summary['progress']}")

    # Show memory stats
    mem = execution_result["memory_stats"]
    print(f"\n  {Colors.BOLD}🗄️ Memory System{Colors.RESET}")
    print(f"  📌 Episodic:   {mem['episodic']['active_entries']} active entries")
    print(f"  🧠 Semantic:   {mem['semantic']['entities']} entities, {mem['semantic']['facts']} facts")
    print(f"  🔄 Procedural: {mem['procedural']['preferences']} preferences, {mem['procedural']['templates']} templates")


# ─────────────────────── DEMO SCENARIOS ───────────────────────

DEMO_SCENARIOS = [
    "Prepare a competitive analysis of AI recruiting tools in India and draft a strategy document for our board meeting next Tuesday.",
    "Analyze our team's last sprint — pull the JIRA data, identify why we missed the deadline, and prepare a sprint retro with action items.",
    "Research the top 20 VCs investing in AI in India, identify the best 5 fits for our Series A, and draft personalized outreach emails.",
]


# ─────────────────────── MAIN ───────────────────────

def main():
    print_banner()
    print_copilot_fleet()

    # Let user pick a scenario or type their own
    print(f"  {Colors.BOLD}🚀 Choose a scenario:{Colors.RESET}\n")
    for i, scenario in enumerate(DEMO_SCENARIOS, 1):
        print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {scenario[:70]}...")
    print(f"  {Colors.CYAN}[4]{Colors.RESET} Type your own task\n")

    try:
        choice = input(f"  {Colors.BOLD}Enter choice (1-4): {Colors.RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "1"

    if choice == "4":
        user_input = input(f"\n  {Colors.BOLD}Your task: {Colors.RESET}").strip()
    elif choice in ("1", "2", "3"):
        user_input = DEMO_SCENARIOS[int(choice) - 1]
    else:
        user_input = DEMO_SCENARIOS[0]

    # Initialize Orchestrator
    orchestrator = Orchestrator()

    # ═══════════════ STEP 1: ASK ═══════════════
    print_step(1, "ASK", "You tell Parallax what you need")
    print(f"  {Colors.VIOLET}\"{user_input}\"{Colors.RESET}\n")
    time.sleep(1)

    # Parse intent
    intent = orchestrator.parse_intent(user_input)
    print(f"  {Colors.BOLD}🧠 Intent Parsed:{Colors.RESET}")
    for key, value in intent.to_dict().items():
        if value:
            print(f"  {Colors.DIM}{key:<16}{Colors.RESET} {value}")
    time.sleep(1)

    # ═══════════════ STEP 2: PLAN ═══════════════
    print_step(2, "PLAN", "Parallax decomposes your task and assigns co-pilots")

    graph = orchestrator.decompose(intent)
    print_task_graph(graph)
    time.sleep(1)

    # ═══════════════ STEP 3: WATCH ═══════════════
    print_step(3, "WATCH", "Co-pilots are working — watch live progress")

    # Print empty progress bars first
    for cp_id in {t.assigned_copilot for t in graph.tasks}:
        info = COPILOT_REGISTRY[cp_id]
        print(f"  {info['icon']} {info['name']:<22} [{'░' * 20}]   0%")
    print()  # Extra line

    time.sleep(0.5)
    simulate_progress(graph)
    time.sleep(0.5)

    # Execute tasks (this also generates inter-agent messages)
    execution_result = orchestrator.execute(graph)

    # Show agent communications
    messages = execution_result.get("messages", [])
    if messages:
        print_messages(messages)

    # ═══════════════ STEP 4: GUIDE ═══════════════
    print_step(4, "GUIDE", "A co-pilot needs your decision")

    print(f"  {Colors.YELLOW}{Colors.BOLD}🤔 Decision Needed{Colors.RESET}")
    print(f"  {Colors.DIM}From: 📊 Analyst Co-Pilot | Confidence: 65%{Colors.RESET}\n")
    print(f"  Conflicting market size data found from multiple sources:\n")
    print(f"  {Colors.WHITE}{'Source':<20} {'Value':<15} {'Year':<8} {'Credibility'}{Colors.RESET}")
    print(f"  {'─' * 55}")
    print(f"  {'Nasscom Report':<20} {'₹2,400 Cr':<15} {'2024':<8} {Colors.GREEN}0.92{Colors.RESET}")
    print(f"  {'IMARC Group':<20} {'₹3,200 Cr':<15} {'2025':<8} {Colors.CYAN}0.88{Colors.RESET}")
    print(f"  {'TechBlog.in':<20} {'₹4,100 Cr':<15} {'2026':<8} {Colors.RED}0.41{Colors.RESET}")
    print(f"\n  {Colors.GREEN}💡 Recommendation: Use IMARC Group (most recent credible source){Colors.RESET}")
    print(f"\n  {Colors.BOLD}→ Using recommendation...{Colors.RESET}")
    time.sleep(1)

    # ═══════════════ STEP 5: REVIEW ═══════════════
    print_step(5, "REVIEW", "Quality-checked deliverables ready for you")

    print(f"  {Colors.GREEN}{Colors.BOLD}📦 DELIVERABLE READY{Colors.RESET}\n")
    print(f"  📄 Strategy_Document.pdf     — 14 pages, board-formatted")
    print(f"  📋 Executive_Summary.pdf     — 1 page, 4 bullet points")
    print(f"  📊 3 charts: market map, feature matrix, growth projection")
    print()
    print(f"  {Colors.BOLD}🛡️ Quality Co-Pilot Notes:{Colors.RESET}")
    print(f"  {Colors.GREEN}✅ All financial claims sourced — 14 citations{Colors.RESET}")
    print(f"  {Colors.GREEN}✅ Executive summary: 4 bullet points (optimal){Colors.RESET}")
    print(f"  {Colors.GREEN}✅ Compliance: Revenue disclaimer added{Colors.RESET}")
    print(f"  {Colors.YELLOW}⚠️  Competitor X pricing from March — verify before board meeting{Colors.RESET}")
    print()

    print_results(execution_result)
    time.sleep(1)

    # ═══════════════ STEP 6: LEARN ═══════════════
    print_step(6, "LEARN", "Your feedback makes Parallax smarter")

    try:
        feedback = input(f"  {Colors.BOLD}Your feedback (or press Enter to skip): {Colors.RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        feedback = ""

    if feedback:
        learn_result = orchestrator.learn_from_feedback(feedback, rating=0.9)
        print(f"\n  {Colors.GREEN}🧠 Feedback stored in Procedural Memory{Colors.RESET}")
        if learn_result["preferences_extracted"]:
            for key, value in learn_result["preferences_extracted"].items():
                print(f"  {Colors.CYAN}📌 Learned: {key} → {value}{Colors.RESET}")
        print(f"  {Colors.DIM}Template saved for future similar tasks{Colors.RESET}")
    else:
        orchestrator.learn_from_feedback("No feedback", rating=0.85)
        print(f"\n  {Colors.DIM}Task completed — no feedback provided{Colors.RESET}")

    # Final summary
    print(f"""
{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              ⬡  That's Parallax.                             ║
    ║                                                              ║
    ║        10 AI Co-Pilots. One task. Smarter every day.          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}    github.com/FrozenLionMax/Parallax · Team Parallax · IndiaRuns 2026{Colors.RESET}
""")


if __name__ == "__main__":
    main()
