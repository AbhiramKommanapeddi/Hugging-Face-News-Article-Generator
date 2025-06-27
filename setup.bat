@echo off
echo ========================================
echo HUGGING FACE NEWS ARTICLE GENERATOR
echo Windows Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Starting setup...
echo.

REM Run the Python setup script
python setup.py

if %errorlevel% neq 0 (
    echo.
    echo Setup encountered errors. Please check the output above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo Quick start commands:
echo   1. Test CLI: python main.py --sample
echo   2. Web UI:   streamlit run web_interface.py
echo   3. Demo:     python demo.py
echo.
pause
