# Frontend dashboard and upgraded version

## What's new

The project now includes a browser-based Streamlit dashboard in `dashboard.py`, alongside the original Pygame simulation and command-line/headless modes.

Dashboard capabilities:
- Responsive browser UI with sidebar controls for random seed and obstacle density
- Interactive occupancy map showing obstacles, start, goal, and the A* route
- Route status, step count, free/blocked cells, planning time, collision check, and route-efficiency estimate
- Downloadable JSON metrics and CSV route coordinates
- Expandable route-coordinate view

## Run on Windows

From the project root, activate the virtual environment and install requirements:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run dashboard.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open that address in your browser.

Shortcut after setup:

```powershell
.\run_dashboard_windows.bat
```

## Run on macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run dashboard.py
```

## Existing modes still work

```bash
python main.py                 # Pygame animated simulation
python main.py --headless      # Save static PNG and JSON metrics
python -m unittest discover -s tests -v
```

## Honest scope statement

The dashboard visualizes a simulated grid and runs A* path planning. It is not a trained deep-learning perception model and does not detect real objects from camera images. Future upgrade directions include dynamic obstacle replanning, OpenCV camera perception, optional YOLO integration, ROS 2, and CARLA.
