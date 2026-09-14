import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader } from 'lucide-react';
import './ChatInput.css';

const ChatInput = ({ onSendMessage, disabled, loading }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled && !loading) {
      onSendMessage(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-input-container">
      <div className="chat-input-wrapper">
        <form onSubmit={handleSubmit} className="chat-input-form">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={disabled ? 'Please set your age group first to continue...' : 'Describe your symptoms...'}
            className="chat-input"
            rows={1}
            disabled={disabled || loading}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!message.trim() || disabled || loading}
            title="Send message (Enter)"
          >
            {loading ? (
              <Loader size={20} className="spinner" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </form>
        <div className="input-footer">
          <span className="footer-text">
            CarePulse can make mistakes. Please verify important information.
          </span>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;

