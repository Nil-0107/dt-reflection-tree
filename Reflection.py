#!/usr/bin/env python3
"""
===========================================================================
  DAILY REFLECTION TREE — PROTOTYPE BACKEND
  DeepThought Fellowship Assignment | Part B

  Dataset   :  Custom-authored tree (29 nodes, 3 axes, 0 LLM at runtime)
               Embedded below as TREE_JSON — also saveable as .json file
  Stack     :  Pure Python 3.8+  |  Zero external dependencies
  Run       :  python deterministic_decision_tree.py
  Run (demo):  python deterministic_decision_tree.py --demo victor
               python deterministic_decision_tree.py --demo victim

  Axes encoded in the tree
  ─────────────────────────────────────────────────────────────────────────
  Axis 1  Locus of Control   Victim ↔ Victor        Rotter (1954)
  Axis 2  Orientation        Entitlement ↔ Contribution  Organ (1988)
  Axis 3  Radius of Concern  Self-centric ↔ Altrocentric Maslow (1969)
===========================================================================
"""

import json
import sys
import textwrap
import os
from typing import Optional, Dict, Any

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — DATASET
#  The entire reflection tree as embedded JSON.
#  29 nodes hand-authored; no LLM is called when this tree runs.
#  You can also save TREE_JSON to reflection_tree.json and load it from disk.
# ═══════════════════════════════════════════════════════════════════════════════

