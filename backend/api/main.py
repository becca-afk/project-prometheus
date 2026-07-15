"""
Main FastAPI Application - Project Prometheus API

This is the complete API server for the AI detection system.
Provides endpoints for all detection modules and enterprise integrations.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import logging
import uvicorn
from datetime import datetime

# Import core engines
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.fusion_engine import MultimodalFusionEngine, ChainOfCustodyTracker
from core.face_forensics import FaceForensicsEngine, VideoForensicsEngine
from core.academic_forensics import AcademicForensicsEngine
from integrations.enterprise_hub import EnterpriseIntegrationHub, MockIntegrationHub

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Project Prometheus - Advanced AI Detection API",
    description="Enterprise-grade AI detection system for academic integrity and deepfake detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
fusion_engine = MultimodalFusionEngine()
custody_tracker = ChainOfCustodyTracker()
integration_hub = EnterpriseIntegrationHub()

# Use mock integration by default (can be switched to real integration)
mock_integration = MockIntegrationHub()

# Request/Response Models
class TextAnalysisRequest(BaseModel):
    text: str
    student_id: Optional[str] = None
    document_history: Optional[List[Dict]] = None

class ExcelAnalysisRequest(BaseModel):
    data: str
    version_history: Optional[List[Dict]] = None
    student_id: Optional[str] = None

class CodeAnalysisRequest(BaseModel):
    code: str
    student_id: Optional[str] = None

class GoogleDocRequest(BaseModel):
    doc_id: str
    credentials: Optional[Dict] = None
    student_id: Optional[str] = None

class GoogleSheetRequest(BaseModel):
    sheet_id: str
    credentials: Optional[Dict] = None
    student_id: Optional[str] = None

class MicrosoftWordRequest(BaseModel):
    file_id: str
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    student_id: Optional[str] = None

class CaseCreateRequest(BaseModel):
    case_id: str
    student_id: str
    submission_info: Dict[str, Any]

class CaseNoteRequest(BaseModel):
    note: str
    author: str


# Health Check Endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "fusion_engine": "operational",
            "face_forensics": "operational",
            "academic_forensics": "operational",
            "integration_hub": "operational"
        }
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Project Prometheus API",
        "description": "Advanced AI Detection System for Academic Integrity",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "analyze_complete": "/analyze/complete",
            "analyze_image": "/analyze/image",
            "analyze_text": "/analyze/text",
            "analyze_excel": "/analyze/excel",
            "analyze_code": "/analyze/code",
            "analyze_video": "/analyze/video",
            "integrations": "/integrations/*"
        }
    }


# Complete Analysis Endpoint
@app.post("/analyze/complete")
async def complete_analysis(
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    excel_data: Optional[str] = Form(None),
    code: Optional[str] = Form(None),
    student_id: Optional[str] = Form(None),
    use_mock_integration: bool = Form(False)
):
    """
    The ultimate endpoint - analyzes everything you throw at it.
    
    Supports:
    - Image upload (face/deepfake detection)
    - Video upload (video deepfake detection)
    - Text input (AI text detection)
    - Excel data (AI formula detection)
    - Code input (AI code detection)
    """
    input_data = {}
    
    # Process image
    if image:
        try:
            image_bytes = await image.read()
            input_data['image'] = image_bytes
        except Exception as e:
            logger.error(f"Error reading image: {str(e)}")
    
    # Process video
    if video:
        try:
            video_bytes = await video.read()
            input_data['video'] = video_bytes
        except Exception as e:
            logger.error(f"Error reading video: {str(e)}")
    
    # Process text
    if text:
        input_data['text'] = text
    
    # Process Excel data
    if excel_data:
        input_data['excel'] = excel_data
    
    # Process code
    if code:
        input_data['code'] = code
    
    # Add student ID if provided
    if student_id:
        input_data['student_id'] = student_id
    
    # Run analysis
    try:
        result = await fusion_engine.analyze_all(input_data)
        
        # Add educational context for teachers
        if result['final_verdict'] in ['AI-Generated', 'Suspicious']:
            result['teacher_notes'] = {
                "actions_to_take": [
                    "Request student to explain their work verbally",
                    "Check for sudden improvement in writing quality",
                    "Verify sources cited (AI often hallucinates references)",
                    "Review the document's revision history for paste events",
                    "Compare with student's previous work samples"
                ],
                "evidence_strength": result['confidence'],
                "recommended_hearing": "Academic integrity review recommended" if result['confidence'] > 0.7 else "Further investigation suggested",
                "detection_methods_used": result['chain_of_custody']['analysis_modules_used']
            }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in complete analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Image Analysis Endpoint
@app.post("/analyze/image")
async def analyze_image(
    image: UploadFile = File(...),
    student_id: Optional[str] = Form(None)
):
    """
    Analyze an image for deepfake/face swap detection.
    """
    try:
        image_bytes = await image.read()
        
        # Run face analysis
        result = fusion_engine.face_engine.analyze_face(image_bytes)
        
        # Add metadata
        result['analysis_metadata'] = {
            "filename": image.filename,
            "content_type": image.content_type,
            "student_id": student_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Video Analysis Endpoint
@app.post("/analyze/video")
async def analyze_video(
    video: UploadFile = File(...),
    student_id: Optional[str] = Form(None)
):
    """
    Analyze a video for deepfake detection.
    """
    try:
        video_bytes = await video.read()
        
        # Run video analysis
        result = fusion_engine.video_engine.analyze_video(video_bytes)
        
        # Add metadata
        result['analysis_metadata'] = {
            "filename": video.filename,
            "content_type": video.content_type,
            "student_id": student_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in video analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Text Analysis Endpoint
@app.post("/analyze/text")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text for AI generation detection.
    """
    try:
        result = fusion_engine.academic_engine.analyze_text(
            request.text,
            request.student_id,
            request.document_history
        )
        
        # Add metadata
        result['analysis_metadata'] = {
            "student_id": request.student_id,
            "text_length": len(request.text),
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in text analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Excel Analysis Endpoint
@app.post("/analyze/excel")
async def analyze_excel(request: ExcelAnalysisRequest):
    """
    Analyze Excel/Google Sheets data for AI-generated formulas.
    """
    try:
        result = fusion_engine.academic_engine.analyze_excel(
            request.data,
            request.version_history
        )
        
        # Add metadata
        result['analysis_metadata'] = {
            "student_id": request.student_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in Excel analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Code Analysis Endpoint
@app.post("/analyze/code")
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code for AI generation detection.
    """
    try:
        result = fusion_engine.academic_engine.analyze_code(
            request.code,
            request.student_id
        )
        
        # Add metadata
        result['analysis_metadata'] = {
            "student_id": request.student_id,
            "code_length": len(request.code),
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in code analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Google Docs Integration Endpoint
@app.post("/integrations/google-doc")
async def analyze_google_doc(request: GoogleDocRequest):
    """
    Connect to Google Docs and analyze a document with full revision history.
    """
    try:
        # Use mock integration by default for testing
        doc_data = mock_integration.fetch_google_doc_with_revisions(request.doc_id)
        
        # Analyze the content with academic forensics
        text_result = fusion_engine.academic_engine.analyze_text(
            doc_data['content'],
            request.student_id,
            doc_data.get('revision_history')
        )
        
        # Combine results
        result = {
            "google_doc_data": doc_data,
            "analysis_result": text_result,
            "integration_metadata": {
                "platform": "google_docs",
                "doc_id": request.doc_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in Google Docs integration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Google Sheets Integration Endpoint
@app.post("/integrations/google-sheet")
async def analyze_google_sheet(request: GoogleSheetRequest):
    """
    Connect to Google Sheets and analyze with version history.
    """
    try:
        # Use mock integration by default
        sheet_data = mock_integration.fetch_google_sheet_with_revisions(request.sheet_id)
        
        # Convert sheet data to string format for analysis
        data_str = str(sheet_data['data'])
        
        # Analyze with Excel forensics
        excel_result = fusion_engine.academic_engine.analyze_excel(
            data_str,
            sheet_data.get('revision_history')
        )
        
        # Combine results
        result = {
            "google_sheet_data": sheet_data,
            "analysis_result": excel_result,
            "integration_metadata": {
                "platform": "google_sheets",
                "sheet_id": request.sheet_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in Google Sheets integration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Microsoft Word Integration Endpoint
@app.post("/integrations/microsoft-word")
async def analyze_microsoft_word(request: MicrosoftWordRequest):
    """
    Connect to Microsoft Word and analyze a document with version history.
    """
    try:
        # Use mock integration by default
        word_data = mock_integration.fetch_microsoft_word_with_revisions(request.file_id)
        
        # Analyze the content
        text_result = fusion_engine.academic_engine.analyze_text(
            word_data['content'],
            request.student_id,
            word_data.get('versions')
        )
        
        # Combine results
        result = {
            "microsoft_word_data": word_data,
            "analysis_result": text_result,
            "integration_metadata": {
                "platform": "microsoft_word",
                "file_id": request.file_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in Microsoft Word integration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Microsoft Excel Integration Endpoint
@app.post("/integrations/microsoft-excel")
async def analyze_microsoft_excel(request: MicrosoftWordRequest):
    """
    Connect to Microsoft Excel and analyze with version history.
    """
    try:
        # Use mock integration by default
        excel_data = mock_integration.fetch_microsoft_excel_with_versions(request.file_id)
        
        # Convert data to string format
        data_str = str(excel_data['data'])
        
        # Analyze with Excel forensics
        excel_result = fusion_engine.academic_engine.analyze_excel(
            data_str,
            excel_data.get('versions')
        )
        
        # Combine results
        result = {
            "microsoft_excel_data": excel_data,
            "analysis_result": excel_result,
            "integration_metadata": {
                "platform": "microsoft_excel",
                "file_id": request.file_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in Microsoft Excel integration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Chain of Custody Endpoints
@app.post("/custody/create-case")
async def create_case(request: CaseCreateRequest):
    """
    Create a new academic integrity case with chain of custody tracking.
    """
    try:
        case = custody_tracker.create_case(
            request.case_id,
            request.student_id,
            request.submission_info
        )
        return JSONResponse(content=case)
        
    except Exception as e:
        logger.error(f"Error creating case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/custody/{case_id}/add-analysis")
async def add_analysis_to_case(case_id: str, analysis_result: Dict[str, Any]):
    """
    Add analysis results to an existing case.
    """
    try:
        custody_tracker.add_analysis_result(case_id, analysis_result)
        return {"status": "success", "message": "Analysis added to case"}
        
    except Exception as e:
        logger.error(f"Error adding analysis to case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/custody/{case_id}/add-note")
async def add_note_to_case(case_id: str, request: CaseNoteRequest):
    """
    Add a note to a case (for professor/admin use).
    """
    try:
        custody_tracker.add_note(case_id, request.note, request.author)
        return {"status": "success", "message": "Note added to case"}
        
    except Exception as e:
        logger.error(f"Error adding note to case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/custody/{case_id}/report")
async def get_case_report(case_id: str):
    """
    Generate a comprehensive chain of custody report for a case.
    """
    try:
        report = custody_tracker.generate_report(case_id)
        return JSONResponse(content=report)
        
    except Exception as e:
        logger.error(f"Error generating case report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Integration Connection Endpoints
@app.post("/integrations/connect-google")
async def connect_google(credentials: Dict[str, Any]):
    """
    Connect to Google Workspace APIs.
    """
    try:
        success = integration_hub.connect_google(credentials)
        return {
            "status": "success" if success else "failed",
            "connection_status": integration_hub.get_connection_status()
        }
        
    except Exception as e:
        logger.error(f"Error connecting to Google: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/integrations/connect-microsoft")
async def connect_microsoft(
    tenant_id: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...)
):
    """
    Connect to Microsoft 365 APIs.
    """
    try:
        success = integration_hub.connect_microsoft(tenant_id, client_id, client_secret)
        return {
            "status": "success" if success else "failed",
            "connection_status": integration_hub.get_connection_status()
        }
        
    except Exception as e:
        logger.error(f"Error connecting to Microsoft: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/integrations/status")
async def get_integration_status():
    """
    Get current connection status for all integration platforms.
    """
    return integration_hub.get_connection_status()


# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
