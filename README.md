# Junior-AI-ZikraInfoTech

----

# 🤖 Support Ticket Resolution Agent with Multi-Step Review Loop 

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-Phi%20Model-red)](https://ollama.com/)

This project implements an **AI-powered Support Ticket Resolution Agent** built with  
**LangGraph** for workflow orchestration and **Retrieval-Augmented Generation (RAG)** for contextual knowledge.  

✨ Key Features:
- Multi-step **review + retry loop** → ensures only policy-compliant, high-quality answers reach the customer.  
- Hybrid LLM setup → works with **Ollama (Phi model)** locally or **OpenAI models** via API.  
- Contextual answers retrieved from a **JSON knowledge base**.  
- Automatic **escalation to human agent** when the AI fails to resolve after retries.  

Designed to work seamlessly with **LangGraph Studio** for debugging and visualization.


## ASCII

```

## ⚙️ How it Works

The Support Agent follows a structured workflow using **LangGraph**:

```text
+---------------+
|    START      |
+-------+-------+
        |
        v
+-------+-------+     User Input (Subject, Description)
|  INPUT Node   |
+-------+-------+
        |
        v
+-------+-------+     Classify ticket (e.g., billing, technical)
| CLASSIFY Node |
+-------+-------+
        |
        v
+-------+-------+     Retrieve context from knowledge base (RAG)
| RETRIEVE Node |
+-------+-------+
        |
        v
+-------+-------+     Draft response using LLM & context
|  DRAFT Node   | <----------------+
+-------+-------+                  |
        |                          |
        v                          |
+-------+-------+     Review drafted response
|  REVIEW Node  |
+-------+-------+
        |
        | Conditional Routing (route_review function)
        |
+-------+-------+--------------------------+
|       |                                  |
v       v                                  v
+-------+-------+  (IF APPROVED)    +-------+-------+ (IF REJECTED & Attempts < 2)
|      END      |                   |  RETRY Node   |
+---------------+                   +-------+-------+
                                            |
                                            | (Prep for next draft)
                                            +------------------------->
                                                    ^
                                                    |
                                                    | (IF REJECTED & Attempts >= 2)
                                                    |
                                            +-------+-------+
                                            | ESCALATE Node |
                                            +-------+-------+
                                                    |
                                                    v
                                            +---------------+
                                            |      END      |
                                            +---------------+

```
----
