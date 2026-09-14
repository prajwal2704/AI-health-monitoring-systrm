# CarePulse API - Quick Reference Guide

## Base Configuration
- **Base URL:** `http://localhost:5000`
- **Content-Type:** `application/json` (for POST requests)
- **CORS:** Enabled

## Essential Endpoints

### 1. Initialize Conversation
```javascript
POST /api/conversation/start
Body: {}
Response: { conversation_id, state: "awaiting_age", age_groups: [...] }
```
**Action:** Store `conversation_id` immediately. Show age selector.

### 2. Set Age (REQUIRED)
```javascript
POST /api/conversation/{conversation_id}/age
Body: { age: "18-64 years (Adult)" }
Response: { state: "ready" | "awaiting_language", message: "..." }
```
**Action:** If `state === "ready"`, show chat. If `state === "awaiting_language"`, show language selector.

### 3. Set Language (Optional, defaults to English)
```javascript
POST /api/conversation/{conversation_id}/language
Body: { language: "english" }
Response: { state: "ready", message: "..." }
```
**Action:** If `state === "ready"`, show chat interface.

### 4. Send Message (REQUIRES age to be set)
```javascript
POST /api/conversation/{conversation_id}/chat
Body: { message: "I have a headache" }
Response: {
  success: true,
  response: {
    summary: "...",
    home_care: "...",
    medical_attention: "...",
    possible_causes: "...",
    disclaimer: "⚠️ ..."
  }
}
```
**Action:** Display all 4 sections + disclaimer. Show loading during request.

### 5. Get Configuration
```javascript
GET /api/config/age-groups      // Returns: { age_groups: [...] }
GET /api/config/languages        // Returns: { languages: {...}, default_language: "english" }
GET /api/conversation/{id}/status // Returns: { state, age, language, message_count }
```

## Required UI Flow

```
1. User clicks "Start" 
   → POST /conversation/start
   → Store conversation_id
   → Show age dropdown

2. User selects age
   → POST /conversation/{id}/age
   → If state="ready" → Show chat
   → If state="awaiting_language" → Show language dropdown

3. User selects language (or skip, defaults to English)
   → POST /conversation/{id}/language
   → Show chat interface

4. User types symptom
   → POST /conversation/{id}/chat
   → Display structured response (A, B, C, D sections)
   → Show disclaimer prominently
```

## Critical Validation Rules

1. **Age is MANDATORY** - Cannot send chat message without age
2. **Language defaults to English** - Can skip language selection
3. **Store conversation_id** - Required for all subsequent requests
4. **Check state** - Use `/status` endpoint or maintain state in UI

## Response Structure (Display Format)

When displaying medical response, show:
- **(A) Summary:** `response.summary`
- **(B) Home Care:** `response.home_care`
- **(C) Medical Attention:** `response.medical_attention`
- **(D) Possible Causes:** `response.possible_causes`
- **Disclaimer:** `response.disclaimer` (make prominent with warning icon)

## Error Handling

All errors return: `{ success: false, error: "message" }`

Common errors:
- `"Please select your age group first"` → Show age selector
- `"Please select your preferred language"` → Show language selector
- `"Conversation not found"` → Restart conversation
- `"Message is required"` → Validate input before sending

## Age Groups (Exact Strings)
```
"0-2 years (Infant)"
"3-5 years (Toddler)"
"6-12 years (Child)"
"13-17 years (Adolescent)"
"18-64 years (Adult)"
"65+ years (Senior)"
```

## Language Codes
```
"english", "hindi", "bengali", "telugu", "marathi", "tamil", 
"gujarati", "kannada", "malayalam", "punjabi", "odia", "urdu", "assamese"
```

## State Values
- `"initial"` - Just created
- `"awaiting_age"` - Need age selection
- `"awaiting_language"` - Need language selection
- `"ready"` - Can accept chat messages
- `"in_conversation"` - Has messages

## React/Next.js Quick Start Template

```javascript
// State
const [convId, setConvId] = useState(null);
const [state, setState] = useState('initial');
const [age, setAge] = useState(null);
const [messages, setMessages] = useState([]);

// Start
const start = async () => {
  const res = await fetch('http://localhost:5000/api/conversation/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  });
  const data = await res.json();
  setConvId(data.conversation_id);
  setState(data.state);
};

// Set Age
const setAge = async (ageValue) => {
  const res = await fetch(`http://localhost:5000/api/conversation/${convId}/age`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ age: ageValue })
  });
  const data = await res.json();
  setAge(data.age);
  setState(data.state);
};

// Send Message
const sendMessage = async (text) => {
  const res = await fetch(`http://localhost:5000/api/conversation/${convId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  });
  const data = await res.json();
  if (data.success) {
    setMessages([...messages, 
      { role: 'user', content: text },
      { role: 'assistant', content: data.response }
    ]);
  }
};
```

## Key Points for AI Code Generation

1. ✅ Always validate age is set before allowing chat
2. ✅ Store conversation_id in state/localStorage
3. ✅ Show loading indicators during API calls
4. ✅ Display all 4 response sections (A, B, C, D)
5. ✅ Make disclaimer prominent (warning style)
6. ✅ Handle errors gracefully
7. ✅ Follow state flow (initial → age → language → ready → chat)
8. ✅ Use exact age group strings from API
9. ✅ Default language to "english" if not selected
10. ✅ Test error scenarios (missing age, invalid ID, etc.)

