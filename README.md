# AI-Based Autonomous Navigation System

A beginner-friendly, simulation-first autonomous navigation portfolio project. A virtual agent navigates a 2D occupancy grid from a start point to a goal while avoiding blocked cells. The A* search algorithm plans a route; a Pygame visualizer animates the agent; a Streamlit web dashboard provides controls, route analysis, and downloadable evidence; a headless mode exports a map and JSON metrics.

> **Scope note:** This version is a grid-world navigation prototype. Obstacles are simulated map cells, not camera-based object detections. It does not control a real vehicle and is not a safety-certified autonomous driving system.

## Why this project?
The core ideas—environment representation, route planning, obstacle avoidance, visualization, repeatable tests, and metrics—are useful foundations for robotics, warehouse automation, delivery robots, and autonomous vehicle research. Real-world systems add sensors, localization, perception, motion planning, and safety layers.

## Features
- Deterministic 2D environment using a configurable random seed
- A* path planning with Manhattan heuristic and four-way movement
- Animated Pygame simulation with pause, restart, save, and quit controls
- Headless run for CI/laptops without a display
- Streamlit frontend with adjustable random seed and obstacle density
- Dashboard metrics, occupancy-map visualization, and JSON/CSV downloads
- Exports `outputs/navigation_result.png` and `outputs/metrics.json`
- Unit tests for route finding, obstacle avoidance, and unreachable goals

## Tech stack
- Python 3.10–3.12
- Pygame: interactive simulation
- Streamlit: browser-based dashboard frontend
- NumPy / Matplotlib: scientific Python dependencies and map visualization
- Python `unittest`: tests

## Architecture
```text
Seed + grid settings
        |
        v
Environment generator ---> Occupancy grid / obstacle cells
        |                              |
        +--------------+---------------+
                       v
                 A* path planner <--- Start + Goal
                       |
                       v
                 Planned waypoint list
                       |
             +---------+---------+
             v                   v
      Pygame animation     Metrics + static map
                                  |
                                  v
                       outputs/*.png, *.json
```

## Folder structure
```text
AI-Based-Autonomous-Navigation-System/
├── main.py                    # CLI and interactive simulation entry point
├── dashboard.py               # Streamlit browser dashboard
├── requirements.txt           # Python dependencies
├── run_windows.bat            # Windows convenience launcher
├── run_headless_windows.bat   # Windows headless report launcher
├── run_dashboard_windows.bat  # Windows dashboard launcher
├── src/
│   ├── config.py              # grid, agent and simulation settings
│   ├── environment.py         # seeded obstacle map generation
│   ├── planner.py             # A* route planning
│   ├── visualization.py       # export static map image
│   └── metrics.py             # JSON run summary
├── tests/test_planner.py      # automated unit tests
├── outputs/                   # generated results (kept in Git)
├── docs/                      # execution and frontend/upgrade guide
└── assets/                    # optional demo GIF/screenshots
```

## Installation

### Windows (PowerShell)
```powershell
# 1. Open this folder in VS Code / terminal
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python --version
python -c "import pygame, matplotlib, numpy; print('Dependencies OK')"
```
If PowerShell blocks activation, use Command Prompt instead:
```bat
.venv\Scripts\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import pygame, matplotlib, numpy; print('Dependencies OK')"
```

## Run the browser frontend (recommended demo)

After activating `.venv` and installing requirements, run:

```bash
python -m streamlit run dashboard.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`). The dashboard lets you change the random seed and obstacle density, inspect the A* route, review metrics, and download JSON metrics and route CSV evidence. On Windows, `run_dashboard_windows.bat` is also available after environment setup.

See [`docs/FRONTEND_AND_UPGRADE.md`](docs/FRONTEND_AND_UPGRADE.md) for frontend features and commands.

## Run the project

Interactive animated simulation:
```bash
python main.py
```

Headless run (creates files without opening a window):
```bash
python main.py --headless
```

Change the map seed or obstacle density:
```bash
python main.py --seed 21 --density 0.22
python main.py --headless --seed 21 --density 0.22
```

Run tests:
```bash
python -m unittest discover -s tests -v
```

Save proof assets while the GUI is running by pressing **S**. Controls: **Space** pauses/resumes, **R** restarts, **S** saves the static map and metrics, **Q/Esc** exits.

