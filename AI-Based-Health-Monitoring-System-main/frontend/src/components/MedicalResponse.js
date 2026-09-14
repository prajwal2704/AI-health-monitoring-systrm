import React from 'react';
import { AlertTriangle, Home, Heart, Lightbulb } from 'lucide-react';
import './MedicalResponse.css';

const MedicalResponse = ({ response, mode }) => {
  if (!response) return null;

  // Show conversational response in general mode
  if (mode !== 'medical') {
    const displayText = typeof response === 'string'
      ? response
      : (response.summary || response.message || response.content || 'Hello! I\'m here to help you with any health-related questions or concerns you might have. How can I assist you today?');
    return (
      <div className="conversational-response">
        <div className="text-content">
          {displayText}
        </div>
      </div>
    );
  }

  // Ensure we have the expected structure for medical responses
  if (typeof response === 'string') {
    return (
      <div className="medical-response">
        <div className="text-content">{response}</div>
      </div>
    );
  }

  return (
    <div className="medical-response">
      {/* Summary Section */}
      {response.summary && (
        <div className="response-section">
          <div className="section-header">
            <Lightbulb size={18} className="section-icon" />
            <h3>(A) Brief Summary of Symptoms</h3>
          </div>
          <div className="section-content">{response.summary}</div>
        </div>
      )}

      {/* Home Care Section */}
      {response.home_care && (
        <div className="response-section">
          <div className="section-header">
            <Home size={18} className="section-icon" />
            <h3>(B) Home Care Recommendations</h3>
          </div>
          <div className="section-content">
            {response.home_care.split('\n').map((line, index) => (
              <div key={index} className="content-line">
                {line}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Medical Attention Section */}
      {response.medical_attention && (
        <div className="response-section attention-section">
          <div className="section-header">
            <Heart size={18} className="section-icon attention-icon" />
            <h3>(C) When to Seek Medical Attention</h3>
          </div>
          <div className="section-content">
            {response.medical_attention.split('\n').map((line, index) => (
              <div key={index} className="content-line">
                {line}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Possible Causes Section */}
      {response.possible_causes && (
        <div className="response-section">
          <div className="section-header">
            <Lightbulb size={18} className="section-icon" />
            <h3>(D) Possible Causes</h3>
          </div>
          <div className="section-content">
            {response.possible_causes.split('\n').map((line, index) => (
              <div key={index} className="content-line">
                {line}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Disclaimer */}
      {response.disclaimer && (
        <div className="disclaimer-section">
          <div className="disclaimer-header">
            <AlertTriangle size={20} className="disclaimer-icon" />
            <h3>Important Disclaimer</h3>
          </div>
          <div className="disclaimer-content">{response.disclaimer}</div>
        </div>
      )}
    </div>
  );
};

export default MedicalResponse;

