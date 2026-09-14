import React from 'react';
import { MessageSquare, Clock } from 'lucide-react';
import './ConversationHistory.css';

const ConversationHistory = ({ conversations, onSelectConversation, currentConversationId }) => {
  if (!conversations || conversations.length === 0) {
    return (
      <div className="conversation-history-empty">
        <MessageSquare size={24} className="empty-icon" />
        <p>No conversation history</p>
        <span className="empty-hint">Start a new chat to begin</span>
      </div>
    );
  }

  return (
    <div className="conversation-history">
      <div className="conversation-history-header">
        <h3>Conversations</h3>
      </div>
      <div className="conversation-list">
        {conversations.map((conv) => (
          <div
            key={conv.id}
            className={`conversation-item ${
              conv.id === currentConversationId ? 'active' : ''
            }`}
            onClick={() => onSelectConversation(conv.id)}
          >
            <MessageSquare size={16} className="conversation-icon" />
            <div className="conversation-info">
              <p className="conversation-title">{conv.title || 'New Conversation'}</p>
              <div className="conversation-meta">
                <Clock size={12} />
                <span>{conv.lastMessageTime || 'Just now'}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConversationHistory;

