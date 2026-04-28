from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import os

app = FastAPI(title="Reflection Tree API")

# ===========================================================================
# 1. DATASET LOADING
# ===========================================================================

# This logic finds the JSON file in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TREE_FILE_PATH = os.path.join(BASE_DIR, "reflection-tree.json")

def load_tree_data():
    """Loads the tree structure from the local JSON file"""
    if not os.path.exists(TREE_FILE_PATH):
        raise FileNotFoundError(f"Could not find {TREE_FILE_PATH}. Please ensure the JSON file is in the same folder.")
    
    with open(TREE_FILE_PATH, "r") as f:
        return json.load(f)

# Load the data once when the server starts
TREE_DATA = load_tree_data()
NODES = TREE_DATA["nodes"]

# ===========================================================================
# 2. MODELS
# ===========================================================================
class AppState(BaseModel):
    answers: Dict[str, str]
    signals: Dict[str, Dict[str, int]]

class ActionRequest(BaseModel):
    current_node_id: str
    choice_label: Optional[str] = None
    state: AppState

class ActionResponse(BaseModel):
    node: Dict[str, Any]
    state: AppState

# ===========================================================================
# 3. BACKEND LOGIC
# ===========================================================================
def get_dominant(state: AppState, axis: str) -> str:
    """Return whichever pole has the higher tally; ties go to the first pole"""
    counts = state.signals[axis]
    poles = list(counts.keys())
    return poles[0] if counts[poles[0]] >= counts[poles[1]] else poles[1]

def tally_signal(state: AppState, signal: str):
    """Increment the pole counter for signals like 'axis:pole'"""
    if not signal:
        return
    parts = signal.split(":")
    if len(parts) == 2:
        axis, pole = parts
        if axis in state.signals and pole in state.signals[axis]:
            state.signals[axis][pole] += 1

def interpolate_text(text: str, state: AppState) -> str:
    """Replace {NODE_ID} placeholders with user answers"""
    for node_id, answer in state.answers.items():
        text = text.replace(f"{{{node_id}}}", answer)
    return text

def resolve_decision(node: dict, state: AppState) -> str:
    """Evaluate routing rules top-to-bottom"""
    for rule in node["routing"]:
        cond = rule["condition"]
        if cond == "answer_in":
            if state.answers.get(rule["node"], "") in rule["values"]:
                return rule["next"]
        elif cond == "dominant":
            if get_dominant(state, rule["axis"]) == rule["pole"]:
                return rule["next"]
        elif cond == "default":
            return rule["next"]
    return None

def build_summary(template: str, state: AppState) -> str:
    """Fill in the final report using calculated axis results"""
    a1 = get_dominant(state, "axis1")
    a2 = get_dominant(state, "axis2")
    a3 = get_dominant(state, "axis3")

    labels = {
        "axis1": {
            "internal": ("Toward ownership", "You stayed in the driver's seat, even on a rough road."),
            "external": ("Toward circumstance", "Today pulled your attention outward. Worth noticing where choice was hiding."),
        },
        "axis2": {
            "contribution": ("Toward giving", "You offered something beyond what was asked of you."),
            "entitlement":  ("Toward receiving", "Your attention tracked what you were getting."),
        },
        "axis3": {
            "altrocentric": ("Toward others", "Your frame included the people around you."),
            "self":         ("Toward self", "Your focus stayed close today."),
        },
    }

    a1_label, a1_detail = labels["axis1"][a1]
    a2_label, a2_detail = labels["axis2"][a2]
    a3_label, a3_detail = labels["axis3"][a3]
    
    combos = {
        ("internal", "contribution", "altrocentric"): "Three for three — agency, generosity, an outward gaze.",
        ("internal", "contribution", "self"): "You owned your day and gave something real.",
        ("internal", "entitlement", "altrocentric"): "You see your own agency clearly.",
        ("internal", "entitlement", "self"): "You stayed in control today.",
        ("external", "contribution", "altrocentric"): "Even in difficulty, you gave to others.",
        ("external", "contribution", "self"): "You contributed despite the circumstances.",
        ("external", "entitlement", "altrocentric"): "Today was hard, but you still noticed others.",
        ("external", "entitlement", "self"): "A day that felt beyond your control.",
    }
    closing = combos.get((a1, a2, a3), "Every day is a data point.")

    result = template
    result = result.replace("{axis1_label}", a1_label).replace("{axis1_detail}", a1_detail)
    result = result.replace("{axis2_label}", a2_label).replace("{axis2_detail}", a2_detail)
    result = result.replace("{axis3_label}", a3_label).replace("{axis3_detail}", a3_detail)
    result = result.replace("{closing}", closing)
    return result

def get_next_visible_node(node_id: str, state: AppState) -> dict:
    """Recursively process decision nodes until a visible node is hit"""
    while True:
        if not node_id:
            return None
        node = NODES[node_id].copy()
        
        if node["type"] == "decision":
            node_id = resolve_decision(node, state)
            continue
            
        if node["type"] in ["question", "reflection"]:
            node["text"] = interpolate_text(node["text"], state)
        elif node["type"] == "summary":
            node["text"] = build_summary(node["text"], state)
            
        return node

# ===========================================================================
# 4. API ENDPOINTS
# ===========================================================================
@app.get("/init")
def init_session():
    """Initializes a new reflection session"""
    initial_state = AppState(
        answers={},
        signals={
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"altrocentric": 0, "self": 0},
        }
    )
    start_node = get_next_visible_node(TREE_DATA["start"], initial_state)
    return ActionResponse(node=start_node, state=initial_state)

@app.post("/submit", response_model=ActionResponse)
def submit_action(req: ActionRequest):
    """Updates state based on choice and returns the next UI node"""
    current_node = NODES[req.current_node_id]
    
    if current_node["type"] == "question" and req.choice_label:
        req.state.answers[req.current_node_id] = req.choice_label
        chosen_opt = next((o for o in current_node["options"] if o["label"] == req.choice_label), None)
        if not chosen_opt:
            raise HTTPException(status_code=400, detail="Invalid choice")
            
        tally_signal(req.state, chosen_opt.get("signal"))
        next_id = chosen_opt["next"]
        
    elif current_node["type"] == "reflection":
        tally_signal(req.state, current_node.get("signal"))
        next_id = current_node.get("next")
        
    else:
        next_id = current_node.get("next")

    next_node = get_next_visible_node(next_id, req.state)
    return ActionResponse(node=next_node, state=req.state)