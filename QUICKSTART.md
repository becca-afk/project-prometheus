# Quick Start Guide

Get Project Prometheus up and running in 5 minutes.

## Prerequisites Check

Ensure you have:
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/project-prometheus.git
cd project-prometheus
```

## Step 2: Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp backend/.env.example backend/.env
```

## Step 3: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Go back to root
cd ..
```

## Step 4: Start the Services

**Terminal 1 - Backend:**
```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Start the backend server
cd backend
python -m api.main
```

**Terminal 2 - Frontend:**
```bash
# Start the frontend server
cd frontend
npm start
```

## Step 5: Access the Application

- **Frontend**: Open http://localhost:3000 in your browser
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Quick Test

### Test Text Analysis

1. Open http://localhost:3000
2. Navigate to "Text Analysis"
3. Paste some text and click "Analyze"
4. View the AI detection results

### Test Image Analysis

1. Navigate to "Image Analysis"
2. Upload an image
3. Click "Analyze Image"
4. View the deepfake detection results

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in backend/.env
API_PORT=8001
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Port already in use:**
```bash
# The React dev server will automatically suggest an alternative port
# or kill the process using port 3000
```

**Module not found:**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Read the full [README.md](README.md)
- Configure Google/Microsoft integrations
- Download optional face detection models
- Set up chain of custody tracking

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/project-prometheus/issues
- Documentation: https://docs.projectprometheus.ai
