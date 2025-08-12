# Private AI Knowledge Worker Agent

A local, privacy-focused AI agent that can read and understand your emails, then answer questions about them.  
It uses **Retrieval-Augmented Generation (RAG)** with a local LLM, ensuring all data stays on your machine.

## Features
- 📂 Ingest and index personal documents
- 📧 Connect to Gmail via IMAP to read and process emails
- 🔍 Store and search data using ChromaDB
- 🧠 Use a local LLM (via Ollama) for conversational querying
- 🔒 100% privacy — no cloud APIs needed

## Tech Stack
- **Python**
- **Ollama** (local LLM)
- **ChromaDB** (vector database)
- **IMAP** (email fetching)
- **LangChain** (RAG orchestration)

## Installation & Setup

### 1 Clone the repository
```
git clone https://github.com/yourusername/local-rag-agent.git
cd local-rag-agent
```
### 2 Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
### 3 Install dependencies
```
pip install -r requirements.txt
```
### 4 Configure environment variables
```
Create a .env file in the project root:
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_app_password
EMAIL_IMAP=imap.gmail.com
```
### 5 Running the Agent
```
python main.py
```
This will:
Load emails from your inbox.
Store & index them in ChromaDB.
Start a conversation interface with your local LLM.
