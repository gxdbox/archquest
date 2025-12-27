#!/bin/bash

# ArchQuest 启动脚本
# Quick start script for ArchQuest

echo "🎮 Starting ArchQuest..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# 检查 Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first."
    echo "Visit: https://ollama.com/"
    exit 1
fi

# 检查依赖
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt

# 检查 Ollama 服务
if ! curl -s http://localhost:11434/ > /dev/null 2>&1; then
    echo "⚠️  Ollama service not running. Starting Ollama..."
    echo "Please run 'ollama serve' in another terminal first."
    exit 1
fi

# 检查模型
if ! ollama list | grep -q "qwen:7b"; then
    echo "📥 Downloading qwen:7b model (this may take a while)..."
    ollama pull qwen:7b
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "🚀 Starting backend on http://localhost:8000"
echo "🎨 Starting frontend on http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# 启动后端
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
python3 -m streamlit run frontend/app.py --server.port 8501 &
FRONTEND_PID=$!

# 等待用户中断
wait

# 清理
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo ""
echo "👋 ArchQuest stopped. See you next time!"
