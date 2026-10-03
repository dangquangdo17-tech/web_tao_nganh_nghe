import sys
import os
import subprocess
import shutil
import webbrowser
import threading

# Tìm đường dẫn Git
GIT_EXE = "git"
for candidate in [
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
    r"C:\Users\Admin\AppData\Local\Programs\Git\cmd\git.exe"
]:
    if os.path.exists(candidate):
        GIT_EXE = candidate
        break

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_git_push(repo_url, log_callback=print, done_callback=None):
    repo_url = repo_url.strip()
    if not repo_url:
        log_callback("❌ Lỗi: Bạn chưa nhập đường dẫn GitHub Repository!\n")
        if done_callback:
            done_callback(False)
        return

    # Chuẩn hóa link repo
    if not repo_url.endswith(".git") and "github.com" in repo_url:
        repo_url = repo_url + ".git"

    log_callback(f"📂 Thư mục dự án: {PROJECT_DIR}\n")
    log_callback(f"🔗 Kết nối tới GitHub: {repo_url}\n")
    log_callback("⏳ Đang thiết lập remote 'origin'...\n")

    try:
        # Xóa remote cũ nếu có
        subprocess.run([GIT_EXE, "remote", "remove", "origin"], cwd=PROJECT_DIR, capture_output=True)

        # Thêm remote mới
        res = subprocess.run([GIT_EXE, "remote", "add", "origin", repo_url], cwd=PROJECT_DIR, capture_output=True, text=True)
        if res.returncode != 0:
            log_callback(f"⚠️ Remote add: {res.stderr}\n")

        # Đổi tên nhánh sang main
        subprocess.run([GIT_EXE, "branch", "-M", "main"], cwd=PROJECT_DIR, capture_output=True)

        # Đảm bảo đã add và commit mọi thay đổi mới nhất
        subprocess.run([GIT_EXE, "add", "."], cwd=PROJECT_DIR, capture_output=True)
        subprocess.run([GIT_EXE, "commit", "-m", "Deploy to Render"], cwd=PROJECT_DIR, capture_output=True)

        log_callback("🚀 Đang đẩy toàn bộ mã nguồn lên nhánh 'main'...\n")
        log_callback("(Lưu ý: Nếu trình duyệt hiện popup yêu cầu đăng nhập GitHub, bạn hãy bấm 'Authorize' để cấp quyền nhé)\n")

        # Push lên GitHub
        proc = subprocess.Popen(
            [GIT_EXE, "push", "-u", "origin", "main", "--force"],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in proc.stdout:
            log_callback(line)

        proc.wait()

        if proc.returncode == 0:
            log_callback("\n" + "=" * 60 + "\n")
            log_callback("✅ THÀNH CÔNG RỰC RỠ: Toàn bộ code đã được đẩy lên GitHub!\n")
            log_callback("=" * 60 + "\n")
            log_callback("👉 Bước tiếp theo: Vào https://dashboard.render.com/ để tạo Web Service.\n")
            if done_callback:
                done_callback(True)
        else:
            log_callback(f"\n❌ Đẩy code thất bại (Mã lỗi {proc.returncode}).\n")
            log_callback("Gợi ý: Hãy kiểm tra xem bạn đã tạo repository trên GitHub chưa, hoặc link repo có chính xác không.\n")
            if done_callback:
                done_callback(False)

    except Exception as ex:
        log_callback(f"\n❌ Lỗi ngoài ý muốn: {ex}\n")
        if done_callback:
            done_callback(False)


def launch_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("EduCompass AI - Đẩy Code Lên GitHub Để Deploy Render")
    root.geometry("640x540")
    root.minsize(580, 480)
    root.configure(bg="#f8fafc")

    # Style
    style = ttk.Style(root)
    style.theme_use("clam")

    # Header Frame
    header_frame = tk.Frame(root, bg="#4338ca", padx=16, pady=12)
    header_frame.pack(fill="x")

    lbl_title = tk.Label(
        header_frame,
        text="🚀 CÔNG CỤ TẢI CODE LÊN GITHUB CHO RENDER",
        font=("Segoe UI", 12, "bold"),
        fg="#ffffff",
        bg="#4338ca"
    )
    lbl_title.pack(anchor="w")

    lbl_subtitle = tk.Label(
        header_frame,
        text="Tự động đồng bộ toàn bộ mã nguồn EduCompass AI lên GitHub trong 1 click",
        font=("Segoe UI", 9),
        fg="#c7d2fe",
        bg="#4338ca"
    )
    lbl_subtitle.pack(anchor="w")

    # Body Frame
    body_frame = tk.Frame(root, bg="#f8fafc", padx=16, pady=12)
    body_frame.pack(fill="both", expand=True)

    # Step 1
    step1_box = tk.LabelFrame(
        body_frame,
        text=" Bước 1: Tạo Repository Trên GitHub ",
        font=("Segoe UI", 9, "bold"),
        fg="#1e1b4b",
        bg="#ffffff",
        padx=10,
        pady=8
    )
    step1_box.pack(fill="x", pady=(0, 10))

    btn_open_github = tk.Button(
        step1_box,
        text="🌐 Bấm vào đây để mở trang tạo Repository mới (github.com/new)",
        font=("Segoe UI", 9, "bold"),
        bg="#4f46e5",
        fg="#ffffff",
        activebackground="#4338ca",
        activeforeground="#ffffff",
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2",
        command=lambda: webbrowser.open("https://github.com/new")
    )
    btn_open_github.pack(anchor="w", fill="x")

    # Step 2
    step2_box = tk.LabelFrame(
        body_frame,
        text=" Bước 2: Dán Link GitHub Repository Vừa Tạo ",
        font=("Segoe UI", 9, "bold"),
        fg="#1e1b4b",
        bg="#ffffff",
        padx=10,
        pady=8
    )
    step2_box.pack(fill="x", pady=(0, 10))

    lbl_entry_hint = tk.Label(
        step2_box,
        text="Dán đường link (ví dụ: https://github.com/username/educompass-ai.git):",
        font=("Segoe UI", 8),
        fg="#64748b",
        bg="#ffffff"
    )
    lbl_entry_hint.pack(anchor="w")

    entry_frame = tk.Frame(step2_box, bg="#ffffff")
    entry_frame.pack(fill="x", pady=(4, 0))

    entry_url = tk.Entry(
        entry_frame,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )
    entry_url.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 6))

    def paste_clipboard():
        try:
            val = root.clipboard_get()
            entry_url.delete(0, tk.END)
            entry_url.insert(0, val.strip())
        except Exception:
            pass

    btn_paste = tk.Button(
        entry_frame,
        text="📋 Dán",
        font=("Segoe UI", 9),
        bg="#e2e8f0",
        fg="#1e293b",
        relief="flat",
        padx=8,
        pady=3,
        cursor="hand2",
        command=paste_clipboard
    )
    btn_paste.pack(side="right")

    # Step 3 Action Button
    btn_push = tk.Button(
        body_frame,
        text="🚀 BẮT ĐẦU ĐẨY CODE LÊN GITHUB NGAY",
        font=("Segoe UI", 10, "bold"),
        bg="#10b981",
        fg="#ffffff",
        activebackground="#059669",
        activeforeground="#ffffff",
        relief="flat",
        pady=8,
        cursor="hand2"
    )
    btn_push.pack(fill="x", pady=(0, 10))

    # Log Terminal
    log_box = tk.LabelFrame(
        body_frame,
        text=" Nhật Ký Tiến Trình ",
        font=("Segoe UI", 8, "bold"),
        fg="#475569",
        bg="#f8fafc"
    )
    log_box.pack(fill="both", expand=True)

    text_log = tk.Text(
        log_box,
        wrap="word",
        font=("Consolas", 8),
        bg="#1e293b",
        fg="#f8fafc",
        relief="flat",
        padx=6,
        pady=6
    )
    scroll = tk.Scrollbar(log_box, command=text_log.yview)
    text_log.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    text_log.pack(side="left", fill="both", expand=True)

    text_log.insert("end", f"✓ Đã sẵn sàng. Git: {GIT_EXE}\n")
    text_log.insert("end", "Hãy nhập link GitHub của bạn ở trên rồi bấm nút màu xanh.\n\n")

    def append_log(msg):
        text_log.insert("end", msg)
        text_log.see("end")

    def on_done(success):
        btn_push.config(state="normal", text="🚀 BẮT ĐẦU ĐẨY CODE LÊN GITHUB NGAY")
        if success:
            btn_open_render.pack(fill="x", pady=(6, 0))
            messagebox.showinfo(
                "Đẩy code thành công!",
                "Toàn bộ mã nguồn đã tải lên GitHub thành công!\n\nBây giờ bạn có thể bấm nút 'Mở Dashboard Render' để kích hoạt dịch vụ 24/7!"
            )

    btn_open_render = tk.Button(
        body_frame,
        text="🌐 BẤM ĐÂY ĐỂ MỞ DASHBOARD RENDER.COM & KÍCH HOẠT",
        font=("Segoe UI", 10, "bold"),
        bg="#6366f1",
        fg="#ffffff",
        relief="flat",
        pady=8,
        cursor="hand2",
        command=lambda: webbrowser.open("https://dashboard.render.com/")
    )

    def start_push_thread():
        url = entry_url.get().strip()
        if not url:
            messagebox.showwarning("Chưa nhập link", "Vui lòng dán link GitHub Repository của bạn vào ô nhập!")
            return
        btn_push.config(state="disabled", text="⏳ Đang tải mã nguồn lên... Xin chờ...")
        t = threading.Thread(target=run_git_push, args=(url, append_log, on_done), daemon=True)
        t.start()

    btn_push.config(command=start_push_thread)

    root.mainloop()


def launch_cli():
    print("=" * 60)
    print("🚀 CÔNG CỤ TẢI MÃ NGUỒN LÊN GITHUB CHO RENDER")
    print("=" * 60)
    print("\nBước 1: Mở https://github.com/new để tạo repository mới.")
    print("Ví dụ đặt tên: educompass-ai\n")
    repo_url = input("Bước 2: Dán đường dẫn GitHub Repo của bạn vào đây: ").strip()
    run_git_push(repo_url, print)
    input("\nNhấn Enter để kết thúc...")


if __name__ == "__main__":
    try:
        launch_gui()
    except Exception:
        launch_cli()
