#!/bin/bash
# ─────────────────────────────────────────────────────────────
# CodeRefine AI — Quick Start
# ─────────────────────────────────────────────────────────────

set -e
cd "$(dirname "$0")"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       CodeRefine AI — Quick Start                ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# 1. Check .env
# FIX: was `cp .env.example .env` which failed because .env.example didn't exist in zip
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "📋 Creating .env from template..."
    cp .env.example .env
  else
    echo "📋 Creating .env with defaults..."
    cat > .env << 'ENVEOF'
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=qwen/qwen-2.5-coder-32b-instruct:free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
ENVEOF
  fi
  echo ""
  echo "⚠️  ACTION REQUIRED:"
  echo "   Open .env and set your OPENROUTER_API_KEY"
  echo "   Get a free key at: https://openrouter.ai/keys"
  echo ""
  read -p "Press Enter after setting your API key..."
fi

# 2. Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🚀 Starting CodeRefine AI..."
echo "   App:  http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

# 3. Run
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
