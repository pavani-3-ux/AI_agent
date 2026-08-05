# 🤖 AI Agent — Level 1 to Level 8

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Qwen3](https://img.shields.io/badge/Qwen3-4B-orange)
![LangChain](https://img.shields.io/badge/LangChain-AI%20Framework-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-purple)
![RAG](https://img.shields.io/badge/RAG-PDF%20Retrieval-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

A production-oriented AI Agent developed progressively from a basic **LLM + Calculator** application into a complete AI Agent system with **multiple tools, persistent memory, web search, RAG, PDF retrieval, planning, multi-agent orchestration, and a ChatGPT-style web interface**.

The project is built using Python and a locally running **Qwen3:4b model through Ollama**, with LangChain-based integrations and a FastAPI-powered production interface.

---

# 📌 Table of Contents

- [Project Overview](#-project-overview)
- [What is an AI Agent?](#-what-is-an-ai-agent)
- [Project Goal](#-project-goal)
- [Development Journey](#-development-journey)
- [Level 1 — LLM + Calculator](#-level-1--llm--calculator)
- [Level 2 — Multiple Tools](#-level-2--multiple-tools)
- [Level 3 — Persistent Memory](#-level-3--persistent-memory)
- [Level 4 — Web Search](#-level-4--web-search)
- [Level 5 — RAG + PDFs](#-level-5--rag--pdfs)
- [Level 6 — Planning](#-level-6--planning)
- [Level 7 — Multi-Agent System](#-level-7--multi-agent-system)
- [Level 8 — Production AI Agent](#-level-8--production-ai-agent)
- [Final Architecture](#-final-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [File Responsibilities](#-file-responsibilities)
- [RAG Pipeline](#-rag-pipeline)
- [Web Search](#-web-search)
- [Planning](#-planning)
- [Multi-Agent System](#-multi-agent-system)
- [Production Interface](#-production-interface)
- [Logging](#-logging)
- [Installation](#-installation)
- [Ollama Setup](#-ollama-setup)
- [Environment Variables](#-environment-variables)
- [Running the Project](#-running-the-project)
- [Example Queries](#-example-queries)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Learning Outcomes](#-learning-outcomes)
- [Project Progress](#-project-progress)
- [Future Improvements](#-future-improvements)
- [Conclusion](#-conclusion)
- [Author](#-author)

---

# 🚀 Project Overview

This project demonstrates the complete evolution of an AI Agent.

Instead of building only a chatbot that generates text, the system progressively adds capabilities that allow the agent to:

- Understand user requests
- Select appropriate tools
- Perform calculations
- Search external information
- Retrieve information from documents
- Remember previous information
- Break complex tasks into steps
- Coordinate multiple capabilities
- Produce a final response
- Provide a browser-based chat interface

The development follows this architecture:

```text
LEVEL 1
LLM + Calculator
        ↓
LEVEL 2
Multiple Tools
        ↓
LEVEL 3
Persistent Memory
        ↓
LEVEL 4
Web Search
        ↓
LEVEL 5
RAG + PDFs
        ↓
LEVEL 6
Planning / Multi-step Tasks
        ↓
LEVEL 7
Multi-Agent System
        ↓
LEVEL 8
Production AI Agent
