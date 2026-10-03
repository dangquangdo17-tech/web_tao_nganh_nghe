import uvicorn
import os
import sys

if __name__ == "__main__":
    # Đảm bảo UTF-8 cho console
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    port = int(os.environ.get("PORT", 1234))
    print("=" * 70)
    print("🚀 Khởi động Hệ Thống Web Tư Vấn Tuyển Sinh & Hướng Nghiệp Đa Tác Tử")
    print(f"📍 Cổng dịch vụ (Port):         {port}")
    print(f"📍 Máy hiện tại (Local):       http://localhost:{port}")
    print(f"🌐 Mọi máy trong mạng LAN/Wifi: http://192.168.1.6:{port}")
    print("=" * 70)

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
