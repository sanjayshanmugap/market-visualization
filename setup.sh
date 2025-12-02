#!/bin/bash

# Setup script for Data Visualization Portfolio

set -e

echo "🚀 Setting up Data Visualization Portfolio..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check for Homebrew (needed for Manim dependencies on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew not found. Manim installation may fail."
        echo "   Install Homebrew: https://brew.sh"
        echo "   Then run: brew install pkg-config cairo pango ffmpeg"
    else
        echo "📦 Checking Manim system dependencies..."
        # Check if required system packages are installed
        if ! brew list pkg-config &> /dev/null 2>&1 || ! brew list cairo &> /dev/null 2>&1; then
            echo "📦 Installing Manim system dependencies (pkg-config, cairo, pango, ffmpeg)..."
            brew install pkg-config cairo pango ffmpeg 2>&1 || echo "⚠️  Failed to install some dependencies. Manim may not work correctly."
        else
            echo "✓ Manim system dependencies already installed"
        fi
    fi
fi

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd src/ui
npm install
cd ../..

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/viz/{static,data,stories}
mkdir -p data/cache

echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start API server: npm run api (or: uvicorn src.api.main:app --reload)"
echo "  3. Start frontend: npm run dev (or: cd src/ui && npm run dev)"
echo "  4. Generate sample stories: python scripts/generate_stories.py"
echo "  5. Generate Manim animations: python scripts/generate_manim_animations.py"

