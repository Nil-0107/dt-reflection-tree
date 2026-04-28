from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json

app = FastAPI(title="Reflection Tree API")

# ===========================================================================
# 1. DATASET
# ===========================================================================
TREE_JSON = r"""
{
  "start": "START",
  "nodes": {
    "START": {
      "id": "START", "type": "start",
      "text": "## Good evening.\n\nThis is a 5-minute reflection on your day.\nNo right answers. No grades. Just an honest look at how things went.\n\nTake a breath — let's begin.",
      "next": "A1_OPEN"
    },
    "A1_OPEN": {
      "id": "A1_OPEN", "type": "question",
      "text": "### AXIS 1 — HOW YOU HANDLED TODAY\n\nIf today were a weather report, it would be...",
      "options": [
        {"label": "Sunny — things mostly went my way", "next": "A1_D1", "signal": "axis1:internal"},
        {"label": "Cloudy — mixed bag, some good some rough", "next": "A1_D1", "signal": "axis1:internal"},
        {"label": "Stormy — a lot hit me today", "next": "A1_D1", "signal": "axis1:external"},
        {"label": "Foggy — I couldn't see what was happening or why", "next": "A1_D1", "signal": "axis1:external"}
      ]
    },
    "A1_D1": {
      "id": "A1_D1", "type": "decision",
      "routing": [
        {"condition": "answer_in", "node": "A1_OPEN", "values": ["Sunny — things mostly went my way", "Cloudy — mixed bag, some good some rough"], "next": "A1_Q_HIGH"},
        {"condition": "answer_in", "node": "A1_OPEN", "values": ["Stormy — a lot hit me today", "Foggy — I couldn't see what was happening or why"], "next": "A1_Q_LOW"}
      ]
    },
    "A1_Q_HIGH": {
      "id": "A1_Q_HIGH", "type": "question",
      "text": "You said it felt like **\"{A1_OPEN}\"**.\n\nWhen something went well today, what do you think made it happen?",
      "options": [
        {"label": "I had prepared well for it", "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "I adapted in the moment when things shifted", "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "The right people showed up for me", "next": "A1_D2", "signal": "axis1:external"},
        {"label": "Timing and luck were on my side", "next": "A1_D2", "signal": "axis1:external"}
      ]
    },
    "A1_Q_LOW": {
      "id": "A1_Q_LOW", "type": "question",
      "text": "You said it felt like **\"{A1_OPEN}\"**.\n\nWhen things got difficult today, what was your first instinct?",
      "options": [
        {"label": "Figure out what I could still control", "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "Push through and handle it myself", "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "Wait and hope things improved on their own", "next": "A1_D2", "signal": "axis1:external"},
        {"label": "Feel stuck — I wasn't sure what move to make", "next": "A1_D2", "signal": "axis1:external"}
      ]
    },
    "A1_D2": {
      "id": "A1_D2", "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis1", "pole": "internal", "next": "A1_Q2_INT"},
        {"condition": "dominant", "axis": "axis1", "pole": "external", "next": "A1_Q2_EXT"},
        {"condition": "default", "next": "A1_Q2_INT"}
      ]
    },
    "A1_Q2_INT": {
      "id": "A1_Q2_INT", "type": "question",
      "text": "One more on this.\n\nThink of a specific decision you made today — small or large. Looking back at it now, what do you notice?",
      "options": [
        {"label": "I made the best call I could with what I had", "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "I could have decided differently — and I see how now", "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "It didn't really feel like my call to make", "next": "A1_D3", "signal": "axis1:external"},
        {"label": "I was mostly reacting to what was happening around me", "next": "A1_D3", "signal": "axis1:external"}
      ]
    },
    "A1_Q2_EXT": {
      "id": "A1_Q2_EXT", "type": "question",
      "text": "Let me ask it differently.\n\nIf you had just a little more control today, what would you have done?",
      "options": [
        {"label": "Spoken up sooner about something that was bothering me", "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "Asked for help instead of trying to figure it out alone", "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "Nothing — the situation was genuinely out of my hands", "next": "A1_D3", "signal": "axis1:external"},
        {"label": "I'm not sure — it's hard to see what I could have changed", "next": "A1_D3", "signal": "axis1:external"}
      ]
    },
    "A1_D3": {
      "id": "A1_D3", "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis1", "pole": "internal", "next": "A1_R_INT"},
        {"condition": "dominant", "axis": "axis1", "pole": "external", "next": "A1_R_EXT"},
        {"condition": "default", "next": "A1_R_INT"}
      ]
    },
    "A1_R_INT": {
      "id": "A1_R_INT", "type": "reflection",
      "text": "You see your hand in what happened today.\n\nThat's not the same as saying everything was under your control — it rarely is. It means you stayed in the driver's seat even when the road was rough.\n\nThat's agency. Notice it.",
      "signal": "axis1:internal", "next": "BRIDGE_1_2"
    },
    "A1_R_EXT": {
      "id": "A1_R_EXT", "type": "reflection",
      "text": "When a day is heavy, attention naturally pulls outward — to what others did or didn't do, to circumstances you didn't choose.\n\nFair enough. But somewhere in that day, you made a call. You always do — even if it was just deciding how to hold the weight.\n\nWhat was that call?",
      "signal": "axis1:external", "next": "BRIDGE_1_2"
    },
    "BRIDGE_1_2": {
      "id": "BRIDGE_1_2", "type": "bridge",
      "text": "That's the first lens — how you showed up for yourself.\n\nNow let's turn it outward.\n\n---\n**Next: what you gave today.**\n---",
      "next": "A2_OPEN"
    },
    "A2_OPEN": {
      "id": "A2_OPEN", "type": "question",
      "text": "### AXIS 2 — WHAT YOU GAVE\n\nThink about your interactions today. Which of these moments feels most like yours?",
      "options": [
        {"label": "I helped someone with something that wasn't my responsibility", "next": "A2_D1", "signal": "axis2:contribution"},
        {"label": "I shared knowledge or explained something that helped someone else", "next": "A2_D1", "signal": "axis2:contribution"},
        {"label": "I felt my work didn't get the recognition it deserved", "next": "A2_D1", "signal": "axis2:entitlement"},
        {"label": "I did what was expected — nothing more, nothing less", "next": "A2_D1", "signal": "axis2:entitlement"}
      ]
    },
    "A2_D1": {
      "id": "A2_D1", "type": "decision",
      "routing": [
        {"condition": "answer_in", "node": "A2_OPEN", "values": ["I helped someone with something that wasn't my responsibility", "I shared knowledge or explained something that helped someone else"], "next": "A2_Q_CONTRIB"},
        {"condition": "answer_in", "node": "A2_OPEN", "values": ["I felt my work didn't get the recognition it deserved", "I did what was expected — nothing more, nothing less"], "next": "A2_Q_ENTITLE"}
      ]
    },
    "A2_Q_CONTRIB": {
      "id": "A2_Q_CONTRIB", "type": "question",
      "text": "That moment when you gave something — what was going through your mind at the time?",
      "options": [
        {"label": "I wanted to help — it felt like the natural thing to do", "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I did it because no one else was going to", "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I wasn't thinking — I just acted", "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "Honestly, I was thinking it would be noticed and appreciated", "next": "A2_D2", "signal": "axis2:entitlement"}
      ]
    },
    "A2_Q_ENTITLE": {
      "id": "A2_Q_ENTITLE", "type": "question",
      "text": "When you felt your effort wasn't fully seen today — how did you respond?",
      "options": [
        {"label": "I let it go and kept focusing on the work", "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I found a way to bring it up constructively", "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I quietly pulled back — why go above and beyond if it isn't noticed?", "next": "A2_D2", "signal": "axis2:entitlement"},
        {"label": "I felt resentful for a while and couldn't shake it", "next": "A2_D2", "signal": "axis2:entitlement"}
      ]
    },
    "A2_D2": {
      "id": "A2_D2", "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis2", "pole": "contribution", "next": "A2_R_CONTRIB"},
        {"condition": "dominant", "axis": "axis2", "pole": "entitlement", "next": "A2_R_ENTITLE"},
        {"condition": "default", "next": "A2_R_CONTRIB"}
      ]
    },
    "A2_R_CONTRIB": {
      "id": "A2_R_CONTRIB", "type": "reflection",
      "text": "You gave something today that wasn't required of you.\n\nOrganizational scientists call this \"citizenship behavior\" — discretionary effort beyond the job description. It's the invisible glue that holds teams together. It doesn't show up in KPIs, but it shapes every culture that actually works.\n\nYou did that today.",
      "signal": "axis2:contribution", "next": "BRIDGE_2_3"
    },
    "A2_R_ENTITLE": {
      "id": "A2_R_ENTITLE", "type": "reflection",
      "text": "Notice the gap between what you expected and what you received today.\n\nThat gap is worth sitting with — not because you're wrong to want recognition, but because the gap itself is information. It tells you what you value, what you might ask for directly, and what you're measuring your contribution against.\n\nWhat are you measuring it against?",
      "signal": "axis2:entitlement", "next": "BRIDGE_2_3"
    },
    "BRIDGE_2_3": {
      "id": "BRIDGE_2_3", "type": "bridge",
      "text": "One more lens to go.\n\nWe've looked at how you handled today and what you gave. Now let's zoom out — past you, past your immediate work — to everyone else today's events touched.\n\n---",
      "next": "A3_OPEN"
    },
    "A3_OPEN": {
      "id": "A3_OPEN", "type": "question",
      "text": "### AXIS 3 — WHO ELSE WAS IN YOUR FRAME\n\nWhen you think about today's biggest challenge or moment — who else comes to mind?",
      "options": [
        {"label": "Mostly just me — it was my problem to navigate", "next": "A3_D1", "signal": "axis3:self"},
        {"label": "My immediate team — we were all in it together", "next": "A3_D1", "signal": "axis3:altrocentric"},
        {"label": "A specific colleague who seemed to have it harder than me", "next": "A3_D1", "signal": "axis3:altrocentric"},
        {"label": "The people downstream — customers or users depending on our work", "next": "A3_D1", "signal": "axis3:altrocentric"}
      ]
    },
    "A3_D1": {
      "id": "A3_D1", "type": "decision",
      "routing": [
        {"condition": "answer_in", "node": "A3_OPEN", "values": ["Mostly just me — it was my problem to navigate"], "next": "A3_Q_SELF"},
        {"condition": "answer_in", "node": "A3_OPEN", "values": ["My immediate team — we were all in it together", "A specific colleague who seemed to have it harder than me", "The people downstream — customers or users depending on our work"], "next": "A3_Q_ALTRO"}
      ]
    },
    "A3_Q_SELF": {
      "id": "A3_Q_SELF", "type": "question",
      "text": "What do you think today looked like from your team's perspective?",
      "options": [
        {"label": "They probably didn't notice what I was dealing with", "next": "A3_D2", "signal": "axis3:self"},
        {"label": "We were all stressed — I probably wasn't the only one struggling", "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "Honestly, I was too focused on my situation to pay attention to theirs", "next": "A3_D2", "signal": "axis3:self"},
        {"label": "Some of them were probably having a harder time than me, actually", "next": "A3_D2", "signal": "axis3:altrocentric"}
      ]
    },
    "A3_Q_ALTRO": {
      "id": "A3_Q_ALTRO", "type": "question",
      "text": "When you thought about the others today's events were affecting — what did that shift for you?",
      "options": [
        {"label": "It made my own stress feel a little smaller", "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "It gave me clarity on what actually mattered", "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "It made me want to do something — even something small", "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "Not much — I was still caught in my own experience", "next": "A3_D2", "signal": "axis3:self"}
      ]
    },
    "A3_D2": {
      "id": "A3_D2", "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis3", "pole": "altrocentric", "next": "A3_R_ALTRO"},
        {"condition": "dominant", "axis": "axis3", "pole": "self", "next": "A3_R_SELF"},
        {"condition": "default", "next": "A3_R_ALTRO"}
      ]
    },
    "A3_R_SELF": {
      "id": "A3_R_SELF", "type": "reflection",
      "text": "> There's nothing wrong with being absorbed in your own experience — especially on a hard day.\n>\n> But Maslow noticed something in his later work: people who reported the most sustained meaning weren't the ones who had achieved the most for themselves. They were the ones who had oriented toward something beyond themselves.\n>\n> That doesn't mean ignoring your needs. It means the frame can be wider — and sometimes that's where relief is hiding.",
      "signal": "axis3:self", "next": "SUMMARY"
    },
    "A3_R_ALTRO": {
      "id": "A3_R_ALTRO", "type": "reflection",
      "text": "> You moved beyond your own frame today — even briefly.\n>\n> Maslow called this self-transcendence: the shift from 'What do I need?' to 'What does this situation need from me?' It's not self-sacrifice. It's the discovery that contributing to something larger than yourself is one of the most reliable sources of meaning humans have ever found.\n>\n> You touched that today.",
      "signal": "axis3:altrocentric", "next": "SUMMARY"
    },
    "SUMMARY": {
      "id": "SUMMARY", "type": "summary",
      "text": "### YOUR REFLECTION FOR TODAY\n---\n\n**Agency** → {axis1_label}  \n*{axis1_detail}*\n\n**Contribution** → {axis2_label}  \n*{axis2_detail}*\n\n**Radius** → {axis3_label}  \n*{axis3_detail}*\n\n---\n**{closing}**\n---",
      "next": "END"
    },
    "END": {
      "id": "END", "type": "end",
      "text": "### That's it for tonight.\n\nSame questions tomorrow — different answers, if today became something useful.\n\nSee you then."
    }
  }
}
"""
TREE_DATA = json.loads(TREE_JSON)
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
    counts = state.signals[axis]
    poles = list(counts.keys())
    return poles[0] if counts[poles[0]] >= counts[poles[1]] else poles[1]