# ===========================================================================
# DATASET NOTES & REVISIONS:
# - V1 of this tree used a scoring system (+1/-1), but I realized that 
#   violates the constraint of "no moralizing." Rebuilt it to just tally 
#   the dominant poles (internal vs external) instead.
# - Rewrote A1_Q_LOW: Originally had "I got lucky", but that felt too passive. 
#   Swapped to "Timing and luck were on my side" to make it more realistic.
# - Axis 1 is heavily rooted in the Stoic dichotomy of control. Kept the 
#   language focused on 'agency' rather than 'fault'.
# ===========================================================================
TREE_JSON = r"""
{
  "meta": {
    "version": "1.0.0",
    "description": "Daily Reflection Tree — DT Fellowship prototype",
    "total_nodes": 29,
    "axes": {
      "axis1": {
        "name":   "Locus of Control",
        "poles":  ["internal", "external"],
        "source": "Rotter (1954), Dweck Growth Mindset (2006)"
      },
      "axis2": {
        "name":   "Orientation",
        "poles":  ["contribution", "entitlement"],
        "source": "Organ OCB (1988), Campbell Entitlement Scale (2004)"
      },
      "axis3": {
        "name":   "Radius of Concern",
        "poles":  ["altrocentric", "self"],
        "source": "Maslow Self-Transcendence (1969), Batson (2011)"
      }
    }
  },
  "start": "START",
  "nodes": {

    "START": {
      "id":   "START",
      "type": "start",
      "text": "Good evening.\n\nThis is a 5-minute reflection on your day.\nNo right answers. No grades. Just an honest look at how things went.\n\nTake a breath — let's begin.",
      "next": "A1_OPEN"
    },

    "A1_OPEN": {
      "id":   "A1_OPEN",
      "type": "question",
      "text": "AXIS 1 — HOW YOU HANDLED TODAY\n\nIf today were a weather report, it would be...",
      "options": [
        {"label": "Sunny — things mostly went my way",                           "next": "A1_D1", "signal": "axis1:internal"},
        {"label": "Cloudy — mixed bag, some good some rough",                    "next": "A1_D1", "signal": "axis1:internal"},
        {"label": "Stormy — a lot hit me today",                                 "next": "A1_D1", "signal": "axis1:external"},
        {"label": "Foggy — I couldn't see what was happening or why",            "next": "A1_D1", "signal": "axis1:external"}
      ]
    },

    "A1_D1": {
      "id":   "A1_D1",
      "type": "decision",
      "routing": [
        {"condition": "answer_in", "node": "A1_OPEN",
         "values": ["Sunny — things mostly went my way",
                    "Cloudy — mixed bag, some good some rough"],
         "next": "A1_Q_HIGH"},
        {"condition": "answer_in", "node": "A1_OPEN",
         "values": ["Stormy — a lot hit me today",
                    "Foggy — I couldn't see what was happening or why"],
         "next": "A1_Q_LOW"}
      ]
    },

    "A1_Q_HIGH": {
      "id":   "A1_Q_HIGH",
      "type": "question",
      "text": "You said it felt like \"{A1_OPEN}\".\n\nWhen something went well today, what do you think made it happen?",
      "options": [
        {"label": "I had prepared well for it",                     "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "I adapted in the moment when things shifted",   "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "The right people showed up for me",             "next": "A1_D2", "signal": "axis1:external"},
        {"label": "Timing and luck were on my side",               "next": "A1_D2", "signal": "axis1:external"}
      ]
    },

    "A1_Q_LOW": {
      "id":   "A1_Q_LOW",
      "type": "question",
      "text": "You said it felt like \"{A1_OPEN}\".\n\nWhen things got difficult today, what was your first instinct?",
      "options": [
        {"label": "Figure out what I could still control",         "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "Push through and handle it myself",             "next": "A1_D2", "signal": "axis1:internal"},
        {"label": "Wait and hope things improved on their own",    "next": "A1_D2", "signal": "axis1:external"},
        {"label": "Feel stuck — I wasn't sure what move to make", "next": "A1_D2", "signal": "axis1:external"}
      ]
    },

    "A1_D2": {
      "id":   "A1_D2",
      "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis1", "pole": "internal", "next": "A1_Q2_INT"},
        {"condition": "dominant", "axis": "axis1", "pole": "external", "next": "A1_Q2_EXT"},
        {"condition": "default",                                       "next": "A1_Q2_INT"}
      ]
    },

    "A1_Q2_INT": {
      "id":   "A1_Q2_INT",
      "type": "question",
      "text": "One more on this.\n\nThink of a specific decision you made today — small or large. Looking back at it now, what do you notice?",
      "options": [
        {"label": "I made the best call I could with what I had",                 "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "I could have decided differently — and I see how now",         "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "It didn't really feel like my call to make",                   "next": "A1_D3", "signal": "axis1:external"},
        {"label": "I was mostly reacting to what was happening around me",        "next": "A1_D3", "signal": "axis1:external"}
      ]
    },

    "A1_Q2_EXT": {
      "id":   "A1_Q2_EXT",
      "type": "question",
      "text": "Let me ask it differently.\n\nIf you had just a little more control today, what would you have done?",
      "options": [
        {"label": "Spoken up sooner about something that was bothering me",       "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "Asked for help instead of trying to figure it out alone",       "next": "A1_D3", "signal": "axis1:internal"},
        {"label": "Nothing — the situation was genuinely out of my hands",       "next": "A1_D3", "signal": "axis1:external"},
        {"label": "I'm not sure — it's hard to see what I could have changed",   "next": "A1_D3", "signal": "axis1:external"}
      ]
    },

    "A1_D3": {
      "id":   "A1_D3",
      "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis1", "pole": "internal", "next": "A1_R_INT"},
        {"condition": "dominant", "axis": "axis1", "pole": "external", "next": "A1_R_EXT"},
        {"condition": "default",                                       "next": "A1_R_INT"}
      ]
    },

    "A1_R_INT": {
      "id":   "A1_R_INT",
      "type": "reflection",
      "text": "You see your hand in what happened today.\n\nThat's not the same as saying everything was under your control — it rarely is. It means you stayed in the driver's seat even when the road was rough.\n\nThat's agency. Notice it.",
      "signal": "axis1:internal",
      "next":   "BRIDGE_1_2"
    },

    "A1_R_EXT": {
      "id":   "A1_R_EXT",
      "type": "reflection",
      "text": "When a day is heavy, attention naturally pulls outward — to what others did or didn't do, to circumstances you didn't choose.\n\nFair enough. But somewhere in that day, you made a call. You always do — even if it was just deciding how to hold the weight.\n\nWhat was that call?",
      "signal": "axis1:external",
      "next":   "BRIDGE_1_2"
    },

    "BRIDGE_1_2": {
      "id":   "BRIDGE_1_2",
      "type": "bridge",
      "text": "That's the first lens — how you showed up for yourself.\n\nNow let's turn it outward.\n\n──────────────────────────────────────\nNext: what you gave today.\n──────────────────────────────────────",
      "next": "A2_OPEN"
    },

    "A2_OPEN": {
      "id":   "A2_OPEN",
      "type": "question",
      "text": "AXIS 2 — WHAT YOU GAVE\n\nThink about your interactions today. Which of these moments feels most like yours?",
      "options": [
        {"label": "I helped someone with something that wasn't my responsibility",         "next": "A2_D1", "signal": "axis2:contribution"},
        {"label": "I shared knowledge or explained something that helped someone else",     "next": "A2_D1", "signal": "axis2:contribution"},
        {"label": "I felt my work didn't get the recognition it deserved",                 "next": "A2_D1", "signal": "axis2:entitlement"},
        {"label": "I did what was expected — nothing more, nothing less",                  "next": "A2_D1", "signal": "axis2:entitlement"}
      ]
    },

    "A2_D1": {
      "id":   "A2_D1",
      "type": "decision",
      "routing": [
        {"condition": "answer_in", "node": "A2_OPEN",
         "values": ["I helped someone with something that wasn't my responsibility",
                    "I shared knowledge or explained something that helped someone else"],
         "next": "A2_Q_CONTRIB"},
        {"condition": "answer_in", "node": "A2_OPEN",
         "values": ["I felt my work didn't get the recognition it deserved",
                    "I did what was expected — nothing more, nothing less"],
         "next": "A2_Q_ENTITLE"}
      ]
    },

    "A2_Q_CONTRIB": {
      "id":   "A2_Q_CONTRIB",
      "type": "question",
      "text": "That moment when you gave something — what was going through your mind at the time?",
      "options": [
        {"label": "I wanted to help — it felt like the natural thing to do",       "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I did it because no one else was going to",                     "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I wasn't thinking — I just acted",                              "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "Honestly, I was thinking it would be noticed and appreciated", "next": "A2_D2", "signal": "axis2:entitlement"}
      ]
    },

    "A2_Q_ENTITLE": {
      "id":   "A2_Q_ENTITLE",
      "type": "question",
      "text": "When you felt your effort wasn't fully seen today — how did you respond?",
      "options": [
        {"label": "I let it go and kept focusing on the work",                           "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I found a way to bring it up constructively",                         "next": "A2_D2", "signal": "axis2:contribution"},
        {"label": "I quietly pulled back — why go above and beyond if it isn't noticed?", "next": "A2_D2", "signal": "axis2:entitlement"},
        {"label": "I felt resentful for a while and couldn't shake it",                  "next": "A2_D2", "signal": "axis2:entitlement"}
      ]
    },

    "A2_D2": {
      "id":   "A2_D2",
      "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis2", "pole": "contribution", "next": "A2_R_CONTRIB"},
        {"condition": "dominant", "axis": "axis2", "pole": "entitlement",  "next": "A2_R_ENTITLE"},
        {"condition": "default",                                           "next": "A2_R_CONTRIB"}
      ]
    },

    "A2_R_CONTRIB": {
      "id":   "A2_R_CONTRIB",
      "type": "reflection",
      "text": "You gave something today that wasn't required of you.\n\nOrganizational scientists call this \"citizenship behavior\" — discretionary effort beyond the job description. It's the invisible glue that holds teams together. It doesn't show up in KPIs, but it shapes every culture that actually works.\n\nYou did that today.",
      "signal": "axis2:contribution",
      "next":   "BRIDGE_2_3"
    },

    "A2_R_ENTITLE": {
      "id":   "A2_R_ENTITLE",
      "type": "reflection",
      "text": "Notice the gap between what you expected and what you received today.\n\nThat gap is worth sitting with — not because you're wrong to want recognition, but because the gap itself is information. It tells you what you value, what you might ask for directly, and what you're measuring your contribution against.\n\nWhat are you measuring it against?",
      "signal": "axis2:entitlement",
      "next":   "BRIDGE_2_3"
    },

    "BRIDGE_2_3": {
      "id":   "BRIDGE_2_3",
      "type": "bridge",
      "text": "One more lens to go.\n\nWe've looked at how you handled today and what you gave. Now let's zoom out — past you, past your immediate work — to everyone else today's events touched.\n\n──────────────────────────────────────",
      "next": "A3_OPEN"
    },

    "A3_OPEN": {
      "id":   "A3_OPEN",
      "type": "question",
      "text": "AXIS 3 — WHO ELSE WAS IN YOUR FRAME\n\nWhen you think about today's biggest challenge or moment — who else comes to mind?",
      "options": [
        {"label": "Mostly just me — it was my problem to navigate",                           "next": "A3_D1", "signal": "axis3:self"},
        {"label": "My immediate team — we were all in it together",                           "next": "A3_D1", "signal": "axis3:altrocentric"},
        {"label": "A specific colleague who seemed to have it harder than me",               "next": "A3_D1", "signal": "axis3:altrocentric"},
        {"label": "The people downstream — customers or users depending on our work",        "next": "A3_D1", "signal": "axis3:altrocentric"}
      ]
    },

    "A3_D1": {
      "id":   "A3_D1",
      "type": "decision",
      "routing": [
        {"condition": "answer_in", "node": "A3_OPEN",
         "values": ["Mostly just me — it was my problem to navigate"],
         "next": "A3_Q_SELF"},
        {"condition": "answer_in", "node": "A3_OPEN",
         "values": ["My immediate team — we were all in it together",
                    "A specific colleague who seemed to have it harder than me",
                    "The people downstream — customers or users depending on our work"],
         "next": "A3_Q_ALTRO"}
      ]
    },

    "A3_Q_SELF": {
      "id":   "A3_Q_SELF",
      "type": "question",
      "text": "What do you think today looked like from your team's perspective?",
      "options": [
        {"label": "They probably didn't notice what I was dealing with",                   "next": "A3_D2", "signal": "axis3:self"},
        {"label": "We were all stressed — I probably wasn't the only one struggling",      "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "Honestly, I was too focused on my situation to pay attention to theirs","next": "A3_D2", "signal": "axis3:self"},
        {"label": "Some of them were probably having a harder time than me, actually",    "next": "A3_D2", "signal": "axis3:altrocentric"}
      ]
    },

    "A3_Q_ALTRO": {
      "id":   "A3_Q_ALTRO",
      "type": "question",
      "text": "When you thought about the others today's events were affecting — what did that shift for you?",
      "options": [
        {"label": "It made my own stress feel a little smaller",             "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "It gave me clarity on what actually mattered",             "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "It made me want to do something — even something small",  "next": "A3_D2", "signal": "axis3:altrocentric"},
        {"label": "Not much — I was still caught in my own experience",       "next": "A3_D2", "signal": "axis3:self"}
      ]
    },

    "A3_D2": {
      "id":   "A3_D2",
      "type": "decision",
      "routing": [
        {"condition": "dominant", "axis": "axis3", "pole": "altrocentric", "next": "A3_R_ALTRO"},
        {"condition": "dominant", "axis": "axis3", "pole": "self",         "next": "A3_R_SELF"},
        {"condition": "default",                                           "next": "A3_R_ALTRO"}
      ]
    },

    "A3_R_SELF": {
      "id":   "A3_R_SELF",
      "type": "reflection",
      "text": "There's nothing wrong with being absorbed in your own experience — especially on a hard day.\n\nBut Maslow noticed something in his later work: people who reported the most sustained meaning weren't the ones who had achieved the most for themselves. They were the ones who had oriented toward something beyond themselves.\n\nThat doesn't mean ignoring your needs. It means the frame can be wider — and sometimes that's where relief is hiding.",
      "signal": "axis3:self",
      "next":   "SUMMARY"
    },

    "A3_R_ALTRO": {
      "id":   "A3_R_ALTRO",
      "type": "reflection",
      "text": "You moved beyond your own frame today — even briefly.\n\nMaslow called this self-transcendence: the shift from 'What do I need?' to 'What does this situation need from me?' It's not self-sacrifice. It's the discovery that contributing to something larger than yourself is one of the most reliable sources of meaning humans have ever found.\n\nYou touched that today.",
      "signal": "axis3:altrocentric",
      "next":   "SUMMARY"
    },

    "SUMMARY": {
      "id":   "SUMMARY",
      "type": "summary",
      "text": "YOUR REFLECTION FOR TODAY\n══════════════════════════════════════\n\nAgency        → {axis1_label}\n               {axis1_detail}\n\nContribution  → {axis2_label}\n               {axis2_detail}\n\nRadius        → {axis3_label}\n               {axis3_detail}\n\n──────────────────────────────────────\n{closing}\n──────────────────────────────────────",
      "next": "END"
    },

    "END": {
      "id":   "END",
      "type": "end",
      "text": "That's it for tonight.\n\nSame questions tomorrow — different answers, if today became something useful.\n\nSee you then."
    }

  }
}
"""

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — DISPLAY HELPERS
#  Pure terminal UI — no libraries required.
# ═══════════════════════════════════════════════════════════════════════════════

