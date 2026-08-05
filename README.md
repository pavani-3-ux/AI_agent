\# 🤖 Production AI Agent — Level 1 to Level 8



A modular AI Agent built with Python, Ollama, Qwen3, LangChain, RAG, Web Search, Planning, Multi-Agent orchestration, and a production-style Chat UI.



This project was developed progressively from a basic LLM + Calculator system into a production-oriented AI Agent capable of selecting tools, searching the web, retrieving information from PDFs, planning tasks, and coordinating multiple specialized agents.



\---



\## 🚀 Project Overview



The goal of this project is to understand and implement the evolution of an AI system from a simple LLM application into a production-oriented AI Agent.



The final system combines:



\- Local LLM inference

\- Tool usage

\- Persistent memory

\- Web search

\- PDF-based RAG

\- Planning

\- Multi-Agent orchestration

\- FastAPI backend

\- Chat-style web interface

\- Logging and error handling



\### Final Architecture



```text

&#x20;                   USER

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌───────────────┐

&#x20;             │   Chat UI     │

&#x20;             └───────┬───────┘

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌───────────────┐

&#x20;             │ Production    │

&#x20;             │ Agent         │

&#x20;             └───────┬───────┘

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌─────────────────┐

&#x20;             │ Multi-Agent     │

&#x20;             │ Orchestrator    │

&#x20;             └───────┬─────────┘

&#x20;                     │

&#x20;      ┌──────────────┼───────────────┐

&#x20;      │              │               │

&#x20;      ▼              ▼               ▼

&#x20;  Web Search       PDF RAG         Tools

&#x20;      │              │               │

&#x20;      │              │        ┌──────┼──────┐

&#x20;      │              │        │      │      │

&#x20;      ▼              ▼        ▼      ▼      ▼

&#x20;   Internet       Chroma    Calculator Date  ...

&#x20;      │              │

&#x20;      └──────┬───────┘

&#x20;             │

&#x20;             ▼

&#x20;         Qwen3:4b

&#x20;             │

&#x20;             ▼

&#x20;        Final Answer



🧠 Agent Development Journey



The project was developed through eight progressive levels.



Level 1 — LLM + Calculator



The first stage introduced the basic AI Agent concept.



User

&#x20;↓

LLM

&#x20;↓

Calculator Tool

&#x20;↓

Answer



The agent learned to process a user request and use a calculator when arithmetic was required.



Level 2 — Multiple Tools



The agent was extended to work with multiple tools.



Examples include:



Calculator

Current date and time

Other utility operations



The agent determines which capability is appropriate for the user's request.



Level 3 — Persistent Memory



Persistent memory was introduced using a local database.



User

&#x20;↓

Agent

&#x20;↓

Memory

&#x20;↓

Database



This allows the system to maintain information across conversations instead of treating every request as completely independent.



Level 4 — Web Search



Web search capabilities were added so the agent could retrieve information that may not be available in its local model knowledge.



User Question

&#x20;     ↓

Agent

&#x20;     ↓

Web Search

&#x20;     ↓

Search Results

&#x20;     ↓

LLM

&#x20;     ↓

Answer



The project uses web search functionality through the configured search integration.



Level 5 — RAG + PDF



Retrieval-Augmented Generation was implemented for document-based question answering.



The system can retrieve relevant information from the provided PDF and use that information to generate an answer.



PDF

&#x20;↓

Document Extraction

&#x20;↓

Chunking

&#x20;↓

Embeddings

&#x20;↓

Vector Database

&#x20;↓

Similarity Search

&#x20;↓

Relevant Context

&#x20;↓

LLM

&#x20;↓

Answer



The project currently includes:



AI\_Fundamentals.pdf



as a document source.



Level 6 — Planning



Planning was introduced to handle tasks that require multiple steps.



User Task

&#x20;   ↓

Planner

&#x20;   ↓

Task Plan

&#x20;   ↓

Step 1

&#x20;   ↓

Step 2

&#x20;   ↓

Step 3

&#x20;   ↓

Final Result



The planner determines what actions are required before execution.



This creates a separation between:



Planning

Execution

Final response generation

Level 7 — Multi-Agent System



The system was extended into a multi-agent architecture.



Different capabilities can be handled by specialized agents/tools.



&#x20;                User

&#x20;                  │

&#x20;                  ▼

&#x20;            Orchestrator

&#x20;                  │

&#x20;       ┌──────────┼──────────┐

&#x20;       │          │          │

&#x20;       ▼          ▼          ▼

&#x20;     Web         RAG        Tools

&#x20;     Agent       Agent      Agent

&#x20;       │          │          │

&#x20;       └──────────┼──────────┘

&#x20;                  │

&#x20;                  ▼

&#x20;             Final Answer



This makes the system more modular and easier to extend.



Level 8 — Production AI Agent



The final stage combines the previous capabilities into a production-style application.



The application provides:



Chat interface

Local LLM

Multi-Agent orchestration

RAG

Web search

Tools

Planning capabilities

Error handling

Logging

FastAPI backend



The main entry point is:



production\_agent.py

🛠️ Technology Stack

Technology	Purpose

Python	Core programming language

Ollama	Local LLM runtime

Qwen3:4b	Local language model

LangChain	LLM and tool integration

ChromaDB	Vector database

FastAPI	Backend/API layer

Uvicorn	Application server

Tavily	Web search

PyPDF	PDF processing

SQLite	Local persistent memory

HTML/CSS/JavaScript	Chat interface

📁 Project Structure

beginner\_ai\_agent/

│

├── production\_agent.py

├── level7\_multi\_agent.py

├── rag\_pipeline.py

├── tools.py

├── web\_search.py

│

├── AI\_Fundamentals.pdf

├── documents/

│

├── requirements.txt

├── .gitignore

├── .env.example

├── README.md

│

└── archive/

&#x20;   ├── agent.py

&#x20;   ├── agent\_headless.py

&#x20;   ├── executor.py

&#x20;   ├── final\_answer.py

&#x20;   ├── level6\_agent.py

&#x20;   ├── memory.py

&#x20;   ├── planner.py

&#x20;   ├── planning\_agent.py

&#x20;   ├── test\_executor.py

&#x20;   ├── test\_level6.py

&#x20;   └── test\_planner.py

