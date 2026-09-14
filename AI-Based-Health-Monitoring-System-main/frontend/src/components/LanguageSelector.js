import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { getLanguages, setLanguage } from '../services/api';
import './LanguageSelector.css';

const LanguageSelector = ({ conversationId, onLanguageSet, onClose }) => {
  const [languages, setLanguages] = useState({});
  const [selectedLanguage, setSelectedLanguage] = useState('english');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadLanguages();
  }, []);

  const loadLanguages = async () => {
    try {
      const data = await getLanguages();
      setLanguages(data.languages);
      setSelectedLanguage(data.default_language);
    } catch (err) {
      setError('Failed to load languages');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedLanguage) {
      setError('Please select a language');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await setLanguage(conversationId, selectedLanguage);
      if (result.success) {
        onLanguageSet(result);
      } else {
        setError(result.error || 'Failed to set language');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to set language');
    } finally {
      setLoading(false);
    }
  };

  const handleSkip = async () => {
    // Language defaults to English, set it via API to ensure backend state is correct
    setLoading(true);
    try {
      const result = await setLanguage(conversationId, 'english');
      if (result.success) {
        onLanguageSet(result);
      } else {
        // If API fails, still proceed with default
        onLanguageSet({ success: true, language: 'english', state: 'ready' });
      }
    } catch (err) {
      // If API fails, still proceed with default
      onLanguageSet({ success: true, language: 'english', state: 'ready' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Select Your Preferred Language</h2>
          <button className="close-button" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="language-select">Language (Optional - defaults to English)</label>
            <select
              id="language-select"
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="language-select"
            >
              {Object.entries(languages).map(([code, name]) => (
                <option key={code} value={code}>
                  {name} {code !== 'english' ? `(${code})` : ''}
                </option>
              ))}
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="modal-actions">
            <button
              type="button"
              className="btn-secondary"
              onClick={handleSkip}
              disabled={loading}
            >
              Skip (Use English)
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={loading}
            >
              {loading ? 'Setting...' : 'Continue'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LanguageSelector;

