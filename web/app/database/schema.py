import sqlite3
import os
from typing import Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Bảng Trường Đại học
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS universities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        region TEXT NOT NULL,          -- 'Bắc', 'Trung', 'Nam'
        province TEXT NOT NULL,
        type TEXT NOT NULL,            -- 'Công lập', 'Tư thục'
        tuition_range TEXT,            -- Mức học phí (triệu VNĐ/năm)
        website TEXT,
        logo_url TEXT,
        description TEXT
    );
    """)

    # Bảng Ngành đào tạo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS majors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,        -- 'Công nghệ thông tin', 'Kinh tế & Quản lý', 'Y Dược', 'Khoa học Kỹ thuật', 'Xã hội & Nhân văn', 'Nghệ thuật & Thiết kế'
        holland_code TEXT NOT NULL,    -- RIASEC code, vd: 'IRC', 'EAS', 'RIC'
        description TEXT NOT NULL,
        career_prospects TEXT NOT NULL,
        suitable_traits TEXT NOT NULL,
        expected_salary_range TEXT     -- Mức lương khởi điểm ước tính
    );
    """)

    # Bảng Điểm chuẩn lịch sử & Tổ hợp môn (Admission Benchmarks)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admission_benchmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        university_id INTEGER NOT NULL,
        major_id INTEGER NOT NULL,
        combination_code TEXT NOT NULL, -- 'A00', 'A01', 'D01', 'B00', 'C00', 'D07'
        score_2023 REAL NOT NULL,
        score_2024 REAL NOT NULL,
        score_2025 REAL NOT NULL,
        quota INTEGER DEFAULT 100,      -- Chỉ tiêu
        sub_criteria TEXT,              -- Tiêu chí phụ, vd: 'Toán >= 8.0, TTNV <= 2'
        FOREIGN KEY (university_id) REFERENCES universities(id),
        FOREIGN KEY (major_id) REFERENCES majors(id)
    );
    """)

    # Bảng Đề án & Quy chế tuyển sinh (Dùng cho SLM & Admission Agent)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prospectus_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        university_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        ielts_conversion_rules TEXT,    -- JSON hoặc chuỗi quy định quy đổi IELTS
        bonus_points_policy TEXT,       -- Chính sách điểm cộng ưu tiên/khuyến khích
        raw_prospectus_text TEXT,       -- Văn bản đề án tuyển sinh trích xuất
        special_conditions TEXT,
        FOREIGN KEY (university_id) REFERENCES universities(id)
    );
    """)

    conn.commit()
    conn.close()
