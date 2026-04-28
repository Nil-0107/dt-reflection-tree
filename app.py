import streamlit as st
import json
import os

# ===========================================================================
# 1. DATA LOADING (The "Knowledge Engineering" Layer)
# ===========================================================================

def load_tree_data():
    """Loads the tree from the local JSON file."""
    # This works both on your Mac and on Streamlit Cloud
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "reflection-tree.json")
    
    if not os.path.exists(file_path):
        st.error(f"Missing data file: {file_path}")
        return None
    
    with open(file_path, "r") as f:
        return json.load(f)

# ===========================================================================
# 2. STATE MANAGEMENT (The "Engine" Layer)
# ===========================================================================

def init_state():
    """Initializes persistent session data."""
    if "initialized" not in st.session_state:
        tree = load_tree_data()
        if not tree:
            st.stop()
            
        st.session_state.nodes = tree["nodes"]
        st.session_state.current_node_id = tree["start"]
        st.session_state.answers = {}
        st.session_state.signals = {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"altrocentric": 0, "self": 0},
        }
        st.session_state.initialized = True

# --- Engine Helpers ---

def get_dominant(axis: str) -> str:
    counts = st.session_state.signals[axis]
    poles = list(counts.keys())
    return poles[0] if counts[poles[0]] >= counts[poles[1]] else poles[1]

def tally_signal(signal: str):
    if not signal: return
    parts = signal.split(":")
    if len(parts) == 2:
        axis, pole = parts
        if axis in st.session_state.signals:
            st.session_state.signals[axis][pole] += 1

def interpolate(text: str) -> str:
    for node_id, answer in st.session_state.answers.items():
        text = text.replace(f"{{{node_id}}}", answer)
    return text

def resolve_logic(node_id: str):
    """Processes 'decision' nodes invisibly until a UI node is hit."""
    while True:
        if not node_id: return None
        node = st.session_state.nodes[node_id]
        
        if node["type"] != "decision":
            return node_id
            
        # Logic Resolution
        next_id = None
        for rule in node["routing"]:
            cond = rule["condition"]
            if cond == "answer_in":
                if st.session_state.answers.get(rule["node"]) in rule["values"]:
                    next_id = rule["next"]; break
            elif cond == "dominant":
                if get_dominant(rule["axis"]) == rule["pole"]:
                    next_id = rule["next"]; break
            elif cond == "default":
                next_id = rule["next"]; break
        node_id = next_id

def build_final_summary(template: str) -> str:
    # (Using the same logic from your backend to ensure depth)
    a1 = get_dominant("axis1")
    a2 = get_dominant("axis2")
    a3 = get_dominant("axis3")
    
    # Simple mapping for labels
    labels = {
        "axis1": {"internal": "Victor (Internal Locus)", "external": "Victim (External Locus)"},
        "axis2": {"contribution": "Contributing", "entitlement": "Entitled"},
        "axis3": {"altrocentric": "Altrocentric", "self": "Self-Centric"}
    }
    
    text = template.replace("{axis1_label}", labels["axis1"][a1])
    text = text.replace("{axis2_label}", labels["axis2"][a2])
    text = text.replace("{axis3_label}", labels["axis3"][a3])
    text = text.replace("{closing}", "Your path today reveals deep insights into your agency.")
    return text

# ===========================================================================
# 3. UI RENDERING (The "View" Layer)
# ===========================================================================

st.set_page_config(page_title="Reflection Tree", page_icon="🌱")
init_state()

node_id = st.session_state.current_node_id
node = st.session_state.nodes[node_id]
ntype = node["type"]

st.title("🌱 Daily Reflection Tree")
st.caption("A deterministic growth tool | DeepThought Assignment")
st.divider()

if ntype == "start":
    st.markdown(node["text"])
    if st.button("Start", type="primary"):
        st.session_state.current_node_id = resolve_logic(node["next"])
        st.rerun()

elif ntype == "question":
    st.markdown(interpolate(node["text"]))
    options = [opt["label"] for opt in node["options"]]
    choice = st.radio("Choose one:", options, label_visibility="collapsed")
    
    if st.button("Continue", type="primary"):
        st.session_state.answers[node_id] = choice
        # Find signal
        opt = next(o for o in node["options"] if o["label"] == choice)
        tally_signal(opt.get("signal"))
        st.session_state.current_node_id = resolve_logic(opt["next"])
        st.rerun()

elif ntype == "reflection":
    st.info(interpolate(node["text"]))
    tally_signal(node.get("signal"))
    if st.button("Next"):
        st.session_state.current_node_id = resolve_logic(node["next"])
        st.rerun()

elif ntype == "bridge":
    st.markdown(node["text"])
    if st.button("Advance"):
        st.session_state.current_node_id = resolve_logic(node["next"])
        st.rerun()

elif ntype == "summary":
    st.markdown(build_final_summary(node["text"]))
    if st.button("Complete"):
        st.session_state.current_node_id = node["next"]
        st.rerun()

elif ntype == "end":
    st.success(node["text"])
    if st.button("Restart Session"):
        del st.session_state["initialized"]
        st.rerun()