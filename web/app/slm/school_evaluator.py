import re
import json
import uuid
from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from .prospectus_parser import SLMProspectusParser

class SchoolEvaluator:
    """
    Công cụ Thẩm định Hồ sơ & Phỏng vấn Tuyển sinh Chuyên sâu theo Từng Trường Đại học.
    - So điểm & dự báo trúng tuyển tức thì 3 tầng: 🟢 An toàn | 🟡 Cạnh tranh | 🔴 Nguy cơ
    - Kiểm tra điều kiện sàn & tiêu chí phụ đặc thù của trường
    - Khởi tạo Persona & phiên Phỏng vấn thử (AI Mock Interview) với Ban Tuyển sinh
    - Chấm điểm độ phù hợp văn hóa trường (Culture Fit Score) & Chiến thuật đặt nguyện vọng
    """

    # Danh mục định nghĩa Persona đại diện tuyển sinh các trường hàng đầu
    PERSONAS = {
        "BKHN": {
            "name": "Thầy TS. Vũ Đình Tiến",
            "role": "Trưởng phòng Tuyển sinh & Hướng nghiệp",
            "school": "Đại học Bách khoa Hà Nội",
            "motto": "Tư duy sáng tạo, dấn thân kỹ thuật, kiên định kỷ luật",
            "avatar": "🏛️",
            "accent_color": "#b91c1c",
            "culture_traits": ["Tư duy logic", "Chịu áp lực đồ án", "Tự học chuyên sâu", "Kỷ luật cao"]
        },
        "NEU": {
            "name": "Cô PGS.TS Nguyễn Thị Mai",
            "role": "Cố vấn Ban Tuyển sinh & Hướng nghiệp",
            "school": "Trường Đại học Kinh tế Quốc dân",
            "motto": "Bản lĩnh kinh tế, tư duy phân tích, thích ứng toàn cầu",
            "avatar": "📈",
            "accent_color": "#1d4ed8",
            "culture_traits": ["Tư duy thị trường", "Phân tích tài chính", "Kỹ năng kết nối", "Ngoại ngữ"]
        },
        "FTU": {
            "name": "Thầy ThS. Hoàng Văn Hải",
            "role": "Đại diện Ban Tuyển sinh & Hợp tác Quốc tế",
            "school": "Trường Đại học Ngoại thương",
            "motto": "Khát vọng hội nhập, bản lĩnh ngoại thương, năng động đỉnh cao",
            "avatar": "🚢",
            "accent_color": "#991b1b",
            "culture_traits": ["Tiếng Anh lưu loát", "Tư duy phản biện", "Khởi nghiệp đổi mới", "Hoạt động xã hội"]
        },
        "HCMUT": {
            "name": "Thầy PGS.TS Trần Minh Đức",
            "role": "Phó ban Đào tạo & Tuyển sinh",
            "school": "Trường ĐH Bách khoa - ĐHQG-HCM",
            "motto": "Vững nền tảng kỹ nghệ, làm chủ công nghệ tương lai",
            "avatar": "⚙️",
            "accent_color": "#0284c7",
            "culture_traits": ["Kỹ năng thực hành", "Nghiên cứu ứng dụng", "Làm việc nhóm", "Giải quyết vấn đề"]
        },
        "UET": {
            "name": "Cô TS. Lê Thu Trang",
            "role": "Cố vấn Tuyển sinh & Công nghệ Mũi nhọn",
            "school": "Trường Đại học Công nghệ - ĐHQGHN",
            "motto": "Chuẩn mực học thuật, tiên phong AI & Công nghệ cao",
            "avatar": "🔬",
            "accent_color": "#059669",
            "culture_traits": ["Thuật toán máy tính", "Đam mê nghiên cứu", "Tư duy trừu tượng", "Chuẩn quốc tế"]
        },
        "HMU": {
            "name": "Thầy BS.CKII Đặng Văn Nam",
            "role": "Hội đồng Tuyển sinh & Quản lý Đào tạo Y khoa",
            "school": "Trường Đại học Y Hà Nội",
            "motto": "Sâu y lý, giàu y đức, bền bỉ phụng sự người bệnh",
            "avatar": "🩺",
            "accent_color": "#047857",
            "culture_traits": ["Lòng trắc ẩn", "Sức bền trực đêm", "Tỉ mỉ cẩn trọng", "Học tập suốt đời"]
        },
        "UMP": {
            "name": "Cô TS.BS Phạm Thị Lan",
            "role": "Ban Đào tạo Đại học & Sau Đại học",
            "school": "Đại học Y Dược TP. Hồ Chí Minh",
            "motto": "Tinh hoa y học phương Nam, nhân ái và cống hiến",
            "avatar": "💊",
            "accent_color": "#0f766e",
            "culture_traits": ["Trách nhiệm sinh mệnh", "Tập trung cao độ", "Y đức trong sáng", "Kiên nhẫn"]
        },
        "UEH": {
            "name": "Thầy TS. Phan Quốc Huy",
            "role": "Ban Đào tạo & Đổi mới Sáng tạo",
            "school": "Đại học Kinh tế TP. Hồ Chí Minh",
            "motto": "Đổi mới sáng tạo, chuyển đổi số và phát triển bền vững",
            "avatar": "📊",
            "accent_color": "#ea580c",
            "culture_traits": ["Tư duy kinh tế số", "Đa ngành linh hoạt", "Kỹ năng lãnh đạo", "Sáng tạo"]
        },
        "UIT": {
            "name": "Thầy ThS. Đỗ Minh Quân",
            "role": "Ban Tuyển sinh & Hướng nghiệp Công nghệ",
            "school": "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM",
            "motto": "Chuyên sâu CNTT, dẫn đầu kỷ nguyên trí tuệ nhân tạo",
            "avatar": "💻",
            "accent_color": "#2563eb",
            "culture_traits": ["Thực chiến lập trình", "Đam mê công nghệ", "An ninh mạng", "Sáng tạo giải pháp"]
        },
        "DUT": {
            "name": "Thầy TS. Nguyễn Bá Hùng",
            "role": "Ban Tuyển sinh ĐH Bách khoa - ĐH Đà Nẵng",
            "school": "Trường ĐH Bách khoa - ĐH Đà Nẵng",
            "motto": "Trung tâm kỹ thuật công nghệ lớn nhất miền Trung",
            "avatar": "🏗️",
            "accent_color": "#0369a1",
            "culture_traits": ["Kỹ thuật ứng dụng", "Chăm chỉ vượt khó", "Đoàn kết sáng tạo"]
        },
        "DUE": {
            "name": "Cô ThS. Trần Phương Uyên",
            "role": "Cố vấn Ban Tuyển sinh ĐH Kinh tế - ĐH Đà Nẵng",
            "school": "Trường ĐH Kinh tế - ĐH Đà Nẵng",
            "motto": "Năng động kinh tế miền Trung - Tây Nguyên",
            "avatar": "📉",
            "accent_color": "#4338ca",
            "culture_traits": ["Tư duy kinh doanh", "Giao tiếp thuyết phục", "Khát vọng vươn xa"]
        }
    }

    # Bảng điểm mẫu nhanh được cá nhân hóa cho từng trường để học sinh test ngay
    SAMPLE_SCORES_BY_SCHOOL = {
        "BKHN": {
            "toan": 8.8, "van": 7.2, "anh": 8.5, "ly": 8.8, "hoa": 8.0, "sinh": 6.5, "su": 6.5, "dia": 6.5,
            "gpa": 8.6, "ielts": 6.5, "tsa": 72, "apt": "", "hsa": "", "priority": "KV2"
        },
        "NEU": {
            "toan": 8.5, "van": 8.0, "anh": 8.8, "ly": 7.5, "hoa": 7.0, "sinh": 6.0, "su": 7.5, "dia": 7.5,
            "gpa": 8.8, "ielts": 6.5, "tsa": "", "apt": "", "hsa": 96, "priority": "KV2"
        },
        "FTU": {
            "toan": 9.0, "van": 8.2, "anh": 9.2, "ly": 8.0, "hoa": 7.5, "sinh": 6.0, "su": 7.0, "dia": 7.0,
            "gpa": 9.1, "ielts": 7.5, "tsa": "", "apt": "", "hsa": 105, "priority": "KV3"
        },
        "HCMUT": {
            "toan": 8.6, "van": 7.0, "anh": 8.2, "ly": 8.5, "hoa": 8.0, "sinh": 6.5, "su": 6.0, "dia": 6.0,
            "gpa": 8.7, "ielts": 6.5, "tsa": "", "apt": 860, "hsa": "", "priority": "KV2"
        },
        "UIT": {
            "toan": 8.5, "van": 7.0, "anh": 8.0, "ly": 8.2, "hoa": 7.5, "sinh": 6.0, "su": 6.5, "dia": 6.5,
            "gpa": 8.5, "ielts": 6.0, "tsa": "", "apt": 840, "hsa": "", "priority": "KV2"
        },
        "HMU": {
            "toan": 9.2, "van": 7.5, "anh": 8.0, "ly": 7.5, "hoa": 9.0, "sinh": 9.4, "su": 6.0, "dia": 6.0,
            "gpa": 9.2, "ielts": 6.5, "tsa": "", "apt": "", "hsa": "", "priority": "KV1"
        },
        "UMP": {
            "toan": 9.0, "van": 7.5, "anh": 8.2, "ly": 7.5, "hoa": 9.0, "sinh": 9.2, "su": 6.0, "dia": 6.0,
            "gpa": 9.1, "ielts": 6.5, "tsa": "", "apt": 920, "hsa": "", "priority": "KV2"
        },
        "UEH": {
            "toan": 8.2, "van": 8.0, "anh": 8.5, "ly": 7.2, "hoa": 7.0, "sinh": 6.0, "su": 7.5, "dia": 7.5,
            "gpa": 8.5, "ielts": 6.5, "tsa": "", "apt": 810, "hsa": "", "priority": "KV2"
        },
        "UET": {
            "toan": 9.0, "van": 7.5, "anh": 8.5, "ly": 8.8, "hoa": 8.2, "sinh": 6.5, "su": 6.0, "dia": 6.0,
            "gpa": 8.9, "ielts": 7.0, "tsa": "", "apt": "", "hsa": 102, "priority": "KV2"
        }
    }

    @classmethod
    def get_school_persona(cls, school_code: str) -> Dict[str, Any]:
        """Trả về thông tin persona đại diện tuyển sinh của trường"""
        code = school_code.upper()
        if code in cls.PERSONAS:
            p = dict(cls.PERSONAS[code])
            p["code"] = code
            return p

        # Fallback cho trường khác
        uni = DatabaseManager.get_school_full_profile(code)
        name = uni.get("name", f"Trường ĐH {code}") if uni else f"Trường ĐH {code}"
        return {
            "code": code,
            "name": f"Thầy/Cô Đại diện Ban Tuyển sinh",
            "role": "Cố vấn Tuyển sinh & Đào tạo",
            "school": name,
            "motto": "Đồng hành cùng sĩ tử, chắp cánh ước mơ giảng đường",
            "avatar": "🎓",
            "accent_color": "#4f46e5",
            "culture_traits": ["Năng động", "Chăm chỉ", "Tự tin", "Trách nhiệm"]
        }

    @classmethod
    def get_sample_score_for_school(cls, school_code: str) -> Dict[str, Any]:
        """Lấy điểm mẫu điển hình cho trường được chọn"""
        code = school_code.upper()
        if code in cls.SAMPLE_SCORES_BY_SCHOOL:
            return cls.SAMPLE_SCORES_BY_SCHOOL[code]
        # Mặc định an toàn
        return {
            "toan": 8.0, "van": 7.5, "anh": 8.0, "ly": 7.5, "hoa": 7.0, "sinh": 6.5, "su": 6.5, "dia": 6.5,
            "gpa": 8.2, "ielts": 6.5, "tsa": 65, "apt": 780, "hsa": 88, "priority": "KV2"
        }

    @classmethod
    def calculate_priority_points(cls, area: str, ethnicity: str, raw_score: float) -> float:
        """Tính điểm ưu tiên theo quy chế Bộ GD&ĐT 2025 có giảm trừ từ 22.5 điểm trở lên"""
        area_map = {"KV1": 0.75, "KV2-NT": 0.5, "KV2": 0.25, "KV3": 0.0}
        area_pts = area_map.get(area, 0.0)
        eth_pts = 1.0 if ethnicity == "minority" else 0.0
        total_base = area_pts + eth_pts

        if raw_score >= 22.5 and total_base > 0:
            scale = (30.0 - raw_score) / 7.5
            return round(max(0.0, total_base * scale), 2)
        return round(total_base, 2)

    @classmethod
    def calculate_combo_score(cls, combo: str, exam_scores: Dict[str, float], ielts_score: Optional[float], ielts_map: Dict[str, float]) -> float:
        """Tính điểm 3 môn trong tổ hợp xét tuyển, tự động quy đổi IELTS nếu có lợi"""
        sub_map = {
            "toan": exam_scores.get("Toán", 0.0),
            "van": exam_scores.get("Ngữ văn", 0.0),
            "anh": exam_scores.get("Tiếng Anh", 0.0),
            "ly": exam_scores.get("Vật lý", 0.0),
            "hoa": exam_scores.get("Hóa học", 0.0),
            "sinh": exam_scores.get("Sinh học", 0.0),
            "su": exam_scores.get("Lịch sử", 0.0),
            "dia": exam_scores.get("Địa lý", 0.0)
        }

        # Quy đổi IELTS nếu thí sinh có nộp
        if ielts_score and ielts_score >= 4.0:
            converted = SLMProspectusParser.calculate_converted_score(ielts_score, ielts_map)
            if converted > sub_map["anh"]:
                sub_map["anh"] = converted

        combo_upper = combo.upper()
        if combo_upper == "A00":
            return sub_map["toan"] + sub_map["ly"] + sub_map["hoa"]
        elif combo_upper == "A01":
            return sub_map["toan"] + sub_map["ly"] + sub_map["anh"]
        elif combo_upper == "B00":
            return sub_map["toan"] + sub_map["hoa"] + sub_map["sinh"]
        elif combo_upper == "C00":
            return sub_map["van"] + sub_map["su"] + sub_map["dia"]
        elif combo_upper == "D01":
            return sub_map["toan"] + sub_map["van"] + sub_map["anh"]
        elif combo_upper == "D07":
            return sub_map["toan"] + sub_map["hoa"] + sub_map["anh"]
        elif combo_upper == "D14":
            return sub_map["van"] + sub_map["su"] + sub_map["anh"]
        elif combo_upper == "D15":
            return sub_map["van"] + sub_map["dia"] + sub_map["anh"]
        else:
            return sub_map["toan"] + sub_map["van"] + sub_map["anh"]

    @classmethod
    def evaluate_school_admission(
        cls,
        school_code: str,
        exam_scores: Dict[str, float],
        transcript_gpa: float = 7.5,
        ielts_score: Optional[float] = None,
        tsa_score: Optional[float] = None,
        apt_score: Optional[float] = None,
        hsa_score: Optional[float] = None,
        priority_area: str = "KV3",
        ethnicity: str = "kinh"
    ) -> Dict[str, Any]:
        """
        Thẩm định chi tiết cơ hội vào trường đại học được chỉ định:
        Phân 3 tầng: 🟢 An toàn | 🟡 Cạnh tranh | 🔴 Nguy cơ
        Kiểm tra tiêu chí phụ & điều kiện sàn
        """
        school_profile = DatabaseManager.get_school_full_profile(school_code)
        if not school_profile:
            return {
                "status": "error",
                "message": f"Không tìm thấy dữ liệu trường với mã: {school_code}"
            }

        prospectus = school_profile.get("prospectus") or {}
        ielts_map = prospectus.get("ielts_conversion_map") or {
            "IELTS 5.0": 8.0, "IELTS 5.5": 8.5, "IELTS 6.0": 9.0, "IELTS 6.5": 9.5, "IELTS 7.0+": 10.0
        }
        benchmarks = school_profile.get("benchmarks") or []

        # Kiểm tra điều kiện sàn & tiêu chí phụ chung của trường
        criteria_alerts = []
        math_score = exam_scores.get("Toán", 0.0)

        # Điều kiện sàn đặc thù theo từng trường
        code = school_code.upper()
        if code == "BKHN":
            if math_score < 7.0:
                criteria_alerts.append({
                    "type": "warning",
                    "title": "Cảnh báo Điều kiện Môn Toán",
                    "detail": f"Điểm môn Toán của bạn đang là {math_score:.1f}. Một số ngành BKHN ưu tiên xét điều kiện môn Toán $\\ge 7.0$."
                })
            criteria_alerts.append({
                "type": "info",
                "title": "Kỳ thi Đánh giá tư duy (TSA)",
                "detail": "BKHN dành tới 30-40% chỉ tiêu cho phương thức Đánh giá tư duy (TSA thang điểm 100)."
            })
        elif code == "NEU":
            if math_score < 6.0:
                criteria_alerts.append({
                    "type": "warning",
                    "title": "Điều kiện sàn môn Toán NEU",
                    "detail": f"Điểm Toán ({math_score:.1f}) dưới ngưỡng tối thiểu 6.0 để xét tuyển tổ hợp kinh tế tại NEU."
                })
        elif code == "FTU":
            if transcript_gpa < 8.0:
                criteria_alerts.append({
                    "type": "warning",
                    "title": "Điều kiện học bạ THPT Ngoại thương",
                    "detail": "Phương thức xét tuyển kết hợp FTU yêu cầu học lực 3 năm THPT loại Giỏi (GPA $\\ge 8.0$)."
                })
            if not ielts_score or ielts_score < 6.5:
                criteria_alerts.append({
                    "type": "info",
                    "title": "Lợi thế chứng chỉ IELTS tại FTU",
                    "detail": "FTU ưu tiên xét tuyển chứng chỉ IELTS $\\ge 6.5$ quy đổi từ 8.5 - 10.0 điểm tiếng Anh."
                })

        # Phân tầng từng ngành
        safe_majors = []
        competitive_majors = []
        risky_majors = []

        math_priority = exam_scores.get("Toán", 7.0)

        for b in benchmarks:
            combo = b.get("combination_code", "A00")
            raw_score = cls.calculate_combo_score(combo, exam_scores, ielts_score, ielts_map)
            priority_pts = cls.calculate_priority_points(priority_area, ethnicity, raw_score)
            final_score = round(raw_score + priority_pts, 2)

            benchmark_2025 = b.get("score_2025") or 25.0
            diff = round(final_score - benchmark_2025, 2)

            # Dự báo xác suất đỗ
            if diff >= 1.5:
                prob = min(98, int(85 + diff * 5))
                tier = "safe"
            elif diff >= -1.0:
                prob = max(35, min(80, int(60 + diff * 15)))
                tier = "competitive"
            else:
                prob = max(5, int(30 + diff * 8))
                tier = "risky"

            major_item = {
                "major_code": b.get("major_code"),
                "major_name": b.get("major_name"),
                "combination": combo,
                "benchmark_2023": b.get("score_2023"),
                "benchmark_2024": b.get("score_2024"),
                "benchmark_2025": benchmark_2025,
                "student_score": final_score,
                "raw_score": round(raw_score, 2),
                "priority_points": priority_pts,
                "score_difference": diff,
                "admission_probability": prob,
                "tier": tier,
                "quota": b.get("quota", 100),
                "sub_criteria": b.get("sub_criteria", "Xét thứ tự nguyện vọng và môn chính"),
                "career_prospects": b.get("career_prospects", ""),
                "expected_salary": b.get("expected_salary_range", "15 - 30 tr/tháng")
            }

            if tier == "safe":
                safe_majors.append(major_item)
            elif tier == "competitive":
                competitive_majors.append(major_item)
            else:
                risky_majors.append(major_item)

        # Sắp xếp ngành trong từng nhóm theo điểm chênh lệch giảm dần
        safe_majors.sort(key=lambda x: x["score_difference"], reverse=True)
        competitive_majors.sort(key=lambda x: x["score_difference"], reverse=True)
        risky_majors.sort(key=lambda x: x["score_difference"], reverse=True)

        persona = cls.get_school_persona(school_code)

        return {
            "status": "success",
            "school_info": {
                "code": school_profile.get("code"),
                "name": school_profile.get("name"),
                "region": school_profile.get("region"),
                "province": school_profile.get("province"),
                "type": school_profile.get("type"),
                "tuition_range": school_profile.get("tuition_range"),
                "website": school_profile.get("website"),
                "description": school_profile.get("description")
            },
            "persona": persona,
            "tiers": {
                "safe": safe_majors,
                "competitive": competitive_majors,
                "risky": risky_majors
            },
            "counts": {
                "total": len(benchmarks),
                "safe": len(safe_majors),
                "competitive": len(competitive_majors),
                "risky": len(risky_majors)
            },
            "criteria_alerts": criteria_alerts
        }

    @classmethod
    def start_mock_interview(
        cls,
        school_code: str,
        student_data: Dict[str, Any],
        target_major_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Khởi tạo phiên phỏng vấn thử với Đại diện tuyển sinh của trường
        """
        persona = cls.get_school_persona(school_code)
        session_id = f"session_{school_code}_{uuid.uuid4().hex[:8]}"

        # Lấy thông tin ngành mục tiêu
        school_profile = DatabaseManager.get_school_full_profile(school_code)
        target_major_name = "ngành mà em mong muốn"
        target_major_diff = 0.0
        target_tier = "vừa sức"

        if school_profile and target_major_code:
            for b in school_profile.get("benchmarks", []):
                if b.get("major_code") == target_major_code:
                    target_major_name = b.get("major_name")
                    break

        # Câu chào và câu hỏi số 1
        first_question = (
            f"Chào em! Thầy/Cô rất vui được đón tiếp em tham gia buổi thẩm định hồ sơ trực tuyến của {persona['school']}. "
            f"Qua dữ liệu xét tuyển vừa tính toán, Thầy/Cô nhận thấy em đang đặc biệt quan tâm đến **{target_major_name}**. "
            f"Em hãy chia sẻ chân thành: **Điều gì là động lực lớn nhất thôi thúc em quyết tâm chọn {persona['school']} và ngành này?**"
        )

        quick_replies = [
            f"Em đam mê danh tiếng đào tạo và mạng lưới cựu sinh viên xuất sắc của {persona['school']}.",
            f"Em muốn theo đuổi thực chiến ngành {target_major_name} để làm việc tại các tập đoàn lớn.",
            f"Môi trường học tập kỷ luật, chuẩn mực và bạn bè ưu tú của trường là nơi em muốn thuộc về."
        ]

        return {
            "session_id": session_id,
            "school_code": school_code,
            "target_major_code": target_major_code,
            "target_major_name": target_major_name,
            "persona": persona,
            "turn_index": 1,
            "total_turns": 3,
            "bot_message": first_question,
            "quick_replies": quick_replies,
            "is_finished": False
        }

    @classmethod
    def process_interview_turn(
        cls,
        session_id: str,
        school_code: str,
        turn_index: int,
        user_answer: str,
        target_major_name: str = "Ngành mục tiêu",
        qa_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Xử lý từng lượt phỏng vấn và sinh Bản Nhận Xét Chung Cuộc ở lượt cuối
        """
        persona = cls.get_school_persona(school_code)
        code = school_code.upper()

        if turn_index == 1:
            # Chuyển sang Câu 2: Độ phù hợp văn hóa & Áp lực học tập
            if code in ["BKHN", "HCMUT", "DUT"]:
                q2 = (
                    f"Rất tuyệt vời! Động lực của em rất rõ ràng. "
                    f"Tuy nhiên, {persona['school']} nổi tiếng cả nước là ngôi trường kỹ thuật có chương trình học rất nặng, "
                    f"đồ án dồn dập và thi cử cực kỳ nghiêm ngặt. "
                    f"**Em đã chuẩn bị phương pháp tự học, kỹ năng làm việc nhóm và sức bền tinh thần ra sao để vượt qua những học kỳ khắc nghiệt này?**"
                )
                q2_replies = [
                    "Em đã quen với việc tự học lập trình/giải thuật mỗi ngày và không ngại làm lại từ đầu khi gặp lỗi.",
                    "Em có thói quen lập thời gian biểu chi tiết, ưu tiên bài tập lớn và chủ động tìm bạn bè giỏi để học nhóm.",
                    "Em tin rằng áp lực cao chính là lò luyện tốt nhất giúp em trưởng thành vượt bậc sau khi ra trường."
                ]
            elif code in ["NEU", "FTU", "UEH", "DUE"]:
                q2 = (
                    f"Thầy/Cô đánh giá cao sự tự tin của em! "
                    f"Môi trường tại {persona['school']} rất năng động và cạnh tranh cao. Sinh viên không chỉ cần học giỏi "
                    f"mà còn phải liên tục tham gia cuộc thi khởi nghiệp, thuyết trình tiếng Anh và hoạt động ngoại khóa. "
                    f"**Em tự tin nhất ở thế mạnh cá nhân nào để khẳng định mình trong môi trường 'toàn nhân tài' này?**"
                )
                q2_replies = [
                    "Em tự tin vào khả năng ngoại ngữ, giao tiếp linh hoạt và tư duy phân tích tình huống kinh doanh.",
                    "Em có khả năng kết nối nhóm tốt, tinh thần trách nhiệm cao và ham học hỏi cái mới.",
                    "Em thích thử thách bản thân ở các dự án thực tế, không ngại bị phản biện để hoàn thiện ý tưởng."
                ]
            elif code in ["HMU", "UMP", "HMED"]:
                q2 = (
                    f"Một tinh thần phụng sự rất đáng trân trọng! "
                    f"Học ngành Y Dược là một hành trình dài ít nhất 6 năm, thường xuyên phải trực đêm, đối mặt với sinh mệnh con người và khối lượng kiến thức khổng lồ. "
                    f"**Điều gì sẽ là điểm tựa lớn nhất giúp em giữ vững lòng kiên trì và y đức qua những năm tháng cam go đó?**"
                )
                q2_replies = [
                    "Lòng trắc ẩn và ước mơ chữa bệnh cứu người là lý tưởng sống bất biến của em.",
                    "Em có sức khỏe tốt, tính cách cẩn trọng tỉ mỉ và đã sẵn sàng cho những ca trực dài hơi.",
                    "Gia đình luôn là hậu phương vững chắc và em có tính kiên định cao khi đã chọn con đường này."
                ]
            else:
                q2 = (
                    f"Cảm ơn câu trả lời rất chân thành của em! "
                    f"Để học tốt tại {persona['school']}, tính chủ động và khả năng tự nghiên cứu là yếu tố quyết định. "
                    f"**Em đã từng tự mình vượt qua một môn học khó hoặc một dự án thử thách nào trong thời gian học THPT chưa?**"
                )
                q2_replies = [
                    "Em từng tự tìm tòi tài liệu nâng cao và giải quyết thành công các bài toán phức tạp ngoài sách giáo khoa.",
                    "Em luôn giữ thói quen tự học có kỷ luật, đọc thêm sách chuyên ngành mỗi khi có thời gian rảnh.",
                    "Em biết cách hỏi thầy cô và tìm sự hỗ trợ đúng lúc từ các bạn trong nhóm."
                ]

            return {
                "session_id": session_id,
                "turn_index": 2,
                "total_turns": 3,
                "persona": persona,
                "bot_message": q2,
                "quick_replies": q2_replies,
                "is_finished": False
            }

        elif turn_index == 2:
            # Chuyển sang Câu 3: Khả năng tài chính & Lựa chọn hệ đào tạo
            q3 = (
                f"Tư duy rất bản lĩnh và chín chắn! "
                f"Hiện nay tại {persona['school']}, trường triển khai song song cả **Hệ Chuẩn (học phí đại trà, cạnh tranh điểm cao)** "
                f"và các **Chương trình Tiên tiến / Chất lượng cao / Đào tạo quốc tế (học bằng tiếng Anh, học phí cao hơn nhưng ngưỡng điểm dễ thở hơn)**. "
                f"**Định hướng và khả năng tài chính của gia đình em đang ưu tiên phương án nào hơn?**"
            )
            q3_replies = [
                "Gia đình em ưu tiên Hệ Chuẩn tiết kiệm chi phí, em tự tin sẽ nỗ lực đạt điểm số cao nhất.",
                "Gia đình em hoàn toàn ủng hộ Hệ Tiên tiến / CLC để em được học bằng tiếng Anh và có cơ hội trao đổi quốc tế.",
                "Em đặt mục tiêu săn học bổng khuyến học của trường để trang trải học phí và rèn luyện bản thân."
            ]

            return {
                "session_id": session_id,
                "turn_index": 3,
                "total_turns": 3,
                "persona": persona,
                "bot_message": q3,
                "quick_replies": q3_replies,
                "is_finished": False
            }

        else:
            # Lượt 3 hoàn thành -> Xuất BẢN NHẬN XÉT CHUNG CUỘC (Evaluation Report)
            # Tính toán Fit Score (từ 88% đến 96% theo độ thuyết phục)
            fit_score = 92
            if len(user_answer) > 40:
                fit_score = 95
            elif len(user_answer) < 15:
                fit_score = 88

            report = {
                "fit_score": fit_score,
                "candidate_evaluation": (
                    f"Học sinh thể hiện động lực chọn trường xuất phát từ sự am hiểu sâu sắc về thế mạnh của {persona['school']}. "
                    f"Tư duy kỷ luật tự giác cao, tinh thần chuẩn bị tâm lý vững vàng trước áp lực thi cử và môi trường đại học. "
                    f"Mức độ tương thích văn hóa (Culture Fit) đạt {fit_score}%."
                ),
                "strengths_observed": [
                    "Mục tiêu rõ ràng, định hướng học tập nghiêm túc",
                    "Khả năng tự học và ý thức chủ động vượt khó tốt",
                    "Thái độ cầu thị, trung thực và bản lĩnh tự tin"
                ],
                "tactical_recommendation": {
                    "nv1_advice": f"Nên mạnh dạn đăng ký **NV1** vào ngành mơ ước: **{target_major_name}**.",
                    "nv2_backup": f"Nên đặt **NV2** vào một ngành có điểm chuẩn thấp hơn 1.0 - 1.5 điểm cùng thuộc {persona['school']} (thuộc nhóm An Toàn) để chắc chắn nắm giữ tấm vé trở thành sinh viên chính thức của trường.",
                    "interview_passed": True
                },
                "closing_words": (
                    f"Ban Tuyển sinh {persona['school']} đánh giá rất cao tinh thần của em! "
                    f"Hãy tự tin hoàn thiện hồ sơ và giữ vững phong độ ôn tập. Hẹn gặp lại em vào ngày nhập học sắp tới tại giảng đường {persona['school']}!"
                )
            }

            final_message = (
                f"Tuyệt vời! Buổi phỏng vấn đã hoàn tất thành công. "
                f"Thầy/Cô đã hoàn thiện **Bản Đánh Giá Năng Lực & Độ Phù Hợp (Fit Score: {fit_score}%)** dành riêng cho em ở bên dưới!"
            )

            return {
                "session_id": session_id,
                "turn_index": 3,
                "total_turns": 3,
                "persona": persona,
                "bot_message": final_message,
                "quick_replies": [],
                "is_finished": True,
                "evaluation_report": report
            }
