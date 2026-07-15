import React, { useState } from 'react';
import './ChainOfCustody.css';

function ChainOfCustody() {
  const [caseId, setCaseId] = useState('');
  const [studentId, setStudentId] = useState('');
  const [submissionInfo, setSubmissionInfo] = useState('');
  const [activeCase, setActiveCase] = useState(null);
  const [caseReport, setCaseReport] = useState(null);
  const [note, setNote] = useState('');
  const [author, setAuthor] = useState('');

  const handleCreateCase = async () => {
    if (!caseId.trim() || !studentId.trim()) return;
    
    try {
      const response = await fetch('http://localhost:8000/custody/create-case', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          case_id: caseId,
          student_id: studentId,
          submission_info: {
            description: submissionInfo,
            created_at: new Date().toISOString()
          }
        })
      });
      const data = await response.json();
      setActiveCase(data);
      setCaseReport(null);
    } catch (error) {
      console.error('Failed to create case:', error);
    }
  };

  const handleAddNote = async () => {
    if (!note.trim() || !author.trim() || !activeCase) return;
    
    try {
      await fetch(`http://localhost:8000/custody/${activeCase.case_id}/add-note`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ note, author })
      });
      setNote('');
      // Refresh case report
      handleGenerateReport();
    } catch (error) {
      console.error('Failed to add note:', error);
    }
  };

  const handleGenerateReport = async () => {
    if (!activeCase) return;
    
    try {
      const response = await fetch(`http://localhost:8000/custody/${activeCase.case_id}/report`);
      const data = await response.json();
      setCaseReport(data);
    } catch (error) {
      console.error('Failed to generate report:', error);
    }
  };

  return (
    <div className="custody-page">
      <div className="container">
        <h1>⚖️ Chain of Custody</h1>
        <p className="subtitle">Track academic integrity cases with complete audit trails</p>
        
        <div className="custody-grid">
          <div className="case-creation">
            <h2>Create New Case</h2>
            
            <input 
              type="text"
              placeholder="Case ID"
              value={caseId}
              onChange={(e) => setCaseId(e.target.value)}
              className="input"
            />
            
            <input 
              type="text"
              placeholder="Student ID"
              value={studentId}
              onChange={(e) => setStudentId(e.target.value)}
              className="input"
            />
            
            <textarea
              placeholder="Submission information/description"
              value={submissionInfo}
              onChange={(e) => setSubmissionInfo(e.target.value)}
              className="input textarea"
            />
            
            <button 
              onClick={handleCreateCase}
              disabled={!caseId.trim() || !studentId.trim()}
              className="btn btn-primary"
            >
              Create Case
            </button>
          </div>
          
          {activeCase && (
            <div className="case-management">
              <h2>Case Management</h2>
              
              <div className="case-info">
                <h3>Active Case: {activeCase.case_id}</h3>
                <p>Student: {activeCase.student_id}</p>
                <p>Status: {activeCase.status}</p>
                <p>Created: {new Date(activeCase.created_at).toLocaleString()}</p>
              </div>
              
              <div className="add-note">
                <h3>Add Note</h3>
                <input 
                  type="text"
                  placeholder="Author"
                  value={author}
                  onChange={(e) => setAuthor(e.target.value)}
                  className="input"
                />
                <textarea
                  placeholder="Note content"
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  className="input textarea"
                />
                <button 
                  onClick={handleAddNote}
                  disabled={!note.trim() || !author.trim()}
                  className="btn btn-secondary"
                >
                  Add Note
                </button>
              </div>
              
              <button 
                onClick={handleGenerateReport}
                className="btn btn-primary"
              >
                Generate Report
              </button>
            </div>
          )}
        </div>
        
        {caseReport && (
          <div className="case-report">
            <h2>Chain of Custody Report</h2>
            
            <div className="report-section">
              <h3>Case Information</h3>
              <p><strong>Case ID:</strong> {caseReport.case_id}</p>
              <p><strong>Student ID:</strong> {caseReport.student_id}</p>
              <p><strong>Created:</strong> {new Date(caseReport.created_at).toLocaleString()}</p>
              <p><strong>Status:</strong> {caseReport.status}</p>
            </div>
            
            {caseReport.analysis_summary && (
              <div className="report-section">
                <h3>Analysis Summary</h3>
                <p><strong>Total Analyses:</strong> {caseReport.analysis_summary.total_analyses}</p>
                <p><strong>Final Verdict:</strong> {caseReport.analysis_summary.final_verdict}</p>
              </div>
            )}
            
            {caseReport.notes && caseReport.notes.length > 0 && (
              <div className="report-section">
                <h3>Case Notes</h3>
                {caseReport.notes.map((noteItem, index) => (
                  <div key={index} className="note-item">
                    <p><strong>{noteItem.author}</strong> - {new Date(noteItem.timestamp).toLocaleString()}</p>
                    <p>{noteItem.note}</p>
                  </div>
                ))}
              </div>
            )}
            
            <div className="report-section">
              <h3>Report Metadata</h3>
              <p><strong>Generated:</strong> {new Date(caseReport.report_generated_at).toLocaleString()}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChainOfCustody;
