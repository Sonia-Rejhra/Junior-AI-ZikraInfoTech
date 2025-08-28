from typing import TypedDict, List, Optional

class AgentState(TypedDict, total=False):
    # input ticket
    ticket: dict              # { "subject": str, "description": str }

    # classification
    category: str

    # retrieval
    context: List[str]

    # draft & review
    draft: str
    review: dict              # { "approved": bool, "feedback": str }

    # retry tracking
    attempts: int
    failed_drafts: List[str]
    reviewer_feedback: List[str]

    # escalation
    escalated: bool
    answer: str               # final response (either approved draft or escalation msg)
