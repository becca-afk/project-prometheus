"""
FaceForensicsEngine - Deepfake & Face-Swap Detection Module

This module detects if a face has been swapped, synthesized, or manipulated
using 7 different biometric signals and forensic techniques.
"""

import cv2
import numpy as np
from scipy.spatial import distance
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FaceForensicsEngine:
    """
    Detects if a face has been swapped, synthesized, or manipulated.
    Uses 7 different biometric signals for comprehensive analysis.
    """
    
    def __init__(self):
        self.face_detector = None
        self.landmark_predictor = None
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize face detection models with fallbacks"""
        try:
            # Try to load dlib models
            import dlib
            self.face_detector = dlib.get_frontal_face_detector()
            logger.info("Dlib face detector initialized")
        except ImportError:
            logger.warning("Dlib not available, using OpenCV fallback")
            self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        try:
            import dlib
            self.landmark_predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
        except:
            logger.warning("Landmark predictor not available")
            self.landmark_predictor = None
    
    def analyze_face(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Perform comprehensive face forensics analysis.
        
        Args:
            image_bytes: Raw image data as bytes
            
        Returns:
            Dictionary containing analysis results with confidence scores
        """
        results = {
            "face_swap_detected": False,
            "synthesis_detected": False,
            "confidence": 0.0,
            "anomalies": [],
            "biometric_scores": {}
        }
        
        try:
            # Convert bytes to numpy array
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if img is None:
                results['anomalies'].append({
                    "test": "Image decoding",
                    "finding": "Failed to decode image",
                    "value": "decode_error"
                })
                return results
            
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Run all detection tests
            self._test_eye_symmetry(img, results)
            self._test_skin_texture(img, results)
            self._test_compression_artifacts(img, results)
            self._test_frequency_domain(img, results)
            self._test_face_geometry(rgb_img, results)
            self._test_lighting_consistency(rgb_img, results)
            self._test_edge_consistency(img, results)
            
            # Calculate final confidence
            if results['anomalies']:
                results['confidence'] = min(1.0, len(results['anomalies']) * 0.15)
                if results['confidence'] > 0.5:
                    results['synthesis_detected'] = True
                if results['confidence'] > 0.7:
                    results['face_swap_detected'] = True
            
        except Exception as e:
            logger.error(f"Error in face analysis: {str(e)}")
            results['anomalies'].append({
                "test": "Analysis error",
                "finding": f"Processing error: {str(e)}",
                "value": "error"
            })
        
        return results
    
    def _test_eye_symmetry(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 1: Eye symmetry analysis - AI avatars often have unnaturally symmetrical features"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            if isinstance(self.face_detector, cv2.CascadeClassifier):
                faces = self.face_detector.detectMultiScale(gray, 1.1, 4)
            else:
                faces = self.face_detector(gray, 1)
            
            if len(faces) == 0:
                return
            
            for face in faces:
                if isinstance(face, tuple):  # dlib rect
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                else:  # OpenCV rect
                    x, y, w, h = face
                
                # Extract eye regions (simplified)
                eye_region_y = y + int(h * 0.3)
                eye_region_height = int(h * 0.2)
                left_eye_x = x + int(w * 0.2)
                right_eye_x = x + int(w * 0.6)
                
                # Check symmetry by comparing pixel intensity distributions
                left_eye = gray[eye_region_y:eye_region_y+eye_region_height, 
                               left_eye_x:left_eye_x+int(w*0.2)]
                right_eye = gray[eye_region_y:eye_region_y+eye_region_height, 
                                right_eye_x:right_eye_x+int(w*0.2)]
                
                if left_eye.size > 0 and right_eye.size > 0:
                    left_hist = cv2.calcHist([left_eye], [0], None, [16], [0, 256])
                    right_hist = cv2.calcHist([right_eye], [0], None, [16], [0, 256])
                    
                    # Normalize histograms
                    left_hist = left_hist / left_hist.sum()
                    right_hist = right_hist / right_hist.sum()
                    
                    # Calculate correlation
                    correlation = cv2.compareHist(left_hist, right_hist, cv2.HISTCMP_CORREL)
                    
                    results['biometric_scores']['eye_symmetry'] = float(correlation)
                    
                    # Too perfect correlation suggests AI generation
                    if correlation > 0.95:
                        results['anomalies'].append({
                            "test": "Eye symmetry",
                            "finding": "Unnaturally symmetrical eye regions",
                            "value": correlation
                        })
                        results['synthesis_detected'] = True
        
        except Exception as e:
            logger.error(f"Error in eye symmetry test: {str(e)}")
    
    def _test_skin_texture(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 2: Skin texture analysis - AI smooths out natural skin imperfections"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply Laplacian for edge detection (measures texture)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            results['biometric_scores']['skin_texture_variance'] = float(laplacian_var)
            
            # Real skin has higher variance (pores, imperfections)
            # AI-generated skin is often too smooth
            if laplacian_var < 30:
                results['anomalies'].append({
                    "test": "Skin texture",
                    "finding": "Unnaturally smooth skin (low texture variance)",
                    "value": laplacian_var
                })
                results['synthesis_detected'] = True
            elif laplacian_var > 500:
                # Too high variance might indicate compression artifacts
                results['anomalies'].append({
                    "test": "Skin texture",
                    "finding": "Unusual texture variance (possible artifacts)",
                    "value": laplacian_var
                })
        
        except Exception as e:
            logger.error(f"Error in skin texture test: {str(e)}")
    
    def _test_compression_artifacts(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 3: Compression artifact analysis - Deepfakes often have double compression"""
        try:
            # Convert to YUV color space
            yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            
            # Analyze the Y channel (luminance)
            y_channel = yuv[:, :, 0]
            
            # Calculate blockiness measure (8x8 DCT block artifacts)
            h, w = y_channel.shape
            blockiness = 0
            
            # Check horizontal block boundaries
            for i in range(7, h, 8):
                diff = np.abs(y_channel[i, :] - y_channel[i+1, :])
                blockiness += np.mean(diff)
            
            # Check vertical block boundaries
            for j in range(7, w, 8):
                diff = np.abs(y_channel[:, j] - y_channel[:, j+1])
                blockiness += np.mean(diff)
            
            blockiness = blockiness / (h + w) * 100
            
            results['biometric_scores']['compression_blockiness'] = float(blockiness)
            
            # High blockiness indicates compression artifacts
            if blockiness > 5.0:
                results['anomalies'].append({
                    "test": "Compression artifacts",
                    "finding": "Significant compression blockiness detected",
                    "value": blockiness
                })
        
        except Exception as e:
            logger.error(f"Error in compression artifact test: {str(e)}")
    
    def _test_frequency_domain(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 4: Frequency domain analysis - GANs have characteristic frequency patterns"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply FFT
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f)
            
            # Calculate power spectrum
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
            
            # Analyze high-frequency content
            h, w = magnitude_spectrum.shape
            center_h, center_w = h // 2, w // 2
            
            # Extract high-frequency region
            high_freq_region = magnitude_spectrum[center_h-50:center_h+50, center_w-50:center_w+50]
            high_freq_energy = np.mean(high_freq_region)
            
            results['biometric_scores']['high_frequency_energy'] = float(high_freq_energy)
            
            # AI-generated images often have abnormal high-frequency patterns
            if high_freq_energy < 50 or high_freq_energy > 200:
                results['anomalies'].append({
                    "test": "Frequency domain",
                    "finding": "Abnormal high-frequency energy distribution",
                    "value": high_freq_energy
                })
        
        except Exception as e:
            logger.error(f"Error in frequency domain test: {str(e)}")
    
    def _test_face_geometry(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 5: Face geometry analysis - Detects unnatural face proportions"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            if isinstance(self.face_detector, cv2.CascadeClassifier):
                faces = self.face_detector.detectMultiScale(gray, 1.1, 4)
            else:
                faces = self.face_detector(gray, 1)
            
            if len(faces) == 0:
                return
            
            for face in faces:
                if isinstance(face, tuple):
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                else:
                    x, y, w, h = face
                
                # Calculate face aspect ratio
                aspect_ratio = h / w if w > 0 else 0
                
                results['biometric_scores']['face_aspect_ratio'] = float(aspect_ratio)
                
                # Normal face aspect ratio is typically 1.2-1.4
                if aspect_ratio < 1.0 or aspect_ratio > 1.6:
                    results['anomalies'].append({
                        "test": "Face geometry",
                        "finding": "Unusual face aspect ratio",
                        "value": aspect_ratio
                    })
        
        except Exception as e:
            logger.error(f"Error in face geometry test: {str(e)}")
    
    def _test_lighting_consistency(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 6: Lighting consistency - Face swaps often have inconsistent lighting"""
        try:
            # Convert to LAB color space for better lighting analysis
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel = lab[:, :, 0]
            
            # Calculate lighting gradient across the image
            gradient_x = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0, ksize=3)
            gradient_y = cv2.Sobel(l_channel, cv2.CV_64F, 0, 1, ksize=3)
            
            gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
            avg_gradient = np.mean(gradient_magnitude)
            
            results['biometric_scores']['lighting_gradient'] = float(avg_gradient)
            
            # Unusually uniform or extreme lighting suggests manipulation
            if avg_gradient < 5 or avg_gradient > 50:
                results['anomalies'].append({
                    "test": "Lighting consistency",
                    "finding": "Inconsistent lighting pattern detected",
                    "value": avg_gradient
                })
        
        except Exception as e:
            logger.error(f"Error in lighting consistency test: {str(e)}")
    
    def _test_edge_consistency(self, img: np.ndarray, results: Dict[str, Any]):
        """Test 7: Edge consistency - Face swaps often have edge discontinuities"""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Calculate edge density
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            results['biometric_scores']['edge_density'] = float(edge_density)
            
            # Abnormal edge density suggests manipulation
            if edge_density < 0.01 or edge_density > 0.15:
                results['anomalies'].append({
                    "test": "Edge consistency",
                    "finding": "Unusual edge density pattern",
                    "value": edge_density
                })
        
        except Exception as e:
            logger.error(f"Error in edge consistency test: {str(e)}")


class VideoForensicsEngine:
    """
    Extended forensics for video analysis including temporal consistency checks.
    """
    
    def __init__(self):
        self.face_engine = FaceForensicsEngine()
    
    def analyze_video(self, video_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze video for deepfake detection using temporal consistency.
        
        Args:
            video_bytes: Raw video data as bytes
            
        Returns:
            Dictionary containing video analysis results
        """
        results = {
            "deepfake_detected": False,
            "confidence": 0.0,
            "anomalies": [],
            "temporal_scores": {}
        }
        
        try:
            # Convert bytes to numpy array
            np_arr = np.frombuffer(video_bytes, np.uint8)
            
            # Create temporary file for video processing
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as f:
                f.write(np_arr)
                temp_path = f.name
            
            # Open video capture
            cap = cv2.VideoCapture(temp_path)
            
            if not cap.isOpened():
                results['anomalies'].append({
                    "test": "Video loading",
                    "finding": "Failed to open video file",
                    "value": "load_error"
                })
                return results
            
            frame_count = 0
            frame_scores = []
            
            # Sample frames (every 10th frame to save processing time)
            sample_rate = 10
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % sample_rate == 0:
                    # Convert frame to bytes for face analysis
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    
                    # Analyze frame
                    frame_result = self.face_engine.analyze_face(frame_bytes)
                    frame_scores.append(frame_result.get('confidence', 0))
                
                frame_count += 1
            
            cap.release()
            
            # Clean up temp file
            import os
            os.unlink(temp_path)
            
            if frame_scores:
                # Analyze temporal consistency
                score_variance = np.var(frame_scores)
                avg_score = np.mean(frame_scores)
                
                results['temporal_scores']['average_frame_confidence'] = float(avg_score)
                results['temporal_scores']['frame_variance'] = float(score_variance)
                
                # High variance in frame scores suggests manipulation
                if score_variance > 0.1:
                    results['anomalies'].append({
                        "test": "Temporal consistency",
                        "finding": "Inconsistent detection scores across frames",
                        "value": score_variance
                    })
                
                results['confidence'] = avg_score
                if avg_score > 0.6:
                    results['deepfake_detected'] = True
            
        except Exception as e:
            logger.error(f"Error in video analysis: {str(e)}")
            results['anomalies'].append({
                "test": "Video analysis error",
                "finding": f"Processing error: {str(e)}",
                "value": "error"
            })
        
        return results
