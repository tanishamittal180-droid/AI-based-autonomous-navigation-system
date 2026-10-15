# Execution commands quick reference

## Windows PowerShell
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Windows Command Prompt
```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Headless output, tests, and custom maps
```bash
python main.py --headless
python -m unittest discover -s tests -v
python main.py --seed 21 --density 0.22
python main.py --headless --seed 21 --density 0.22
```

## Outputs
- `outputs/navigation_result.png`
- `outputs/metrics.json`

GUI controls: Space = pause/resume; R = restart; S = save outputs; Q/Esc = quit.
