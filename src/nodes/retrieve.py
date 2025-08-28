import os, json
from src.simple_rag import retrieve

def retrieve_context(state):
    """
    Retrieve relevant documents for the classified ticket.
    Uses simple RAG from knowledge_base.json
    """
    ticket = state["ticket"]
    category = state["category"]

    query = f"{ticket['subject']} {ticket['description']}"
    docs = retrieve(category, query)

    # Agar kuch nahi mila, fallback default docs
    if not docs:
        kb_path = os.path.join("data", "knowledge_base.json")
        with open(kb_path, "r", encoding="utf-8") as f:
            KB = json.load(f)

        docs = KB.get(category, [])[:2]  # fallback to first 2 docs

    print(f"\n📚 Retrieved {len(docs)} docs for category {category}")
    return {"context": docs}
