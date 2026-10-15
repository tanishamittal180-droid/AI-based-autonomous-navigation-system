"""Streamlit web dashboard for the AI-Based Autonomous Navigation System."""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.config import GRID_WIDTH, GRID_HEIGHT, START, GOAL
from src.environment import make_obstacles
from src.planner import astar

st.set_page_config(page_title="NavAI | Autonomous Navigation", page_icon="🧭", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.7rem; padding-bottom: 2rem; max-width: 1450px;}
.hero {padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(120deg,#101828,#1d2939 65%,#344054); color: white; margin-bottom: 1rem;}
.hero h1 {font-size: 2.15rem; margin: 0 0 .3rem 0; color: white;}
.hero p {color:#d0d5dd; margin:0; font-size:1rem;}
.small-note {color:#667085;font-size:.85rem;}
div[data-testid="stMetric"] {background:#f8fafc; border:1px solid #eaecf0; padding: .85rem; border-radius: 12px;}
</style>
<div class="hero"><h1>🧭 NavAI — Autonomous Navigation Studio</h1><p>Plan routes, inspect obstacle fields, evaluate navigation metrics, and export reproducible simulation evidence.</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Simulation settings")
    seed = st.number_input("Random seed", min_value=0, max_value=999999, value=7, step=1)
    density = st.slider("Obstacle density", min_value=0.02, max_value=0.40, value=0.19, step=0.01)
    show_grid = st.checkbox("Show grid lines", value=True)
    show_explored = st.checkbox("Show route waypoints", value=True)
    st.divider()
    st.caption("Fixed map coordinates")
    st.code(f"Grid: {GRID_WIDTH} × {GRID_HEIGHT}\nStart: {START}\nGoal: {GOAL}")
    run_button = st.button("🚀 Generate / refresh route", type="primary", use_container_width=True)

# Session state makes a generated scenario stable until the user asks to refresh.
if "nav_run" not in st.session_state or run_button:
    obstacles = make_obstacles(density=float(density), seed=int(seed))
    started = time.perf_counter()
    path = astar(GRID_WIDTH, GRID_HEIGHT, obstacles, START, GOAL)
    elapsed_ms = (time.perf_counter() - started) * 1000
    st.session_state.nav_run = {
        "seed": int(seed), "density": float(density), "obstacles": obstacles,
        "path": path, "elapsed_ms": elapsed_ms,
    }
run = st.session_state.nav_run
obstacles = run["obstacles"]
path = run["path"]

# If controls are changed, the user can press refresh to regenerate the scenario.
if run["seed"] != int(seed) or run["density"] != float(density):
    st.info("Settings changed. Click **Generate / refresh route** to apply them.")

success = bool(path and path[-1] == GOAL)
steps = len(path) - 1 if path else 0
free_cells = GRID_WIDTH * GRID_HEIGHT - len(obstacles)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Navigation status", "ROUTE FOUND" if success else "NO ROUTE")
col2.metric("Movement steps", steps if success else "—")
col3.metric("Obstacle cells", len(obstacles))
col4.metric("Free cells", free_cells)
col5.metric("Planning time", f"{run['elapsed_ms']:.2f} ms")

left, right = st.columns([1.8, 1])
with left:
    st.subheader("🗺️ Live occupancy map")
    fig, ax = plt.subplots(figsize=(10, 6.3))
    ax.set_xlim(-0.5, GRID_WIDTH - 0.5); ax.set_ylim(GRID_HEIGHT - 0.5, -0.5)
    ax.set_aspect("equal")
    if show_grid:
        ax.set_xticks(range(GRID_WIDTH)); ax.set_yticks(range(GRID_HEIGHT))
        ax.grid(True, linewidth=.35, alpha=.4)
    else:
        ax.set_xticks([]); ax.set_yticks([])
    if obstacles:
        ox, oy = zip(*obstacles)
        ax.scatter(ox, oy, marker="s", s=100, color="#344054", label="Obstacle", zorder=2)
    if path and show_explored:
        px, py = zip(*path)
        ax.plot(px, py, color="#1570ef", linewidth=2.8, marker="o", markersize=3, label="Planned route", zorder=3)
    ax.scatter([START[0]], [START[1]], marker="o", s=180, color="#12b76a", edgecolor="white", linewidth=1.2, label="Start", zorder=5)
    ax.scatter([GOAL[0]], [GOAL[1]], marker="*", s=280, color="#f04438", edgecolor="white", linewidth=1.0, label="Goal", zorder=5)
    ax.set_title("A* route plan · 4-direction movement", fontsize=13, pad=12)
    ax.set_xlabel("Grid X"); ax.set_ylabel("Grid Y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=4, frameon=False)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.subheader("📊 Route analysis")
    if success:
        st.success("A collision-free route was found.")
        st.write(f"**Start:** `{START}`")
        st.write(f"**Destination:** `{GOAL}`")
        st.write(f"**Path nodes:** {len(path)}")
        st.write(f"**Collision cells on route:** {sum(p in obstacles for p in path)}")
        st.write(f"**Manhattan distance lower bound:** {abs(START[0]-GOAL[0]) + abs(START[1]-GOAL[1])} steps")
        efficiency = (abs(START[0]-GOAL[0]) + abs(START[1]-GOAL[1])) / steps * 100 if steps else 100
        st.write(f"**Route efficiency vs. lower bound:** {efficiency:.1f}%")
    else:
        st.error("No valid path exists for this generated map. Try lowering obstacle density or changing the seed.")
    st.markdown("**Legend**")
    st.markdown("🟢 Start · 🔴 Goal · ⬛ Obstacle · 🔵 Planned route")
    st.caption("This prototype plans over simulated occupancy cells. It does not use a camera or control a physical vehicle.")

st.divider()
st.subheader("📦 Export simulation evidence")
metrics = {
    "project": "AI-Based Autonomous Navigation System",
    "algorithm": "A* (Manhattan heuristic; four-way movement)",
    "seed": run["seed"], "obstacle_density": run["density"],
    "grid": {"width": GRID_WIDTH, "height": GRID_HEIGHT},
    "start": list(START), "goal": list(GOAL), "path_found": success,
    "path_nodes_including_start_and_goal": len(path) if path else 0,
    "movement_steps": steps if success else None,
    "obstacle_count": len(obstacles),
    "collision_cells_on_path": sum(p in obstacles for p in path) if path else None,
    "planning_time_ms": round(run["elapsed_ms"], 4),
    "status": "success" if success else "no_path",
    "scope_note": "Simulated grid occupancy only; no camera-based detection or physical vehicle control."
}
exp1, exp2, exp3 = st.columns([1, 1, 1.4])
with exp1:
    st.download_button("⬇️ Download metrics.json", data=json.dumps(metrics, indent=2), file_name="navigation_metrics.json", mime="application/json", use_container_width=True)
with exp2:
    csv_text = "step,x,y\n" + "\n".join(f"{i},{x},{y}" for i,(x,y) in enumerate(path)) if path else "step,x,y\n"
    st.download_button("⬇️ Download route.csv", data=csv_text, file_name="navigation_route.csv", mime="text/csv", use_container_width=True)
with exp3:
    st.info("Use the download buttons to save run-specific evidence. You can attach the JSON, CSV, and map screenshot to your GitHub README.")

with st.expander("🔍 View route coordinates"):
    if path:
        st.code(" → ".join(f"({x}, {y})" for x, y in path), language="text")
    else:
        st.write("No route coordinates are available for this map.")

st.markdown('<p class="small-note">NavAI student portfolio prototype · Python + Streamlit + Matplotlib · Simulation only</p>', unsafe_allow_html=True)
