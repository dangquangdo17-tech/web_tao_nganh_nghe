@echo off
chcp 65001 >nul
echo =======================================================================
echo 🚀 ĐẨY MÃ NGUỒN LÊN GITHUB ĐỂ DEPLOY TỰ ĐỘNG LÊN RENDER
echo =======================================================================
echo.
echo Bước 1: Tạo một Repository mới trên GitHub (https://github.com/new)
echo Ví dụ đặt tên: educompass-ai (chọn Public hoặc Private đều được)
echo.
set /p REPO_URL="Nhập đường dẫn GitHub Repo của bạn (ví dụ: https://github.com/username/educompass-ai.git): "

if "%REPO_URL%"=="" (
    echo [Lỗi] Bạn chưa nhập link GitHub repository!
    pause
    exit /b
)

echo.
echo ⏳ Đang kết nối và đẩy mã nguồn lên GitHub...
"C:\Program Files\Git\cmd\git.exe" remote remove origin 2>nul
"C:\Program Files\Git\cmd\git.exe" remote add origin %REPO_URL%
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================================
    echo ✅ ĐÃ ĐẨY CODE LÊN GITHUB THÀNH CÔNG!
    echo.
    echo Bước 2: Truy cập https://dashboard.render.com/
    echo 1. Bấm nút [New +] -> Chọn [Web Service]
    echo 2. Chọn kho GitHub bạn vừa đẩy lên: %REPO_URL%
    echo 3. Render sẽ tự động nhận diện file render.yaml và cài đặt toàn bộ!
    echo 4. Bấm [Create Web Service] -> Sau 2 phút bạn sẽ có link .onrender.com vĩnh viễn!
    echo =======================================================================
) else (
    echo.
    echo ❌ Có lỗi khi push lên GitHub. Vui lòng kiểm tra lại quyền đăng nhập GitHub hoặc link repo.
)
pause
