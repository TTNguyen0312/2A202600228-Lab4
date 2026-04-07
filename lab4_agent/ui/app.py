import re
import sys
import os
import json

# ── Path setup: resolve to lab4_agent/ so relative file opens work ──────────
AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AGENT_DIR)
sys.path.insert(0, AGENT_DIR)

import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage
from agent import graph

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TravelBuddy",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* App background */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #1e2230 !important;
        color: #e8eaf0 !important;
    }

    /* Remove default block container padding bleeding */
    [data-testid="block-container"] {
        padding-top: 1.5rem !important;
    }

    /* Column divider */
    [data-testid="stVerticalBlock"] { gap: 0.5rem; }

    /* Chat container background */
    [data-testid="stChatMessageContent"] p { color: #e8eaf0; }

    /* Chat input box */
    [data-testid="stChatInput"] textarea {
        background: #2c3148 !important;
        color: #e8eaf0 !important;
        border: 1px solid #3d4466 !important;
        border-radius: 8px !important;
    }

    /* Section headers */
    h2 { color: #a8b4ff !important; }

    /* Caption */
    .stCaption { color: #7b8298 !important; }

    /* Info box */
    [data-testid="stInfo"] {
        background: #2c3148 !important;
        color: #a8b4ff !important;
        border: 1px solid #3d4466 !important;
    }

    /* Flow cards */
    .flow-card {
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-left: 4px solid;
    }
    .flow-card-title {
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 6px;
    }
    .flow-detail {
        font-family: monospace;
        font-size: 12px;
        background: rgba(0,0,0,0.25);
        color: #d4d8f0;
        border-radius: 4px;
        padding: 5px 8px;
        margin-top: 4px;
        word-break: break-all;
    }

    /* Horizontal rule */
    hr { border-color: #3d4466 !important; }
</style>
""", unsafe_allow_html=True)

# ── Node display config ───────────────────────────────────────────────────────
NODE_CFG = {
    "classifier":         ("🧭", "Classifier",                  "#4d8af0", "#1e2d4a"),
    "trip_planner_node":  ("🗺️", "Trip Planner (gpt-4o-mini)",  "#34a853", "#1a3028"),
    "tour_guide_node":    ("🏔️", "Tour Guide (gpt-4o)",          "#e05252", "#3a1e1e"),
    "trip_tools":         ("🔧", "Trip Tools",                   "#fb8c00", "#3a2a10"),
    "tour_tools":         ("🔧", "Tour Tools",                   "#fb8c00", "#3a2a10"),
    "rejection_node":     ("🚫", "Rejection",                    "#9334e6", "#2a1a3a"),
}

# ── Session state ─────────────────────────────────────────────────────────────
if "messages"   not in st.session_state: st.session_state.messages   = []
if "agent_flow" not in st.session_state: st.session_state.agent_flow = []

# ── Layout ────────────────────────────────────────────────────────────────────
col_chat, col_flow = st.columns([3, 2], gap="large")

# ════════════════════════════════════════════════════════════════════════════
#  CHAT PANEL
# ════════════════════════════════════════════════════════════════════════════
with col_chat:
    st.markdown("## ✈️ TravelBuddy")
    st.caption("Trợ lý du lịch thông minh – hỏi về vé máy bay, khách sạn, lịch trình tham quan")

    chat_area = st.container(height=540, border=False)
    with chat_area:
        for msg in st.session_state.messages:
            avatar = "🧑" if msg["role"] == "user" else "✈️"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    user_input = st.chat_input("Hỏi gì đó về du lịch Việt Nam...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.agent_flow = []

        wrapped     = f"<user_query>{user_input}</user_query>"
        flow_events = []
        final_resp  = ""

        for chunk in graph.stream(
            {"messages": [("human", wrapped)], "intent": ""},
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                event = {"node": node_name, "details": []}

                if node_name == "classifier":
                    intent = state_update.get("intent", "?")
                    event["intent"] = intent
                    event["details"].append(f"intent = {intent}")

                elif "messages" in state_update:
                    for msg in state_update["messages"]:
                        if isinstance(msg, AIMessage):
                            if msg.tool_calls:
                                for tc in msg.tool_calls:
                                    args = json.dumps(tc["args"], ensure_ascii=False)
                                    event["details"].append(f"→ {tc['name']}({args})")
                            elif msg.content:
                                final_resp = msg.content
                                event["details"].append("direct reply ✓")
                        elif isinstance(msg, ToolMessage):
                            preview = msg.content[:140] + "…" if len(msg.content) > 140 else msg.content
                            event["details"].append(f"result: {preview}")

                flow_events.append(event)

        st.session_state.agent_flow = flow_events

        final_resp = re.sub(
            r"<user_query>.*?</user_query>", "", final_resp, flags=re.DOTALL
        ).strip()
        st.session_state.messages.append({"role": "assistant", "content": final_resp})
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
#  AGENT FLOW PANEL
# ════════════════════════════════════════════════════════════════════════════
with col_flow:
    st.markdown("## 🔍 Agent Flow")
    st.caption("Luồng xử lý theo từng node của LangGraph")

    if not st.session_state.agent_flow:
        st.info("Gửi tin nhắn để xem luồng xử lý của agent...")
    else:
        for event in st.session_state.agent_flow:
            node = event["node"]
            icon, label, color, bg = NODE_CFG.get(node, ("⚙️", node, "#666", "#f5f5f5"))

            detail_html = "".join(
                f'<div class="flow-detail">{d}</div>'
                for d in event["details"]
            ) if event["details"] else ""

            st.markdown(f"""
            <div class="flow-card" style="border-color:{color}; background:{bg}">
                <div class="flow-card-title" style="color:{color}">{icon} {label}</div>
                {detail_html}
            </div>
            """, unsafe_allow_html=True)

        # Summary bar
        nodes_hit = [e["node"] for e in st.session_state.agent_flow]
        st.markdown("---")
        st.caption(f"**Nodes executed:** {' → '.join(nodes_hit)}")
