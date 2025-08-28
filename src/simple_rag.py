import json, os

with open(os.path.join("data", "knowledge_base.json"), "r", encoding="utf-8") as f:
    KB = json.load(f)

def retrieve(category: str, query: str) -> list[str]:
    """
    Simple keyword-based retrieval from KB.
    """
    docs = KB.get(category, [])
    if not docs:
        return []
    tokens = {w.lower() for w in query.split() if len(w) > 2}
    scored = [(sum(1 for t in tokens if t in d.lower()), d) for d in docs]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:3]]
