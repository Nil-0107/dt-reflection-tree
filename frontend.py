import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="DT Daily Reflection", layout="centered")

# --- Initialize or Restart Session ---
if "node" not in st.session_state:
    response = requests.get(f"{API_URL}/init").json()
    st.session_state.node = response["node"]
    st.session_state.app_state = response["state"]

def submit_action(choice_label=None):
    payload = {
        "current_node_id": st.session_state.node["id"],
        "choice_label": choice_label,
        "state": st.session_state.app_state
    }
    res = requests.post(f"{API_URL}/submit", json=payload).json()
    st.session_state.node = res["node"]
    st.session_state.app_state = res["state"]

# --- UI Render Logic ---
node = st.session_state.node

if not node:
    st.stop()

st.title("🌱 Daily Reflection Tree")
st.divider()

ntype = node["type"]

if ntype == "start":
    st.markdown(node["text"])
    if st.button("Begin Reflection", type="primary"):
        submit_action()

elif ntype == "question":
    st.markdown(node["text"])
    options = [opt["label"] for opt in node["options"]]
    choice = st.radio("Select an option:", options, label_visibility="collapsed")
    st.write("")
    if st.button("Continue", type="primary"):
        submit_action(choice_label=choice)

elif ntype == "reflection":
    st.info(node["text"])
    if st.button("Next", type="primary"):
        submit_action()

elif ntype == "bridge":
    st.markdown(node["text"])
    if st.button("Next Lens", type="primary"):
        submit_action()

elif ntype == "summary":
    st.markdown(node["text"])
    if st.button("Finish", type="primary"):
        submit_action()

elif ntype == "end":
    st.success(node["text"])
    if st.button("Restart Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()