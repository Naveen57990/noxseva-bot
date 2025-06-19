@echo off
cd /d %~dp0
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Starting the AI Voice Bot...
python app.py
pause