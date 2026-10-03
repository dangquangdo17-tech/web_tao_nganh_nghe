import sqlite3
import json
from typing import List, Dict, Any, Optional
from .schema import get_connection

class DatabaseManager:
    @staticmethod
    def get_all_universities(region: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        if region and region != "Tất cả":
            cursor.execute("SELECT * FROM universities WHERE region = ?", (region,))
        else:
            cursor.execute("SELECT * FROM universities")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_all_majors() -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM majors")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def _parse_tuition_min(tuition_str: Optional[str]) -> float:
        if not tuition_str:
            return 25.0
        import re
        m = re.search(r"(\d+(\.\d+)?)", tuition_str)
        if m:
            try:
                return float(m.group(1))
            except Exception:
                return 25.0
        return 25.0

    @staticmethod
    def search_benchmarks(
        combinations: List[str], 
        min_score: float = 0.0, 
        max_score: float = 30.0, 
        region: Optional[str] = None,
        category: Optional[str] = None,
        tuition_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        
        placeholders = ",".join(["?"] * len(combinations))
        query = f"""
        SELECT 
            b.id as benchmark_id,
            u.id as university_id,
            u.code as university_code,
            u.name as university_name,
            u.region,
            u.province,
            u.type as university_type,
            u.tuition_range,
            u.website,
            m.id as major_id,
            m.code as major_code,
            m.name as major_name,
            m.category as major_category,
            m.holland_code,
            m.description as major_description,
            m.career_prospects,
            m.expected_salary_range,
            b.combination_code,
            b.score_2023,
            b.score_2024,
            b.score_2025,
            b.quota,
            b.sub_criteria
        FROM admission_benchmarks b
        JOIN universities u ON b.university_id = u.id
        JOIN majors m ON b.major_id = m.id
        WHERE b.combination_code IN ({placeholders})
          AND b.score_2025 BETWEEN ? AND ?
        """
        params = list(combinations) + [min_score, max_score]

        if region and region != "Tất cả":
            query += " AND u.region = ?"
            params.append(region)
            
        if category and category != "Tất cả":
            query += " AND m.category = ?"
            params.append(category)

        query += " ORDER BY b.score_2025 DESC"

        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if tuition_level and tuition_level != "Tất cả":
            filtered = []
            for r in rows:
                t_val = DatabaseManager._parse_tuition_min(r.get("tuition_range"))
                if tuition_level == "under_20" and t_val <= 20:
                    filtered.append(r)
                elif tuition_level == "20_40" and 18 <= t_val <= 42:
                    filtered.append(r)
                elif tuition_level == "over_40" and t_val >= 40:
                    filtered.append(r)
            return filtered

        return rows

    @staticmethod
    def search_dream_benchmarks(
        keyword: Optional[str] = None, 
        major_codes: Optional[List[str]] = None, 
        limit: int = 35
    ) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()

        base_select = """
        SELECT 
            b.id as benchmark_id,
            u.id as university_id,
            u.code as university_code,
            u.name as university_name,
            u.region,
            u.province,
            u.type as university_type,
            u.tuition_range,
            u.website,
            m.id as major_id,
            m.code as major_code,
            m.name as major_name,
            m.category as major_category,
            m.holland_code,
            m.description as major_description,
            m.career_prospects,
            m.expected_salary_range,
            b.combination_code,
            b.score_2023,
            b.score_2024,
            b.score_2025,
            b.quota,
            b.sub_criteria
        FROM admission_benchmarks b
        JOIN universities u ON b.university_id = u.id
        JOIN majors m ON b.major_id = m.id
        """

        if keyword and keyword.strip():
            kw = f"%{keyword.strip().lower()}%"
            exact_code = keyword.strip().lower()
            exact_name_like = f"%{exact_code}%"
            query = base_select + """
            WHERE LOWER(u.code) LIKE ? 
               OR LOWER(u.name) LIKE ?
               OR LOWER(m.name) LIKE ?
               OR LOWER(m.code) LIKE ?
               OR LOWER(m.category) LIKE ?
               OR LOWER(b.combination_code) LIKE ?
            ORDER BY 
                CASE 
                    WHEN LOWER(u.code) = ? THEN 1
                    WHEN LOWER(u.name) LIKE ? THEN 2
                    ELSE 3
                END,
                b.score_2025 DESC
            LIMIT ?
            """
            cursor.execute(query, (kw, kw, kw, kw, kw, kw, exact_code, exact_name_like, limit))
        elif major_codes:
            placeholders = ",".join(["?"] * len(major_codes))
            query = base_select + f"""
            WHERE m.code IN ({placeholders})
            ORDER BY b.score_2025 DESC
            LIMIT ?
            """
            cursor.execute(query, (*major_codes, limit))
        else:
            query = base_select + """
            ORDER BY b.score_2025 DESC
            LIMIT ?
            """
            cursor.execute(query, (limit,))

        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_prospectus(university_code: str, year: int = 2025) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT p.*, u.name as university_name, u.code as university_code
        FROM prospectus_rules p
        JOIN universities u ON p.university_id = u.id
        WHERE u.code = ? AND p.year = ?
        """, (university_code, year))
        row = cursor.fetchone()
        conn.close()
        if row:
            data = dict(row)
            if data.get("ielts_conversion_rules"):
                try:
                    data["ielts_conversion_map"] = json.loads(data["ielts_conversion_rules"])
                except Exception:
                    data["ielts_conversion_map"] = {}
            return data
        return None

    @staticmethod
    def get_all_prospectuses(year: int = 2025) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT p.*, u.name as university_name, u.code as university_code
        FROM prospectus_rules p
        JOIN universities u ON p.university_id = u.id
        WHERE p.year = ?
        """, (year,))
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_school_full_profile(school_code: str) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM universities WHERE UPPER(code) = ?", (school_code.strip().upper(),))
        uni_row = cursor.fetchone()
        if not uni_row:
            conn.close()
            return None

        uni_data = dict(uni_row)
        uni_id = uni_data["id"]

        # Fetch prospectus
        cursor.execute("SELECT * FROM prospectus_rules WHERE university_id = ? AND year = 2025", (uni_id,))
        prospectus_row = cursor.fetchone()
        prospectus_data = dict(prospectus_row) if prospectus_row else None
        if prospectus_data and prospectus_data.get("ielts_conversion_rules"):
            try:
                prospectus_data["ielts_conversion_map"] = json.loads(prospectus_data["ielts_conversion_rules"])
            except Exception:
                prospectus_data["ielts_conversion_map"] = {}

        # Fetch benchmarks & majors
        cursor.execute("""
        SELECT 
            b.id as benchmark_id,
            b.combination_code,
            b.score_2023,
            b.score_2024,
            b.score_2025,
            b.quota,
            b.sub_criteria,
            m.id as major_id,
            m.code as major_code,
            m.name as major_name,
            m.category as major_category,
            m.holland_code,
            m.description as major_description,
            m.career_prospects,
            m.expected_salary_range
        FROM admission_benchmarks b
        JOIN majors m ON b.major_id = m.id
        WHERE b.university_id = ?
        ORDER BY b.score_2025 DESC
        """, (uni_id,))
        benchmark_rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        uni_data["prospectus"] = prospectus_data
        uni_data["benchmarks"] = benchmark_rows
        return uni_data
