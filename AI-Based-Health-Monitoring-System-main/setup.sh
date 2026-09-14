#!/bin/bash
echo "Setting up CarePulse Health Platform..."
echo

echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error creating virtual environment"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo "Creating .env file..."
python3 setup_env.py

echo
echo "Setup complete!"
echo
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app.py"

