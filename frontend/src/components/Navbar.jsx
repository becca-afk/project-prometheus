import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar({ darkMode, setDarkMode }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Link to="/">
            <h1>🔍 Project Prometheus</h1>
          </Link>
        </div>
        
        <div className="navbar-links">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/image" className="nav-link">Image</Link>
          <Link to="/text" className="nav-link">Text</Link>
          <Link to="/video" className="nav-link">Video</Link>
          <Link to="/excel" className="nav-link">Excel</Link>
          <Link to="/code" className="nav-link">Code</Link>
          <Link to="/integrations" className="nav-link">Integrations</Link>
          <Link to="/custody" className="nav-link">Chain of Custody</Link>
        </div>
        
        <button 
          className="theme-toggle"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
