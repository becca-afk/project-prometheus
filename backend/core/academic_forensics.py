"""
AcademicForensicsEngine - Plagiarism & AI-Writing Detection Module

This module analyzes student submissions for AI-generated content.
Works with text, spreadsheets, and code with stylometric fingerprinting.
"""

import re
import hashlib
from datetime import datetime
from collections import Counter
from typing import Dict, Any, Optional, List
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AcademicForensicsEngine:
    """
    Analyzes student submissions for AI-generated content.
    Works with text, spreadsheets, and code.
    """
    
    def __init__(self):
        # Stylometric fingerprint database (student's writing style)
        self.student_style_db: Dict[str, Dict] = {}
        
        # Common AI phrases and patterns
        self.ai_markers = [
            "delve into", "it is imperative", "leverage", "synergize", 
            "in the realm of", "as an AI", "I don't have personal opinions",
            "it's worth noting", "a comprehensive approach",
            "the crux of the matter", "paradigm shift", "holistic",
            "multifaceted", "nuanced", "underscore", "pivotal",
            "foster", "cultivate", "streamline", "optimize",
            "enhance", "facilitate", "implement", "deploy"
        ]
        
        # AI sentence patterns
        self.ai_sentence_patterns = [
            r"It is (important|noteworthy|crucial|essential) to (note|mention|highlight)",
            r"(In|With) (regard|respect|relation) to",
            r"(It is worth noting|It's important to mention)",
            r"(Furthermore|Moreover|Additionally|In addition)",
            r"(Therefore|Thus|Consequently|As a result)",
        ]
        
    def analyze_text(self, text: str, student_id: Optional[str] = None, 
                    document_history: Optional[List] = None) -> Dict[str, Any]:
        """
        Analyzes text for AI generation.
        
        Args:
            text: The text content to analyze
            student_id: Optional student identifier for style comparison
            document_history: Optional revision history from Google Docs/Word
            
        Returns:
            Dictionary containing analysis results
        """
        results = {
            "ai_likelihood": 0.0,
            "plagiarism_detected": False,
            "anomalies": [],
            "stylometric_breakdown": {},
            "revision_analysis": {}
        }
        
        if not text or len(text.strip()) < 50:
            results['anomalies'].append({
                "test": "Text length",
                "finding": "Text too short for meaningful analysis",
                "value": len(text)
            })
            return results
        
        try:
            # Run all detection tests
            self._test_burstiness(text, results)
            self._test_vocabulary_richness(text, results)
            self._test_ai_marker_phrases(text, results)
            self._test_sentence_patterns(text, results)
            self._test_readability_metrics(text, results)
            self._test_error_patterns(text, results)
            
            # Style comparison if student ID provided
            if student_id:
                self._test_style_consistency(text, student_id, results)
            
            # Revision history analysis if provided
            if document_history:
                self._analyze_revision_history(document_history, results)
            
            # Calculate final AI likelihood score
            results['ai_likelihood'] = min(1.0, results['ai_likelihood'])
            
        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            results['anomalies'].append({
                "test": "Analysis error",
                "finding": f"Processing error: {str(e)}",
                "value": "error"
            })
        
        return results
    
    def _test_burstiness(self, text: str, results: Dict[str, Any]):
        """Test 1: Perplexity & Burstiness - AI text has uniform sentence lengths"""
        try:
            sentences = re.split(r'[.!?]+', text)
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            
            if not sentence_lengths:
                return
            
            avg_length = np.mean(sentence_lengths)
            std_length = np.std(sentence_lengths)
            burstiness = std_length / avg_length if avg_length > 0 else 0
            
            results['stylometric_breakdown']['avg_sentence_length'] = float(avg_length)
            results['stylometric_breakdown']['sentence_length_std'] = float(std_length)
            results['stylometric_breakdown']['burstiness'] = float(burstiness)
            
            # AI text has low burstiness (uniform sentence lengths)
            if burstiness < 0.35:
                results['anomalies'].append({
                    "test": "Burstiness",
                    "finding": "Sentence lengths are too uniform (AI characteristic)",
                    "value": burstiness
                })
                results['ai_likelihood'] += 0.18
            elif burstiness < 0.45:
                results['ai_likelihood'] += 0.08
        
        except Exception as e:
            logger.error(f"Error in burstiness test: {str(e)}")
    
    def _test_vocabulary_richness(self, text: str, results: Dict[str, Any]):
        """Test 2: Vocabulary Richness - AI has characteristic vocabulary patterns"""
        try:
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            unique_words = set(words)
            
            if not words:
                return
            
            vocab_richness = len(unique_words) / len(words)
            
            # Calculate Type-Token Ratio (TTR)
            ttr = len(unique_words) / len(words) if len(words) > 0 else 0
            
            # Calculate hapax legomena (words appearing only once)
            word_counts = Counter(words)
            hapax_ratio = sum(1 for count in word_counts.values() if count == 1) / len(words)
            
            results['stylometric_breakdown']['vocab_richness'] = float(vocab_richness)
            results['stylometric_breakdown']['type_token_ratio'] = float(ttr)
            results['stylometric_breakdown']['hapax_ratio'] = float(hapax_ratio)
            
            # AI often has moderate vocab richness
            if vocab_richness < 0.35:
                results['anomalies'].append({
                    "test": "Vocabulary richness",
                    "finding": "Vocabulary is too limited",
                    "value": vocab_richness
                })
                results['ai_likelihood'] += 0.12
            elif vocab_richness > 0.75:
                results['anomalies'].append({
                    "test": "Vocabulary richness",
                    "finding": "Unusually high vocabulary diversity",
                    "value": vocab_richness
                })
                results['ai_likelihood'] += 0.08
        
        except Exception as e:
            logger.error(f"Error in vocabulary richness test: {str(e)}")
    
    def _test_ai_marker_phrases(self, text: str, results: Dict[str, Any]):
        """Test 3: AI Marker Phrases - Common AI-generated phrases"""
        try:
            text_lower = text.lower()
            ai_phrase_count = 0
            found_phrases = []
            
            for marker in self.ai_markers:
                if marker.lower() in text_lower:
                    ai_phrase_count += text_lower.count(marker.lower())
                    found_phrases.append(marker)
            
            if ai_phrase_count > 0:
                results['anomalies'].append({
                    "test": "AI marker phrases",
                    "finding": f"Found {ai_phrase_count} common AI phrases: {found_phrases[:5]}",
                    "value": ai_phrase_count
                })
                results['ai_likelihood'] += min(0.25, ai_phrase_count * 0.04)
        
        except Exception as e:
            logger.error(f"Error in AI marker phrases test: {str(e)}")
    
    def _test_sentence_patterns(self, text: str, results: Dict[str, Any]):
        """Test 4: Sentence Patterns - AI uses characteristic sentence structures"""
        try:
            pattern_matches = 0
            matched_patterns = []
            
            for pattern in self.ai_sentence_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    pattern_matches += len(matches)
                    matched_patterns.append(pattern[:30] + "...")
            
            if pattern_matches > 0:
                results['anomalies'].append({
                    "test": "AI sentence patterns",
                    "finding": f"Found {pattern_matches} AI sentence patterns",
                    "value": pattern_matches
                })
                results['ai_likelihood'] += min(0.15, pattern_matches * 0.03)
        
        except Exception as e:
            logger.error(f"Error in sentence patterns test: {str(e)}")
    
    def _test_readability_metrics(self, text: str, results: Dict[str, Any]):
        """Test 5: Readability Metrics - AI text has characteristic readability"""
        try:
            # Calculate basic readability metrics
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            words = re.findall(r'\b[a-zA-Z]+\b', text)
            
            if not sentences or not words:
                return
            
            avg_sentence_length = len(words) / len(sentences)
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Flesch Reading Ease (simplified)
            syllables = sum(self._count_syllables(word) for word in words)
            flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (syllables / len(words)))
            
            results['stylometric_breakdown']['avg_word_length'] = float(avg_word_length)
            results['stylometric_breakdown']['flesch_reading_ease'] = float(flesch_score)
            
            # AI text often has very consistent readability
            if flesch_score > 80 and avg_word_length > 4.5:
                results['anomalies'].append({
                    "test": "Readability metrics",
                    "finding": "Unusually high readability with complex words",
                    "value": flesch_score
                })
                results['ai_likelihood'] += 0.10
        
        except Exception as e:
            logger.error(f"Error in readability metrics test: {str(e)}")
    
    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count in a word"""
        word = word.lower()
        if word.endswith('e'):
            word = word[:-1]
        vowels = 'aeiouy'
        count = 0
        prev_char_was_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = is_vowel
        return max(1, count)
    
    def _test_error_patterns(self, text: str, results: Dict[str, Any]):
        """Test 6: Error Patterns - AI makes different errors than humans"""
        try:
            # Common human typos vs AI patterns
            human_typos = ['teh', 'adn', 'taht', 'dont', 'cant', 'wont', 'im', 'youre', 'theyre']
            
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            typo_count = sum(1 for word in words if word in human_typos)
            
            # Check for perfect grammar (suspicious)
            # AI rarely makes simple typos but may have style inconsistencies
            if len(words) > 100 and typo_count == 0:
                results['anomalies'].append({
                    "test": "Error patterns",
                    "finding": "No common typos found (suspicious for human writing)",
                    "value": typo_count
                })
                results['ai_likelihood'] += 0.08
            
            results['stylometric_breakdown']['common_typo_count'] = typo_count
        
        except Exception as e:
            logger.error(f"Error in error patterns test: {str(e)}")
    
    def _test_style_consistency(self, text: str, student_id: str, results: Dict[str, Any]):
        """Test 7: Stylometric Fingerprinting - Compare to student's past work"""
        try:
            if student_id not in self.student_style_db:
                # First time seeing this student - build their profile
                self._build_student_profile(student_id, text)
                return
            
            student_profile = self.student_style_db[student_id]
            similarity = self._compare_style(text, student_profile)
            
            results['stylometric_breakdown']['style_similarity'] = float(similarity)
            
            if similarity < 0.45:
                results['anomalies'].append({
                    "test": "Style consistency",
                    "finding": f"Text style diverges from student's historical writing (similarity: {similarity:.2f})",
                    "value": similarity
                })
                results['ai_likelihood'] += 0.20
            elif similarity < 0.60:
                results['ai_likelihood'] += 0.08
        
        except Exception as e:
            logger.error(f"Error in style consistency test: {str(e)}")
    
    def _build_student_profile(self, student_id: str, text: str):
        """Build a stylometric profile for a student"""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        sentences = re.split(r'[.!?]+', text)
        
        profile = {
            'corpus': [text],
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'avg_sentence_length': np.mean([len(s.split()) for s in sentences if s.strip()]) if sentences else 0,
            'vocab_richness': len(set(words)) / len(words) if words else 0,
            'created_at': datetime.now().isoformat()
        }
        
        self.student_style_db[student_id] = profile
    
    def _compare_style(self, text: str, profile: Dict) -> float:
        """Compare text to student's historical writing profile"""
        try:
            # Extract current text features
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            sentences = re.split(r'[.!?]+', text)
            
            if not words or not sentences:
                return 0.5
            
            current_avg_word_length = np.mean([len(w) for w in words])
            current_avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
            current_vocab_richness = len(set(words)) / len(words)
            
            # Calculate similarity scores
            word_length_diff = abs(current_avg_word_length - profile.get('avg_word_length', 0))
            sentence_length_diff = abs(current_avg_sentence_length - profile.get('avg_sentence_length', 0))
            vocab_diff = abs(current_vocab_richness - profile.get('vocab_richness', 0))
            
            # Normalize and combine
            similarity = 1 - ((word_length_diff * 0.3 + sentence_length_diff * 0.4 + vocab_diff * 0.3) / 3)
            return max(0, min(1, similarity))
        
        except Exception as e:
            logger.error(f"Error comparing style: {str(e)}")
            return 0.5
    
    def _analyze_revision_history(self, history: List, results: Dict[str, Any]):
        """Analyze Google Docs or Word revision history"""
        try:
            if len(history) < 2:
                results['revision_analysis'] = {
                    "pasted_content": False,
                    "typing_speed": 0,
                    "consistency": 0,
                    "message": "Insufficient revision history"
                }
                return
            
            revision_analysis = {
                "pasted_content": False,
                "typing_speed": 0,
                "consistency": 0,
                "total_revisions": len(history)
            }
            
            additions = []
            for i in range(1, len(history)):
                prev_content = str(history[i-1])
                curr_content = str(history[i])
                
                # Check if a large chunk was added suddenly
                content_diff = len(curr_content) - len(prev_content)
                if content_diff > 300:  # More than 300 chars added at once
                    revision_analysis['pasted_content'] = True
                
                # Calculate typing speed if timestamps available
                if isinstance(history[i], dict) and isinstance(history[i-1], dict):
                    if 'timestamp' in history[i] and 'timestamp' in history[i-1]:
                        try:
                            time_diff = (datetime.fromisoformat(history[i]['timestamp']) - 
                                       datetime.fromisoformat(history[i-1]['timestamp'])).total_seconds()
                            if time_diff > 0 and content_diff > 0:
                                additions.append(content_diff / time_diff)
                        except:
                            pass
            
            if additions:
                revision_analysis['typing_speed'] = float(np.mean(additions))
                if np.mean(additions) > 0:
                    revision_analysis['consistency'] = float(1 - (np.std(additions) / np.mean(additions)))
                    
                    # Humans have variable typing speeds
                    if revision_analysis['consistency'] > 0.85:
                        revision_analysis['pasted_content'] = True
            
            results['revision_analysis'] = revision_analysis
            
            if revision_analysis['pasted_content']:
                results['anomalies'].append({
                    "test": "Revision history",
                    "finding": "Content appears to have been pasted in large chunks",
                    "value": "Paste detected"
                })
                results['ai_likelihood'] += 0.25
        
        except Exception as e:
            logger.error(f"Error analyzing revision history: {str(e)}")
    
    def analyze_excel(self, excel_data: str, version_history: Optional[List] = None) -> Dict[str, Any]:
        """
        Analyzes Excel/Google Sheets for AI-generated formulas.
        
        Args:
            excel_data: Excel data as string or CSV content
            version_history: Optional version history from Excel/Sheets
            
        Returns:
            Dictionary containing Excel analysis results
        """
        results = {
            "ai_generated_formulas": [],
            "anomaly_score": 0.0,
            "complexity_analysis": {},
            "suspicious_patterns": []
        }
        
        try:
            # Parse Excel content
            formula_pattern = r'=([A-Z]+\([^)]*\)|[^=]+)'
            formulas = re.findall(formula_pattern, str(excel_data))
            
            if not formulas:
                results['complexity_analysis']['formula_count'] = 0
                return results
            
            results['complexity_analysis']['formula_count'] = len(formulas)
            
            # Analyze each formula
            for formula in formulas:
                complexity = self._formula_complexity(formula)
                if complexity > 0.6:
                    results['ai_generated_formulas'].append({
                        "formula": formula[:50] + "..." if len(formula) > 50 else formula,
                        "complexity": float(complexity),
                        "reason": "Formula is unnaturally complex"
                    })
                    results['anomaly_score'] += 0.12
            
            # Check for suspicious patterns
            self._detect_excel_patterns(excel_data, results)
            
            # Check version history
            if version_history:
                paste_events = self._detect_excel_paste_events(version_history)
                if paste_events > len(version_history) * 0.25:
                    results['anomaly_score'] += 0.30
                    results['suspicious_patterns'].append("High paste event ratio in version history")
            
            results['anomaly_score'] = min(1.0, results['anomaly_score'])
        
        except Exception as e:
            logger.error(f"Error in Excel analysis: {str(e)}")
            results['suspicious_patterns'].append(f"Analysis error: {str(e)}")
        
        return results
    
    def _formula_complexity(self, formula: str) -> float:
        """Measures formula complexity based on nesting depth and function count"""
        try:
            functions = len(re.findall(r'[A-Z]+\(', formula))
            parentheses = formula.count('(')
            operators = len(re.findall(r'[+\-*/^&]', formula))
            
            # Complex formulas have many nested functions and operators
            complexity = (functions * 0.4) + (parentheses * 0.1) + (operators * 0.05)
            return min(1.0, complexity / 8)
        except:
            return 0.0
    
    def _detect_excel_patterns(self, excel_data: str, results: Dict[str, Any]):
        """Detect suspicious patterns in Excel data"""
        try:
            # Check for perfect consistency (suspicious)
            lines = str(excel_data).split('\n')
            if len(lines) > 5:
                line_lengths = [len(line) for line in lines]
                if np.std(line_lengths) < 2:
                    results['suspicious_patterns'].append("Unusually consistent row lengths")
                    results['anomaly_score'] += 0.15
        
        except Exception as e:
            logger.error(f"Error detecting Excel patterns: {str(e)}")
    
    def _detect_excel_paste_events(self, history: List) -> int:
        """Detects paste events in Excel version history"""
        paste_count = 0
        for entry in history:
            if isinstance(entry, dict):
                if entry.get('event_type') == 'paste' or entry.get('type') == 'paste':
                    paste_count += 1
        return paste_count
    
    def analyze_code(self, code: str, student_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyzes code for AI generation.
        
        Args:
            code: Source code to analyze
            student_id: Optional student identifier for style comparison
            
        Returns:
            Dictionary containing code analysis results
        """
        results = {
            "ai_likelihood": 0.0,
            "anomalies": [],
            "code_metrics": {}
        }
        
        try:
            if not code or len(code.strip()) < 20:
                results['anomalies'].append({
                    "test": "Code length",
                    "finding": "Code too short for meaningful analysis",
                    "value": len(code)
                })
                return results
            
            # Calculate code metrics
            lines = code.split('\n')
            code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            
            # Average line length
            avg_line_length = np.mean([len(line) for line in code_lines]) if code_lines else 0
            
            # Comment ratio
            comment_lines = [line for line in lines if line.strip().startswith('#')]
            comment_ratio = len(comment_lines) / len(lines) if lines else 0
            
            # Function count
            function_count = len(re.findall(r'def\s+\w+|function\s+\w+', code))
            
            results['code_metrics'] = {
                'total_lines': len(lines),
                'code_lines': len(code_lines),
                'avg_line_length': float(avg_line_length),
                'comment_ratio': float(comment_ratio),
                'function_count': function_count
            }
            
            # AI code often has perfect formatting and high comment ratio
            if comment_ratio > 0.3 and len(code_lines) > 10:
                results['anomalies'].append({
                    "test": "Comment ratio",
                    "finding": "Unusually high comment ratio",
                    "value": comment_ratio
                })
                results['ai_likelihood'] += 0.15
            
            # Perfect line length consistency
            if len(code_lines) > 5 and np.std([len(line) for line in code_lines]) < 5:
                results['anomalies'].append({
                    "test": "Line length consistency",
                    "finding": "Unusually consistent line lengths",
                    "value": np.std([len(line) for line in code_lines])
                })
                results['ai_likelihood'] += 0.12
            
            results['ai_likelihood'] = min(1.0, results['ai_likelihood'])
        
        except Exception as e:
            logger.error(f"Error in code analysis: {str(e)}")
            results['anomalies'].append({
                "test": "Analysis error",
                "finding": f"Processing error: {str(e)}",
                "value": "error"
            })
        
        return results
