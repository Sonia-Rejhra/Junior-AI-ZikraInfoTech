from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.llm import llm

def generate_draft(state):
    context = state.get("context", [])
    ticket = state["ticket"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a support agent. Answer politely and follow company policy."),
        ("user", "Subject: {subject}\nDescription: {description}\n\nRelevant context:\n{context}\n\nNow draft a helpful response:")
    ])

    chain = prompt | llm | StrOutputParser()

    draft = chain.invoke({
        "subject": ticket["subject"],
        "description": ticket["description"],
        "context": "\n".join(context)
    })

    print("\n✍️ Draft Generated:", draft)
    return {"draft": draft}
