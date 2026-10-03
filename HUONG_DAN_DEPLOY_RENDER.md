# Hướng Dẫn Triển Khai EduCompass AI Lên Render (render.com)

Hệ thống đã được đóng gói và cấu hình hoàn chỉnh các tệp tự động hóa triển khai:
- `render.yaml`: Blueprint cấu hình dịch vụ Render tự động (Python 3.11, auto-build, auto-start).
- `Procfile`: Khởi chạy chuẩn web worker.
- `.python-version`: Chỉ định phiên bản Python 3.11.8.
- `requirements.txt`: Danh sách thư viện đầy đủ.
- `run.py`: Đã hỗ trợ cổng động `PORT` của Render (không lo lỗi Port binding timeout).
- `Dockerfile`: Hỗ trợ cả triển khai bằng Docker Container nếu cần.

---

## Các Bước Triển Khai Trong 3 Phút

### Bước 1: Tạo Repository Trên GitHub
1. Truy cập [https://github.com/new](https://github.com/new)
2. Đặt tên repository: `educompass-ai` (chọn **Public** hoặc **Private** đều được).
3. Bấm **Create repository**.
4. Sao chép đường dẫn repo (ví dụ: `https://github.com/your-username/educompass-ai.git`).

---

### Bước 2: Đẩy Mã Nguồn Lên GitHub
Bạn chỉ cần **nhấp đúp chuột** vào file:
👉 **`push_to_github.bat`** (nằm ngay trong thư mục `C:\chọn ngành nghề`)
- Dán đường dẫn GitHub Repo của bạn vào và nhấn **Enter**.
- Script sẽ tự động đẩy toàn bộ mã nguồn lên nhánh `main`.

*(Hoặc nếu dùng dòng lệnh, gõ trong terminal:)*
```bash
git remote add origin https://github.com/your-username/educompass-ai.git
git branch -M main
git push -u origin main
```

---

### Bước 3: Đưa Lên Render (render.com)
1. Truy cập [https://dashboard.render.com/](https://dashboard.render.com/) (Đăng nhập bằng tài khoản GitHub của bạn).
2. Ở góc trên bên phải, bấm nút **`[New +]`** $\rightarrow$ Chọn **`Web Service`**.
3. Chọn tùy chọn **Build and deploy from a Git repository** $\rightarrow$ Bấm **Next**.
4. Chọn repository **`educompass-ai`** bạn vừa tạo (hoặc dán link repo vào ô *Public Git repository*).
5. Render sẽ **tự động đọc file `render.yaml`** đã chuẩn bị sẵn! Nếu bạn tự cấu hình thủ công:
   - **Name**: `educompass-ai`
   - **Region**: `Singapore` (để tốc độ tải về Việt Nam nhanh nhất)
   - **Root Directory**: `web`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `python run.py` (hoặc `uvicorn app.main:app --host 0.0.0.0 --port $PORT`)
   - **Plan Type**: `Free`
6. Bấm nút **`[Create Web Service]`** ở dưới cùng.

---

## Kết Quả
- Sau khoảng 1 - 2 phút, Render sẽ cài đặt xong và cấp cho bạn một đường link miễn phí hoạt động 24/7 vĩnh viễn, ví dụ:
  🌐 **`https://educompass-ai.onrender.com`**
- Bạn có thể gửi link này cho bất kỳ ai trên mọi máy tính, điện thoại, máy tính bảng để truy cập bất cứ lúc nào!
