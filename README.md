# 🌱 Deterministic Daily Reflection Tree

**DT Fellowship Assignment | Practice-Driven Growth Management System (PDGMS)**

Live app: https://dt-reflection-tree-jhnatnvvocnptalz8n3jbp.streamlit.app/

A deterministic reflection tool designed to move an employee through three psychological axes:
**Locus of Control**, **Orientation**, and **Radius of Concern**.

Unlike typical AI chatbots, this tool is a **Deterministic Decision Tree**. It uses **no LLM at runtime**, ensuring the reflection experience is **predictable, auditable, and grounded** in establis[...]

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

## ⚙️ The Reflection Engine (Logic Core)

The application uses a custom-built **State Machine** in Python. This engine is responsible for “walking” the tree based on the data provided in `reflection-tree.json`.

### 1) State Accumulation (Psychological Signals)

Instead of simple scoring, the engine uses **Semantic Tallying**. Each choice the user makes carries a “signal” (e.g., `axis1:internal`). These are stored in the session state and used by lat[...]

```python
def tally_signal(signal: str):
    # Splits 'axis1:internal' into Axis and Pole
    # Increments the specific counter in st.session_state
```

### 2) Invisible Logic Resolution (The “Decision” Loop)

One of the most advanced features of the engine is its ability to handle **Silent Nodes**. When the user submits an answer, the engine enters a loop. If the next node in the tree is a `type: deci[...]

The engine repeats this until it finds a **Visible** node (Question, Reflection, or Summary).

### 3) Routing Logic Patterns

The `Reflection.py` engine supports three types of deterministic routing:

| Rule Type | Logic | Purpose |
|---|---|---|
| `answer_in` | `if answer in [value1, value2]` | Branches based on a specific prior answer. |
| `dominant` | `if axis1_internal > axis1_external` | Branches based on accumulated psychological signals. |
| `default` | `else: move to X` | Ensures the state machine never gets stuck. |

### 4) Dynamic Text Interpolation

To make the tool feel personalized without using an LLM, the engine uses **String Interpolation**. It scans the text for placeholders like `{A1_OPEN}` and replaces them with the user’s actual p[...]

```python
def interpolate(text: str):
    # Replaces placeholders with user-provided answers
    # Result: "You said it felt like 'Stormy' today..."
```

**Why this belongs in your README:**

By adding this section, you are telling the DeepThought Growth Team that you didn’t just write a “quiz”—you built an **Extensible Engine**. You can argue that:

- **Auditable:** The logic is 100% transparent and can be audited by management.
- **Scalability:** New axes can be added to the JSON without changing the Python code.
- **Efficiency:** The system runs with near-zero latency because it doesn’t wait for API calls to an LLM.

---

## Notes

- This project is deterministic by design;
- 
