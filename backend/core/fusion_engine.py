"""
MultimodalFusionEngine - Master Judge for Unified Analysis

This module combines results from all detection modules into a single verdict
using weighted ensemble with confidence calibration.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional
import numpy as np
import logging
from datetime import datetime

from .face_forensics import FaceForensicsEngine, VideoForensicsEngine
from .academic_forensics import AcademicForensicsEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultimodalFusionEngine:
    """
    Combines results from all detection modules into a single verdict.
    Uses a weighted ensemble with confidence calibration.
    """
    
    def __init__(self):
        self.face_engine = FaceForensicsEngine()
        self.video_engine = VideoForensicsEngine()
        self.academic_engine = AcademicForensicsEngine()
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Weights for each modality (tuned for academic integrity use cases)
        self.weights = {
            "face_swap": 0.30,
            "video_deepfake": 0.25,
            "text_ai": 0.25,
            "excel_ai": 0.12,
            "code_ai": 0.08
        }
        
        # Detection thresholds
        self.thresholds = {
            "definitely_ai": 0.75,
            "suspicious": 0.50,
            "likely_human": 0.25
        }
    
    async def analyze_all(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Master analysis function that runs all applicable detection modules.
        
        Input data can contain:
        - 'image': bytes (for face analysis)
        - 'video': bytes (for video deepfake analysis)
        - 'text': str (for AI text detection)
        - 'excel': str or bytes (for Excel formula analysis)
        - 'code': str (for AI code detection)
        - 'student_id': str (for style comparison)
        - 'document_history': list of revisions (for Google Docs/Word)
        - 'version_history': list of Excel revisions
        
        Returns:
            Comprehensive analysis report with final verdict
        """
        tasks = []
        task_names = []
        
        # Determine which analyses to run
        if 'image' in input_data:
            tasks.append(self._run_face_analysis(input_data['image']))
            task_names.append('face')
        else:
            tasks.append(asyncio.sleep(0, result=None))
            task_names.append('face')
            
        if 'video' in input_data:
            tasks.append(self._run_video_analysis(input_data['video']))
            task_names.append('video')
        else:
            tasks.append(asyncio.sleep(0, result=None))
            task_names.append('video')
            
        if 'text' in input_data:
            tasks.append(self._run_text_analysis(
                input_data['text'],
                input_data.get('student_id'),
                input_data.get('document_history')
            ))
            task_names.append('text')
        else:
            tasks.append(asyncio.sleep(0, result=None))
            task_names.append('text')
            
        if 'excel' in input_data:
            tasks.append(self._run_excel_analysis(
                input_data['excel'],
                input_data.get('version_history')
            ))
            task_names.append('excel')
        else:
            tasks.append(asyncio.sleep(0, result=None))
            task_names.append('excel')
        
        if 'code' in input_data:
            tasks.append(self._run_code_analysis(
                input_data['code'],
                input_data.get('student_id')
            ))
            task_names.append('code')
        else:
            tasks.append(asyncio.sleep(0, result=None))
            task_names.append('code')
        
        # Run all tasks in parallel
        results_list = await asyncio.gather(*tasks)
        
        # Map results back to task names
        results_dict = dict(zip(task_names, results_list))
        
        # Build comprehensive report
        report = self._build_comprehensive_report(results_dict, input_data)
        
        return report
    
    def _build_comprehensive_report(self, results_dict: Dict[str, Any], 
                                    input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build the final comprehensive analysis report"""
        report = {
            "final_verdict": "Human-Verified",
            "confidence": 0.0,
            "analysis_timestamp": datetime.now().isoformat(),
            "layer_results": {
                "face_forensics": results_dict.get('face'),
                "video_forensics": results_dict.get('video'),
                "academic_forensics": results_dict.get('text'),
                "excel_forensics": results_dict.get('excel'),
                "code_forensics": results_dict.get('code')
            },
            "evidence": [],
            "recommendations": [],
            "chain_of_custody": {
                "student_id": input_data.get('student_id', 'unknown'),
                "analysis_modules_used": [],
                "data_types_analyzed": []
            }
        }
        
        # Calculate weighted score
        total_score = 0.0
        total_weight = 0.0
        
        # Face analysis
        face_result = results_dict.get('face')
        if face_result and face_result.get('confidence', 0) > 0:
            weight = self.weights['face_swap']
            score = face_result.get('confidence', 0)
            total_score += score * weight
            total_weight += weight
            
            report['chain_of_custody']['analysis_modules_used'].append('face_forensics')
            report['chain_of_custody']['data_types_analyzed'].append('image')
            
            if face_result.get('face_swap_detected'):
                report['evidence'].append({
                    "type": "Face swap detected",
                    "severity": "high",
                    "detail": "Biometric anomalies found in facial structure",
                    "confidence": score,
                    "anomalies_count": len(face_result.get('anomalies', []))
                })
            elif face_result.get('synthesis_detected'):
                report['evidence'].append({
                    "type": "AI-generated face detected",
                    "severity": "medium",
                    "detail": "Synthetic face characteristics identified",
                    "confidence": score,
                    "anomalies_count": len(face_result.get('anomalies', []))
                })
        
        # Video analysis
        video_result = results_dict.get('video')
        if video_result and video_result.get('confidence', 0) > 0:
            weight = self.weights['video_deepfake']
            score = video_result.get('confidence', 0)
            total_score += score * weight
            total_weight += weight
            
            report['chain_of_custody']['analysis_modules_used'].append('video_forensics')
            report['chain_of_custody']['data_types_analyzed'].append('video')
            
            if video_result.get('deepfake_detected'):
                report['evidence'].append({
                    "type": "Video deepfake detected",
                    "severity": "high",
                    "detail": "Temporal inconsistencies found in video",
                    "confidence": score,
                    "anomalies_count": len(video_result.get('anomalies', []))
                })
        
        # Text analysis
        text_result = results_dict.get('text')
        if text_result:
            weight = self.weights['text_ai']
            score = text_result.get('ai_likelihood', 0)
            total_score += score * weight
            total_weight += weight
            
            report['chain_of_custody']['analysis_modules_used'].append('academic_forensics')
            report['chain_of_custody']['data_types_analyzed'].append('text')
            
            if score > self.thresholds['suspicious']:
                report['evidence'].append({
                    "type": "AI-generated text detected",
                    "severity": "high" if score > self.thresholds['definitely_ai'] else "medium",
                    "detail": f"Stylometric anomalies: {len(text_result.get('anomalies', []))} indicators",
                    "confidence": score,
                    "anomalies_count": len(text_result.get('anomalies', []))
                })
        
        # Excel analysis
        excel_result = results_dict.get('excel')
        if excel_result and excel_result.get('anomaly_score', 0) > 0:
            weight = self.weights['excel_ai']
            score = excel_result.get('anomaly_score', 0)
            total_score += score * weight
            total_weight += weight
            
            report['chain_of_custody']['analysis_modules_used'].append('excel_forensics')
            report['chain_of_custody']['data_types_analyzed'].append('excel')
            
            if score > self.thresholds['suspicious']:
                report['evidence'].append({
                    "type": "AI-generated Excel formulas",
                    "severity": "medium",
                    "detail": f"Found {len(excel_result.get('ai_generated_formulas', []))} suspicious formulas",
                    "confidence": score,
                    "anomalies_count": len(excel_result.get('ai_generated_formulas', []))
                })
        
        # Code analysis
        code_result = results_dict.get('code')
        if code_result and code_result.get('ai_likelihood', 0) > 0:
            weight = self.weights['code_ai']
            score = code_result.get('ai_likelihood', 0)
            total_score += score * weight
            total_weight += weight
            
            report['chain_of_custody']['analysis_modules_used'].append('code_forensics')
            report['chain_of_custody']['data_types_analyzed'].append('code')
            
            if score > self.thresholds['suspicious']:
                report['evidence'].append({
                    "type": "AI-generated code detected",
                    "severity": "medium",
                    "detail": f"Code anomalies: {len(code_result.get('anomalies', []))} indicators",
                    "confidence": score,
                    "anomalies_count": len(code_result.get('anomalies', []))
                })
        
        # Calculate final score
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.0
        
        # Determine verdict
        if final_score > self.thresholds['definitely_ai']:
            report['final_verdict'] = "AI-Generated"
            report['confidence'] = final_score
            report['recommendations'].extend([
                "Immediate academic integrity review recommended",
                "Request student to explain their work verbally",
                "Verify sources cited (AI often hallucinates references)",
                "Review document revision history for paste events",
                "Consider formal academic dishonesty proceedings"
            ])
        elif final_score > self.thresholds['suspicious']:
            report['final_verdict'] = "Suspicious"
            report['confidence'] = final_score
            report['recommendations'].extend([
                "Manual review recommended",
                "Discuss with student about their work process",
                "Check for sudden improvement in quality",
                "Verify cited sources and references"
            ])
        elif final_score > self.thresholds['likely_human']:
            report['final_verdict'] = "Likely Human"
            report['confidence'] = 1 - final_score
            report['recommendations'].append("No immediate action required")
        else:
            report['final_verdict'] = "Human-Verified"
            report['confidence'] = 1 - final_score
            report['recommendations'].append("Work appears to be human-generated")
        
        # Add educational context for teachers
        if report['final_verdict'] in ['AI-Generated', 'Suspicious']:
            report['teacher_notes'] = {
                "actions_to_take": [
                    "Request student to explain their work verbally",
                    "Check for sudden improvement in writing quality",
                    "Verify sources cited (AI often hallucinates references)",
                    "Review the document's revision history for paste events",
                    "Compare with student's previous work samples"
                ],
                "evidence_strength": report['confidence'],
                "recommended_hearing": "Academic integrity review recommended" if final_score > 0.7 else "Further investigation suggested",
                "detection_methods_used": report['chain_of_custody']['analysis_modules_used']
            }
        
        return report
    
    async def _run_face_analysis(self, image_bytes: bytes):
        """Run face analysis in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, self.face_engine.analyze_face, image_bytes
        )
    
    async def _run_video_analysis(self, video_bytes: bytes):
        """Run video analysis in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, self.video_engine.analyze_video, video_bytes
        )
    
    async def _run_text_analysis(self, text: str, student_id: Optional[str], 
                                history: Optional[list]):
        """Run text analysis in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.academic_engine.analyze_text,
            text, student_id, history
        )
    
    async def _run_excel_analysis(self, excel_data: str, version_history: Optional[list]):
        """Run Excel analysis in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.academic_engine.analyze_excel,
            excel_data, version_history
        )
    
    async def _run_code_analysis(self, code: str, student_id: Optional[str]):
        """Run code analysis in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.academic_engine.analyze_code,
            code, student_id
        )
    
    def analyze_single_modal(self, data_type: str, data: Any, 
                            **kwargs) -> Dict[str, Any]:
        """
        Analyze a single modality (synchronous version for simple cases).
        
        Args:
            data_type: Type of data ('image', 'text', 'excel', 'code')
            data: The actual data to analyze
            **kwargs: Additional parameters (student_id, history, etc.)
            
        Returns:
            Analysis results for the single modality
        """
        try:
            if data_type == 'image':
                return self.face_engine.analyze_face(data)
            elif data_type == 'text':
                return self.academic_engine.analyze_text(
                    data,
                    kwargs.get('student_id'),
                    kwargs.get('document_history')
                )
            elif data_type == 'excel':
                return self.academic_engine.analyze_excel(
                    data,
                    kwargs.get('version_history')
                )
            elif data_type == 'code':
                return self.academic_engine.analyze_code(
                    data,
                    kwargs.get('student_id')
                )
            else:
                return {
                    "error": f"Unknown data type: {data_type}",
                    "anomalies": []
                }
        except Exception as e:
            logger.error(f"Error in single modal analysis: {str(e)}")
            return {
                "error": str(e),
                "anomalies": [{
                    "test": "Analysis error",
                    "finding": str(e),
                    "value": "error"
                }]
            }


