#!/bin/bash

# Install Python dependencies
cd /workspace/backend
pip install -r requirements.txt

# Install Node dependencies
cd /workspace/frontend
npm install

# Create necessary directories
mkdir -p /workspace/logs
mkdir -p /workspace/models

# Copy environment file
cd /workspace/backend
if [ ! -f .env ]; then
    cp .env.example .env
fi

echo "✅ Development environment setup complete!"
echo "🚀 Run 'cd backend && python -m api.main' to start the backend"
echo "🌐 Run 'cd frontend && npm start' to start the frontend"
