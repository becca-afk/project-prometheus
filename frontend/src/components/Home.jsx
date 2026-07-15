import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <div className="hero">
        <h1 className="hero-title">Project Prometheus</h1>
        <p className="hero-subtitle">Advanced AI Detection System for Academic Integrity</p>
        <p className="hero-description">
          Enterprise-grade multi-vector adversarial AI detection for images, videos, text, 
          spreadsheets, and code. Protect academic integrity with forensic-level analysis.
        </p>
        
        <div className="hero-buttons">
          <Link to="/image" className="btn btn-primary">Analyze Image</Link>
          <Link to="/text" className="btn btn-secondary">Analyze Text</Link>
          <Link to="/video" className="btn btn-secondary">Analyze Video</Link>
        </div>
      </div>
      
      <div className="features">
        <h2 className="features-title">Detection Capabilities</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">👤</div>
            <h3>Deepfake Detection</h3>
            <p>Detect face swaps, synthetic faces, and manipulated media using 7 biometric signals</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>AI Text Detection</h3>
            <p>Identify AI-generated writing with stylometric fingerprinting and burstiness analysis</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Excel Analysis</h3>
            <p>Detect AI-generated formulas and suspicious patterns in spreadsheets</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">💻</div>
            <h3>Code Detection</h3>
            <p>Analyze code for AI generation with style consistency checks</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔗</div>
            <h3>Enterprise Integrations</h3>
            <p>Connect to Google Workspace and Microsoft 365 for document history analysis</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">⚖️</div>
            <h3>Chain of Custody</h3>
            <p>Complete audit trails for academic integrity proceedings and hearings</p>
          </div>
        </div>
      </div>
      
      <div className="stats">
        <div className="stat-item">
          <div className="stat-number">7</div>
          <div className="stat-label">Biometric Signals</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">5</div>
          <div className="stat-label">Detection Modules</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">2</div>
          <div className="stat-label">Enterprise Platforms</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">100%</div>
          <div className="stat-label">Forensic Grade</div>
        </div>
      </div>
    </div>
  );
}

export default Home;
