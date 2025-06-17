@echo off
echo Running from: %~dp0

:: Go to the script's directory
cd /d %~dp0

:: Create venv if not exists
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

:: Activate venv
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
) else (
    echo [ERROR] Cannot find venv\Scripts\activate.bat
    pause
    exit /b
)

:: Run hand_gesture.py
if exist "hand_gesture.py" (
    call venv\Scripts\python.exe hand_gesture.py
) else (
    echo [ERROR] Cannot find hand_gesture.py
)
pause
