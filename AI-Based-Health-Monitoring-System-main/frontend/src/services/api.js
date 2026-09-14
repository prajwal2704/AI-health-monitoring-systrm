import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add authentication header to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('session_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle expired or invalid sessions automatically
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const isAuthRoute = error.config?.url?.includes('/api/auth/');
      if (!isAuthRoute) {
        localStorage.removeItem('session_token');
        localStorage.removeItem('user');
        window.location.reload();
      }
    }
    return Promise.reject(error);
  }
);

// Health check
export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Get configuration
export const getAgeGroups = async () => {
  const response = await api.get('/api/config/age-groups');
  return response.data.age_groups;
};

export const getLanguages = async () => {
  const response = await api.get('/api/config/languages');
  return response.data;
};

export const getLLMProviders = async () => {
  const response = await api.get('/api/config/llm-providers');
  return response.data;
};

// Conversation management
export const startConversation = async (userId = null) => {
  const response = await api.post('/api/conversation/start', {
    user_id: userId,
  });
  return response.data;
};

export const setAge = async (conversationId, age) => {
  const response = await api.post(`/api/conversation/${conversationId}/age`, {
    age,
  });
  return response.data;
};

export const setLanguage = async (conversationId, language) => {
  const response = await api.post(
    `/api/conversation/${conversationId}/language`,
    {
      language,
    }
  );
  return response.data;
};

export const sendMessage = async (conversationId, message) => {
  const response = await api.post(`/api/conversation/${conversationId}/chat`, {
    message,
  });
  return response.data;
};

export const getConversationStatus = async (conversationId) => {
  const response = await api.get(
    `/api/conversation/${conversationId}/status`
  );
  return response.data;
};

// Authentication API functions
export const registerUser = async (userData) => {
  const response = await api.post('/api/auth/register', userData);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await api.post('/api/auth/login', credentials);
  return response.data;
};

export const logoutUser = async () => {
  const response = await api.post('/api/auth/logout');
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/api/auth/me');
  return response.data;
};

export const getUserConversations = async () => {
  const response = await api.get('/api/user/conversations');
  return response.data;
};

export const saveConversation = async (conversationData) => {
  const response = await api.post('/api/user/conversations', {
    conversation: conversationData
  });
  return response.data;
};

