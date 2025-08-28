# 🤖 Support Ticket Agent using RAG and LangGraph

This project implements an intelligent **AI-powered Support Ticket Agent** leveraging **LangGraph** for workflow orchestration and **Retrieval-Augmented Generation (RAG)** for contextual responses.  
The agent resolves routine inquiries, retries bad drafts automatically, and escalates tough cases with full context.

---

## 🧩 Workflow Diagram

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
---