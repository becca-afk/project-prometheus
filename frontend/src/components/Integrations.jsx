import React, { useState } from 'react';
import './Integrations.css';

function Integrations() {
  const [platform, setPlatform] = useState('google');
  const [fileId, setFileId] = useState('');
  const [studentId, setStudentId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState({
    google: false,
    microsoft: false
  });

  const handleConnect = async (targetPlatform) => {
    try {
      if (targetPlatform === 'google') {
        // Mock connection - in production, this would use OAuth
        setConnectionStatus(prev => ({ ...prev, google: true }));
      } else if (targetPlatform === 'microsoft') {
        // Mock connection - in production, this would use OAuth
        setConnectionStatus(prev => ({ ...prev, microsoft: true }));
      }
    } catch (error) {
      console.error('Connection failed:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!fileId.trim()) return;
    
    setAnalyzing(true);
    
    try {
      const endpoint = platform === 'google' 
        ? 'http://localhost:8000/integrations/google-doc'
        : 'http://localhost:8000/integrations/microsoft-word';
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          doc_id: fileId,
          file_id: fileId,
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
    <div className="integrations-page">
      <div className="container">
        <h1>🔗 Enterprise Integrations</h1>
        <p className="subtitle">Connect to Google Workspace and Microsoft 365 for document analysis</p>
        
        <div className="connection-status">
          <div className={`status-card ${connectionStatus.google ? 'connected' : 'disconnected'}`}>
            <div className="status-icon">{connectionStatus.google ? '✅' : '❌'}</div>
            <h3>Google Workspace</h3>
            <p>{connectionStatus.google ? 'Connected' : 'Not Connected'}</p>
            {!connectionStatus.google && (
              <button onClick={() => handleConnect('google')} className="btn btn-secondary">
                Connect
              </button>
            )}
          </div>
          
          <div className={`status-card ${connectionStatus.microsoft ? 'connected' : 'disconnected'}`}>
            <div className="status-icon">{connectionStatus.microsoft ? '✅' : '❌'}</div>
            <h3>Microsoft 365</h3>
            <p>{connectionStatus.microsoft ? 'Connected' : 'Not Connected'}</p>
            {!connectionStatus.microsoft && (
              <button onClick={() => handleConnect('microsoft')} className="btn btn-secondary">
                Connect
              </button>
            )}
          </div>
        </div>
        
        <div className="analysis-form">
          <h2>Analyze Document</h2>
          
          <div className="platform-selector">
            <button 
              className={`platform-btn ${platform === 'google' ? 'active' : ''}`}
              onClick={() => setPlatform('google')}
            >
              Google Docs/Sheets
            </button>
            <button 
              className={`platform-btn ${platform === 'microsoft' ? 'active' : ''}`}
              onClick={() => setPlatform('microsoft')}
            >
              Microsoft Word/Excel
            </button>
          </div>
          
          <input 
            type="text"
            placeholder={`${platform === 'google' ? 'Google Doc/Sheet ID' : 'Microsoft File ID'}`}
            value={fileId}
            onChange={(e) => setFileId(e.target.value)}
            className="input"
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
            disabled={!fileId.trim() || analyzing}
            className="btn btn-primary"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Document'}
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
            
            {platform === 'google' ? (
              <>
                {results.google_doc_data && (
                  <div className="document-info">
                    <h3>Document Info</h3>
                    <p>Title: {results.google_doc_data.doc_metadata?.title}</p>
                    <p>Revisions: {results.google_doc_data.revision_history?.length}</p>
                  </div>
                )}
                
                {results.analysis_result && (
                  <div className="analysis-result">
                    <h3>AI Detection Results</h3>
                    <p>AI Likelihood: {(results.analysis_result.ai_likelihood * 100).toFixed(1)}%</p>
                    <p>Anomalies: {results.analysis_result.anomalies?.length || 0}</p>
                  </div>
                )}
              </>
            ) : (
              <>
                {results.microsoft_word_data && (
                  <div className="document-info">
                    <h3>Document Info</h3>
                    <p>Versions: {results.microsoft_word_data.versions?.length}</p>
                  </div>
                )}
                
                {results.analysis_result && (
                  <div className="analysis-result">
                    <h3>AI Detection Results</h3>
                    <p>AI Likelihood: {(results.analysis_result.ai_likelihood * 100).toFixed(1)}%</p>
                    <p>Anomalies: {results.analysis_result.anomalies?.length || 0}</p>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Integrations;
