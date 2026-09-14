# CarePulse - Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- API key for at least one LLM provider (OpenAI or Google Gemini)

## Quick Setup (Windows)

1. **Run the setup script:**
   ```bash
   setup.bat
   ```

2. **Edit `.env` file** and add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   # OR
   GEMINI_API_KEY=your-gemini-key-here
   ```

3. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

4. **Start the server:**
   ```bash
   python app.py
   ```

5. **Test the API** (in another terminal):
   ```bash
   python test_api.py
   ```

## Quick Setup (Linux/Mac)

1. **Make setup script executable:**
   ```bash
   chmod +x setup.sh
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

3. **Edit `.env` file** and add your API key

4. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

5. **Start the server:**
   ```bash
   python app.py
   ```

6. **Test the API:**
   ```bash
   python test_api.py
   ```

## Manual Setup

If the setup scripts don't work, follow these steps:

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate it:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   python setup_env.py
   ```

5. **Edit `.env`** and add your API keys

6. **Run the application:**
   ```bash
   python app.py
   ```

## Getting API Keys

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key to your `.env` file

### Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## Testing the API

Once the server is running, you can:

1. **Use the test script:**
   ```bash
   python test_api.py
   ```

2. **Use curl:**
   ```bash
   curl http://localhost:5000/health
   ```

3. **Use Python:**
   ```python
   import requests
   response = requests.get("http://localhost:5000/health")
   print(response.json())
   ```

## Common Issues

### "API key not found" error
- Make sure you've created the `.env` file
- Check that your API key is correctly entered in `.env`
- Ensure there are no extra spaces or quotes around the key

### "Module not found" error
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

### Port already in use
- Change `FLASK_PORT` in `.env` to a different port (e.g., 5001)
- Or stop the process using port 5000

### LLM provider errors
- Verify your API key is valid
- Check your API quota/credits
- Try switching to a different provider in `.env`

## Next Steps

- Read `README.md` for detailed documentation
- Check `API_EXAMPLES.md` for API usage examples
- Start building your frontend to interact with the backend!

