"""
Core AI Detection Engines
"""

from .face_forensics import FaceForensicsEngine, VideoForensicsEngine
from .academic_forensics import AcademicForensicsEngine
from .fusion_engine import MultimodalFusionEngine, ChainOfCustodyTracker

__all__ = [
    'FaceForensicsEngine',
    'VideoForensicsEngine',
    'AcademicForensicsEngine',
    'MultimodalFusionEngine',
    'ChainOfCustodyTracker'
]
