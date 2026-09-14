# CarePulse - Clinical Health Monitoring & Disease Diagnostic System

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/prajwal2704/AI-health-monitoring-systrm)

A comprehensive clinical health monitoring and disease prediction system that provides differential diagnostic evaluations, vitals tracking, and conversational medical guidance based on user-reported symptoms. The system features a built-in clinical rule engine covering 40+ medical conditions alongside multi-provider LLM support (Gemini, OpenAI, Anthropic).

## Features

- **Conversational Chat Interface**: Backend logic for chat-based interactions
- **Medical Symptom Analysis**: Provides possible diagnoses, medicine recommendations, and health guidance
- **Age-Based Validation**: Mandatory age selection with age-appropriate recommendations
- **Multi-Language Support**: Supports English and 13 Indian regional languages (default: English)
- **Structured Medical Responses**: Responses include:
  - (A) Brief Summary of Symptoms
  - (B) Home Care Recommendations
  - (C) When to Seek Medical Attention
  - (D) Possible Causes
- **Multiple LLM Support**: Easily switchable between OpenAI, Gemini, and other providers
- **Safety Disclaimers**: Clear disclaimers about informational purposes only

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
LLM_PROVIDER=openai  # or 'gemini'
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Start Conversation
```
POST /api/conversation/start
Body: { "user_id": "optional_user_id" }
Response: { "conversation_id": "...", "state": "awaiting_age", "age_groups": [...] }
```

### 2. Set Age
```
POST /api/conversation/<conversation_id>/age
Body: { "age": "18-64 years (Adult)" }
Response: { "success": true, "state": "ready" }
```

### 3. Set Language
```
POST /api/conversation/<conversation_id>/language
Body: { "language": "hindi" }
Response: { "success": true, "state": "ready" }
```

### 4. Send Chat Message
```
POST /api/conversation/<conversation_id>/chat
Body: { "message": "I have a fever and headache" }
Response: {
  "success": true,
  "response": {
    "summary": "...",
    "home_care": "...",
    "medical_attention": "...",
    "possible_causes": "...",
    "disclaimer": "..."
  }
}
```

### 5. Get Conversation Status
```
GET /api/conversation/<conversation_id>/status
Response: { "state": "ready", "age": "...", "language": "..." }
```

### 6. Get Configuration
```
GET /api/config/age-groups
GET /api/config/languages
GET /api/config/llm-providers
```

### 7. Switch LLM Provider
```
POST /api/config/switch-provider
Body: { "provider": "gemini" }
```

## Usage Flow

1. **Start a conversation**: Call `/api/conversation/start` to get a `conversation_id`
2. **Set age**: Call `/api/conversation/<id>/age` with an age group from the provided list
3. **Set language** (optional): Call `/api/conversation/<id>/language` (defaults to English)
4. **Chat**: Send messages to `/api/conversation/<id>/chat` with symptoms or questions

## Supported Age Groups

- 0-2 years (Infant)
- 3-5 years (Toddler)
- 6-12 years (Child)
- 13-17 years (Adolescent)
- 18-64 years (Adult)
- 65+ years (Senior)

## Supported Languages

- English (default)
- Hindi (हिंदी)
- Bengali (বাংলা)
- Telugu (తెలుగు)
- Marathi (मराठी)
- Tamil (தமிழ்)
- Gujarati (ગુજરાતી)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)
- Odia (ଓଡ଼ିଆ)
- Urdu (اردو)
- Assamese (অসমীয়া)

## LLM Provider Configuration

The system supports multiple LLM providers:

- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Google Gemini**: Gemini Pro, etc.
- **Anthropic Claude**: (Placeholder for future implementation)

Switch providers by:
1. Changing `LLM_PROVIDER` in `.env`
2. Or using the `/api/config/switch-provider` endpoint

## Important Notes

⚠️ **Medical Disclaimer**: This chatbot provides informational guidance only and does not replace professional medical advice. Always consult qualified healthcare professionals for proper medical evaluation and treatment.

## Project Structure

```
.
├── app.py                      # Flask application and API endpoints
├── config.py                   # Configuration management
├── llm_providers.py            # LLM provider abstraction layer
├── conversation_manager.py     # Conversation state management
├── medical_response_generator.py # Medical response generation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Development

The system uses:
- **Flask**: Web framework
- **LangChain**: LLM integration and abstraction
- **python-dotenv**: Environment variable management

## License

This project is for educational and informational purposes only.

