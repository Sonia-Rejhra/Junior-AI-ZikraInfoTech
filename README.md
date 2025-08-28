-----
# 🤖 Support Ticket Agent using RAG and LangGraph
This project implements an intelligent AI-powered Support Ticket Agent...



[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)](https://langchain-ai.github.io/langgraph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-Phi%20Model-red)](https://ollama.com/)

This project implements an **AI-powered Support Ticket Resolution Agent** built with  
**LangGraph** for workflow orchestration and **Retrieval-Augmented Generation (RAG)** for contextual knowledge.  

-----

✨ Key Features:
- Multi-step **review + retry loop** → ensures only policy-compliant, high-quality answers reach the customer.  
- Hybrid LLM setup → works with **Ollama (Phi model)** locally or **OpenAI models** via API.  
- Contextual answers retrieved from a **JSON knowledge base**.  
- Automatic **escalation to human agent** when the AI fails to resolve after retries.  

Designed to work seamlessly with **LangGraph Studio** for debugging and visualization.



## 🧩 Workflow Diagram

```

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
                                            +------------------->
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
## LangGraph Studio Workflow

<img width="307" height="263" alt="image" src="https://github.com/user-attachments/assets/c00ccc45-d0aa-49c0-a836-1f1fdd825d7d" />

**Simplified Flow:**

```
flowchart TD
    A[START] --> B[INPUT: User provides subject + description]
    B --> C[CLASSIFY: Determine ticket category]
    C --> D[RETRIEVE: Fetch knowledge base context]
    D --> E[DRAFT: Generate response]
    E --> F[REVIEW: Check draft quality]

    F -->|Approved ✅| G[END]
    F -->|Rejected ❌ & Attempts < 2| H[RETRY: Feedback sent to Draft]
    H --> E

    F -->|Rejected ❌ & Attempts ≥ 2| I[ESCALATE: Hand over to human]
    I --> G

----
```

## ⚙️ Architectural Decisions  

The agent is built on **LangGraph’s `StateGraph`**, with a clear modular design. Every piece has a single responsibility, making the system easy to extend and debug.  

1. **LangGraph Orchestration (`src/main.py`)**  

   - The function `support_agent()` defines and compiles the whole workflow.  
   - Handles multi-step execution with conditional routing and retry loops.  
   - Easy to visualize and debug in **LangGraph Studio**.  

2. **Atomic Nodes (`src/nodes/*.py`)**  
   - Each operation is its own node: `classify`, `retrieve`, `draft`, `review`, `retry`, `escalate`.  
   - This modular approach makes testing and maintenance simple.  

3. **Centralized State (`src/state.py`)**  
   - A shared `AgentState` (`TypedDict`) keeps ticket info, category, context, drafts, attempts, etc.  
   - Ensures data flows consistently between nodes.  

4. **Retrieval-Augmented Generation (RAG)**  
   - Implemented in `src/simple_rag.py`.  
   - Loads docs from `data/mock_docs.json` and injects relevant info into the draft.  
   - Prevents hallucinations by grounding answers in knowledge base.  

5. **Self-Correction Loop**  
   - Draft → Review → Retry flow ensures bad drafts don’t reach the user.  
   - `review` node gives feedback, `retry` node updates state, and draft regenerates.  
   - Mimics a real QA process.  

6. **Escalation (`src/nodes/escalate.py`)**  
   - If retries fail, ticket is logged into `escalations.csv`.  
   - Ensures unresolved issues are handed off cleanly to human agents. 

----

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Virtual Environment (recommended)**
- **Ollama** (agar local LLM chala rahe ho)
  - Install from [Ollama](https://ollama.com/download)
  - Example: `ollama run phi`
- **OpenAI API key** (agar cloud-based LLM use karna hai)

---

### Installation

1.  **Clone Repository:**

   ```bash
   git clone https://github.com/Sonia-Rejhra/Junior-AI-ZikraInfoTech.git
   cd Sonia-Rejhra

2. **Create Virtual Environment**
  python -m venv .venv
  .venv\Scripts\activate
  ```