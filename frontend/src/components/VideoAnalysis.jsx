import React, { useState } from 'react';
import './VideoAnalysis.css';

function VideoAnalysis() {
  const [video, setVideo] = useState(null);
  const [studentId, setStudentId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);

  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setVideo(file);
      setResults(null);
    }
  };

  const handleAnalyze = async () => {
    if (!video) return;
    
    setAnalyzing(true);
    const formData = new FormData();
    formData.append('video', video);
    if (studentId) formData.append('student_id', studentId);

    try {
      const response = await fetch('http://localhost:8000/analyze/video', {
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
        <h1>🎥 Video Analysis</h1>
        <p className="subtitle">Detect deepfakes and temporal inconsistencies in video</p>
        
        <div className="analysis-form">
          <div className="upload-zone">
            <input 
              type="file" 
              accept="video/*"
              onChange={handleVideoUpload}
              className="file-input"
            />
            <div className="upload-content">
              <div className="upload-icon">📹</div>
              <p>Click to upload or drag and drop</p>
              <p className="upload-hint">Supports MP4, WebM, AVI</p>
            </div>
          </div>
          
          {video && (
            <div className="file-info">
              <span>Selected: {video.name}</span>
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
            disabled={!video || analyzing}
            className="btn btn-primary"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Video'}
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
              <div className={`verdict ${results.deepfake_detected ? 'high' : 'low'}`}>
                <h3>Verdict</h3>
                <p className="verdict-text">
                  {results.deepfake_detected ? 'DEEPFAKE DETECTED' : 'HUMAN VERIFIED'}
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
            
            {results.temporal_scores && (
              <div className="temporal-scores">
                <h3>Temporal Analysis</h3>
                {Object.entries(results.temporal_scores).map(([key, value]) => (
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

export default VideoAnalysis;
