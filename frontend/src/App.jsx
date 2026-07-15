import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import ImageAnalysis from './components/ImageAnalysis';
import TextAnalysis from './components/TextAnalysis';
import VideoAnalysis from './components/VideoAnalysis';
import ExcelAnalysis from './components/ExcelAnalysis';
import CodeAnalysis from './components/CodeAnalysis';
import Integrations from './components/Integrations';
import ChainOfCustody from './components/ChainOfCustody';
import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <Router>
      <div className={`App ${darkMode ? 'dark' : 'light'}`}>
        <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/image" element={<ImageAnalysis />} />
            <Route path="/text" element={<TextAnalysis />} />
            <Route path="/video" element={<VideoAnalysis />} />
            <Route path="/excel" element={<ExcelAnalysis />} />
            <Route path="/code" element={<CodeAnalysis />} />
            <Route path="/integrations" element={<Integrations />} />
            <Route path="/custody" element={<ChainOfCustody />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
