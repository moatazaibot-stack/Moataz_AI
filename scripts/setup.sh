#!/bin/bash
# Moataz AI — Development Setup Script
set -euo pipefail

echo "🔧 Moataz AI v1.0 — Development Setup"
echo "======================================"

# Check prerequisites
command -v bun &> /dev/null || { echo "❌ Bun not found. Install: https://bun.sh"; exit 1; }

echo "📦 Installing dependencies..."
bun install

echo "🗄️  Setting up database..."
cp .env.example .env.local 2>/dev/null || true
bun run db:push

echo "✅ Setup complete!"
echo ""
echo "   Start development: bun run dev"
echo "   Run tests:         bun test"
echo "   Build:             bun run build"
