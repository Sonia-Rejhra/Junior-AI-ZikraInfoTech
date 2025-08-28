from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.input_node import receive_input
from src.nodes.classify import classify
from src.nodes.retrieve import retrieve_context
from src.nodes.draft import generate_draft
from src.nodes.review import review_draft
from src.nodes.retry import retry_with_feedback
from src.nodes.escalate import escalate


def support_agent():
    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("input", receive_input)
    builder.add_node("classify", classify)
    builder.add_node("retrieve", retrieve_context)
    builder.add_node("draft", generate_draft)
    builder.add_node("review", review_draft)
    builder.add_node("retry", retry_with_feedback)
    builder.add_node("escalate", escalate)

    # Entry point
    builder.set_entry_point("input")

    # Edges
    builder.add_edge("input", "classify")
    builder.add_edge("classify", "retrieve")
    builder.add_edge("retrieve", "draft")
    builder.add_edge("draft", "review")

    # Conditional routing after review
    def route_review(state: AgentState):
        if state.get("review", {}).get("approved", False):
            return END
        elif state.get("attempts", 0) < 2:
            return "retry"
        else:
            return "escalate"

    builder.add_conditional_edges("review", route_review)
    builder.add_edge("retry", "draft")
    builder.add_edge("escalate", END)

    return builder.compile()


if __name__ == "__main__":
    graph = support_agent()
    print("🚀 Support Agent started (type 'exit' to quit)\n")

    while True:
        subject = input("Subject: ")
        if subject.lower() == "exit":
            break
        description = input("Description: ")

        final_state = graph.invoke({
            "ticket": {"subject": subject, "description": description}
        })

        print("\n✅ Final Answer:", final_state.get("answer", final_state.get("draft")))
        print("Category:", final_state.get("category"))
        print("Attempts:", final_state.get("attempts", 0))
        print("Escalated:", final_state.get("escalated", False))
        print("---------------\n")
