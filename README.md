# Daily Reflection Tree — Local setup

This project is a pure-Python CLI prototype and has no external dependencies.

Quick start (macOS / Linux):

```bash
# Create a virtual environment in the project folder
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# (No dependencies required) — but if you add any, install them from requirements.txt
pip install -r requirements.txt

# Run the app
python deterministic_decision_tree.py

# Run demo personas
python deterministic_decision_tree.py --demo victor
python deterministic_decision_tree.py --demo victim

# Run the FastAPI backend server
uvicorn backend:app --reload
```

If you prefer an automated helper, run `./make_venv.sh` (then `source .venv/bin/activate`).
# dt-reflection-tree
