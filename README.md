
````md
# 🧠 Social Media Blog - Agentic Content Generation System

Welcome to **Social Media Blog**, a fully orchestrated multi-agent content generation system powered by **CrewAI** and deployed with **FastAPI**. This intelligent backend generates high-quality, trend-driven blog content through collaborative agents, delivering a storytelling experience shaped by automation and AI creativity.

## 🚀 Live Project Links

- 🔗 **GitHub Repo:** [https://github.com/SBAK729/social_media_blog](https://github.com/SBAK729/social_media_blog)
- 🌐 **Live API Deployment:** [https://social-media-blog-0aw9.onrender.com](https://social-media-blog-0aw9.onrender.com)
- 📝 **Frontend Site:** [https://story-loom-gsmw.vercel.app](https://story-loom-gsmw.vercel.app)

---

## 🧩 Features

### ✅ Agentic System via CrewAI
- **TrendHunterAgent:** Finds hot and relevant blog topics using real-time data.
- **WriterAgent:** Crafts engaging content based on topic and context.
- **EditorAgent:** Refines tone, structure, and readability.
- **SummarizingAgent:** Generates blog summaries and meta descriptions.

### ✅ Fully Orchestrated Workflow
- CrewAI coordination for step-by-step task execution
- Seamless agent collaboration and result passing
- Logs for agent decisions and reasoning paths

### ✅ RAG with Vector Database
- **ChromaDB** used for topic/document embedding
- Semantic similarity search using OpenAI/Gemini embeddings
- Context-aware writing using embedded chunks

### ✅ FastAPI Backend
- RESTful endpoint: `POST /api/generate-blog`
- Customization: tone, platform guidelines, manual/auto topic input
- Swagger UI enabled for testing (`/docs`)
- Full CORS and rate-limiting support
- Dockerized and ready for cloud deployment

---

## 🧪 API Usage

### 🔥 POST `/api/generate-blog`


---

## 📦 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/SBAK729/social_media_blog.git
cd social_media_blog

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env  # Then fill in keys

# Run the app
uvicorn app.main:app --reload
```

Then visit: `http://localhost:8000/docs` to test the API via Swagger UI.

---

## 🐳 Docker Setup

```bash
# Build the container
docker build -t social-blog-api .

# Run the container
docker run -d -p 8000:8000 --env-file .env social-blog-api
```

---

## 🧠 Agent Design & Workflow

* Each agent uses a dedicated structured prompt with role-specific instructions.
* CrewAI coordinates the interaction and retry logic.
* Memory and output logging are enabled for traceability and debugging.

---

## 🔍 Retrieval-Augmented Generation (RAG)

* Embedded knowledge snippets from past blog posts or reference content
* Integrated semantic retrieval for context injection
* Dynamic fallback to LLM-only generation if vector store is empty

---

## 🔐 Security & Error Handling

* Input validation via Pydantic models
* CORS configured for frontend use
* Graceful fallbacks on LLM errors or retrieval failures
* Logging and audit trail for all agent actions

---

## 🧪 Postman Collection

A full Postman collection is available to test endpoints locally or after deployment.

> 📁 *Add `/docs` URL or link to exported Postman collection here if required*

---

## 🌍 Deployment

This app is fully containerized and can be deployed on:

* ✅ Render
* ✅ Railway
* ✅ AWS EC2 or ECS
* ✅ GCP Cloud Run

Set environment variables (e.g., `GEMINI_API_KEY`, `MODEL_PROVIDER`, `CHROMADB_PATH`) in your cloud dashboard.



