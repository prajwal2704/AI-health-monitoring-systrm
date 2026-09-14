# CarePulse - API Specification

## Overview

This document provides a complete API specification for building a frontend UI for CarePulse. The API follows RESTful principles and returns JSON responses.

**Base URL:** `http://localhost:5000`

**Content-Type:** `application/json` (for all POST requests)

**CORS:** Enabled for all origins

---

## Authentication

No authentication required for this version. All endpoints are publicly accessible.

---

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the server is running and healthy.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "status": "healthy",
  "service": "CarePulse Health Platform"
}
```

**Status Codes:**
- `200 OK`: Server is healthy

---

### 2. Get LLM Provider Information

**Endpoint:** `GET /api/config/llm-providers`

**Description:** Get information about available and currently active LLM providers.

**Request:**
```http
GET /api/config/llm-providers HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "success": true,
  "current_provider": "gemini",
  "available_providers": ["openai", "gemini"],
  "all_providers": ["openai", "gemini", "anthropic"]
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `current_provider` (string): Currently active LLM provider
- `available_providers` (array): List of providers with valid API keys
- `all_providers` (array): List of all supported providers

**Status Codes:**
- `200 OK`: Request successful

---

### 3. Get Available Age Groups

**Endpoint:** `GET /api/config/age-groups`

**Description:** Get the list of available age groups for user selection.

**Request:**
```http
GET /api/config/age-groups HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "success": true,
  "age_groups": [
    "0-2 years (Infant)",
    "3-5 years (Toddler)",
    "6-12 years (Child)",
    "13-17 years (Adolescent)",
    "18-64 years (Adult)",
    "65+ years (Senior)"
  ]
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `age_groups` (array of strings): List of age group options

**Status Codes:**
- `200 OK`: Request successful

**UI Recommendation:** Use this to populate a dropdown/select component for age selection.

---

### 4. Get Supported Languages

**Endpoint:** `GET /api/config/languages`

**Description:** Get the list of supported languages with their display names.

**Request:**
```http
GET /api/config/languages HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "success": true,
  "languages": {
    "english": "English",
    "hindi": "हिंदी",
    "bengali": "বাংলা",
    "telugu": "తెలుగు",
    "marathi": "मराठी",
    "tamil": "தமிழ்",
    "gujarati": "ગુજરાતી",
    "kannada": "ಕನ್ನಡ",
    "malayalam": "മലയാളം",
    "punjabi": "ਪੰਜਾਬੀ",
    "odia": "ଓଡ଼ିଆ",
    "urdu": "اردو",
    "assamese": "অসমীয়া"
  },
  "default_language": "english"
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `languages` (object): Key-value pairs where key is language code and value is display name
- `default_language` (string): Default language code

**Status Codes:**
- `200 OK`: Request successful

**UI Recommendation:** Use this to populate a language selector. Display the native script names for better UX.

---

### 5. Start New Conversation

**Endpoint:** `POST /api/conversation/start`

**Description:** Initialize a new conversation session. Returns a conversation ID that must be used for all subsequent requests.

**Request:**
```http
POST /api/conversation/start HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "optional_user_id_string"
}
```

**Note:** `user_id` is optional. If not provided, the server will generate a unique ID.

**Response:**
```json
{
  "success": true,
  "conversation_id": "f535257f-fb50-47db-8793-beddff101e04",
  "message": "Conversation started. Please select your age group.",
  "state": "awaiting_age",
  "age_groups": [
    "0-2 years (Infant)",
    "3-5 years (Toddler)",
    "6-12 years (Child)",
    "13-17 years (Adolescent)",
    "18-64 years (Adult)",
    "65+ years (Senior)"
  ]
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `conversation_id` (string): Unique identifier for this conversation (REQUIRED for all subsequent requests)
- `message` (string): Human-readable message about current state
- `state` (string): Current conversation state (`"awaiting_age"`)
- `age_groups` (array): List of available age groups

**Status Codes:**
- `200 OK`: Conversation created successfully
- `500 Internal Server Error`: Server error

**UI Flow:**
1. Call this endpoint when user first visits or clicks "Start Chat"
2. Store `conversation_id` in state/localStorage
3. Show age selection UI based on `age_groups`
4. Display `message` to guide the user

---

### 6. Set Age Group

**Endpoint:** `POST /api/conversation/{conversation_id}/age`

**Description:** Set the user's age group. This is MANDATORY before processing any symptoms.

**Request:**
```http
POST /api/conversation/{conversation_id}/age HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

**Path Parameters:**
- `conversation_id` (string, required): The conversation ID from step 5

**Request Body:**
```json
{
  "age": "18-64 years (Adult)"
}
```

