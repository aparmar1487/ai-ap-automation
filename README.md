🧠 AI-Driven Accounts Payable (AP) Automation using LangFlow, Microsoft Fabric & MCP Orchestration

This project is a hands-on learning and build environment for developing an AI-powered Accounts Payable automation system that combines structured SAP-style data, unstructured invoice documents, and AI reasoning workflows orchestrated through LangFlow and the Model Context Protocol (MCP).

The goal is to simulate a real enterprise finance automation use case—from invoice ingestion to matching and intelligent query answering—using open-source and Microsoft ecosystem tools.

🎯 Project Objectives

Build an AI workflow assistant (Ask Agent) that answers questions about AP data (structured + unstructured).

Develop a 3-Way Match Agent that automates invoice extraction, validation, and classification into Full Match, Partial Match, or No Match.

Implement an MCP-based reasoning router that selects the right engine based on query intent:

SQL Engine → numeric summaries and aggregations

Graph Engine → relationship and multi-hop reasoning

RAG Engine → semantic and policy-based explanations

Load and manage SAP-style datasets inside a Microsoft Fabric Lakehouse (Bronze → Silver → Gold).

Enable model performance evaluation through Eval Tools (e.g., OpenAI Evals, LangSmith, or TruLens).

Manage code and workflow versions via GitHub, promoting MLOps-style collaboration and documentation.



Step 1 – Environment and Setup
1. Create and Clone the Repository
# On GitHub: create repo named ai-ap-automation
git clone https://github.com/<your-username>/ai-ap-automation.git
cd ai-ap-automation

2. Create Folder Structure
ai-ap-automation/
├── data/
│   ├── sap_tables/     # SAP dummy tables (LFA1, EKKO, EKPO, etc.)
│   ├── invoices/       # Sample vendor invoice PDFs
│   └── policies/       # AP policy docs (PDF/DOCX)
├── lakehouse/          # Fabric data lakehouse scripts or exports
├── agents/             # AI agent logic
├── workflows/          # LangFlow JSONs
├── eval/               # Model evaluation files
├── ui/                 # Chat UI or Streamlit app (future)
└── README.md

3. Install Python 3.11

Download from python.org/downloads/macos

Verify installation:

python3.11 --version
pip3.11 --version

4. Create Virtual Environment
python3.11 -m venv .venv
source .venv/bin/activate

5. Upgrade pip
pip install --upgrade pip

6. Install Dependencies
pip install langflow openai llama-index neo4j pandas chromadb

7. Run LangFlow
langflow run
Open in browser → http://localhost:7860
