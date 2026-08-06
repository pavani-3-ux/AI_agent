# 🤖 AI Agent - Multi-Agent Intelligent Assistant

An intelligent AI Assistant built using **FastAPI, LangChain, Ollama (Qwen3), ChromaDB, and Tavily**.

The agent intelligently routes user queries to the appropriate tool, enabling live internet search, PDF-based question answering (RAG), calculations, unit conversions, and general AI conversations through a clean ChatGPT-style interface.

---

# 🚀 Features

- 💬 ChatGPT-like Web Interface
- 🤖 Local LLM using Qwen3 (Ollama)
- 🌐 Live Internet Search (Tavily)
- 📄 PDF Question Answering (RAG)
- 🧠 Intelligent Multi-Agent Routing
- 🧮 Calculator Tool
- 📏 Unit Converter
- 📅 Date & Time Tool
- ⚡ FastAPI Backend
- 💾 ChromaDB Vector Database
- 🔍 Semantic Search
- 🔒 Environment Variable Support
- 🖥️ Lightweight Local Deployment

---

# 🏗️ Architecture

```
                User
                  │
                  ▼
        ChatGPT-like Interface
                  │
                  ▼
           FastAPI Backend
                  │
                  ▼
        Multi-Agent Supervisor
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
 General AI   Live Web     PDF Search
   (Qwen3)     (Tavily)    (ChromaDB)

     │            │            │
     └────────────┼────────────┘
                  ▼
            Final Response
```

---

# 📂 Project Structure

```
AI_agent/
│
├── production_agent.py
├── level7_multi_agent.py
├── web_search.py
├── rag_pipeline.py
├── tools.py
│
├── documents/
├── chroma_db/
├── archive/
│
├── AI_Fundamentals.pdf
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

- Python
- FastAPI
- LangChain
- Ollama
- Qwen3
- ChromaDB
- Tavily Search API
- Sentence Transformers
- HuggingFace
- HTML
- CSS
- JavaScript

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/pavani-3-ux/AI_agent.git
```

Go to the project folder

```bash
cd AI_agent
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

Example:

```env
TAVILY_API_KEY=your_tavily_api_key
```

---

# ▶️ Run the Project

Start the application

```bash
python production_agent.py
```

Open in your browser

```
http://127.0.0.1:8000
```

---

# 💬 Example Queries

### General AI

```
Explain Machine Learning.
```

### Live Internet Search

```
What are the latest AI developments today?
```

### Current Information

```
Who is the current CEO of Microsoft?
```

### Technology News

```
Latest technology news today
```

### Calculator

```
Calculate 258 * 963
```

### Unit Conversion

```
Convert 25 km to miles
```

### Date & Time

```
What is today's date?
```

### PDF RAG

```
According to my PDF, what is Artificial Intelligence?
```

---

# 🧠 Agent Capabilities

- Intelligent Query Routing
- Live Internet Search
- Retrieval-Augmented Generation (RAG)
- Semantic PDF Search
- Tool Calling
- Local LLM Inference
- Context-Aware Responses
- FastAPI REST Backend
- Chat-Based User Interface

---

# 🚀 Future Improvements

- Streaming Responses
- Conversation Memory
- Multi-PDF Upload
- Authentication
- User Accounts
- Voice Assistant
- Image Understanding
- Docker Support
- Cloud Deployment
- Agentic Workflow Automation

---

# 📦 Requirements

Install all dependencies using

```bash
pip install -r requirements.txt
```

---

# 👨‍💻 Author

**Pavani**

AI & Data Analytics Enthusiast

---

# ⭐ If you like this project

Give it a ⭐ on GitHub.
