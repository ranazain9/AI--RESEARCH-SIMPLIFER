# 📚 AI Research Paper Simplifier

An advanced **Retrieval-Augmented Generation (RAG)** application designed to transform complex research papers into simple, actionable insights. Built with a production-first mindset using **FastAPI**, **Streamlit**, and **LangChain**.

---

## 🌐 Live Deployment

- **🔗 Frontend**: https://ai--research-simplifer.streamlit.app/
- **🔗 Backend API**: https://ai-research.up.railway.app/
- **📦 Docker Image**: `ranazain12/ai-app`

---

## ✨ Features

- **🚀 Automated RAG Pipeline**: Intelligent PDF loading, chunking, and indexing.
- **🧠 Advanced Retrieval**: Uses MMR (Maximal Marginal Relevance) for diverse context retrieval.
- **💬 Structured Answers**: Provides simple explanations, technical details, methodology, and citations.
- **🏗️ Production-Ready Architecture**: Modular backend, centralized configuration, and containerized deployment.
- **🎨 Modern UI**: Vibrant Streamlit interface with a premium dark/glassmorphic aesthetic.
- **🐳 Docker Support**: One-command setup for the entire stack with pre-built Docker image.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **Embeddings**: HuggingFace (BAAI/bge-small-en-v1.5)
- **Vector DB**: FAISS (Persistent local storage)
- **Orchestration**: LangChain

---

## 📂 Project Structure

```text
├── app/                      # Backend Core
│   ├── api/                  # API Routes (Upload, Query, Health)
│   ├── core/                 # Configuration & Orchestration
│   │   ├── config.py         # Pydantic-based settings
│   │   ├── pipeline.py       # Orchestration logic
│   │   └── logging_config.py # Structured logging
│   ├── modules/              # RAG Components (Modularized)
│   │   ├── upload/           # PDF Loading
│   │   ├── splitter/         # Text Chunking
│   │   ├── model/            # LLM & Embedding models
│   │   ├── vectors/          # Vector Store management
│   │   ├── retriever/        # Retrieval logic
│   │   ├── prompts/          # RAG Prompts & Templates
│   │   └── config/           # RAG-specific helpers
│   ├── schemas/              # Pydantic request/response models
│   ├── services/             # Business logic (RAG Service)
│   └── main.py               # Application entry point
├── frontend/                 # Streamlit UI Application
├── docs/                     # Detailed technical documentation
├── testing/                  # Test scripts & sample papers
├── Dockerfile                # Production container build
├── docker-compose.yml        # Multi-container orchestration
├── requirements.txt          # Python dependencies
└── .env                      # Environment secrets
```

---

## 🚀 Quick Start

### Option 1: Use Live Deployment (Recommended)

No setup needed! Just visit the services:

1. **Frontend**: https://ai--research-simplifer.streamlit.app/
2. **Backend API**: https://ai-research.up.railway.app/
3. **API Documentation**: https://ai-research.up.railway.app/docs

---

### Option 2: Docker (Local)

Pull and run the pre-built Docker image:

```bash
docker pull ranazain12/ai-app
docker run -e GROQ_API_KEY=your_key_here -p 8000:8000 ranazain12/ai-app
```

Then visit:
- **API Docs**: http://localhost:8000/docs
- **Frontend**: Run locally via `streamlit run frontend/streamlit_app.py`

---

### Option 3: Docker Compose (Local Full Stack)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ranazain9/AI--RESEARCH-SIMPLIFER.git
    cd AI--RESEARCH-SIMPLIFER
    ```

2.  **Configure environment**:
    Create a `.env` file from the example:
    ```bash
    cp .env.example .env
    ```
    Add your `GROQ_API_KEY` to the `.env` file.

3.  **Start the full stack**:
    ```bash
    docker-compose up --build
    ```

4.  **Access the services**:
    - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Frontend**: [http://localhost:8501](http://localhost:8501)

---

### Option 4: Manual Setup (Development)

1.  **Clone and install**:
    ```bash
    git clone https://github.com/ranazain9/AI--RESEARCH-SIMPLIFER.git
    cd AI--RESEARCH-SIMPLIFER
    pip install -r requirements.txt
    ```

2.  **Configure environment**:
    ```bash
    cp .env.example .env
    # Edit .env and add your GROQ_API_KEY
    ```

3.  **Run Backend**:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

4.  **Run Frontend** (in a new terminal):
    ```bash
    streamlit run frontend/streamlit_app.py
    ```

5.  **Access services**:
    - **Backend API**: http://localhost:8000
    - **API Docs**: http://localhost:8000/docs
    - **Frontend**: http://localhost:8501

---

## 🔬 RAG Pipeline Workflow

1.  **Extraction**: PDF content is extracted page-by-page.
2.  **Chunking**: Recursive character splitting with optimal overlap.
3.  **Embedding**: Text chunks are converted to vectors using `bge-small-en-v1.5`.
4.  **Retrieval**: Queries use MMR to find the top 6 most relevant and diverse context chunks.
5.  **Generation**: The context is passed through a custom system prompt to the **Llama 3.3 70B** model.
6.  **Response**: A structured JSON response is returned, including simplified explanations and technical breakdowns.

---

## 📝 Usage Note
- The system enforces strict RAG rules to prevent hallucinations.
- If the uploaded paper doesn't contain the answer, the AI will clearly state it.
- Always check the **Citations** section for evidence-backed answers.

---

## 🚀 Deployment & Infrastructure

### Production Deployment

The application is deployed on the following platforms:

| Service | Platform | URL |
|---------|----------|-----|
| **Backend API** | Railway | https://ai-research.up.railway.app/ |
| **Frontend** | Streamlit Cloud | https://ai--research-simplifer.streamlit.app/ |

### Docker Image

Pre-built Docker image available on Docker Hub:

```bash
# Pull the image
docker pull ranazain12/ai-app

# Run the image
docker run -e GROQ_API_KEY=your_key_here -p 8000:8000 ranazain12/ai-app
```

**Image Details:**
- Repository: `ranazain12/ai-app`
- Latest tag: `latest`
- Base: Python 3.10
- Size: Optimized for production

### API Endpoints (Production)

**Base URL**: `https://ai-research.up.railway.app`

- **Swagger UI**: https://ai-research.up.railway.app/docs
- **ReDoc**: https://ai-research.up.railway.app/redoc
- **Health**: https://ai-research.up.railway.app/health

### Environment Variables

Required for both local and production deployment:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Optional:
```bash
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_LOG_LEVEL=info
```

---

## 🤝 Contributing
Contributions are welcome! Please check the `docs/` folder for implementation summaries and route details.

