import React, { useState } from 'react';
import axios from 'axios';
import { Activity, Sparkles, BrainCircuit } from 'lucide-react';
import './App.css';

function App() {
  const [attendance, setAttendance] = useState(50);
  const [assignment, setAssignment] = useState(50);
  const [test, setTest] = useState(50);
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handlePredict = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://localhost:8000/predict', {
        attendance,
        assignment,
        test
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to connect to the prediction server. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="blob blob-1"></div>
      <div className="blob blob-2"></div>
      
      <div className="container">
        <div className="header">
          <h1>Student Performance AI</h1>
          <p>Powered by a Hybrid Fuzzy Logic & Neural Network System</p>
        </div>

        <div className="controls">
          <div className="slider-group">
            <div className="slider-header">
              <label className="slider-label">Attendance Score</label>
              <span className="slider-value">{attendance}%</span>
            </div>
            <input 
              type="range" 
              min="0" max="100" 
              value={attendance} 
              onChange={(e) => setAttendance(parseInt(e.target.value))}
            />
          </div>

          <div className="slider-group">
            <div className="slider-header">
              <label className="slider-label">Assignment Marks</label>
              <span className="slider-value">{assignment}%</span>
            </div>
            <input 
              type="range" 
              min="0" max="100" 
              value={assignment} 
              onChange={(e) => setAssignment(parseInt(e.target.value))}
            />
          </div>

          <div className="slider-group">
            <div className="slider-header">
              <label className="slider-label">Test Marks</label>
              <span className="slider-value">{test}%</span>
            </div>
            <input 
              type="range" 
              min="0" max="100" 
              value={test} 
              onChange={(e) => setTest(parseInt(e.target.value))}
            />
          </div>

          {error && <div style={{color: '#ef4444', fontSize: '0.9rem', textAlign: 'center'}}>{error}</div>}

          <button className="predict-btn" onClick={handlePredict} disabled={loading}>
            {loading ? (
              <Activity className="lucide-spin" size={20} style={{ animation: 'spin 2s linear infinite' }} />
            ) : (
              <Sparkles size={20} />
            )}
            {loading ? 'Analyzing...' : 'Predict Performance'}
          </button>
        </div>

        {result && (
          <div className="result-card">
            <div className="result-header">Prediction Result</div>
            <div className={`performance-level level-${result.prediction}`}>
              {result.prediction}
            </div>
            
            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Neural Net Confidence</span>
                <span className="metric-value">{(result.confidence * 100).toFixed(1)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Fuzzy Output Score</span>
                <span className="metric-value">{result.fuzzy_score.toFixed(1)}/100</span>
              </div>
            </div>

            <div className="explanation">
              <strong><BrainCircuit size={14} style={{display:'inline', marginBottom:'-2px'}} /> Hybrid Intel:</strong> The system used Fuzzy Logic to process the ambiguous human rules and produce a score of {result.fuzzy_score.toFixed(1)}, which was then fed alongside the raw inputs into an Artificial Neural Network, classifying the final performance as <em>{result.prediction}</em>.
            </div>
          </div>
        )}
      </div>
      <style>{`
        @keyframes spin { 100% { transform: rotate(360deg); } }
      `}</style>
    </>
  );
}

export default App;
