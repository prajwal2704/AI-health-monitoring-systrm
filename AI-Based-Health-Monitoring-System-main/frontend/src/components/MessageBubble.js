import React from 'react';
import { User, Bot } from 'lucide-react';
import MedicalResponse from './MedicalResponse';
import { detectConversationMode } from '../utils/conversationModeDetector';
import './MessageBubble.css';

const MessageBubble = ({ message, conversationMode }) => {
  const isUser = message.role === 'user';

  // Use the mode from the message props, which is set when the message is created
  const mode = message.mode || conversationMode;

  return (
    <div className={`message-container ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-wrapper">
        <div className="avatar">
          {isUser ? (
            <div className="avatar-user">
              <User size={20} />
            </div>
          ) : (
            <div className="avatar-assistant">
              <Bot size={20} />
            </div>
          )}
        </div>
        <div className="message-content">
          {isUser ? (
            <div className="user-text">{message.content}</div>
          ) : (
            <div className="assistant-text">
              {message.content && typeof message.content === 'object' ? (
                <MedicalResponse response={message.content} mode={mode} />
              ) : (
                <div className="text-content">
                  {typeof message.content === 'string' ? message.content : 'Hello! I\'m here to help you with any health-related questions or concerns you might have. How can I assist you today?'}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;

