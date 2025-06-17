@echo off
echo Running from: %~dp0

:: Go to the script's directory
cd /d %~dp0

:: Check if venv activate script exists
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
) else (
    echo [ERROR] Cannot find venv\Scripts\activate.bat
    pause
    exit /b
)

:: Check if hand_gesture.py exists
if exist "yolo_webcam.py" (
    call venv\Scripts\python.exe hand_gesture.py
) else (
    echo [ERROR] Cannot find hand_gesture.py
)

pause
