@echo off
cd /d "%~dp0"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" push_to_github.py
) else (
    python push_to_github.py
)
if %ERRORLEVEL% NEQ 0 pause
