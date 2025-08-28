import csv
import os
from datetime import datetime

def escalate(state):
    """
    Escalate the ticket to a human agent after failed attempts.
    Save escalation info into a CSV log.
    """
    ticket = state["ticket"]
    category = state.get("category", "Unknown")
    attempts = state.get("attempts", 0)
    failed_drafts = state.get("failed_drafts", [])
    reviewer_feedback = state.get("reviewer_feedback", [])

    escalation_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "subject": ticket["subject"],
        "description": ticket["description"],
        "category": category,
        "attempts": attempts,
        "failed_drafts": " || ".join(failed_drafts),
        "feedback": " || ".join(reviewer_feedback),
    }

    # ensure folder exists
    os.makedirs("logs", exist_ok=True)
    file_path = os.path.join("logs", "escalations.csv")

    # write header if file doesn't exist
    file_exists = os.path.exists(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=escalation_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(escalation_data)

    return {"escalated": True, "answer": "This ticket has been escalated to a human support agent."}
