from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..slm.prospectus_parser import SLMProspectusParser
from .state import CounselorState

class AdmissionAgent:
    """
    Agent Tuyển sinh & Quy chế:
    Nắm bắt quy chế tuyển sinh, công thức tính điểm ưu tiên khu vực chuẩn Bộ GD&ĐT,
    phân tích đề án tuyển sinh các trường và tối ưu hóa điểm số thông qua chứng chỉ ngoại ngữ (IELTS).
    """

    PRIORITY_POINTS_BASE = {
        "KV1": 0.75,
        "KV2-NT": 0.5,
        "KV2": 0.25,
        "KV3": 0.0
    }

    ETHNICITY_POINTS_BASE = {
        "minority": 1.0,
        "dân tộc thiểu số": 1.0,
        "dan_toc_thieu_so": 1.0,
        "kinh": 0.0
    }

    @classmethod
    def calculate_ministry_priority_score(cls, total_score: float, area_code: str, ethnicity: str = "kinh") -> Dict[str, float]:
        """
        Tính điểm ưu tiên theo công thức giảm dần của Bộ GD&ĐT (Áp dụng từ năm 2023):
        Tổng mức ưu tiên gốc = Điểm ưu tiên khu vực + Điểm ưu tiên đối tượng (Dân tộc thiểu số: 1.0đ, Người Kinh: 0đ)
        Nếu Tổng điểm >= 22.5: Điểm ưu tiên = [(30 - Tổng điểm) / 7.5] * Tổng mức điểm ưu tiên gốc
        Nếu Tổng điểm < 22.5: Điểm ưu tiên = Tổng mức điểm ưu tiên gốc
        """
        area_pts = cls.PRIORITY_POINTS_BASE.get(area_code, 0.0)
        eth_clean = (ethnicity or "kinh").lower().strip()
        ethnicity_pts = 1.0 if eth_clean in ["minority", "dân tộc thiểu số", "dan_toc_thieu_so", "dtt"] else 0.0

        base_priority = area_pts + ethnicity_pts
        if base_priority <= 0:
            return {
                "base_priority": 0.0,
                "area_priority": 0.0,
                "ethnicity_priority": 0.0,
                "scaled_priority": 0.0
            }

        if total_score < 22.5:
            scaled = base_priority
        else:
            scaled = ((30.0 - total_score) / 7.5) * base_priority
            scaled = max(0.0, round(scaled, 2))

        return {
            "base_priority": round(base_priority, 2),
            "area_priority": round(area_pts, 2),
            "ethnicity_priority": round(ethnicity_pts, 2),
            "scaled_priority": scaled
        }

    @classmethod
    def analyze(cls, state: CounselorState) -> Dict[str, Any]:
        ielts = state.ielts_score
        priority_area = state.priority_area or "KV3"
        ethnicity = state.ethnicity or "kinh"
        exam_scores = state.exam_scores or {}
        raw_english = float(exam_scores.get("Tiếng Anh", exam_scores.get("anh", 7.0)))

        # 1. Khảo sát bảng quy đổi IELTS của các trường top đầu qua SLM Prospectus Parser
        prospectuses = DatabaseManager.get_all_prospectuses(year=2025)
        ielts_advantages = []

        if ielts and ielts >= 5.0:
            for p in prospectuses:
                u_code = p["university_code"]
                u_name = p["university_name"]
                conv_map = p.get("ielts_conversion_map", {})
                converted_score = SLMProspectusParser.calculate_converted_score(ielts, conv_map)
                
                gain = converted_score - raw_english
                if gain > 0:
                    ielts_advantages.append({
                        "university_code": u_code,
                        "university_name": u_name,
                        "ielts_band": ielts,
                        "converted_english_score": converted_score,
                        "original_english_score": raw_english,
                        "score_gain": round(gain, 2)
                    })

        # 2. Tính điểm ưu tiên khu vực và đối tượng dân tộc
        academic_analysis = state.academic_analysis or {}
        top_score = float(academic_analysis.get("top_score", 24.0))
        priority_info = cls.calculate_ministry_priority_score(top_score, priority_area, ethnicity)
        calculated_priority = priority_info["scaled_priority"]

        # 3. Phân tích các tiêu chí phụ (Sub-criteria) từ đề án tuyển sinh
        sub_criteria_alerts = []
        math_score = float(exam_scores.get("Toán", exam_scores.get("toan", 7.0)))
        if math_score < 8.0:
            sub_criteria_alerts.append(
                "Lưu ý tiêu chí phụ: Một số ngành IT top 1 (như BKHN, UET) yêu cầu điểm môn Toán >= 8.5 - 9.0 "
                "khi xét điều kiện hòa điểm. Bạn nên chủ động chuẩn bị các nguyện vọng dự phòng."
            )

        is_minority = priority_info["ethnicity_priority"] > 0
        ethnicity_label = "Dân tộc thiểu số (+1.0đ)" if is_minority else "Dân tộc Kinh (0đ)"
        area_label = f"Khu vực {priority_area} (+{priority_info['area_priority']}đ)"

        admission_comment = (
            f"Về chính sách ưu tiên tuyển sinh: Bạn thuộc đối tượng **{ethnicity_label}** và **{area_label}**, "
            f"tổng mức ưu tiên gốc là **+{priority_info['base_priority']} điểm**. "
            f"Sau khi áp dụng công thức phân hóa điểm thi của Bộ GD&ĐT, bạn được cộng chính thức **+{calculated_priority:.2f} điểm ưu tiên** "
            f"vào tổng điểm xét tuyển đại học. "
        )

        if ielts_advantages:
            best_gain = max(ielts_advantages, key=lambda x: x["score_gain"])
            admission_comment += (
                f"Đặc biệt, chứng chỉ **IELTS {ielts}** là 'vũ khí chiến lược' giúp bạn nâng điểm Tiếng Anh từ "
                f"{raw_english} lên tới **{best_gain['converted_english_score']} điểm** (tăng thêm +{best_gain['score_gain']}đ) "
                f"tại các trường như {best_gain['university_name']}, mở toang cánh cửa vào các khối A01, D01."
            )
        elif ielts and ielts < 5.0:
            admission_comment += f"Chứng chỉ IELTS {ielts} hiện chưa đạt ngưỡng quy đổi tối thiểu (5.0 - 5.5) tại các trường đại học lớn."

        return {
            "priority_area": priority_area,
            "ethnicity": ethnicity,
            "area_priority": priority_info["area_priority"],
            "ethnicity_priority": priority_info["ethnicity_priority"],
            "base_priority": priority_info["base_priority"],
            "calculated_priority": calculated_priority,
            "ielts_score": ielts,
            "ielts_advantages": ielts_advantages,
            "sub_criteria_alerts": sub_criteria_alerts,
            "commentary": admission_comment
        }
