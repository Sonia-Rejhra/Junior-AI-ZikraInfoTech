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

```
----

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
  ```

2.  **Create Virtual Environment:**

   ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

1. **Copy .env.example to .env:**
   ```bash
   cp .env.example .env
   ```

2.  **Fill required variables in .env:**
    ```bash
      USE_OLLAMA=true   # true for local, false for OpenAI
      OLLAMA_MODEL=phi
      OPENAI_MODEL=gpt-4o-mini
    ```

### `requirements.txt` Content:
  ```bash
   langchain==0.2.5
   langchain-core==0.2.9
   langgraph==0.0.51
   langchain-community==0.2.5
   ollama==0.1.8
   pydantic==2.7.4
   pandas==2.2.2
   sentence-transformers==2.7.0
   scikit-learn==1.5.0
   ```

### Knowledge Base Setup

The RAG system loads data from `data/mock_docs.json`.  
This file contains a JSON object where keys are categories (like billing, technical, security, general) and values are lists of documents.  
Ensure this file is correctly populated with your support knowledge.

**Example `data/mock_docs.json` content:**

```json
{
  "billing": [
    "For billing disputes, please contact billing@example.com or call 1-800-555-BILL. Provide your account number and transaction details. Refunds are processed in 5-7 business days."
  ],
  "technical": [
    "For login issues, try resetting your password. Ensure your browser is updated, clear cache/cookies."
  ],
  "security": [
    "Enable two-factor authentication (2FA) for better security. If you notice suspicious activity, contact support immediately."
  ],
  "general": [
    "Our support team is available 24/7 through live chat and email. Response time is usually within 1 hour."
  ]
}





