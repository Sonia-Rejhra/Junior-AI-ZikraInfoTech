def retry_with_feedback(state):
    # Increment attempts
    attempts = state.get("attempts", 0) + 1

    failed_drafts = state.get("failed_drafts", [])
    failed_drafts.append(state.get("draft", ""))

    reviewer_feedback = state.get("reviewer_feedback", [])
    reviewer_feedback.append(state["review"]["feedback"])

    print(f"\n♻️ Retry attempt {attempts} with feedback: {state['review']['feedback']}")

    return {
        "attempts": attempts,
        "failed_drafts": failed_drafts,
        "reviewer_feedback": reviewer_feedback
    }
