import React, { useState, useEffect, useRef } from 'react';
import { Settings, MessageSquare, LogOut } from 'lucide-react';
import MessageBubble from './components/MessageBubble';
import ChatInput from './components/ChatInput';
import SettingsPanel from './components/SettingsPanel';
import ConversationHistory from './components/ConversationHistory';
import AgeSelector from './components/AgeSelector';
import LanguageSelector from './components/LanguageSelector';
import TopLanguageDropdown from './components/TopLanguageDropdown';
import LoginPage from './components/LoginPage';
import {
  startConversation,
  sendMessage,
  getUserConversations,
  saveConversation,
} from './services/api';
import { getUniqueConversationTitle } from './utils/conversationNaming';
import { detectConversationMode } from './utils/conversationModeDetector';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [sessionToken, setSessionToken] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [state, setState] = useState('initial');
  const [age, setAge] = useState(null);
  const [language, setLanguage] = useState('english');
  const [loading, setLoading] = useState(false);
  const [showAgeSelector, setShowAgeSelector] = useState(false);
  const [showLanguageSelector, setShowLanguageSelector] = useState(false);
  const [showSettingsPanel, setShowSettingsPanel] = useState(false);
  const [error, setError] = useState(null);
  const [conversations, setConversations] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    checkAuthentication();
  }, []);

  useEffect(() => {
    // Only initialize conversation if authenticated and no conversations exist
    if (isAuthenticated && conversations.length === 0 && !conversationId) {
      initializeConversation();
    }
  }, [isAuthenticated, conversations.length, conversationId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const checkAuthentication = () => {
    const token = localStorage.getItem('session_token');
    const userData = localStorage.getItem('user');

    if (token && userData) {
      const parsedUser = JSON.parse(userData);
      setSessionToken(token);
      setUser(parsedUser);
      setIsAuthenticated(true);
      loadUserConversations(token);
    }
  };

  const loadUserConversations = async (token) => {
    try {
      const result = await getUserConversations(token);
      if (result.success) {
        setConversations(result.conversations);
      }
    } catch (err) {
      console.error('Failed to load conversations:', err);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleLoginSuccess = (token, userData) => {
    setSessionToken(token);
    setUser(userData);
    setIsAuthenticated(true);
    loadUserConversations(token);
  };

  const handleLogout = () => {
    localStorage.removeItem('session_token');
    localStorage.removeItem('user');
    setSessionToken(null);
    setUser(null);
    setIsAuthenticated(false);
    setConversations([]);
    setMessages([]);
    setConversationId(null);
    setAge(null);
    setLanguage('english');
    setState('initial');
    setError(null);
  };

  const initializeConversation = async () => {
    try {
      const result = await startConversation();
      if (result.success) {
        setConversationId(result.conversation_id);
        setState(result.state);
        // Show age selector if needed
        if (result.state === 'awaiting_age') {
          setShowAgeSelector(true);
        }
      }
    } catch (err) {
      setError('Failed to initialize conversation. Please refresh the page.');
      console.error('Error initializing conversation:', err);
    }
  };

  const handleAgeSet = (result) => {
    setAge(result.age);
    setState(result.state);
    setShowAgeSelector(false);
    
    // If state is ready, we can start chatting immediately
    // If awaiting_language, show selector but input is still enabled (language defaults to English)
    if (result.state === 'awaiting_language') {
      // Show language selector but don't block input
      // User can skip and use default English, or select a language
      setShowLanguageSelector(true);
    }
    // If state is 'ready', input is already enabled (no action needed)
  };

  const handleLanguageSet = (result) => {
    setLanguage(result.language);
    if (result.state) {
      setState(result.state);
    }
    setShowLanguageSelector(false);

    // If backend returned translated messages, update displayed messages
    if (result.translated_messages && Array.isArray(result.translated_messages)) {
      const translated = result.translated_messages.map((m) => ({
        role: m.role,
        content: m.content,
        timestamp: m.timestamp || new Date().toISOString(),
      }));
      setMessages(translated);
      // Update conversation history entry if present
      setConversations((prevConvs) => {
        const idx = prevConvs.findIndex((c) => c.id === conversationId);
        if (idx >= 0) {
          const copy = [...prevConvs];
          copy[idx] = { ...copy[idx], language: result.language, messages: translated };
          return copy;
        }
        return prevConvs;
      });
    }
  };


  const handleSendMessage = async (messageText) => {
    if (!conversationId || !messageText.trim()) return;

    console.log('=== MESSAGE HANDLING START ===');
    console.log('Current age:', age);
    console.log('User input:', messageText);

    // Detect conversation mode FIRST
    const conversationMode = detectConversationMode(messageText);
    console.log('Detected conversation mode:', conversationMode);

    // CRITICAL RULE: If medical mode is detected, age MUST be set first
    if (conversationMode === 'medical' && !age) {
      console.log('BLOCKING: Medical mode detected but no age set');
      setShowAgeSelector(true);
      // Add a special message to guide the user
      const guidanceMessage = {
        role: 'assistant',
        content: `I understand you're experiencing some health concerns. To provide you with accurate medical guidance and appropriate dosage recommendations, please select your age group first.`,
        timestamp: new Date().toISOString(),
        mode: 'medical_blocked'
      };
      setMessages((prev) => [...prev, guidanceMessage]);
      console.log('=== MESSAGE HANDLING END (BLOCKED) ===');
      return;
    }

    // For general conversation or when age is already set, proceed normally
    if (!age && conversationMode === 'general') {
      console.log('BLOCKING: General mode but no age set');
      setShowAgeSelector(true);
      console.log('=== MESSAGE HANDLING END (BLOCKED) ===');
      return;
    }

    console.log('PROCEEDING: Will call API');
    console.log('=== MESSAGE HANDLING END (PROCEEDING) ===');

    // Add user message to UI immediately
    const userMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString(),
      mode: conversationMode,
    };
    setMessages((prev) => {
      const updated = [...prev, userMessage];
      // Save to conversation history if this is a new conversation
      if (prev.length === 0 && conversationId) {
        const convTitle = getUniqueConversationTitle(updated, conversations, age);
        const newConv = {
          id: conversationId,
          title: convTitle,
          lastMessageTime: new Date().toLocaleTimeString(),
          messages: updated,
          age: age,
          language: language,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        setConversations((prevConvs) => [newConv, ...prevConvs]);

        // Save new conversation to backend
        saveConversation(newConv).catch(err =>
          console.error('Failed to save conversation:', err)
        );
      }
      return updated;
    });
    setLoading(true);
    setError(null);

    try {
      const result = await sendMessage(conversationId, messageText);
      
      if (result.success) {
        const assistantMessage = {
          role: 'assistant',
          content: result.response,
          timestamp: new Date().toISOString(),
          mode: conversationMode, // Attach the detected mode to the assistant message
        };
        setMessages((prev) => {
          const updated = [...prev, assistantMessage];
          // Update conversation in history if it exists
          setConversations((prevConvs) => {
            const existingIndex = prevConvs.findIndex((c) => c.id === conversationId);
            if (existingIndex >= 0) {
              const updatedConvs = [...prevConvs];
              // Update title if it's still generic and we have enough context
              let title = updatedConvs[existingIndex].title;
              if (title === 'New Conversation' || title.length < 10) {
                title = getUniqueConversationTitle(updated, prevConvs, age);
              }
              updatedConvs[existingIndex] = {
                ...updatedConvs[existingIndex],
                title: title,
                messages: updated,
                lastMessageTime: new Date().toLocaleTimeString(),
                updated_at: new Date().toISOString(),
              };

              // Save updated conversation to backend
              saveConversation(updatedConvs[existingIndex]).catch(err =>
                console.error('Failed to save conversation:', err)
              );

              return updatedConvs;
            } else {
              // Create new conversation entry if it doesn't exist
              const convTitle = getUniqueConversationTitle(updated, prevConvs, age);
              return [
                {
                  id: conversationId,
                  title: convTitle,
                  lastMessageTime: new Date().toLocaleTimeString(),
                  messages: updated,
                  age: age,
                  language: language,
                },
                ...prevConvs,
              ];
            }
          });
          return updated;
        });

        // Debug logging
        console.log('User message:', messageText);
        console.log('Detected mode:', conversationMode);
        console.log('Assistant response:', result.response);
        setState('in_conversation');
      } else {
        setError(result.error || 'Failed to get response');
        // Remove user message if error
        setMessages((prev) => {
          const updated = prev.slice(0, -1);
          // Update conversation in history
          setConversations((prevConvs) => {
            const existingIndex = prevConvs.findIndex((c) => c.id === conversationId);
            if (existingIndex >= 0) {
              const updatedConvs = [...prevConvs];
              updatedConvs[existingIndex] = {
                ...updatedConvs[existingIndex],
                messages: updated,
              };
              return updatedConvs;
            }
            return prevConvs;
          });
          return updated;
        });
        
        // Handle specific errors
        if (result.requires_age) {
          setShowAgeSelector(true);
        } else if (result.requires_language) {
          setShowLanguageSelector(true);
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send message');
      // Remove user message if error
      setMessages((prev) => {
        const updated = prev.slice(0, -1);
        // Update conversation in history
        setConversations((prevConvs) => {
          const existingIndex = prevConvs.findIndex((c) => c.id === conversationId);
          if (existingIndex >= 0) {
            const updatedConvs = [...prevConvs];
            updatedConvs[existingIndex] = {
              ...updatedConvs[existingIndex],
              messages: updated,
            };
            return updatedConvs;
          }
          return prevConvs;
        });
        return updated;
      });
      console.error('Error sending message:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async () => {
    // Save current conversation to history if it has messages
    if (messages.length > 0 && conversationId) {
      // Check if this conversation is already in history
      const existingIndex = conversations.findIndex((c) => c.id === conversationId);
      if (existingIndex === -1) {
        // Generate intelligent title
        const convTitle = getUniqueConversationTitle(messages, conversations, age);
        const currentConv = {
          id: conversationId,
          title: convTitle,
          lastMessageTime: new Date().toLocaleTimeString(),
          messages: messages,
          age: age,
          language: language,
          created_at: conversations.find(c => c.id === conversationId)?.created_at || new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        // Save to backend
        try {
          await saveConversation(currentConv);
          setConversations((prev) => [currentConv, ...prev]);
        } catch (err) {
          console.error('Failed to save conversation:', err);
        }
      }
    }

    // Reset state for new conversation
    setMessages([]);
    setAge(null);
    setLanguage('english');
    setState('initial');
    setError(null);
    setConversationId(null);

    // Start new conversation
    initializeConversation();
  };

  const handleSelectConversation = (convId) => {
    const conv = conversations.find((c) => c.id === convId);
    if (conv) {
      setConversationId(conv.id);
      setMessages(conv.messages || []);
      setAge(conv.age);
      setLanguage(conv.language);
      setState('in_conversation');
      setError(null);
    }
  };

  // If not authenticated, show login page
  if (!isAuthenticated) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app">
      <div className="background-image"></div>
      {/* Left Sidebar - Conversation History */}
      <div className="sidebar">
        <div className="sidebar-header">
          <button className="new-chat-button" onClick={handleNewChat}>
            <MessageSquare size={20} />
            <span>New Chat</span>
          </button>
        </div>

        <ConversationHistory
          conversations={conversations}
          onSelectConversation={handleSelectConversation}
          currentConversationId={conversationId}
        />

        <div className="sidebar-actions">
          <button
            className="action-button"
            onClick={() => setShowSettingsPanel(true)}
            title="Settings"
          >
            <Settings size={18} />
            <span>Settings</span>
          </button>
          <button
            className="action-button logout-button"
            onClick={handleLogout}
            title="Logout"
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-content">
        <div className="main-chat-container">
          <div className="user-header">
            <div className="user-info">
              <span className="welcome-user">Welcome, {user?.full_name || 'User'}</span>
            </div>
            {conversationId && (
              <TopLanguageDropdown
                conversationId={conversationId}
                currentLanguage={language}
                onLanguageChanged={handleLanguageSet}
              />
            )}
          </div>
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-content">
              <h1>CarePulse</h1>
              <p>Describe your symptoms and get medical guidance</p>
              {!age && (
                <div className="welcome-action">
                  <button
                    className="welcome-button"
                    onClick={() => setShowAgeSelector(true)}
                  >
                    Get Started - Set Your Age
                  </button>
                  <p className="welcome-hint">
                    You need to set your age group before you can describe symptoms
                  </p>
                </div>
              )}
              {age && state === 'ready' && (
                <div className="welcome-action">
                  <p className="welcome-ready">
                    ✓ Ready! You can now describe your symptoms below.
                  </p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="messages-container">
            {messages.map((message, index) => (
              <MessageBubble
                key={index}
                message={message}
                conversationMode={message.mode}
              />
            ))}
            {loading && (
              <div className="loading-indicator">
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={!age || !conversationId}
          loading={loading}
        />
      </div>
    </div>

    {/* Right Sidebar - Settings Panel */}
    {showSettingsPanel && (
      <SettingsPanel
        conversationId={conversationId}
        age={age}
        language={language}
        onAgeSet={handleAgeSet}
        onLanguageSet={handleLanguageSet}
        onClose={() => setShowSettingsPanel(false)}
      />
    )}

    {/* Modals (for initial setup) */}
    {showAgeSelector && conversationId && !showSettingsPanel && (
      <AgeSelector
        conversationId={conversationId}
        onAgeSet={handleAgeSet}
        onClose={() => setShowAgeSelector(false)}
      />
    )}

    {showLanguageSelector && conversationId && !showSettingsPanel && (
      <LanguageSelector
        conversationId={conversationId}
        onLanguageSet={handleLanguageSet}
        onClose={() => setShowLanguageSelector(false)}
      />
    )}
  </div>
  );
}

export default App;

