# Multi-Agent AI Research System

An intelligent research assistant that automates web research, document retrieval, report generation, fact-checking, and iterative quality improvement using a multi-agent LangGraph workflow.

## 🚀 Overview

This project combines multi-agent orchestration and Retrieval-Augmented Generation (RAG) to produce structured, evidence-based research reports.

The system can:

- Search the web for relevant information
- Extract content from multiple sources
- Retrieve relevant information from uploaded PDF/TXT documents
- Generate structured research reports
- Critically evaluate generated reports
- Fact-check important claims
- Automatically revise reports when quality issues are detected
- Perform a final quality check before completing the workflow

## 🧠 Architecture

```text
                    Research Topic
                          │
                          ▼
                  ┌───────────────┐
                  │  Web Search   │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Multi-Source  │
                  │    Reader     │
                  └───────┬───────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      ┌──────────────┐         ┌──────────────┐
      │ Web Research │         │  RAG Search  │
      │    Context   │         │ PDF / TXT    │
      └──────┬───────┘         └──────┬───────┘
             │                         │
             └────────────┬────────────┘
                          ▼
                  ┌───────────────┐
                  │     Writer    │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │    Critic     │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │ Fact Checker  │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │   Revision    │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │ Quality Check │
                  └───────┬───────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
               PASS              REVISE
                 │                 │
                 ▼                 └──────► Revision
               Final
               Report
✨ Key Features
Multi-Agent Research

Built with LangGraph to orchestrate specialized research stages including search, reading, writing, criticism, fact-checking, and revision.

RAG-Based Document Research

Uses Sentence Transformers and FAISS to retrieve relevant context from user-uploaded PDF and TXT documents.

Multi-Source Web Research

Searches multiple web sources and extracts their content before report generation.

Fact-Checking & Quality Control

Generated reports are evaluated against gathered research. Unsupported claims can trigger another revision cycle.

Iterative Revision

The workflow supports up to two revision attempts based on critic and fact-checking feedback.

Interactive Interface

A Streamlit interface allows users to enter research topics, upload documents, execute the workflow, and view the generated results.

## 🛠️ **Tech Stack**
Python
LangGraph
LangChain
Groq
FAISS
Sentence Transformers
Tavily
BeautifulSoup
PyPDF
Streamlit
📊 Implementation Highlights
8-stage research workflow
Up to 5 web sources retrieved per search
Up to 5 URLs processed per reader call
Top 3 relevant document chunks retrieved through RAG
800-character document chunks with 150-character overlap
PDF and TXT document support
Up to 2 automated revision attempts
Evidence-grounded report generation

📁 Project Structure

multi-agent-ai-research-system/
│
├── agents.py
├── pipeline.py
├── tools.py
├── app.py
│
├── rag_ingest.py
├── rag_chunks.py
├── rag_store.py
├── rag_retrieve.py
├── rag_qa.py
│
├── documents/
├── requirements.txt
└── .gitignore

⚙️ Setup
1. Clone the repository
git clone https://github.com/Anjali-sudo397/multi-agent-ai-research-system.git
cd multi-agent-ai-research-system

2. Create a virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
5. Run the application
streamlit run app.py
🔒 Security

API keys are stored in environment variables and excluded from version control using .gitignore.

Never commit API keys or other credentials to the repository.

📌 Future Improvements
PostgreSQL + pgvector integration
FastAPI backend
React frontend
Persistent vector database
Automated evaluation metrics
Docker deployment
Advanced source citation and verification
👩‍💻 Author

Anjali Kumari

GitHub: @Anjali-sudo397


