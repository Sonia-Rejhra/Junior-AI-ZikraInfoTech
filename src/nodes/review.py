from src.llm import reviewer_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def review_draft(state):
    draft = state["draft"]

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a strict QA reviewer for Zikra Infotech. "
         "Check if the draft:\n"
         "- Does NOT ask for sensitive info (passwords, codes)\n"
         "- Is polite, professional, concise\n"
         "- Uses provided context if relevant\n"
         "- Gives clear next steps\n\n"
         "Respond with:\n"
         "- 'Approved' if okay\n"
         "- 'Rejected - <short reason>' if not okay"),
        ("user", f"Draft to review:\n{draft}")
    ])

    chain = prompt | reviewer_llm | StrOutputParser()
    result = chain.invoke({})

    print("\n🔍 Review Result:", result)

    if "Approved" in result:
        return {"review": {"approved": True, "feedback": "Approved"}}
    else:
        return {"review": {"approved": False, "feedback": result}}
