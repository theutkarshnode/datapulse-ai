from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import (
    inspector_node,
    coder_node,
    executor_node,
    summarizer_node,
)

def should_retry(state: AgentState) -> str:
    """Agar error aaya hai aur retries 3 se kam hain, toh wapas coder pe bhejo."""
    if state.get("error") and state.get("retries", 0) < 1:
        return "coder"
    return "summarizer"

def build_graph():
    workflow = StateGraph(AgentState)

    # Nodes add karo
    workflow.add_node("inspector", inspector_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("summarizer", summarizer_node)

    # Flow connect karo
    workflow.set_entry_point("inspector")
    workflow.add_edge("inspector", "coder")
    workflow.add_edge("coder", "executor")

    # Self-correcting conditional loop
    workflow.add_conditional_edges(
        "executor",
        should_retry,
        {
            "coder": "coder",
            "summarizer": "summarizer",
        },
    )
    workflow.add_edge("summarizer", END)

    return workflow.compile()

agent_graph = build_graph()