**Request Body Fields:**
- `age` (string, required): Must be one of the age groups from `/api/config/age-groups`

**Response (Age set, language not set):**
```json
{
  "success": true,
  "message": "Age set. Please select your preferred language.",
  "age": "18-64 years (Adult)",
  "state": "awaiting_language",
  "languages": ["english", "hindi", "bengali", ...]
}
```

**Response (Age and language both set - ready for chat):**
```json
{
  "success": true,
  "message": "Conversation ready. You can now describe your symptoms.",
  "age": "18-64 years (Adult)",
  "state": "ready",
  "languages": ["english", "hindi", "bengali", ...]
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `message` (string): Human-readable message about next steps
- `age` (string): The age group that was set
- `state` (string): Current conversation state (`"awaiting_language"` or `"ready"`)
- `languages` (array): Available language options (if state is `awaiting_language`)

**Status Codes:**
- `200 OK`: Age set successfully
- `400 Bad Request`: Invalid age group or conversation not found
- `500 Internal Server Error`: Server error

**UI Flow:**
1. User selects age from dropdown
2. Call this endpoint with selected age
3. If `state` is `"awaiting_language"`, show language selector
4. If `state` is `"ready"`, show chat input interface
5. Display `message` to guide user

**Error Response Example:**
```json
{
  "success": false,
  "error": "Invalid age group or conversation not found"
}
```

---

### 7. Set Language

**Endpoint:** `POST /api/conversation/{conversation_id}/language`

**Description:** Set the preferred language for responses. Defaults to English if not set.

**Request:**
```http
POST /api/conversation/{conversation_id}/language HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

**Path Parameters:**
- `conversation_id` (string, required): The conversation ID

**Request Body:**
```json
{
  "language": "english"
}
```

**Request Body Fields:**
- `language` (string, required): Language code from `/api/config/languages` (e.g., "english", "hindi", "bengali")

**Response (Language set, age not set):**
```json
{
  "success": true,
  "message": "Language set. Please select your age group.",
  "language": "english",
  "state": "awaiting_age",
  "age_groups": ["0-2 years (Infant)", ...]
}
```

**Response (Both age and language set - ready):**
```json
{
  "success": true,
  "message": "Conversation ready. You can now describe your symptoms.",
  "language": "english",
  "state": "ready"
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `message` (string): Human-readable message about next steps
- `language` (string): The language code that was set
- `state` (string): Current conversation state
- `age_groups` (array): Available age groups (if state is `awaiting_age`)

**Status Codes:**
- `200 OK`: Language set successfully
- `400 Bad Request`: Invalid language or conversation not found
- `500 Internal Server Error`: Server error

**UI Flow:**
1. User selects language from dropdown
2. Call this endpoint with selected language
3. If `state` is `"ready"`, show chat interface
4. If `state` is `"awaiting_age"`, show age selector
5. Display `message` to guide user

**Note:** Language can be set before or after age. The conversation becomes ready when both are set.

---

### 8. Send Chat Message

**Endpoint:** `POST /api/conversation/{conversation_id}/chat`

**Description:** Send a message describing symptoms or asking medical questions. Age and language must be set first.

**Request:**
```http
POST /api/conversation/{conversation_id}/chat HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

**Path Parameters:**
- `conversation_id` (string, required): The conversation ID

**Request Body:**
```json
{
  "message": "I have been experiencing fever, headache, and body aches for the past 2 days"
}
```

**Request Body Fields:**
- `message` (string, required): User's symptom description or question

