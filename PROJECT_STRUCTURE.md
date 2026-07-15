# Project Structure

```
ai fetector/
├── backend/
│   ├── api/
│   │   └── main.py                 # FastAPI application with all endpoints
│   ├── core/
│   │   ├── __init__.py             # Core module initialization
│   │   ├── face_forensics.py       # Deepfake & face swap detection
│   │   ├── academic_forensics.py   # Text/Excel/code AI detection
│   │   └── fusion_engine.py        # Multimodal fusion & chain of custody
│   ├── integrations/
│   │   ├── __init__.py             # Integrations module initialization
│   │   └── enterprise_hub.py       # Google/Microsoft API connectors
│   ├── config.py                   # Application configuration
│   └── .env.example                # Environment variables template
├── frontend/
│   ├── public/
│   │   └── index.html              # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Navigation bar
│   │   │   ├── Home.jsx            # Landing page
│   │   │   ├── ImageAnalysis.jsx   # Image analysis interface
│   │   │   ├── TextAnalysis.jsx    # Text analysis interface
│   │   │   ├── VideoAnalysis.jsx   # Video analysis interface
│   │   │   ├── ExcelAnalysis.jsx   # Excel analysis interface
│   │   │   ├── CodeAnalysis.jsx    # Code analysis interface
│   │   │   ├── Integrations.jsx    # Enterprise integrations UI
│   │   │   └── ChainOfCustody.jsx  # Chain of custody management
│   │   ├── App.jsx                 # Main React application
│   │   ├── App.css                 # Global styles
│   │   └── index.js                # React entry point
│   ├── package.json                # Node.js dependencies
│   ├── Dockerfile                  # Docker configuration for frontend
│   └── nginx.conf                  # Nginx configuration
├── models/                         # Directory for ML model files
├── tests/
│   ├── __init__.py                 # Test module initialization
│   └── test_core.py                # Core engine unit tests
├── logs/                           # Application logs directory
├── .gitignore                      # Git ignore rules
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_STRUCTURE.md            # This file
├── requirements.txt                # Python dependencies
├── setup.py                        # Python package setup
├── Dockerfile                      # Docker configuration for backend
└── docker-compose.yml              # Multi-container Docker setup
```

## Module Descriptions

### Backend Core Modules

#### `face_forensics.py`
- **FaceForensicsEngine**: Detects deepfakes and face swaps using 7 biometric signals
- **VideoForensicsEngine**: Extends face detection to video with temporal analysis
- Key methods: `analyze_face()`, `analyze_video()`

#### `academic_forensics.py`
- **AcademicForensicsEngine**: Detects AI-generated text, Excel formulas, and code
- Key methods: `analyze_text()`, `analyze_excel()`, `analyze_code()`
- Features: Stylometric fingerprinting, burstiness analysis, revision history analysis

#### `fusion_engine.py`
- **MultimodalFusionEngine**: Combines all detection modules into unified verdicts
- **ChainOfCustodyTracker**: Manages academic integrity cases with audit trails
- Key methods: `analyze_all()`, `analyze_single_modal()`

### Backend Integration Modules

#### `enterprise_hub.py`
- **EnterpriseIntegrationHub**: Connects to Google Workspace and Microsoft 365 APIs
- **MockIntegrationHub**: Testing implementation without real credentials
- Key methods: `fetch_google_doc_with_revisions()`, `fetch_microsoft_word_with_revisions()`

### Backend API

#### `main.py`
- FastAPI application with 15+ endpoints
- Endpoints for all detection types, integrations, and chain of custody
- Includes CORS middleware and static file serving

### Frontend Components

#### Analysis Components
- **ImageAnalysis**: Upload and analyze images for deepfakes
- **TextAnalysis**: Paste text for AI generation detection
- **VideoAnalysis**: Upload videos for temporal deepfake detection
- **ExcelAnalysis**: Analyze spreadsheet data for AI formulas
- **CodeAnalysis**: Analyze source code for AI generation

#### System Components
- **Home**: Landing page with feature overview
- **Integrations**: Configure and use enterprise platform connections
- **ChainOfCustody**: Manage academic integrity cases
- **Navbar**: Navigation with dark/light mode toggle

## Data Flow

### Detection Flow
```
User Input → Frontend Component → API Endpoint → Core Engine → Analysis Result
                                                              ↓
                                                    Fusion Engine (if multi-modal)
                                                              ↓
                                                    Final Verdict + Evidence
```

### Integration Flow
```
Platform Credentials → Enterprise Hub → API Authentication → Document Fetch
                                                              ↓
                                                    Revision History Extraction
                                                              ↓
                                                    Academic Forensics Analysis
```

### Chain of Custody Flow
```
Case Creation → Analysis Results → Notes Addition → Report Generation
                                                              ↓
                                                    Academic Hearing Evidence
```

## Configuration Files

### Environment Variables (.env)
- API configuration (host, port, debug mode)
- Google/Microsoft OAuth credentials
- Model file paths
- Database connection
- File upload limits

### Dependencies
- **requirements.txt**: Python packages with version pinning
- **package.json**: Node.js packages for React frontend

### Docker Configuration
- **Dockerfile**: Backend container image
- **docker-compose.yml**: Multi-container orchestration
- **nginx.conf**: Frontend web server configuration

## Testing Structure

### Unit Tests
- Located in `tests/test_core.py`
- Tests for all core engines
- Async and sync test coverage
- Chain of custody tracking tests

### Test Execution
```bash
# Run all tests
pytest tests/

# Run specific test class
pytest tests/test_core.py::TestFaceForensicsEngine

# Run with coverage
pytest tests/ --cov=backend
```

## Deployment Options

### Development
- Backend: `python -m backend.api.main`
- Frontend: `npm start`

### Production Docker
- Single command: `docker-compose up -d`
- Separate containers for backend and frontend
- Nginx reverse proxy for frontend

### Manual Production
- Backend: Gunicorn/Uvicorn with multiple workers
- Frontend: Nginx serving static build files
- Database: PostgreSQL for chain of custody persistence

## Extension Points

### Adding New Detection Modules
1. Create new engine class in `backend/core/`
2. Add to `MultimodalFusionEngine` weights
3. Create corresponding API endpoint
4. Build frontend component if needed

### Adding New Integrations
1. Extend `EnterpriseIntegrationHub` class
2. Add authentication flow
3. Implement document fetching logic
4. Create frontend integration UI

### Custom Models
1. Place model files in `models/` directory
2. Update model paths in `.env`
3. Modify engine initialization to load custom models
4. Add model-specific analysis methods
