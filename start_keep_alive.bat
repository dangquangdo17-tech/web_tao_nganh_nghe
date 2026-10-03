@echo off
cd /d "%~dp0"
title EduCompass AI - Keep Alive Cron Bot
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" keep_alive_cron.py
) else (
    python keep_alive_cron.py
)
pause
