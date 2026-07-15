"""
Unit tests for Project Prometheus core engines
"""

import pytest
import asyncio
from backend.core.face_forensics import FaceForensicsEngine
from backend.core.academic_forensics import AcademicForensicsEngine
from backend.core.fusion_engine import MultimodalFusionEngine


class TestFaceForensicsEngine:
    """Test suite for FaceForensicsEngine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = FaceForensicsEngine()
    
    def test_engine_initialization(self):
        """Test that engine initializes correctly"""
        assert self.engine is not None
        assert self.engine.face_detector is not None
    
    def test_analyze_face_with_invalid_data(self):
        """Test analysis with invalid image data"""
        result = self.engine.analyze_face(b"invalid image data")
        assert result is not None
        assert 'anomalies' in result
        assert 'confidence' in result


class TestAcademicForensicsEngine:
    """Test suite for AcademicForensicsEngine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = AcademicForensicsEngine()
    
    def test_engine_initialization(self):
        """Test that engine initializes correctly"""
        assert self.engine is not None
        assert len(self.engine.ai_markers) > 0
    
    def test_analyze_text_with_short_text(self):
        """Test analysis with text that's too short"""
        result = self.engine.analyze_text("Short text")
        assert result is not None
        assert 'ai_likelihood' in result
        assert 'anomalies' in result
    
    def test_analyze_text_with_ai_markers(self):
        """Test analysis with text containing AI markers"""
        text = "It is imperative that we delve into this matter and leverage our capabilities."
        result = self.engine.analyze_text(text)
        assert result is not None
        assert result['ai_likelihood'] > 0
    
    def test_analyze_excel_with_simple_data(self):
        """Test Excel analysis with simple data"""
        data = "Name,Alice\nScore,95"
        result = self.engine.analyze_excel(data)
        assert result is not None
        assert 'anomaly_score' in result
    
    def test_analyze_code_with_simple_code(self):
        """Test code analysis with simple code"""
        code = "def hello():\n    print('Hello, World!')"
        result = self.engine.analyze_code(code)
        assert result is not None
        assert 'ai_likelihood' in result


class TestMultimodalFusionEngine:
    """Test suite for MultimodalFusionEngine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = MultimodalFusionEngine()
    
    def test_engine_initialization(self):
        """Test that engine initializes correctly"""
        assert self.engine is not None
        assert self.engine.face_engine is not None
        assert self.engine.academic_engine is not None
    
    @pytest.mark.asyncio
    async def test_analyze_all_with_text_only(self):
        """Test analysis with only text input"""
        input_data = {
            'text': 'This is a test text for analysis.',
            'student_id': 'test_student'
        }
        result = await self.engine.analyze_all(input_data)
        assert result is not None
        assert 'final_verdict' in result
        assert 'confidence' in result
    
    @pytest.mark.asyncio
    async def test_analyze_all_with_empty_input(self):
        """Test analysis with empty input"""
        input_data = {}
        result = await self.engine.analyze_all(input_data)
        assert result is not None
        assert result['final_verdict'] == 'Human-Verified'
    
    def test_analyze_single_modal_text(self):
        """Test single modal analysis for text"""
        result = self.engine.analyze_single_modal(
            'text',
            'This is a test text.',
            student_id='test_student'
        )
        assert result is not None
        assert 'ai_likelihood' in result


class TestChainOfCustodyTracker:
    """Test suite for ChainOfCustodyTracker"""
    
    def setup_method(self):
        """Setup test fixtures"""
        from backend.core.fusion_engine import ChainOfCustodyTracker
        self.tracker = ChainOfCustodyTracker()
    
    def test_create_case(self):
        """Test creating a new case"""
        case = self.tracker.create_case(
            'case_001',
            'student_123',
            {'description': 'Test submission'}
        )
        assert case is not None
        assert case['case_id'] == 'case_001'
        assert case['student_id'] == 'student_123'
    
    def test_add_analysis_result(self):
        """Test adding analysis results to a case"""
        self.tracker.create_case('case_001', 'student_123', {})
        self.tracker.add_analysis_result('case_001', {
            'final_verdict': 'AI-Generated',
            'confidence': 0.85
        })
        report = self.tracker.generate_report('case_001')
        assert len(report['analysis_history']) == 1
    
    def test_add_note(self):
        """Test adding notes to a case"""
        self.tracker.create_case('case_001', 'student_123', {})
        self.tracker.add_note('case_001', 'Test note', 'Professor')
        report = self.tracker.generate_report('case_001')
        assert len(report['notes']) == 1
        assert report['notes'][0]['note'] == 'Test note'
    
    def test_generate_report(self):
        """Test generating a case report"""
        self.tracker.create_case('case_001', 'student_123', {})
        report = self.tracker.generate_report('case_001')
        assert report is not None
        assert report['case_id'] == 'case_001'
        assert 'analysis_summary' in report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
