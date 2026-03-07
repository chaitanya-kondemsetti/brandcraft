# ⚡ CodeRefine AI
### Generative AI-Powered Code Review & Optimization Engine

> **Problem Statement:** CodeRefine : Generative AI-Powered Code Review & Optimization Engine  
> **Technologies:** FastAPI · JavaScript · OpenRouter LLM · Uvicorn

---

## 🏗️ Project Structure

```
coderefine/
├── main.py                        # FastAPI app entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── start.sh                       # One-command startup
│
├── backend/
│   ├── config.py                  # Settings (API key, model, host)
│   │
│   ├── models/
│   │   └── schemas.py             # All Pydantic request/response models
│   │
│   ├── services/
│   │   ├── llm_service.py         # OpenRouter API client (core)
│   │   ├── analysis_service.py    # Bug detection, complexity, quality
│   │   ├── optimizer_service.py   # AI code rewriter
│   │   ├── explain_service.py     # Plain-English code explanation
│   │   ├── security_service.py    # OWASP security audit
│   │   └── chat_service.py        # Conversational AI about code
│   │
│   └── routes/
│       ├── health.py              # GET  /api/health
│       ├── analyze.py             # POST /api/analyze
│       ├── optimize.py            # POST /api/optimize
│       ├── explain.py             # POST /api/explain
│       ├── security.py            # POST /api/security
│       └── chat.py                # POST /api/chat
│
└── frontend/
    └── index.html                 # Full dashboard UI (served at /)
```

---

## 🚀 Quick Start

### 1. Get an OpenRouter API Key (free)
Go to **https://openrouter.ai/keys** → Create account → Copy key

### 2. Set up environment
```bash
cp .env.example .env
# Edit .env — paste your OPENROUTER_API_KEY
```

### 3. Install & run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Or just:
```bash
bash start.sh
```

### 4. Open the app
- **Dashboard:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🤖 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET`  | `/api/health` | Health check + OpenRouter connectivity |
| `POST` | `/api/analyze` | Bug detection, complexity, quality score |
| `POST` | `/api/optimize` | AI code rewriter (fixes all issues) |
| `POST` | `/api/explain` | Plain English explanation |
| `POST` | `/api/security` | OWASP Top 10 security audit |
| `POST` | `/api/chat` | Multi-turn conversational AI |
| `GET`  | `/` | Serves frontend dashboard |

### Example: Analyze code
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def sort(arr):\n    for i in range(len(arr)):\n        for j in range(len(arr)-i-1):\n            if arr[j] < arr[j+1]:\n                arr[j],arr[j+1]=arr[j+1],arr[j]\n    return",
    "language": "auto"
  }'
```

### Example: Chat about code
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def sort(arr): ...",
    "language": "Python",
    "message": "Why is this code slow?",
    "history": []
  }'
```

---

## 🤖 Supported LLM Models (OpenRouter)

Change `OPENROUTER_MODEL` in `.env`:

| Model | Best For | Speed |
|-------|----------|-------|
| `qwen/qwen-2.5-coder-32b-instruct:free` | **Code tasks (recommended)** | Fast |
| `meta-llama/llama-3.3-70b-instruct:free` | General reasoning | Fast |
| `google/gemma-3-27b-it:free` | Balanced | Medium |
| `deepseek/deepseek-r1:free` | Deep reasoning | Slow |
| `mistralai/mistral-7b-instruct:free` | Lightweight | Very fast |

---

## 🌐 Supported Languages

Python · JavaScript · TypeScript · Java · C++ · Go · Rust · PHP · Ruby · Swift

---

## 🔐 Features

- **Bug Detection** — logic errors, wrong comparators, null dereferences, bare returns
- **Warning Analysis** — bad practices, debug statements, raw types
- **Code Optimization** — AI rewrites to production-ready code with type hints + docstrings
- **Big-O Complexity** — time and space complexity with before/after comparison
- **Security Audit** — OWASP Top 10: SQL injection, XSS, hardcoded secrets, insecure HTTP
- **Code Explanation** — plain English breakdown of algorithms and data flow
- **AI Chat** — multi-turn conversation about your code
- **Side-by-Side Diff** — colour-coded before/after view
- **Dark/Light Theme** — persisted in localStorage
- **Keyboard shortcut** — `Ctrl+Enter` to run analysis
