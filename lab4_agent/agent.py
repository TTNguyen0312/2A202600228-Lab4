# --- BẮT ĐẦU CODE agent.py ---

import re
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from tools import search_flights, search_hotels, calculate_budget, get_attractions
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompts
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open("system_prompt_tour_guide.txt", "r", encoding="utf-8") as f:
    TOUR_GUIDE_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str   # "trip_planner" | "tour_guide" | "off_topic"

# 3. Khởi tạo LLM
# Classifer (Bind no tools, chỉ trả lời intent)
llm_classifier = ChatOpenAI(model="gpt-4o-mini")

# Trip planner dùng gpt-4o-mini – đủ cho tìm kiếm và tính toán
llm_trip = ChatOpenAI(model="gpt-4o-mini").bind_tools(
    [search_flights, search_hotels, calculate_budget]
)
# Tour guide dùng gpt-4o – cần lập lịch trình sáng tạo, chi tiết, mạch lạc
llm_tour = ChatOpenAI(model="gpt-4o", temperature=0.7).bind_tools([get_attractions])

# Helpers
def prepend_system(messages: list, prompt: str) -> list:
    if not isinstance(messages[0], SystemMessage):
        return [SystemMessage(content=prompt)] + messages
    return [SystemMessage(content=prompt)] + messages[1:]

def log_response(node_name: str, response: AIMessage):
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  [{node_name}] tool call → {tc['name']}({tc['args']})")
    else:
        print(f"  [{node_name}] direct reply")

#  Classifier (Routing) node
CLASSIFIER_PROMPT = """Phân loại yêu cầu của người dùng thành MỘT trong các nhãn sau:
- trip_planner : tìm vé máy bay, khách sạn, hoặc lập kế hoạch chuyến đi có ngân sách
- tour_guide   : muốn có lịch trình tham quan theo ngày (ngày 1 đi đâu, ngày 2 làm gì, ...), hoặc hỏi gợi ý về nơi du lịch, hoặc hỏi về một địa điểm du lịch
- off_topic    : không liên quan đến du lịch

Chỉ trả về đúng một nhãn, không giải thích."""

def classifier_node(state: AgentState) -> dict:
    last_user = next(
        (m for m in reversed(state["messages"]) if getattr(m, "type", None) == "human"),
        state["messages"][-1],
    )
    result = llm_classifier.invoke([
        SystemMessage(content=CLASSIFIER_PROMPT),
        last_user,
    ])
    intent = result.content.strip().lower()
    if intent not in ("trip_planner", "tour_guide", "off_topic"):
        intent = "off_topic"
    print(f"  [classifier] intent = {intent}")
    return {"intent": intent}

# Specialist nodes 

def trip_planner_node(state: AgentState) -> dict:
    response = llm_trip.invoke(prepend_system(state["messages"], SYSTEM_PROMPT))
    log_response("trip_planner", response)
    return {"messages": [response]}

def tour_guide_node(state: AgentState) -> dict:
    response = llm_tour.invoke(prepend_system(state["messages"], TOUR_GUIDE_PROMPT))
    log_response("tour_guide", response)
    return {"messages": [response]}

def rejection_node(_state: AgentState) -> dict:
    return {"messages": [AIMessage(
        content="Mình chỉ có thể hỗ trợ về du lịch thôi bạn nhé! "
                "Bạn muốn tìm vé/khách sạn hay lên lịch trình tham quan?"
    )]}

#  Router 

def route_by_intent(state: AgentState) -> str:
    return {
        "trip_planner": "trip_planner_node",
        "tour_guide":   "tour_guide_node",
        "off_topic":    "rejection_node",
    }.get(state.get("intent", "off_topic"), "rejection_node")

# Graph Builder

builder = StateGraph(AgentState)

builder.add_node("classifier",       classifier_node)
builder.add_node("trip_planner_node", trip_planner_node)
builder.add_node("tour_guide_node",   tour_guide_node)
builder.add_node("rejection_node",    rejection_node)

builder.add_node("trip_tools", ToolNode([search_flights, search_hotels, calculate_budget]))
builder.add_node("tour_tools", ToolNode([get_attractions]))

# Routing
builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier", route_by_intent, {
    "trip_planner_node": "trip_planner_node",
    "tour_guide_node":   "tour_guide_node",
    "rejection_node":    "rejection_node",
})

# Tool loops
builder.add_conditional_edges("trip_planner_node", tools_condition, {"tools": "trip_tools", END: END})
builder.add_conditional_edges("tour_guide_node",   tools_condition, {"tools": "tour_tools", END: END})
builder.add_edge("trip_tools", "trip_planner_node")
builder.add_edge("tour_tools", "tour_guide_node")

builder.add_edge("rejection_node", END)

graph = builder.compile()

# Chat loop 

if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy – Trợ Lý Du lịch Thông minh")
    print("  Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        wrapped = f"<user_query>{user_input}</user_query>"
        result = graph.invoke({
            "messages":  [("human", wrapped)],
            "intent":    "",
        })
        final = result["messages"][-1]
        # Strip <user_query> tags if the model accidentally echoes them back
        content = re.sub(r"<user_query>.*?</user_query>", "", final.content, flags=re.DOTALL).strip()
        print(f"\nTravelBuddy: {content}")
