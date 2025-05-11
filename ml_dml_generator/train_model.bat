
@echo off
echo Activating virtual environment...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo Starting model training...
python train.py
