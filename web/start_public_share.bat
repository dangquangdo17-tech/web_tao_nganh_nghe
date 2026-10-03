@echo off
chcp 65001 >nul
echo =======================================================================
echo 🚀 HỆ THỐNG WEB TƯ VẤN TUYỂN SINH EDUCOMPASS AI (CHIA SẺ TOÀN MẠNG)
echo =======================================================================
echo.
echo 📍 Máy hiện tại (Local):       http://localhost:1234
echo 🌐 Mọi máy chung Wifi / LAN:  http://192.168.1.6:1234
echo 🌍 Link công khai (Internet): Đang kết nối tunnel...
echo.
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:127.0.0.1:1234 serveo.net
pause
