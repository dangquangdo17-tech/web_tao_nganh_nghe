@echo off
title EduCompass AI - He Thong Tu Van Tuyen Sinh Da Tac Tu
cd /d "%~dp0"

echo ===============================================================================
echo          EDUCOMPASS AI - HE THONG TU VAN TUYEN SINH VA HUONG NGHIEP
echo      Tich hop Da Tac Tu (LangGraph) + RAG HyDE + SLM + CSDL 3 Mien
echo ===============================================================================
echo.

set PYTHONIOENCODING=utf-8
set PYTHON_CMD=

:: 1. Kiem tra python trong PATH
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto FOUND
)

:: 2. Kiem tra cac duong dan pho bien
if exist "C:\ProgramData\miniconda3\python.exe" (
    set PYTHON_CMD=C:\ProgramData\miniconda3\python.exe
    goto FOUND
)
if exist "C:\ProgramData\anaconda3\python.exe" (
    set PYTHON_CMD=C:\ProgramData\anaconda3\python.exe
    goto FOUND
)
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python314\python.exe
    goto FOUND
)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
    goto FOUND
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    goto FOUND
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    goto FOUND
)
if exist "C:\Python312\python.exe" (
    set PYTHON_CMD=C:\Python312\python.exe
    goto FOUND
)
if exist "C:\Python311\python.exe" (
    set PYTHON_CMD=C:\Python311\python.exe
    goto FOUND
)

echo [!] LOI: Khong tim thay Python tren may tinh cua ban!
echo [!] Vui long cai dat Python hoac them vao bien moi truong PATH.
echo.
pause
exit /b 1

:FOUND
echo [+] Tim thay Python tai: %PYTHON_CMD%
echo [+] Dang khoi chay may chu tai: http://localhost:1234
echo [+] Trinh duyet web se tu dong mo sau 3 giay...
echo [+] Nhan Ctrl + C de dung may chu.
echo ===============================================================================
echo.

:: Tu dong mo trinh duyet sau 3 giay bang ping universal
start "" cmd /c "ping 127.0.0.1 -n 4 >nul && start http://localhost:1234"

:: Chay ung dung
"%PYTHON_CMD%" run.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Ung dung da dung voi ma loi %errorlevel%.
    pause
)
