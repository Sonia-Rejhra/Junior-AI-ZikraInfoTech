from src.llm import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Categories
CATEGORIES = ["Billing", "Technical", "Security", "General"]

# Keyword dictionaries
SECURITY_KEYWORDS = ["login", "suspicious", "breach", "hacked", "unauthorized", "2fa", "phishing"]
BILLING_KEYWORDS = ["refund", "payment", "invoice", "charge", "billed", "billing", "subscription"]
TECHNICAL_KEYWORDS = ["error", "crash", "bug", "reset", "server", "loading", "failure", "install", "update"]
GENERAL_KEYWORDS = ["hours", "time", "available", "support hours", "working hours",
                    "schedule", "location", "chat availability", "general info", "holiday"]

def classify(state):
    ticket = state["ticket"]
    text = (ticket["subject"] + " " + ticket["description"]).lower()

    # 1) Heuristic override (priority order)
    if any(word in text for word in SECURITY_KEYWORDS):
        category = "Security"
        print(f"\n🗂 Classified as (keyword override): {category}")
        return {"category": category}

    if any(word in text for word in BILLING_KEYWORDS):
        category = "Billing"
        print(f"\n🗂 Classified as (keyword override): {category}")
        return {"category": category}

    if any(word in text for word in TECHNICAL_KEYWORDS):
        category = "Technical"
        print(f"\n🗂 Classified as (keyword override): {category}")
        return {"category": category}

    if any(word in text for word in GENERAL_KEYWORDS):
        category = "General"
        print(f"\n🗂 Classified as (keyword override): {category}")
        return {"category": category}

    # 2) Fallback → LLM classifier
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a classifier. "
         "Read the ticket and respond with ONLY ONE word: Billing, Technical, Security, or General. "
         "No explanations, no extra text, only the category. "
         "⚠️ If the query is about hours, availability, schedule, or general company info, always return 'General'."),
        ("user", f"Subject: {ticket['subject']}\nDescription: {ticket['description']}")
    ])
    chain = prompt | llm | StrOutputParser()
    raw_category = chain.invoke({}).strip().capitalize()

    if raw_category not in CATEGORIES:
        category = "General"  # fallback default
    else:
        category = raw_category

    print(f"\n🗂 Classified as (LLM): {category}")
    return {"category": category}