WIDTH = 62  # tweaked this down from 80. 62 reads more like a book in the terminal.

def clear_screen():
    # Windows cls, otherwise clear.
    os.system("cls" if os.name == "nt" else "clear")

def rule(char="─"):
    print(char * WIDTH)

def wrap_print(text: str, indent: int = 0):
    """Word-wrap and print text at WIDTH, with optional left indent."""
    prefix = " " * indent
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            print()
        else:
            lines = textwrap.wrap(paragraph, width=WIDTH - indent)
            for line in lines:
                print(prefix + line)

def show_node_text(text: str, style: str = "normal"):
    """Render node text with style-specific framing."""
    print()
    if style == "reflection":
        rule("·")
        wrap_print(text)
        rule("·")
    elif style == "bridge":
        print()
        wrap_print(text)
        print()
    elif style == "summary":
        rule("═")
        wrap_print(text)
        rule("═")
    elif style == "end":
        print()
        wrap_print(text)
        print()
        rule()
    else:
        wrap_print(text)
    print()

def press_continue(auto_answer: str = None):
    """Pause for the user to read, then advance."""
    if auto_answer is not None:
        print("  [ Press Enter to continue ]  →  (auto: advancing)")
        return
    try:
        input("  [ Press Enter to continue ]  ")
    except (EOFError, KeyboardInterrupt):
        print()

