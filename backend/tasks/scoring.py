from datetime import datetime, date

# Default configuration values
DEFAULT_MAX_DAYS_WINDOW = 30
DEFAULT_MAX_HOURS = 40
DEFAULT_MAX_BLOCKED = 5

# Strategy weight presets
STRATEGIES = {
    "smart_balance": {
        "urgency": 0.35,
        "importance": 0.35,
        "effort": 0.15,
        "dependency": 0.15,
    },
    "fastest_wins": {
        "urgency": 0.15,
        "importance": 0.20,
        "effort": 0.60,
        "dependency": 0.05,
    },
    "high_impact": {
        "urgency": 0.15,
        "importance": 0.70,
        "effort": 0.05,
        "dependency": 0.10,
    },
    "deadline_driven": {
        "urgency": 0.70,
        "importance": 0.15,
        "effort": 0.05,
        "dependency": 0.10,
    }
}


# -------------------------
#  DATE PARSER (SAFE)
# -------------------------

def safe_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except:
        return None


# -------------------------
#  CYCLE DETECTION
# -------------------------

def detect_cycles(tasks):
    """
    Detect circular dependencies using DFS.
    Returns:
        (has_cycle, list_of_cycles)
    """
    graph = {}
    for t in tasks:
        tid = str(t.get("id"))
        deps = t.get("dependencies", [])
        graph[tid] = [str(d) for d in deps]

    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            if dep not in visited:
                dfs(dep, path + [dep])
            elif dep in stack:
                cycles.append(path[path.index(dep):] + [dep])

        stack.remove(node)

    for id_ in graph:
        if id_ not in visited:
            dfs(id_, [id_])

    return len(cycles) > 0, cycles


# -------------------------
#  SUB-SCORE CALCULATIONS
# -------------------------

def calculate_sub_scores(task, today, blocked_map):
    warnings = []

    # Parse values
    tid = str(task.get("id"))
    title = task.get("title", "(no title)")
    due = safe_date(task.get("due_date"))
    importance = task.get("importance", 5)
    est_hours = task.get("estimated_hours", 1)

    try:
        est_hours = float(est_hours)
        if est_hours <= 0:
            warnings.append("estimated_hours must be > 0, defaulted to 1")
            est_hours = 1
    except:
        warnings.append("estimated_hours invalid, defaulted to 1")
        est_hours = 1

    try:
        importance = int(importance)
        if not (1 <= importance <= 10):
            warnings.append("importance must be between 1–10, clamped")
            importance = max(1, min(10, importance))
    except:
        warnings.append("importance invalid, defaulted to 5")
        importance = 5

    # URGENCY SCORE
    if due is None:
        urgency = 0
    else:
        days_left = (due - today).days
        if days_left < 0:
            urgency = 100
        else:
            urgency = max(0, min(100, 100 * (1 - days_left / DEFAULT_MAX_DAYS_WINDOW)))

    # IMPORTANCE SCORE (1–10 → 10–100)
    importance_score = importance * 10

    # EFFORT SCORE (quick wins)
    hours = min(est_hours, DEFAULT_MAX_HOURS)
    effort_score = (1 - (hours / DEFAULT_MAX_HOURS)) * 100

    # DEPENDENCY SCORE
    blocked_count = blocked_map.get(tid, 0)
    dependency_score = min(100, (blocked_count / DEFAULT_MAX_BLOCKED) * 100)

    return {
        "urgency_score": round(urgency, 2),
        "importance_score": round(importance_score, 2),
        "effort_score": round(effort_score, 2),
        "dependency_score": round(dependency_score, 2),
        "warnings": warnings
    }


# -------------------------
#  FINAL SCORE + SORTING
# -------------------------

def compute_scores(tasks, strategy="smart_balance"):
    today = date.today()

    # Choose weight preset
    weights = STRATEGIES.get(strategy, STRATEGIES["smart_balance"])

    id_map = {str(t.get("id")): t for t in tasks}

    # Count how many tasks are blocked by each task
    blocked_map = {tid: 0 for tid in id_map}
    for t in tasks:
        for dep in t.get("dependencies", []):
            dep = str(dep)
            if dep in blocked_map:
                blocked_map[dep] += 1

    # Detect cycles
    has_cycle, cycle_list = detect_cycles(tasks)

    results = []
    for tid, task in id_map.items():
        sub = calculate_sub_scores(task, today, blocked_map)

        score = (
            sub["urgency_score"] * weights["urgency"] +
            sub["importance_score"] * weights["importance"] +
            sub["effort_score"] * weights["effort"] +
            sub["dependency_score"] * weights["dependency"]
        )

        score = round(score, 2)

        if score >= 75:
            priority = "High"
        elif score >= 50:
            priority = "Medium"
            priority = "Medium"
        else:
            priority = "Low"

        explanation = (
            f"Urgency={sub['urgency_score']}, "
            f"Importance={sub['importance_score']}, "
            f"Effort={sub['effort_score']}, "
            f"Dependency={sub['dependency_score']}."
        )

        results.append({
            "id": tid,
            "title": task["title"],
            "score": score,
            "priority_level": priority,
            "explanation": explanation,
            "sub_scores": sub,
        })

    # sort high → low
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {
        "tasks": results,
        "has_cycle": has_cycle,
        "cycles": cycle_list,
    }