class ChainOfCustodyTracker:
    """
    Tracks the chain of custody for academic integrity cases.
    Provides audit trails for formal proceedings.
    """
    
    def __init__(self):
        self.cases = {}
    
    def create_case(self, case_id: str, student_id: str, submission_info: Dict) -> Dict:
        """Create a new academic integrity case"""
        case = {
            "case_id": case_id,
            "student_id": student_id,
            "created_at": datetime.now().isoformat(),
            "submission_info": submission_info,
            "analysis_history": [],
            "status": "open",
            "notes": []
        }
        self.cases[case_id] = case
        return case
    
    def add_analysis_result(self, case_id: str, analysis_result: Dict):
        """Add analysis results to a case"""
        if case_id in self.cases:
            self.cases[case_id]['analysis_history'].append({
                "timestamp": datetime.now().isoformat(),
                "result": analysis_result
            })
    
    def add_note(self, case_id: str, note: str, author: str):
        """Add a note to the case (for professor/admin use)"""
        if case_id in self.cases:
            self.cases[case_id]['notes'].append({
                "timestamp": datetime.now().isoformat(),
                "note": note,
                "author": author
            })
    
    def generate_report(self, case_id: str) -> Dict:
        """Generate a comprehensive chain of custody report"""
        if case_id not in self.cases:
            return {"error": "Case not found"}
        
        case = self.cases[case_id]
        
        return {
            "case_id": case['case_id'],
            "student_id": case['student_id'],
            "created_at": case['created_at'],
            "submission_info": case['submission_info'],
            "analysis_summary": self._summarize_analyses(case['analysis_history']),
            "notes": case['notes'],
            "status": case['status'],
            "report_generated_at": datetime.now().isoformat()
        }
    
    def _summarize_analyses(self, analysis_history: list) -> Dict:
        """Summarize all analyses performed on the case"""
        if not analysis_history:
            return {"total_analyses": 0}
        
        summaries = []
        for entry in analysis_history:
            result = entry['result']
            summary = {
                "timestamp": entry['timestamp'],
                "verdict": result.get('final_verdict', 'unknown'),
                "confidence": result.get('confidence', 0),
                "evidence_count": len(result.get('evidence', [])),
                "modules_used": result.get('chain_of_custody', {}).get('analysis_modules_used', [])
            }
            summaries.append(summary)
        
        return {
            "total_analyses": len(summaries),
            "analyses": summaries,
            "final_verdict": summaries[-1]['verdict'] if summaries else 'pending'
        }
