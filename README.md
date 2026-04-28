# 🌱 Deterministic Daily Reflection Tree

**DT Fellowship Assignment | Practice-Driven Growth Management System (PDGMS)**

A deterministic reflection tool designed to move an employee through three psychological axes:
**Locus of Control**, **Orientation**, and **Radius of Concern**.

Unlike typical AI chatbots, this tool is a **Deterministic Decision Tree**. It uses **no LLM at runtime**, ensuring the reflection experience is **predictable, auditable, and grounded** in established management science.

---

## 🌳 Logic & Branching Structure

The core of this project is **state-machine traversal**.

- **"Intelligence" / content** lives in: `reflection-tree.json`
- **Engine / traversal** lives in: Python modules (see below)

### The Three Axes of Reflection

1. **Axis 1: Locus (Victim vs. Victor)**
   - Based on **Rotter (1954)**
   - Surfaces whether the employee perceives **personal agency** in the day’s events.

2. **Axis 2: Orientation (Contribution vs. Entitlement)**
   - Based on **Organ (1988)**
   - Distinguishes between **discretionary effort** and **psychological entitlement**.

3. **Axis 3: Radius (Self-Centrism vs. Altrocentrism)**
   - Informed by **Maslow’s Self-Transcendence (1969)**
   - Explores the **breadth of concern** (self → others → system).

---

## 🏗️ Technical Architecture

During development, this project intentionally explored two architectural patterns.

### 1) Decoupled API (Advanced)

- **Backend** (`backend.py`, `Reflection.py`): FastAPI service that manages psychological state and routing.
- **Frontend** (`frontend.py`): Streamlit UI that communicates with the backend over REST.

**Status:** Fully functional; well-suited for scalable enterprise environments.

### 2) Monolithic App (Production Deployment)

- **App** (`app.py`): A unified Streamlit application merging engine + UI.

**Why this choice?**
For evaluator-friendly deployment: **zero-latency**, fewer moving parts, and higher reliability.

---

## 📂 Project Structure

```text
├── app.py                # Unified Production Streamlit App (run this for deployment)
├── reflection-tree.json  # THE BRAIN: deterministic logic nodes
├── Reflection.py         # Core engine logic (decoupled version)
├── backend.py            # FastAPI entry point (decoupled version)
├── frontend.py           # Streamlit UI (decoupled version)
├── make_venv.sh          # Shell script for automated environment setup
├── requirements.txt      # Project dependencies
└── .gitignore            # Keeps the repo clean of venv and pycache
```

---

## 🚀 Setup & Execution

### Local Setup (macOS / Linux)

If you prefer an automated helper:

```bash
# 1. Make the script executable
chmod +x make_venv.sh

# 2. Run the setup script
./make_venv.sh

# 3. Activate the environment
source .venv/bin/activate
```

Or do it manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Production (Monolithic) App

```bash
streamlit run app.py
```

### Run the API (Decoupled) Version

**Terminal 1 (Backend):**

```bash
uvicorn backend:app --reload
```

**Terminal 2 (Frontend):**

```bash
streamlit run frontend.py
```

---

## 🧠 Knowledge Engineering Highlights

- **Zero-Footprint Personalization**
  - Uses string interpolation (e.g., `{placeholder}`) to reference user answers without generating new text.

- **Invisible Routing**
  - Decision nodes are processed in the background.
  - The user only sees meaningful interaction points; scoring/path selection remains hidden.

- **Modular Content**
  - The full conversation can be updated by editing `reflection-tree.json` alone—no code changes required.

---

## Notes

- This project is deterministic by design; if you want to extend it with probabilistic or LLM-driven behavior, keep the decision-tree contract intact so the system remains testable and auditable.
