import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { getAgeGroups, setAge } from '../services/api';
import './AgeSelector.css';

const AgeSelector = ({ conversationId, onAgeSet, onClose }) => {
  const [ageGroups, setAgeGroups] = useState([]);
  const [selectedAge, setSelectedAge] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAgeGroups();
  }, []);

  const loadAgeGroups = async () => {
    try {
      const groups = await getAgeGroups();
      setAgeGroups(groups);
    } catch (err) {
      setError('Failed to load age groups');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedAge) {
      setError('Please select an age group');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await setAge(conversationId, selectedAge);
      if (result.success) {
        onAgeSet(result);
      } else {
        setError(result.error || 'Failed to set age');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to set age');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Select Your Age Group</h2>
          <button className="close-button" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="age-select">Age Group (Required)</label>
            <select
              id="age-select"
              value={selectedAge}
              onChange={(e) => setSelectedAge(e.target.value)}
              className="age-select"
              required
            >
              <option value="">-- Select Age Group --</option>
              {ageGroups.map((age, index) => (
                <option key={index} value={age}>
                  {age}
                </option>
              ))}
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="modal-actions">
            <button
              type="button"
              className="btn-secondary"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !selectedAge}
            >
              {loading ? 'Setting...' : 'Continue'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AgeSelector;

