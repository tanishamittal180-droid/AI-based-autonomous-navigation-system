"""Small metrics report for reproducible project runs."""
import json
from pathlib import Path
from .planner import Point


def write_metrics(path: list[Point], obstacles: set[Point], start: Point, goal: Point, output: str | Path) -> Path:
    result = {
        "algorithm": "A* (Manhattan heuristic; four-way movement)",
        "start": list(start), "goal": list(goal),
        "path_found": bool(path),
        "path_nodes_including_start_and_goal": len(path),
        "movement_steps": max(0, len(path) - 1) if path else None,
        "obstacle_count": len(obstacles),
        "collision_cells_on_path": sum(point in obstacles for point in path),
        "status": "success" if path and path[-1] == goal else "no_path",
        "note": "Grid cells are simulated occupancy data, not camera-based object detections."
    }
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return output
