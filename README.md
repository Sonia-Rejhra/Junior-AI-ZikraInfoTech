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
```
----

### Environment Variables (Optional but Recommended)

If your application needs to use secrets (like API keys or model settings), create a `.env` file in the root of your project.  
This helps keep sensitive values out of your code.

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file and add your environment variables.**
  ```bash
   # Model selection
   USE_OLLAMA=true
   OLLAMA_MODEL=phi

   # (Optional) OpenAI fallback
   OPENAI_API_KEY=sk-xxxx
   OPENAI_MODEL=gpt-4o-mini

  # (Optional) LangSmith tracing
  LANGSMITH_API_KEY=lsv2-xxxx
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_PROJECT=support-ticket-agent
  ```
----
## ▶️ How to Run the Agent

### 1. Command Line Interface (CLI)

1. **Start Ollama Service**  
   Make sure Ollama is running locally with the model you set in `.env` (default: `phi`).  
   Example to pull a model:  
   ```bash
   ollama run phi
   ```
2. **Activate Virtual Environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   ```
3. **Run The Agent:**
  ```bash
  python -m src.main
  ```
4. **Enter your ticket details when prompted:**

   ```bash
   Subject: Unable to reset password
   Description: The reset link never arrives in my email.
   ```
5. **Type exit anytime to quit.**

### 2. LangGraph Studio (Visual Debugging)
LangGraph Studio gives you a visual flow of how your agent executes each node.

1. **Install the LangGraph CLI (already in requirements.txt).**

2. **Start the LangGraph server:**

  ```bash
  langgraph dev --host 0.0.0.0 --port 8123 src.main:support_agent
  ```

3.  **Open your browser and go to:**
   ```bash
   http://localhost:8123
   ```
4. **Interact with the workflow visually — you can see how the agent moves through**
###  **input → classify → retrieve → draft → review → retry/escalate.**

----

## 🧪 Testing & Demonstrations

Use these scenarios to test the agent’s capabilities (CLI ya LangGraph Studio dono me try kar sakte ho):

### 1. ✅ Happy Path — Successful Resolution
**Scenario:** Straightforward inquiry jo agent khud solve kar leta hai.  
**Input Example:**
Subject: Refund request
Description: I was charged twice for my subscription, can I get a refund?
**Expected Outcome:**  
The agent classifies the ticket as `Billing`, fetches relevant documents, drafts a response, and gets approval.  
The final response includes clear refund process instructions.

### 2. 🔄 Self-Correction Loop — Retry with Feedback
**Scenario:** The first draft is rejected, then the agent improves the response based on feedback.  

**Input Example:**
Subject: App not working
Description: The app crashes every time I try to log in after the update.
**Expected Outcome:**  
The first draft is rejected for missing context or including sensitive info.  
The agent retries with feedback → produces an improved draft → the draft is approved.

**Input Example:**
Subject: Support hours
Description: What time are your agents available for live chat?
**Expected Outcome:**  
The ticket is classified as `General`.  
The agent fetches information from the knowledge base and produces an approved draft with the correct support hours.

## 📂 Project Structure
```
support_agent/
├── .gitignore # Ignore venv, env files, cache, etc.
├── README.md # Documentation (this file)
├── requirements.txt # Python dependencies
├── escalations.csv # Auto-created when a ticket is escalated
├── .env.example # Example environment variables
├── .env # Local environment variables (ignored by Git)
├── data/ # Knowledge base for RAG
│ └── mock_docs.json # Sample support knowledge documents
└── src/ # Source code
   ├── main.py # Workflow definition (LangGraph) + CLI entry
   ├── state.py # AgentState definition (shared memory between nodes)
   ├── llm.py # LLM setup (Ollama or OpenAI depending on env vars)
   ├── simple_rag.py # Simple RAG retrieval logic
   └── nodes/ # Workflow nodes (single responsibility each)
      ├── init.py
      ├── input_node.py # Handles initial user input
      ├── classify.py # Classifies tickets into categories
      ├── retrieve.py # Retrieves relevant docs from RAG KB
      ├── draft.py # Generates draft replies
      ├── review.py # Reviews and approves/rejects drafts
      ├── retry.py # Manages retry loop with feedback
      └── escalate.py # Escalates unresolved tickets to humans

```
----

## 📈 Future Enhancements

* **Smarter RAG:** Upgrade from simple keyword matching to embeddings with a vector database.  
* **Improved Review:** Make draft feedback more consistent and context-aware.  
* **Ticket System Integration:** Connect with platforms like Zendesk or ServiceNow.  
* **User Feedback:** Let users rate replies so the agent can improve.  
* **Clear Human Handoff:** Better mechanisms for escalation to support staff.  

-----

## 📧 Contact & Acknowledgments

Developed by Sonia Bai for Junior AI Assessment Role, at Z360.

Special thanks to the LangChain and LangGraph communities for their powerful tools.

-----