def ask_options(options: list, auto_answer: str = None) -> dict:
    """
    Show numbered options and return the chosen option dict.
    If auto_answer is set (demo mode), pick the matching option silently.
    """
    for i, opt in enumerate(options, 1):
        wrap_print(f"  {i}. {opt['label']}", indent=0)
    print()

    if auto_answer is not None:
        # Demo mode: match by label substring or number
        for i, opt in enumerate(options, 1):
            if auto_answer == str(i) or auto_answer.lower() in opt["label"].lower():
                print(f"  → (demo) Selected: {opt['label']}")
                return opt
        # fallback: first option
        print(f"  → (demo) Selected: {options[0]['label']}")
        return options[0]

    while True:
        try:
            raw = input("  Your choice (number): ").strip()
            idx = int(raw) - 1
            
            # print(f"DEBUG: raw={raw}, idx={idx}, len={len(options)}") # caught an off-by-one error here earlier
            
            if 0 <= idx < len(options):
                return options[idx]
            print(f"  Please enter a number between 1 and {len(options)}.")
        except (ValueError, EOFError):
            print(f"  Please enter a number between 1 and {len(options)}.")


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — REFLECTION AGENT
#  Deterministic tree-walker. No LLM. No randomness.
#  Same answers → same conversation → same reflection. Every time.
# ═══════════════════════════════════════════════════════════════════════════════

