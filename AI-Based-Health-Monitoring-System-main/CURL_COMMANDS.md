# cURL Commands for Testing CarePulse API

## 1. Health Check
```bash
curl -X GET http://localhost:5000/health
```

## 2. Check LLM Provider Configuration
```bash
curl -X GET http://localhost:5000/api/config/llm-providers
```

## 3. Get Available Age Groups
```bash
curl -X GET http://localhost:5000/api/config/age-groups
```

## 4. Get Supported Languages
```bash
curl -X GET http://localhost:5000/api/config/languages
```

## 5. Start a New Conversation
```bash
curl -X POST http://localhost:5000/api/conversation/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response will include:** `conversation_id` - Save this for next steps!

## 6. Set Age Group
```bash
curl -X POST http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/age \
  -H "Content-Type: application/json" \
  -d '{
    "age": "18-64 years (Adult)"
  }'
```

**Available age groups:**
- `"0-2 years (Infant)"`
- `"3-5 years (Toddler)"`
- `"6-12 years (Child)"`
- `"13-17 years (Adolescent)"`
- `"18-64 years (Adult)"`
- `"65+ years (Senior)"`

## 7. Set Language (Optional - defaults to English)
```bash
curl -X POST http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/language \
  -H "Content-Type: application/json" \
  -d '{
    "language": "english"
  }'
```

**Available languages:**
- `"english"` (default)
- `"hindi"`
- `"bengali"`
- `"telugu"`
- `"marathi"`
- `"tamil"`
- `"gujarati"`
- `"kannada"`
- `"malayalam"`
- `"punjabi"`
- `"odia"`
- `"urdu"`
- `"assamese"`

## 8. Send Chat Message (Describe Symptoms)
```bash
curl -X POST http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a mild headache and fever"
  }'
```

## 9. Check Conversation Status
```bash
curl -X GET http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/status
```

## 10. Switch LLM Provider (Admin)
```bash
curl -X POST http://localhost:5000/api/config/switch-provider \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "gemini"
  }'
```

---

## Complete Test Flow Example

Replace `YOUR_CONVERSATION_ID` with the actual ID from step 5:

```bash
# Step 1: Start conversation
curl -X POST http://localhost:5000/api/conversation/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Step 2: Set age (use conversation_id from step 1)
curl -X POST http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/age \
  -H "Content-Type: application/json" \
  -d '{"age": "18-64 years (Adult)"}'

# Step 3: Set language
curl -X POST http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/language \
  -H "Content-Type: application/json" \
  -d '{"language": "english"}'

# Step 4: Send symptom message
curl -X POST http://localhost:5000/api/conversation/YOUR_CONVERSATION_ID/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been experiencing fever, headache, and body aches for the past 2 days"}'
```

## Example Response Structure

When you send a chat message, you'll receive:

```json
{
  "success": true,
  "response": {
    "summary": "Brief summary of symptoms...",
    "home_care": "Home care recommendations...",
    "medical_attention": "When to seek medical attention...",
    "possible_causes": "Possible causes...",
    "disclaimer": "⚠️ IMPORTANT DISCLAIMER: ..."
  },
  "conversation_id": "your-conversation-id"
}
```

## Postman Tips

1. **Create a Collection** with all these endpoints
2. **Use Environment Variables** for `conversation_id` to reuse it across requests
3. **Set Headers**: Make sure `Content-Type: application/json` is set
4. **Test Flow**: Run requests in sequence (start → age → language → chat)