def tally_signal(state: AppState, signal: str):
    if not signal:
        return
    parts = signal.split(":")
    if len(parts) == 2:
        axis, pole = parts
        if axis in state.signals and pole in state.signals[axis]:
            state.signals[axis][pole] += 1

def interpolate_text(text: str, state: AppState) -> str:
    for node_id, answer in state.answers.items():
        text = text.replace(f"{{{node_id}}}", answer)
    return text

def resolve_decision(node: dict, state: AppState) -> str:
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
    a1 = get_dominant(state, "axis1")
    a2 = get_dominant(state, "axis2")
    a3 = get_dominant(state, "axis3")

    labels = {
        "axis1": {
            "internal": ("Toward ownership", "You stayed in the driver's seat, even on a rough road."),
            "external": ("Toward circumstance", "Today pulled your attention outward. Worth noticing where the choice was hiding."),
        },
        "axis2": {
            "contribution": ("Toward giving", "You offered something beyond what was asked of you."),
            "entitlement":  ("Toward receiving", "Your attention tracked what you were getting. That's worth understanding, not judging."),
        },
        "axis3": {
            "altrocentric": ("Toward others", "Your frame included the people around you — their experience mattered to you."),
            "self":         ("Toward self", "Your focus stayed close today. Sometimes that's exactly right."),
        },
    }

    a1_label, a1_detail = labels["axis1"][a1]
    a2_label, a2_detail = labels["axis2"][a2]
    a3_label, a3_detail = labels["axis3"][a3]
    
    combos = {
        ("internal", "contribution", "altrocentric"): "Three for three — agency, generosity, an outward gaze.\nDays like this are worth remembering.",
        ("internal", "contribution", "self"): "You owned your day and gave something real.\nTomorrow: try widening the frame just a little.",
        ("internal", "entitlement", "altrocentric"): "You see your own agency clearly.\nWhat would it look like to extend that energy toward others?",
        ("internal", "entitlement", "self"): "You stayed in control today. The next frontier:\nshifting from 'what did I get' to 'what did I give.'",
        ("external", "contribution", "altrocentric"): "Even on a day where things felt out of your hands, you gave to others.\nThat takes strength.",
        ("external", "contribution", "self"): "You contributed despite the circumstances — give yourself credit.\nTomorrow: notice your agency.",
        ("external", "entitlement", "altrocentric"): "Today was hard, and you still noticed others in the difficulty.\nWhere was your hand in any of it?",
        ("external", "entitlement", "self"): "A day that felt beyond your control, focused inward.\nWhat's one thing you could own from today?",
    }
    closing = combos.get((a1, a2, a3), "Every day is a data point. What does this one tell you?")

    result = template
    result = result.replace("{axis1_label}", a1_label).replace("{axis1_detail}", a1_detail)
    result = result.replace("{axis2_label}", a2_label).replace("{axis2_detail}", a2_detail)
    result = result.replace("{axis3_label}", a3_label).replace("{axis3_detail}", a3_detail)
    result = result.replace("{closing}", closing)
    return result