class ReflectionAgent:
    """
    Loads the reflection tree and walks it node by node.

    State machine:
      self.state["answers"]  — maps node_id → chosen label string
      self.state["signals"]  — per-axis pole tallies used for routing decisions
      
    # NOTE: If we scale this beyond CLI, self.state could easily be dumped 
    # to a PostgreSQL DB or a local JSON file to track the user's progress over weeks.
    """

    def __init__(self, tree: dict, demo_script: list = None):
        self.tree        = tree
        self.nodes       = tree["nodes"]
        self.demo_script = demo_script       # list of answer labels for demo mode
        self.demo_index  = 0
        self.state: Dict[str, Any] = {
            "answers": {},
            "signals": {
                "axis1": {"internal": 0,     "external": 0},
                "axis2": {"contribution": 0, "entitlement": 0},
                "axis3": {"altrocentric": 0, "self": 0},
            },
        }

    # ── Public API ────────────────────────────────────────────────────────────

    def run(self):
        current_id = self.tree["start"]
        while current_id:
            node       = self.nodes[current_id]
            current_id = self._process_node(node)

    # ── Node dispatcher ───────────────────────────────────────────────────────

    def _process_node(self, node: dict) -> Optional[str]:
        ntype    = node["type"]
        is_demo  = self.demo_script is not None   # True in demo mode
        # Non-interactive nodes auto-advance in demo mode but do NOT
        # consume a slot from demo_script. Only question nodes consume slots.
        auto_adv = "" if is_demo else None        # sentinel: "auto-advance, no answer needed"

        if ntype == "start":
            clear_screen()
            rule("═")
            show_node_text(node["text"])
            press_continue(auto_adv)
            return node.get("next")

        elif ntype == "question":
            clear_screen()
            show_node_text(self._interpolate(node["text"]))
            # Only question nodes pull from the demo script
            auto_ans = self._next_demo_answer()
            choice   = ask_options(node["options"], auto_ans)
            self.state["answers"][node["id"]] = choice["label"]
            self._tally(choice.get("signal"))
            return choice["next"]

        elif ntype == "decision":
            # Invisible to the employee — pure routing logic
            return self._resolve_decision(node)

        elif ntype == "reflection":
            clear_screen()
            show_node_text(self._interpolate(node["text"]), style="reflection")
            self._tally(node.get("signal"))
            press_continue(auto_adv)
            return node.get("next")

        elif ntype == "bridge":
            clear_screen()
            show_node_text(node["text"], style="bridge")
            press_continue(auto_adv)
            return node.get("next")

        elif ntype == "summary":
            clear_screen()
            summary_text = self._build_summary(node["text"])
            show_node_text(summary_text, style="summary")
            press_continue(auto_adv)
            return node.get("next")

        elif ntype == "end":
            show_node_text(node["text"], style="end")
            return None

        return None

    # ── Decision routing ──────────────────────────────────────────────────────

    def _resolve_decision(self, node: dict) -> str:
        """
        Evaluate routing rules top-to-bottom; return first match.

        Rule types
        ──────────
        answer_in  : checks whether state["answers"][rule.node] is in rule.values
        dominant   : checks which pole leads in an axis
        default    : always matches (catch-all)
        """
        for rule in node["routing"]:
            cond = rule["condition"]

            if cond == "answer_in":
                stored = self.state["answers"].get(rule["node"], "")
                if stored in rule["values"]:
                    return rule["next"]

            elif cond == "dominant":
                if self._dominant(rule["axis"]) == rule["pole"]:
                    return rule["next"]

            elif cond == "default":
                return rule["next"]

        # Should never reach here if tree is well-formed
        raise RuntimeError(f"Decision node '{node['id']}' has no matching rule.")

    # ── Signal / state helpers ────────────────────────────────────────────────

    def _tally(self, signal: Optional[str]):
        """
        Increment the pole counter for signals of the form  'axis:pole'.
        Signals with extra segments (e.g. 'axis1:final:internal') are informational
        and intentionally ignored here — routing already happened.
        """
        if not signal:
            return
        parts = signal.split(":")
        if len(parts) == 2:
            axis, pole = parts
            if axis in self.state["signals"] and pole in self.state["signals"][axis]:
                self.state["signals"][axis][pole] += 1

    def _dominant(self, axis: str) -> str:
        """Return whichever pole has the higher tally; ties go to the first pole."""
        counts = self.state["signals"][axis]
        poles  = list(counts.keys())
        
        # TODO: Originally tried to build a 'tie-breaker' node if counts were equal, 
        # but it made the tree too bloated. For a 5-minute daily reflection, 
        # defaulting to the first pole on a tie keeps the UX smooth.
        return poles[0] if counts[poles[0]] >= counts[poles[1]] else poles[1]

    # ── Text interpolation ────────────────────────────────────────────────────

    def _interpolate(self, text: str) -> str:
        """Replace {NODE_ID} placeholders with the answer given at that node."""
        for node_id, answer in self.state["answers"].items():
            text = text.replace(f"{{{node_id}}}", answer)
        return text

    # ── Summary builder ───────────────────────────────────────────────────────

    def _build_summary(self, template: str) -> str:
        """
        Fill in the SUMMARY node template using accumulated axis signals.
        Produces a personalised, path-specific end-of-session report.
        No LLM — just lookups and string substitution.
        """
        a1 = self._dominant("axis1")
        a2 = self._dominant("axis2")
        a3 = self._dominant("axis3")

        labels = {
            "axis1": {
                "internal": ("Toward ownership",
                             "You stayed in the driver's seat, even on a rough road."),
                "external": ("Toward circumstance",
                             "Today pulled your attention outward. Worth noticing where the choice was hiding."),
            },
            "axis2": {
                "contribution": ("Toward giving",
                                 "You offered something beyond what was asked of you."),
                "entitlement":  ("Toward receiving",
                                 "Your attention tracked what you were getting. That's worth understanding, not judging."),
            },
            "axis3": {
                "altrocentric": ("Toward others",
                                 "Your frame included the people around you — their experience mattered to you."),
                "self":         ("Toward self",
                                 "Your focus stayed close today. Sometimes that's exactly right."),
            },
        }

        a1_label, a1_detail = labels["axis1"][a1]
        a2_label, a2_detail = labels["axis2"][a2]
        a3_label, a3_detail = labels["axis3"][a3]
        closing             = self._closing(a1, a2, a3)

        result = template
        result = result.replace("{axis1_label}",  a1_label)
        result = result.replace("{axis1_detail}",  a1_detail)
        result = result.replace("{axis2_label}",  a2_label)
        result = result.replace("{axis2_detail}",  a2_detail)
        result = result.replace("{axis3_label}",  a3_label)
        result = result.replace("{axis3_detail}",  a3_detail)
        result = result.replace("{closing}",       closing)
        return result

    def _closing(self, a1: str, a2: str, a3: str) -> str:
        """
        8 deterministic closing reflections — one for every combination of
        axis outcomes. Same answers always produce the same closing.
        """
        combos = {
            ("internal", "contribution", "altrocentric"):
                "Three for three — agency, generosity, an outward gaze.\n"
                "Days like this are worth remembering. They're also repeatable.",
            ("internal", "contribution", "self"):
                "You owned your day and gave something real.\n"
                "Tomorrow: try widening the frame just a little — notice someone else's day too.",
            ("internal", "entitlement", "altrocentric"):
                "You see your own agency clearly.\n"
                "What would it look like to extend that energy toward others, without expecting anything back?",
            ("internal", "entitlement", "self"):
                "You stayed in control today. The next frontier:\n"
                "shifting from 'what did I get' to 'what did I give.' Start small tomorrow.",
            ("external", "contribution", "altrocentric"):
                "Even on a day where things felt out of your hands, you gave to others.\n"
                "That takes a particular kind of strength.",
            ("external", "contribution", "self"):
                "You contributed despite the circumstances — give yourself credit for that.\n"
                "Tomorrow: notice whether you have more agency than today felt like.",
            ("external", "entitlement", "altrocentric"):
                "Today was hard, and you still noticed others in the difficulty.\n"
                "That's the thread to pull. Where was your hand in any of it?",
            ("external", "entitlement", "self"):
                "A day that felt beyond your control, focused inward.\n"
                "What's one thing — however small — you could own from today?",
        }
        return combos.get((a1, a2, a3), "Every day is a data point. What does this one tell you?")

    # ── Demo mode helper ──────────────────────────────────────────────────────

    def _next_demo_answer(self) -> Optional[str]:
        if not self.demo_script:
            return None
        if self.demo_index < len(self.demo_script):
            answer = self.demo_script[self.demo_index]
            self.demo_index += 1
            return answer
        return "1"   # fallback: always pick first option


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — DEMO SCRIPTS
#  Two hard-coded persona paths that exercise different tree branches.
#  Each string matches a substring of the option label (case-insensitive).
# ═══════════════════════════════════════════════════════════════════════════════

