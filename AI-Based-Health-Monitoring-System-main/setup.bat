@echo off
echo Setting up CarePulse Health Platform...
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    exit /b 1
)

echo Creating .env file...
python setup_env.py

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: venv\Scripts\activate
echo 3. Run: python app.py
pause