**Response (Success):**
```json
{
  "success": true,
  "response": {
    "summary": "You are experiencing fever, headache, and body aches for the past 2 days. These symptoms are commonly associated with viral infections...",
    "home_care": "1. Rest and stay hydrated by drinking plenty of fluids...\n2. Take over-the-counter pain relievers like acetaminophen or ibuprofen (age-appropriate dosage)...",
    "medical_attention": "Seek immediate medical attention if:\n- Fever exceeds 103°F (39.4°C)\n- Symptoms worsen or persist for more than 3-4 days...",
    "possible_causes": "Possible causes include:\n1. Viral infection (common cold, influenza)\n2. Bacterial infection\n3. Other conditions...",
    "disclaimer": "⚠️ IMPORTANT DISCLAIMER: This information is for informational purposes only and does not constitute medical advice..."
  },
  "conversation_id": "f535257f-fb50-47db-8793-beddff101e04"
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `response` (object): Structured medical response containing:
  - `summary` (string): Brief summary of the symptoms
  - `home_care` (string): Home care recommendations
  - `medical_attention` (string): When to seek medical attention
  - `possible_causes` (string): Possible causes of symptoms
  - `disclaimer` (string): Medical disclaimer
- `conversation_id` (string): The conversation ID

**Status Codes:**
- `200 OK`: Message processed successfully
- `400 Bad Request`: Missing message, age not set, or language not set
- `404 Not Found`: Conversation not found
- `500 Internal Server Error`: Server error or LLM provider error

**Error Response (Age not set):**
```json
{
  "success": false,
  "error": "Please select your age group first",
  "requires_age": true,
  "age_groups": ["0-2 years (Infant)", ...]
}
```

**Error Response (Language not set):**
```json
{
  "success": false,
  "error": "Please select your preferred language",
  "requires_language": true,
  "languages": ["english", "hindi", ...]
}
```

**UI Flow:**
1. Check if age and language are set (use `/status` endpoint or maintain state)
2. User types message in chat input
3. Show loading indicator
4. Call this endpoint
5. Display response in structured format:
   - Show summary section
   - Show home care section
   - Show medical attention section
   - Show possible causes section
   - Always display disclaimer prominently
6. Handle errors and show appropriate messages

**UI Recommendation:**
- Display response in a card/accordion format with sections (A), (B), (C), (D)
- Use icons or visual separators for each section
- Make disclaimer prominent (warning icon, highlighted background)
- Support markdown formatting if response contains lists

---

### 9. Get Conversation Status

**Endpoint:** `GET /api/conversation/{conversation_id}/status`

**Description:** Get the current status of a conversation including state, age, language, and message count.

**Request:**
```http
GET /api/conversation/{conversation_id}/status HTTP/1.1
Host: localhost:5000
```

**Path Parameters:**
- `conversation_id` (string, required): The conversation ID

**Response:**
```json
{
  "success": true,
  "conversation_id": "f535257f-fb50-47db-8793-beddff101e04",
  "state": "in_conversation",
  "age": "18-64 years (Adult)",
  "language": "english",
  "message_count": 3
}
```

**Response Fields:**
- `success` (boolean): Whether the request was successful
- `conversation_id` (string): The conversation ID
- `state` (string): Current state (`"initial"`, `"awaiting_age"`, `"awaiting_language"`, `"ready"`, `"in_conversation"`)
- `age` (string or null): Set age group or null if not set
- `language` (string): Set language (defaults to "english")
- `message_count` (number): Number of messages exchanged

**Status Codes:**
- `200 OK`: Request successful
- `404 Not Found`: Conversation not found
- `500 Internal Server Error`: Server error

**UI Recommendation:**
- Use this endpoint to restore conversation state on page reload
- Check state to determine which UI to show
- Display age and language in user profile/settings area

---

### 10. Switch LLM Provider (Admin)

**Endpoint:** `POST /api/config/switch-provider`

**Description:** Switch the active LLM provider. Useful for testing or admin purposes.

**Request:**
```http
POST /api/config/switch-provider HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

**Request Body:**
```json
{
  "provider": "gemini"
}
```

**Request Body Fields:**
- `provider` (string, required): Provider name (`"openai"`, `"gemini"`, or `"anthropic"`)

**Response:**
```json
{
  "success": true,
  "provider": "gemini",
  "message": "Switched to gemini provider"
}
```

**Status Codes:**
- `200 OK`: Provider switched successfully
- `400 Bad Request`: Invalid provider name or provider not available
- `500 Internal Server Error`: Server error

**Note:** This is typically an admin function and may not be needed in the main UI.

---

## Conversation States

The conversation follows these states:

1. **`initial`**: Just created, no age or language set
2. **`awaiting_age`**: Waiting for user to select age group
3. **`awaiting_language`**: Waiting for user to select language
4. **`ready`**: Age and language set, ready to accept chat messages
5. **`in_conversation`**: User has sent at least one message

**State Flow:**
```
initial → awaiting_age → awaiting_language → ready → in_conversation
   ↑           ↑              ↑
   └───────────┴──────────────┘
   (can set age or language in any order)
```

---

## Error Handling

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common Error Scenarios:**

1. **Missing Required Fields:**
   ```json
   {
     "success": false,
     "error": "Message is required"
   }
   ```

2. **Invalid Input:**
   ```json
   {
     "success": false,
     "error": "Invalid age group or conversation not found"
   }
   ```

3. **Conversation Not Found:**
   ```json
   {
     "success": false,
     "error": "Conversation not found"
   }
   ```

4. **LLM Provider Error:**
   ```json
   {
     "success": false,
     "error": "Medical response generator is not available. Please check LLM configuration."
   }
   ```

