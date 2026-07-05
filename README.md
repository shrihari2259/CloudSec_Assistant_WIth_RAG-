# 🛡️ CloudSec Assistant

**A domain-restricted RAG chatbot for Cloud Computing & Cybersecurity questions — built with Gemini, Pinecone, and HuggingFace embeddings.**

Ask it about AWS, Azure, GCP, DevOps, Kubernetes, Terraform, or Cybersecurity — and get answers grounded strictly in a curated knowledge base (AWS Well-Architected Framework, NIST Cybersecurity Framework). Ask it anything outside that domain, and it politely declines.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-latest-1C3C3C?logo=langchain&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-000000?logo=pinecone&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-8E75B2?logo=googlegemini&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What it does

CloudSec Assistant is a **Retrieval-Augmented Generation (RAG)** chatbot that:

1. Ingests cloud security reference documents (PDFs) into a vector database
2. Retrieves the most relevant chunks for any question, using semantic search
3. Sends only that retrieved context to a Gemini LLM to generate an answer
4. **Refuses to answer anything outside its domain** — no hallucinated advice on pizza recipes or poetry
5. Shows exactly which source document each answer came from, for transparency

No paid APIs. No OpenAI dependency. 100% free-tier stack.

---

## 🧠 Why this architecture

| Design choice | Reasoning |
|---|---|
| **Local HuggingFace embeddings** (`all-MiniLM-L6-v2`) | Free, fast, runs on CPU — no per-embedding API cost |
| **Pinecone Serverless (free tier)** | Persistent vector storage that survives restarts, unlike an in-memory store |
| **Gemini 2.5 Flash** | Free-tier LLM with strong reasoning-to-cost ratio |
| **Single combined LLM call** | Domain-check + answer generation merged into one prompt to cut API latency roughly in half per question |
| **Streamlit UI** | Instant, demoable chat interface — no separate frontend build needed |

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │   PDF Sources    │
                    │ (AWS WAF, NIST)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Text Splitter   │  chunk_size=800, overlap=100
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ HuggingFace      │  all-MiniLM-L6-v2
                    │ Embeddings       │  (local, free)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Pinecone Index  │  (persistent vector store)
                    └────────┬────────┘
                             │
        User Question ──────┤
                             │
                    ┌────────▼────────┐
                    │  Top-k Retrieval │  k=4
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Gemini 2.5      │  domain check + answer
                    │  Flash (1 call)  │  generation, combined
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Streamlit Chat  │  answer + cited sources
                    └─────────────────┘
```

---

## ✨ Features

- 📄 Multi-format document loading (PDF, with easy extension to DOCX/TXT/Markdown)
- ✂️ Recursive character chunking tuned for technical documentation
- 🔍 Semantic search over a persistent Pinecone vector index
- 🚫 Domain-gating — rejects off-topic questions instead of hallucinating
- 📚 Source attribution on every answer
- 💬 Chat-style Streamlit UI with conversation history
- ⚡ Optimized for low latency (single LLM call per question) and free-tier usage throughout

---

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **Orchestration:** LangChain (latest, non-deprecated APIs)
- **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB:** Pinecone (Serverless, free tier)
- **LLM:** Google Gemini 2.5 Flash (free tier)
- **UI:** Streamlit

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A free [Pinecone](https://www.pinecone.io/) account and API key
- A free [Google AI Studio](https://aistudio.google.com/) API key (for Gemini)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/cloudsec-assistant.git
cd cloudsec-assistant
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy the example file and fill in your real keys:
```bash
cp .env.example .env
```
Then edit `.env`:
```
GOOGLE_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=cloudsec-assistant
```

### 5. Ingest documents into Pinecone
Place your reference PDFs in `data/`, then run:
```bash
python embed.py
```
This chunks the documents, generates embeddings, and uploads them to your Pinecone index. Only needs to be run once (or whenever you add new source documents).

### 6. Launch the chatbot
```bash
streamlit run app.py
```
Opens automatically at `http://localhost:8501`.

---

## 💡 Example Questions

**✅ In-domain (answered from knowledge base):**
- "What is the shared responsibility model in AWS?"
- "What are the five pillars of the AWS Well-Architected Framework?"
- "What does the NIST Cybersecurity Framework recommend for identifying risks?"

**🚫 Out-of-domain (correctly rejected):**
- "What's a good pizza recipe?"
- "Write me a poem about the ocean"

---

## 📁 Project Structure

```
cloudsec-assistant/
├── data/                  # Source PDFs (AWS WAF, NIST CSF, etc.)
├── ingest.py              # Document loading logic
├── embed.py               # Chunking + embedding + Pinecone upload
├── rag_chain.py           # Core RAG pipeline (retrieval + generation)
├── app.py                 # Streamlit chat UI
├── requirements.txt
├── .env.example           # Template for required environment variables
└── README.md
```

---

## 🗺️ Roadmap

- [ ] SQL-based query logging (question, answer, sources, latency)
- [ ] Monitoring dashboard (rejection rate, avg. response time)
- [ ] Support for DOCX and Markdown ingestion
- [ ] Agent-based tool routing (Google ADK)
- [ ] Deployed live demo (Streamlit Community Cloud / EC2)

---

## 📄 License

MIT — free to use, modify, and learn from.

---

## 🙋 About

Built as a hands-on portfolio project to demonstrate practical RAG system design: document ingestion, vector search, LLM orchestration, and domain-constrained generation — using entirely free-tier tools.
