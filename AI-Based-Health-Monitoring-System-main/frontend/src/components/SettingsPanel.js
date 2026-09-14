import React, { useState } from 'react';
import { X, User, Globe } from 'lucide-react';
import AgeSelector from './AgeSelector';
import LanguageSelector from './LanguageSelector';
import './SettingsPanel.css';

const SettingsPanel = ({ 
  conversationId, 
  age, 
  language, 
  onAgeSet, 
  onLanguageSet, 
  onClose 
}) => {
  const [showAgeSelector, setShowAgeSelector] = useState(false);
  const [showLanguageSelector, setShowLanguageSelector] = useState(false);

  const handleAgeSet = (result) => {
    onAgeSet(result);
    setShowAgeSelector(false);
  };

  const handleLanguageSet = (result) => {
    onLanguageSet(result);
    setShowLanguageSelector(false);
  };

  return (
    <>
      <div className="settings-panel-overlay" onClick={onClose}></div>
      <div className="settings-panel">
        <div className="settings-header">
          <h2>Settings</h2>
          <button className="close-button" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="settings-content">
          <div className="settings-section">
            <div className="settings-item">
              <div className="settings-item-header">
                <User size={18} className="settings-icon" />
                <div className="settings-item-info">
                  <h3>Age Group</h3>
                  <p className="settings-value">{age || 'Not set'}</p>
                </div>
              </div>
              <button
                className="settings-change-button"
                onClick={() => setShowAgeSelector(true)}
              >
                {age ? 'Change' : 'Set Age'}
              </button>
            </div>

            <div className="settings-item">
              <div className="settings-item-header">
                <Globe size={18} className="settings-icon" />
                <div className="settings-item-info">
                  <h3>Language</h3>
                  <p className="settings-value">{language || 'English (default)'}</p>
                </div>
              </div>
              <button
                className="settings-change-button"
                onClick={() => setShowLanguageSelector(true)}
              >
                Change
              </button>
            </div>
          </div>
        </div>
      </div>

      {showAgeSelector && conversationId && (
        <AgeSelector
          conversationId={conversationId}
          onAgeSet={handleAgeSet}
          onClose={() => setShowAgeSelector(false)}
        />
      )}

      {showLanguageSelector && conversationId && (
        <LanguageSelector
          conversationId={conversationId}
          onLanguageSet={handleLanguageSet}
          onClose={() => setShowLanguageSelector(false)}
        />
      )}
    </>
  );
};

export default SettingsPanel;

