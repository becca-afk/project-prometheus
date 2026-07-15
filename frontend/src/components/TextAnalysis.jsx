import React, { useState } from 'react';
import './TextAnalysis.css';

function TextAnalysis() {
  const [text, setText] = useState('');
  const [studentId, setStudentId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    
    setAnalyzing(true);
    
    try {
      const response = await fetch('http://localhost:8000/analyze/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text,
          student_id: studentId || null
        })
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
        <h1>📝 Text Analysis</h1>
        <p className="subtitle">Detect AI-generated content with stylometric fingerprinting</p>
        
        <div className="analysis-form">
          <textarea
            placeholder="Paste text to analyze..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="input textarea"
          />
          
          <input 
            type="text"
            placeholder="Student ID (optional)"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            className="input"
          />
          
          <button 
            onClick={handleAnalyze}
            disabled={!text.trim() || analyzing}
            className="btn btn-primary"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Text'}
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
              <div className={`verdict ${results.ai_likelihood > 0.75 ? 'high' : results.ai_likelihood > 0.5 ? 'medium' : 'low'}`}>
                <h3>AI Likelihood</h3>
                <p className="verdict-text">{(results.ai_likelihood * 100).toFixed(1)}%</p>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${results.ai_likelihood * 100}%` }}
                  />
                </div>
              </div>
            </div>
            
            {results.anomalies && results.anomalies.length > 0 && (
              <div className="anomalies">
                <h3>Anomalies Detected</h3>
                {results.anomalies.map((anomaly, index) => (
                  <div key={index} className="result-item">
                    <h4>{anomaly.test}</h4>
                    <p>{anomaly.finding}</p>
                  </div>
                ))}
              </div>
            )}
            
            {results.stylometric_breakdown && (
              <div className="stylometric-breakdown">
                <h3>Stylometric Analysis</h3>
                {Object.entries(results.stylometric_breakdown).map(([key, value]) => (
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

export default TextAnalysis;
