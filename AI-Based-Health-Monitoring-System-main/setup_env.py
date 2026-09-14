"""
Setup script to create .env file from template
"""
import os

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_content = """# LLM Configuration
LLM_PROVIDER=openai  # Options: openai, gemini, anthropic

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro

# Anthropic Configuration (if needed)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-opus-20240229

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
"""
    
    if os.path.exists('.env'):
        print(".env file already exists. Skipping creation.")
        return
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(".env file created successfully!")
    print("Please edit .env and add your API keys before running the application.")

if __name__ == '__main__':
    create_env_file()

