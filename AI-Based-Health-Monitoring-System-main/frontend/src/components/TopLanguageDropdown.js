import React, { useState, useEffect } from 'react';
import { Globe, ChevronDown } from 'lucide-react';
import { getLanguages, setLanguage } from '../services/api';
import './TopLanguageDropdown.css';

const TopLanguageDropdown = ({ conversationId, currentLanguage, onLanguageChanged }) => {
  const [languages, setLanguages] = useState({});
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLanguages();
  }, []);

  const loadLanguages = async () => {
    try {
      const data = await getLanguages();
      setLanguages(data.languages);
    } catch (err) {
      console.error('Failed to load languages:', err);
    }
  };

  const handleLanguageSelect = async (languageCode) => {
    if (languageCode === currentLanguage || !conversationId) {
      setIsOpen(false);
      return;
    }

    setLoading(true);
    try {
      const result = await setLanguage(conversationId, languageCode);

      if (result.success) {
        // Notify parent component of language change
        onLanguageChanged(result);
      }
    } catch (err) {
      console.error('Failed to change language:', err);
    } finally {
      setLoading(false);
      setIsOpen(false);
    }
  };

  const getCurrentLanguageDisplay = () => {
    if (!currentLanguage || !languages[currentLanguage]) {
      return 'English';
    }
    return languages[currentLanguage];
  };

  return (
    <div className="top-language-dropdown">
      <button
        className={`language-button ${loading ? 'loading' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        disabled={loading}
        title="Change language"
      >
        <Globe size={16} className="globe-icon" />
        <span className="language-text">{getCurrentLanguageDisplay()}</span>
        <ChevronDown size={14} className={`chevron-icon ${isOpen ? 'rotated' : ''}`} />
      </button>

      {isOpen && (
        <>
          <div
            className="dropdown-overlay"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="language-dropdown-menu">
            {Object.entries(languages).map(([code, name]) => (
              <button
                key={code}
                className={`language-option ${
                  code === currentLanguage ? 'active' : ''
                }`}
                onClick={() => handleLanguageSelect(code)}
                disabled={loading}
              >
                <span className="language-name">{name}</span>
                {code === currentLanguage && (
                  <span className="checkmark">✓</span>
                )}
                {code !== 'english' && (
                  <span className="language-code">({code})</span>
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default TopLanguageDropdown;