**HTTP Status Codes:**
- `200 OK`: Request successful
- `400 Bad Request`: Invalid input or missing required fields
- `404 Not Found`: Resource not found (e.g., conversation ID)
- `500 Internal Server Error`: Server-side error

---

## Complete User Flow Example

### Step-by-Step Flow:

1. **User visits the site**
   - Call `GET /api/config/age-groups` and `GET /api/config/languages` to populate dropdowns
   - Optionally call `GET /api/config/llm-providers` to show current provider

2. **User clicks "Start Chat"**
   - Call `POST /api/conversation/start`
   - Store `conversation_id` in state/localStorage
   - Show age selection UI

3. **User selects age**
   - Call `POST /api/conversation/{id}/age` with selected age
   - If response `state` is `"awaiting_language"`, show language selector
   - If response `state` is `"ready"`, show chat interface

4. **User selects language (optional, defaults to English)**
   - Call `POST /api/conversation/{id}/language` with selected language
   - If response `state` is `"ready"`, show chat interface

5. **User types symptom message**
   - Validate that age is set (check state or use `/status` endpoint)
   - Call `POST /api/conversation/{id}/chat` with message
   - Display structured response with sections (A), (B), (C), (D)
   - Show disclaimer prominently

6. **User continues conversation**
   - Repeat step 5 for additional messages
   - Maintain conversation history in UI

### React/Next.js Example State Management:

```javascript
const [conversationId, setConversationId] = useState(null);
const [age, setAge] = useState(null);
const [language, setLanguage] = useState('english');
const [state, setState] = useState('initial');
const [messages, setMessages] = useState([]);
const [loading, setLoading] = useState(false);

// Start conversation
const startConversation = async () => {
  const response = await fetch('http://localhost:5000/api/conversation/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  });
  const data = await response.json();
  setConversationId(data.conversation_id);
  setState(data.state);
};

// Set age
const setUserAge = async (selectedAge) => {
  const response = await fetch(`http://localhost:5000/api/conversation/${conversationId}/age`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ age: selectedAge })
  });
  const data = await response.json();
  setAge(data.age);
  setState(data.state);
};

// Send message
const sendMessage = async (messageText) => {
  setLoading(true);
  const response = await fetch(`http://localhost:5000/api/conversation/${conversationId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: messageText })
  });
  const data = await response.json();
  if (data.success) {
    setMessages([...messages, 
      { role: 'user', content: messageText },
      { role: 'assistant', content: data.response }
    ]);
  }
  setLoading(false);
};
```

---

## UI Component Recommendations

### 1. Age Selector Component
- Dropdown/Select component
- Populate from `/api/config/age-groups`
- Show validation error if user tries to chat without selecting

### 2. Language Selector Component
- Dropdown/Select component with native script display
- Populate from `/api/config/languages`
- Default to "english"
- Show flag icons if possible

### 3. Chat Interface Component
- Message input field
- Send button
- Loading indicator during API calls
- Message history display
- Structured response display with sections

### 4. Medical Response Display Component
- Card/Accordion layout
- Sections:
  - (A) Summary - Brief overview
  - (B) Home Care - Recommendations
  - (C) Medical Attention - Warning signs
  - (D) Possible Causes - Potential causes
- Disclaimer section (prominent, warning style)

### 5. Error Handling Component
- Display API errors to user
- Handle network errors
- Show retry options
- Guide user to complete required steps (age/language)

---

## Testing Checklist

- [ ] Health check endpoint works
- [ ] Can start a new conversation
- [ ] Age selection works and updates state
- [ ] Language selection works
- [ ] Cannot send chat message without age
- [ ] Chat message returns structured response
- [ ] All response sections (A-D) are displayed
- [ ] Disclaimer is shown
- [ ] Error handling works for invalid inputs
- [ ] Conversation state persists (test with status endpoint)
- [ ] Multiple messages in same conversation work
- [ ] Language selection changes response language

---

## Notes for AI/LLM Code Generation

1. **Always validate required fields** before API calls
2. **Store conversation_id** in state/localStorage for persistence
3. **Handle loading states** during API calls
4. **Display errors** clearly to users
5. **Follow the state flow** - check state before allowing actions
6. **Structure medical responses** with clear sections (A, B, C, D)
7. **Make disclaimer prominent** - it's a legal/medical requirement
8. **Support markdown** in responses if the LLM returns formatted text
9. **Handle CORS** - API has CORS enabled, but check browser console
10. **Test error scenarios** - missing age, invalid conversation ID, etc.

---

## Additional Resources

- See `API_EXAMPLES.md` for curl command examples

---

**Last Updated:** 2025-12-14
**API Version:** 1.0
**Base URL:** http://localhost:5000