DEMO_SCRIPTS = {

    # Persona: Victor / Contribution / Altrocentric
    # Path: internal locus → contribution → altrocentric
    "victor": [
        "Cloudy",             # A1_OPEN:  mixed day, leans internal
        "I adapted",          # A1_Q_HIGH: adapted in the moment
        "I made the best",    # A1_Q2_INT: owned the decision
        "I helped someone",   # A2_OPEN:  gave discretionary help
        "I wanted to help",   # A2_Q_CONTRIB: natural giving
        "My immediate team",  # A3_OPEN:  team in frame
        "clarity",            # A3_Q_ALTRO: gave clarity on what mattered
    ],

    # Persona: Victim / Entitlement / Self-centric
    # Path: external locus → entitlement → self
    "victim": [
        "Stormy",                # A1_OPEN:  stormy day, leans external
        "Feel stuck",            # A1_Q_LOW:  felt stuck
        "Nothing — the",         # A1_Q2_EXT: nothing I could change
        "I felt my work",        # A2_OPEN:   recognition wasn't there
        "I felt resentful",      # A2_Q_ENTITLE: resentment
        "Mostly just me",        # A3_OPEN:   only myself in frame
        "too focused on my",     # A3_Q_SELF:  stayed self-focused
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    tree = json.loads(TREE_JSON)

    # ── Parse optional --demo flag ──────────────────────────────────────────
    demo_script = None
    if "--demo" in sys.argv:
        idx = sys.argv.index("--demo")
        if idx + 1 < len(sys.argv):
            persona = sys.argv[idx + 1].lower()
            if persona in DEMO_SCRIPTS:
                demo_script = DEMO_SCRIPTS[persona]
                print(f"\n  ▶  DEMO MODE — persona: '{persona}'\n")
            else:
                print(f"Unknown demo persona '{persona}'. Choose: victor | victim")
                sys.exit(1)

    # ── Run the agent ───────────────────────────────────────────────────────
    agent = ReflectionAgent(tree, demo_script=demo_script)
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n\n  Session interrupted. See you tomorrow.\n")

    # ── Print raw state for inspection (useful for debugging / demo) ─────────
    if demo_script is not None:
        print("\n  ── RAW SESSION STATE (debug) ────────────────────────")
        print(json.dumps(agent.state, indent=4))
        print("  ─────────────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()