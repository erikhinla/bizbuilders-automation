#!/bin/bash

# BizBuilders Automation - Quick Deploy Script
# This script helps you deploy the React frontend quickly

echo "🚀 BizBuilders Automation - Deployment Helper"
echo "=============================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Build the project
echo "🔨 Building project..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "📋 Deployment Options:"
echo ""
echo "1. Deploy to Vercel (Recommended - Easiest)"
echo "   Run: npx vercel"
echo ""
echo "2. Deploy to Netlify"
echo "   Run: npx netlify deploy --prod"
echo ""
echo "3. Deploy to Cloudflare Pages"
echo "   Run: npx wrangler pages deploy dist --project-name=bizbuilders-automation"
echo ""
echo "4. Serve locally (for testing)"
echo "   Run: npm run preview"
echo ""
echo "📁 Built files are in the 'dist' directory"
echo ""
echo "For detailed deployment instructions, see DEPLOYMENT_GUIDE.md"

