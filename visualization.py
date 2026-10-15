"""Static map rendering for saved proof assets and headless runs."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .planner import Point


def save_map(path: list[Point], obstacles: set[Point], start: Point, goal: Point,
             width: int, height: int, output: str | Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(height - 0.5, -0.5)
    ax.set_xticks(range(width)); ax.set_yticks(range(height))
    ax.grid(True, linewidth=0.35, alpha=0.45)
    if obstacles:
        ox, oy = zip(*obstacles)
        ax.scatter(ox, oy, marker="s", s=100, color="#344054", label="Obstacle")
    if path:
        px, py = zip(*path)
        ax.plot(px, py, color="#1683ff", linewidth=2.8, marker="o", markersize=3, label="A* route")
    ax.scatter([start[0]], [start[1]], marker="o", s=170, color="#12b76a", edgecolor="black", label="Start", zorder=5)
    ax.scatter([goal[0]], [goal[1]], marker="*", s=250, color="#f04438", edgecolor="black", label="Goal", zorder=5)
    ax.set_title("AI-Based Autonomous Navigation — A* Grid Simulation")
    ax.set_xlabel("Grid X"); ax.set_ylabel("Grid Y")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return output
