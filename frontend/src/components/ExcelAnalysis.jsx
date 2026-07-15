import React, { useState } from 'react';
import './ExcelAnalysis.css';

function ExcelAnalysis() {
  const [data, setData] = useState('');
  const [studentId, setStudentId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    if (!data.trim()) return;
    
    setAnalyzing(true);
    
    try {
      const response = await fetch('http://localhost:8000/analyze/excel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data,
          student_id: studentId || null
        })
      });
      const result = await response.json();
      setResults(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="analysis-page">
      <div className="container">
        <h1>📊 Excel Analysis</h1>
        <p className="subtitle">Detect AI-generated formulas and suspicious patterns</p>
        
        <div className="analysis-form">
          <textarea
            placeholder="Paste Excel data or CSV content..."
            value={data}
            onChange={(e) => setData(e.target.value)}
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
            disabled={!data.trim() || analyzing}
            className="btn btn-primary"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Excel'}
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
              <div className={`verdict ${results.anomaly_score > 0.5 ? 'high' : results.anomaly_score > 0.3 ? 'medium' : 'low'}`}>
                <h3>Anomaly Score</h3>
                <p className="verdict-text">{(results.anomaly_score * 100).toFixed(1)}%</p>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${results.anomaly_score * 100}%` }}
                  />
                </div>
              </div>
            </div>
            
            {results.ai_generated_formulas && results.ai_generated_formulas.length > 0 && (
              <div className="formulas">
                <h3>Suspicious Formulas</h3>
                {results.ai_generated_formulas.map((formula, index) => (
                  <div key={index} className="result-item">
                    <h4>Formula {index + 1}</h4>
                    <p>{formula.formula}</p>
                    <p className="value">Complexity: {formula.complexity.toFixed(4)}</p>
                    <p className="value">Reason: {formula.reason}</p>
                  </div>
                ))}
              </div>
            )}
            
            {results.suspicious_patterns && results.suspicious_patterns.length > 0 && (
              <div className="patterns">
                <h3>Suspicious Patterns</h3>
                {results.suspicious_patterns.map((pattern, index) => (
                  <div key={index} className="result-item">
                    <p>{pattern}</p>
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

export default ExcelAnalysis;