## Expected output
The terminal reports the chosen seed, obstacle count, whether a route was found, path length, and output paths. Successful runs create:
- `outputs/navigation_result.png` — annotated grid map with obstacles, start, goal, and A* route
- `outputs/metrics.json` — route status, number of steps, obstacle count, and collision-cell count

The default seed is designed to produce a route. If a custom map has no route, reduce density or choose another seed.

## Results and limitations
A successful run ends with the agent at the goal and reports zero obstacle cells along the planned route. A* is optimal for this grid when each move has equal cost and the Manhattan heuristic is used. This prototype does not include camera perception, lane detection, deep-learning object detection, localization, continuous vehicle dynamics, or real hardware control.

## Screenshots / demo
Save your outputs and add screenshots to `assets/`. Suggested filenames:
- `assets/01_environment.png`
- `assets/02_astar_path.png`
- `assets/03_agent_navigation.png`
- `assets/04_successful_run.png`
- `assets/05_terminal_metrics.png`

Embed them after capturing real screenshots:
```markdown
![A* planned route](assets/02_astar_path.png)
```
Do not add placeholder screenshots as if they were captured from a real run.

## Upgrade roadmap
1. Add dynamic obstacles and re-planning after map changes.
2. Add a grid editor and selectable start/goal positions.
3. Add camera/video perception with OpenCV and a clearly documented dataset/model.
4. Integrate ROS 2 and Gazebo/Webots for robot middleware and physics simulation.
5. Explore CARLA for road-driving scenarios, then add localization, lane perception, and vehicle control.
6. Add benchmarking across seeds: path length, planning time, success rate, and node expansions.

## GitHub publishing
```bash
git init
git add .
git commit -m "Build simulation-first autonomous navigation prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-autonomous-navigation.git
git push -u origin main
```
Create the empty repository on GitHub first and replace `YOUR_USERNAME`. Suggested topics: `python`, `robotics`, `path-planning`, `astar`, `pygame`, `simulation`, `autonomous-navigation`.

Suggested description: **Simulation-first autonomous navigation prototype using A* path planning, obstacle-aware routing, animated visualization, and reproducible metrics.**

## Proof-building plan
- Day 1: environment setup and initial commit (`chore: set up Python project`); capture dependency check.
- Day 2: grid generation (`feat: generate seeded occupancy grid`); capture environment image.
- Day 3: A* planner and tests (`feat: implement A-star path planner`); capture planned route and test output.
- Day 4: animated agent (`feat: animate agent along planned route`); record a short screen capture.
- Day 5: metrics/export (`feat: export navigation map and run metrics`); commit generated PNG/JSON.
- Day 6: edge-case tests and docs (`test: cover blocked and unreachable routes`); capture test terminal.
- Day 7: README polish and demo (`docs: add setup guide and project demo`); pin the repository and share a truthful project summary.

## Resume bullets (edit to match what you actually ran)
- Built a Python-based 2D autonomous navigation simulator with A* path planning and obstacle-aware route generation.
- Implemented deterministic test maps, animated agent visualization, and exportable route metrics for reproducible experiments.
- Added unit tests for blocked endpoints, obstacle avoidance, and unreachable destinations; documented setup and execution for GitHub.

## Interview quick answers
**Why A*?** It combines known path cost with a heuristic estimate to the goal, efficiently prioritizing promising routes. With equal-cost grid moves and Manhattan distance, the heuristic is admissible.

**How are obstacles represented?** As occupied grid coordinates that the planner is not allowed to enter.

**What happens if no route exists?** The planner returns an empty path and the run reports `no_path`.

**Is this a self-driving car?** No. It is a small navigation simulation that demonstrates route planning concepts; a real vehicle requires perception, localization, dynamics, control, and extensive safety validation.

## Troubleshooting
- **`python` not found:** install Python 3.10–3.12 and enable PATH, or use `py` on Windows.
- **`ModuleNotFoundError`:** activate `.venv` and run `pip install -r requirements.txt`.
- **Pygame window does not open:** try `python main.py --headless`; on remote/headless Linux, a GUI display may not be available.
- **No route found:** lower density, e.g. `--density 0.12`, or try a different seed.
- **Git push rejected:** run `git pull --rebase origin main` if the remote already contains a README, then push again.
- **Generated output not updated:** press `S` in the GUI or run `python main.py --headless`.

## Author
**Your Name** — Student project / portfolio demonstration. Replace this line with your GitHub profile and contact links before publishing.

## License
MIT — see `LICENSE`.
