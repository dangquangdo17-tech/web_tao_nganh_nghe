import time
import requests
from datetime import datetime

TARGET_URL = "https://web-tao-nganh-nghe.onrender.com/api/universities"
INTERVAL_SECONDS = 300 # 5 phút ping một lần

print("=" * 70)
print("🚀 EDUCOMPASS AI - CRON KEEP-ALIVE BOT (GIỮ WEBSITE CHẠY 24/7 MÃI MÃI)")
print(f"📍 Mục tiêu ping: {TARGET_URL}")
print(f"⏱️ Tần suất ping: Mỗi {INTERVAL_SECONDS // 60} phút/lần")
print("=" * 70)

while True:
    now_str = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    try:
        r = requests.get(TARGET_URL, timeout=20)
        if r.status_code == 200:
            print(f"[{now_str}] 🟢 Ping thành công (HTTP {r.status_code}) -> Server Render luôn thức!")
        else:
            print(f"[{now_str}] 🟡 Server phản hồi mã: {r.status_code} -> Đã đánh thức thành công.")
    except Exception as e:
        print(f"[{now_str}] ⚠️ Lỗi kết nối tạm thời: {e}")
    
    time.sleep(INTERVAL_SECONDS)
