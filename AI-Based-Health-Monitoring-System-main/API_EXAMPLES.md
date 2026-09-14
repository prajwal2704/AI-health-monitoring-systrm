# CarePulse API Usage Examples

This document provides example API calls for CarePulse.

## Prerequisites

1. Start the server: `python app.py`
2. The server will run on `http://localhost:5000`

## Example Flow

### 1. Start a Conversation

```bash
curl -X POST http://localhost:5000/api/conversation/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "success": true,
  "conversation_id": "abc123-def456-ghi789",
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

### 2. Set Age Group

```bash
curl -X POST http://localhost:5000/api/conversation/abc123-def456-ghi789/age \
  -H "Content-Type: application/json" \
  -d '{"age": "18-64 years (Adult)"}'
```

Response:
```json
{
  "success": true,
  "message": "Age set. Please select your preferred language.",
  "age": "18-64 years (Adult)",
  "state": "awaiting_language",
  "languages": ["english", "hindi", "bengali", ...]
}
```

### 3. Set Language (Optional - defaults to English)

```bash
curl -X POST http://localhost:5000/api/conversation/abc123-def456-ghi789/language \
  -H "Content-Type: application/json" \
  -d '{"language": "hindi"}'
```

Response:
```json
{
  "success": true,
  "message": "Conversation ready. You can now describe your symptoms.",
  "language": "hindi",
  "state": "ready"
}
```

### 4. Send Chat Message with Symptoms

```bash
curl -X POST http://localhost:5000/api/conversation/abc123-def456-ghi789/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been experiencing fever, headache, and body aches for the past 2 days"}'
```

Response:
```json
{
  "success": true,
  "response": {
    "summary": "You are experiencing fever, headache, and body aches for the past 2 days...",
    "home_care": "1. Rest and stay hydrated...\n2. Take over-the-counter pain relievers...",
    "medical_attention": "Seek immediate medical attention if:\n- Fever exceeds 103°F...",
    "possible_causes": "Possible causes include:\n1. Viral infection (common cold, flu)...",
    "disclaimer": "⚠️ IMPORTANT DISCLAIMER: This information is for informational purposes only..."
  },
  "conversation_id": "abc123-def456-ghi789"
}
```

### 5. Check Conversation Status

```bash
curl -X GET http://localhost:5000/api/conversation/abc123-def456-ghi789/status
```

Response:
```json
{
  "success": true,
  "conversation_id": "abc123-def456-ghi789",
  "state": "in_conversation",
  "age": "18-64 years (Adult)",
  "language": "hindi",
  "message_count": 2
}
```

## Configuration Endpoints

### Get Available Age Groups

```bash
curl -X GET http://localhost:5000/api/config/age-groups
```

### Get Supported Languages

```bash
curl -X GET http://localhost:5000/api/config/languages
```

### Get LLM Provider Information

```bash
curl -X GET http://localhost:5000/api/config/llm-providers
```

Response:
```json
{
  "success": true,
  "current_provider": "openai",
  "available_providers": ["openai", "gemini"],
  "all_providers": ["openai", "gemini", "anthropic"]
}
```

### Switch LLM Provider

```bash
curl -X POST http://localhost:5000/api/config/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini"}'
```

## Python Example

```python
import requests

BASE_URL = "http://localhost:5000"

# Start conversation
response = requests.post(f"{BASE_URL}/api/conversation/start", json={})
conversation_id = response.json()["conversation_id"]

# Set age
requests.post(
    f"{BASE_URL}/api/conversation/{conversation_id}/age",
    json={"age": "18-64 years (Adult)"}
)

# Set language
requests.post(
    f"{BASE_URL}/api/conversation/{conversation_id}/language",
    json={"language": "english"}
)

# Send message
response = requests.post(
    f"{BASE_URL}/api/conversation/{conversation_id}/chat",
    json={"message": "I have a fever and cough"}
)

print(response.json()["response"])
```

## Error Handling

All endpoints return a `success` field. If `success` is `false`, check the `error` field:

```json
{
  "success": false,
  "error": "Age selection is required before processing symptoms"
}
```

Common errors:
- `400 Bad Request`: Missing required fields or invalid input
- `404 Not Found`: Conversation ID not found
- `500 Internal Server Error`: Server-side error (check LLM configuration)

