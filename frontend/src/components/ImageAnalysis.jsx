import React, { useState } from 'react';
import './ImageAnalysis.css';

function ImageAnalysis() {
  const [image, setImage] = useState(null);
  const [studentId, setStudentId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setResults(null);
    }
  };

  const handleAnalyze = async () => {
    if (!image) return;
    
    setAnalyzing(true);
    const formData = new FormData();
    formData.append('image', image);
    if (studentId) formData.append('student_id', studentId);

    try {
      const response = await fetch('http://localhost:8000/analyze/image', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="analysis-page">
      <div className="container">
        <h1>🖼️ Image Analysis</h1>
        <p className="subtitle">Detect deepfakes, face swaps, and synthetic media</p>
        
        <div className="analysis-form">
          <div className="upload-zone">
            <input 
              type="file" 
              accept="image/*"
              onChange={handleImageUpload}
              className="file-input"
            />
            <div className="upload-content">
              <div className="upload-icon">📁</div>
              <p>Click to upload or drag and drop</p>
              <p className="upload-hint">Supports JPG, PNG, HEIC</p>
            </div>
          </div>
          
          {image && (
            <div className="file-info">
              <span>Selected: {image.name}</span>
            </div>
          )}
          
          <input 
            type="text"
            placeholder="Student ID (optional)"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            className="input"
          />
          
          <button 
            onClick={handleAnalyze}
            disabled={!image || analyzing}
            className="btn btn-primary"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Image'}
          </button>
        </div>
        
        {analyzing && (
          <div className="loading">
            <div className="spinner"></div>
          </div>
        )}
        
        {results && (
          <div className="results">
            <h2>Analysis Results</h2>
            
            <div className="result-summary">
              <div className={`verdict ${results.face_swap_detected ? 'high' : results.synthesis_detected ? 'medium' : 'low'}`}>
                <h3>Verdict</h3>
                <p className="verdict-text">
                  {results.face_swap_detected ? 'FACE SWAP DETECTED' : 
                   results.synthesis_detected ? 'SYNTHETIC FACE DETECTED' : 
                   'HUMAN VERIFIED'}
                </p>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${results.confidence * 100}%` }}
                  />
                </div>
                <p className="confidence-text">Confidence: {(results.confidence * 100).toFixed(1)}%</p>
              </div>
            </div>
            
            {results.anomalies && results.anomalies.length > 0 && (
              <div className="anomalies">
                <h3>Anomalies Detected</h3>
                {results.anomalies.map((anomaly, index) => (
                  <div key={index} className="result-item">
                    <h4>{anomaly.test}</h4>
                    <p>{anomaly.finding}</p>
                    <p className="value">Value: {typeof anomaly.value === 'number' ? anomaly.value.toFixed(4) : anomaly.value}</p>
                  </div>
                ))}
              </div>
            )}
            
            {results.biometric_scores && (
              <div className="biometric-scores">
                <h3>Biometric Scores</h3>
                {Object.entries(results.biometric_scores).map(([key, value]) => (
                  <div key={key} className="score-item">
                    <span className="score-label">{key.replace(/_/g, ' ')}</span>
                    <span className="score-value">{typeof value === 'number' ? value.toFixed(4) : value}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageAnalysis;
