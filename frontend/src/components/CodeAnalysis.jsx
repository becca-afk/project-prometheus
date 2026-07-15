import React, { useState } from 'react';
import './CodeAnalysis.css';

function CodeAnalysis() {
  const [code, setCode] = useState('');
  const [studentId, setStudentId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    if (!code.trim()) return;
    
    setAnalyzing(true);
    
    try {
      const response = await fetch('http://localhost:8000/analyze/code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
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
        <h1>💻 Code Analysis</h1>
        <p className="subtitle">Detect AI-generated code with style consistency checks</p>
        
        <div className="analysis-form">
          <textarea
            placeholder="Paste code to analyze..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="input textarea code-input"
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
            disabled={!code.trim() || analyzing}
            className="btn btn-primary"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Code'}
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
              <div className={`verdict ${results.ai_likelihood > 0.5 ? 'high' : 'low'}`}>
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
            
            {results.code_metrics && (
              <div className="code-metrics">
                <h3>Code Metrics</h3>
                {Object.entries(results.code_metrics).map(([key, value]) => (
                  <div key={key} className="score-item">
                    <span className="score-label">{key.replace(/_/g, ' ')}</span>
                    <span className="score-value">{typeof value === 'number' ? value.toFixed(4) : value}</span>
                  </div>
                ))}
              </div>
            )}
            
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
          </div>
        )}
      </div>
    </div>
  );
}

export default CodeAnalysis;
