# ✦ BrandCraft — Generative AI-Powered Branding Automation System

A full-stack AI branding platform that automates brand name generation, logo creation, content writing, sentiment analysis, and brand consulting — powered by Gemini, Stable Diffusion, and IBM Watson.

---

## 🚀 Quick Start (5 minutes)

### 1. Clone & Setup

```bash
cd brandcraft
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your keys (see below)
```

### 3. Run the App

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Open: **http://localhost:8000**

---

## 🔑 Getting API Keys

### Gemini API (Required — Free)
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy into `GEMINI_API_KEY`

### Hugging Face Token (Required for Logo — Free)
1. Create account at https://huggingface.co
2. Go to Settings > Access Tokens
3. Create a token with **Read** permissions
4. Copy into `HF_TOKEN`

### IBM Watson NLU (Optional — Free Tier)
1. Go to https://cloud.ibm.com/catalog/services/natural-language-understanding
2. Create a **Lite** (free) instance
3. Go to Manage > Credentials
4. Copy API key → `IBM_API_KEY`
5. Copy the URL → `IBM_URL`
> If IBM keys are not set, the app falls back to basic keyword-based sentiment analysis automatically.

---

## 📁 Project Structure

```
brandcraft/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── routes/
│   │   ├── brand_name.py        # POST /api/brand-name
│   │   ├── logo.py              # POST /api/logo
│   │   ├── content.py           # POST /api/content
│   │   ├── sentiment.py         # POST /api/sentiment
│   │   └── assistant.py         # POST /api/assistant
│   └── services/
│       ├── gemini_service.py    # Gemini AI integration
│       ├── diffusion_service.py # Hugging Face SD integration
│       └── ibm_service.py       # IBM Watson NLU integration
├── frontend/
│   └── index.html               # Complete SPA (HTML + CSS + JS)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠 Features

| Feature | Endpoint | Powered By |
|---|---|---|
| Brand Name Generator | `POST /api/brand-name` | Gemini 1.5 Flash |
| Logo Generator | `POST /api/logo` | Stable Diffusion XL |
| Content Automation | `POST /api/content` | Gemini 1.5 Flash |
| Sentiment Analysis | `POST /api/sentiment` | IBM Watson NLU |
| Brand Assistant | `POST /api/assistant` | Gemini 1.5 Flash |

---

## 🧪 Test the API

Use the interactive Swagger docs at: **http://localhost:8000/docs**

Or test with curl:
```bash
# Generate brand names
curl -X POST http://localhost:8000/api/brand-name \
  -H "Content-Type: application/json" \
  -d '{"niche": "sustainable coffee", "tone": "friendly", "audience": "millennials"}'

# Generate content
curl -X POST http://localhost:8000/api/content \
  -H "Content-Type: application/json" \
  -d '{"brand_name": "Bloom", "niche": "organic coffee", "content_type": "tagline", "tone": "warm"}'
```

---

## ⚡ Tech Stack

- **Backend**: FastAPI + Uvicorn (Python)
- **Frontend**: Vanilla HTML/CSS/JS (single file SPA)
- **AI Models**:
  - Google Gemini 1.5 Flash — text generation
  - Stable Diffusion XL — image generation via HuggingFace API
  - IBM Watson NLU — sentiment & emotion analysis