def get_next_visible_node(node_id: str, state: AppState) -> dict:
    """Recursively process decision nodes until a visible node is hit."""
    while True:
        if not node_id:
            return None
        node = NODES[node_id].copy()
        
        # If it's a decision node, resolve it invisibly and loop again
        if node["type"] == "decision":
            node_id = resolve_decision(node, state)
            continue
            
        # Format text dynamically before sending to frontend
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
    """Returns a clean state and the starting node."""
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
    """Processes user choice, updates state, and returns next visible node."""
    current_node = NODES[req.current_node_id]
    
    # Update state based on user action
    if current_node["type"] == "question" and req.choice_label:
        req.state.answers[req.current_node_id] = req.choice_label
        
        # Find the chosen option to get the signal and next node
        chosen_opt = next((o for o in current_node["options"] if o["label"] == req.choice_label), None)
        if not chosen_opt:
            raise HTTPException(status_code=400, detail="Invalid choice label")
            
        tally_signal(req.state, chosen_opt.get("signal"))
        next_id = chosen_opt["next"]
        
    elif current_node["type"] == "reflection":
        tally_signal(req.state, current_node.get("signal"))
        next_id = current_node.get("next")
        
    else:
        # Start, Bridge, Summary
        next_id = current_node.get("next")

    # Find the next actual UI node to render
    next_node = get_next_visible_node(next_id, req.state)
    return ActionResponse(node=next_node, state=req.state)