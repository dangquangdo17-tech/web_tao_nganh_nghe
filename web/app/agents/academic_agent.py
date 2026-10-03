import pandas as pd
import numpy as np
from typing import Dict, Any, List
from .state import CounselorState

class AcademicAgent:
    """
    Agent Học thuật:
    Chuyên phân tích bảng điểm thi thử/dự đoán tốt nghiệp và học bạ bằng pandas.
    Xác định tổ hợp môn thế mạnh, tính độ lệch chuẩn điểm số và đánh giá biên độ cạnh tranh.
    """

    COMBINATION_MAPPINGS = {
        "A00": ["Toán", "Vật lý", "Hóa học"],
        "A01": ["Toán", "Vật lý", "Tiếng Anh"],
        "B00": ["Toán", "Hóa học", "Sinh học"],
        "C00": ["Ngữ văn", "Lịch sử", "Địa lý"],
        "D01": ["Toán", "Ngữ văn", "Tiếng Anh"],
        "D07": ["Toán", "Hóa học", "Tiếng Anh"],
        "A02": ["Toán", "Vật lý", "Sinh học"]
    }

    # Bí danh môn học phòng trường hợp người dùng nhập tên rút gọn
    ALIAS_MAP = {
        "toan": "Toán", "toán": "Toán", "math": "Toán",
        "ly": "Vật lý", "lý": "Vật lý", "vat ly": "Vật lý", "vật lý": "Vật lý", "physics": "Vật lý",
        "hoa": "Hóa học", "hóa": "Hóa học", "hoa hoc": "Hóa học", "hóa học": "Hóa học", "chemistry": "Hóa học",
        "van": "Ngữ văn", "văn": "Ngữ văn", "ngu van": "Ngữ văn", "ngữ văn": "Ngữ văn", "literature": "Ngữ văn",
        "anh": "Tiếng Anh", "tieng anh": "Tiếng Anh", "tiếng anh": "Tiếng Anh", "english": "Tiếng Anh",
        "sinh": "Sinh học", "sinh hoc": "Sinh học", "biology": "Sinh học",
        "su": "Lịch sử", "sử": "Lịch sử", "lich su": "Lịch sử", "history": "Lịch sử",
        "dia": "Địa lý", "địa": "Địa lý", "dia ly": "Địa lý", "geography": "Địa lý"
    }

    @classmethod
    def _standardize_subject_scores(cls, scores: Dict[str, float]) -> Dict[str, float]:
        standardized = {}
        for k, v in scores.items():
            k_clean = k.lower().strip()
            std_name = cls.ALIAS_MAP.get(k_clean, k)
            try:
                standardized[std_name] = float(v)
            except (ValueError, TypeError):
                continue
        return standardized

    @classmethod
    def analyze(cls, state: CounselorState) -> Dict[str, Any]:
        exam_scores = cls._standardize_subject_scores(state.exam_scores)
        transcript_scores = cls._standardize_subject_scores(state.transcript_scores)

        # 1. Tính điểm các tổ hợp bằng Pandas
        combo_results = []
        for combo, subjects in cls.COMBINATION_MAPPINGS.items():
            if all(s in exam_scores for s in subjects):
                total_score = sum(exam_scores[s] for s in subjects)
                combo_results.append({
                    "combination": combo,
                    "total_score": round(total_score, 2),
                    "subjects": subjects,
                    "subject_breakdown": {s: exam_scores[s] for s in subjects}
                })

        if not combo_results:
            # Nếu người dùng chỉ nhập một vài môn hoặc thiếu, dự đoán các tổ hợp khả thi nhất
            default_subjects = ["Toán", "Ngữ văn", "Tiếng Anh"]
            total = sum(exam_scores.get(s, 7.0) for s in default_subjects)
            combo_results.append({
                "combination": "D01",
                "total_score": round(total, 2),
                "subjects": default_subjects,
                "subject_breakdown": {s: exam_scores.get(s, 7.0) for s in default_subjects}
            })

        df_combos = pd.DataFrame(combo_results)
        df_combos = df_combos.sort_values(by="total_score", ascending=False).reset_index(drop=True)

        top_combo = df_combos.iloc[0]["combination"]
        top_score = float(df_combos.iloc[0]["total_score"])
        ranked_combos = df_combos.to_dict(orient="records")

        # 2. Thống kê độ lệch và môn mũi nhọn
        all_score_values = list(exam_scores.values())
        mean_score = float(np.mean(all_score_values)) if all_score_values else 7.0
        std_score = float(np.std(all_score_values)) if all_score_values else 0.0

        # Tìm môn điểm cao nhất và thấp nhất
        sorted_subjects = sorted(exam_scores.items(), key=lambda x: x[1], reverse=True)
        strongest_subject = sorted_subjects[0] if sorted_subjects else ("Toán", 7.0)
        weakest_subject = sorted_subjects[-1] if sorted_subjects else ("Toán", 7.0)

        # 3. Đối chiếu Học bạ vs Thi tốt nghiệp
        comparison_notes = []
        if transcript_scores:
            common_subs = set(exam_scores.keys()).intersection(set(transcript_scores.keys()))
            if common_subs:
                diffs = [exam_scores[s] - transcript_scores[s] for s in common_subs]
                avg_diff = float(np.mean(diffs))
                if avg_diff > 0.5:
                    comparison_notes.append(f"Điểm thi tốt nghiệp dự đoán (+{avg_diff:.1f}đ) bứt phá vượt trội so với điểm trung bình học bạ.")
                elif avg_diff < -0.8:
                    comparison_notes.append(f"Điểm thi dự đoán (-{abs(avg_diff):.1f}đ) thấp hơn học bạ. Bạn nên cân nhắc thêm phương thức xét học bạ kết hợp.")
                else:
                    comparison_notes.append("Năng lực học tập trên lớp và phong độ thi cử rất đồng đều và ổn định.")

        # Nhận định từ Agent Học thuật
        academic_comment = (
            f"Tổ hợp thi có lợi thế điểm số cao nhất của bạn là **{top_combo}** với tổng điểm dự kiến **{top_score:.2f} điểm** "
            f"(Môn mũi nhọn: {strongest_subject[0]} đạt {strongest_subject[1]} điểm). "
            f"Độ phân tán điểm số giữa các môn là ±{std_score:.2f} điểm, cho thấy phổ năng lực "
            f"{'rất tập trung và phân hóa rõ rệt' if std_score > 1.2 else 'tương đối cân bằng'}."
        )

        # Đối chiếu tổ hợp chuyên biệt theo câu hỏi của học sinh
        interest_lower = (state.user_interest or "").lower()
        combo_map = {c["combination"]: c["total_score"] for c in ranked_combos}
        
        target_combo_note = ""
        if any(w in interest_lower for w in ["y khoa", "bác sĩ", "y dược", "dược", "sinh học"]):
            if "B00" in combo_map:
                target_combo_note = f" Đối với định hướng Y Dược mà bạn đề cập, tổ hợp cốt lõi **B00 (Toán-Hóa-Sinh)** của bạn đạt **{combo_map['B00']:.2f} điểm**."
            else:
                target_combo_note = " Đối với định hướng Y Dược, bạn chưa đăng ký đủ môn cho tổ hợp cốt lõi B00 (Toán-Hóa-Sinh)."
        elif any(w in interest_lower for w in ["luật", "báo chí", "truyền thông", "xã hội", "sử", "địa"]):
            if "C00" in combo_map:
                target_combo_note = f" Đối với định hướng Xã hội & Luật, tổ hợp cốt lõi **C00 (Văn-Sử-Địa)** của bạn đạt **{combo_map['C00']:.2f} điểm**."
            else:
                target_combo_note = " Đối với định hướng Xã hội & Luật, bạn chưa đăng ký đủ môn cho tổ hợp cốt lõi C00 (Văn-Sử-Địa)."
        elif any(w in interest_lower for w in ["kinh tế", "ngoại thương", "kinh doanh", "logistics", "marketing", "ngôn ngữ", "tiếng anh"]):
            if "D01" in combo_map:
                target_combo_note = f" Đối với định hướng Kinh tế & Ngoại ngữ, tổ hợp **D01 (Toán-Văn-Anh)** của bạn đạt **{combo_map['D01']:.2f} điểm**."
            elif "A01" in combo_map:
                target_combo_note = f" Đối với định hướng Kinh tế & Quản lý, tổ hợp **A01 (Toán-Lý-Anh)** của bạn đạt **{combo_map['A01']:.2f} điểm**."
        elif any(w in interest_lower for w in ["máy tính", "cntt", "ai", "robot", "ô tô", "bán dẫn", "kỹ thuật", "phần mềm"]):
            tech_notes = []
            if "A00" in combo_map:
                tech_notes.append(f"**A00 (Toán-Lý-Hóa)** đạt **{combo_map['A00']:.2f} điểm**")
            if "A01" in combo_map:
                tech_notes.append(f"**A01 (Toán-Lý-Anh)** đạt **{combo_map['A01']:.2f} điểm**")
            if tech_notes:
                target_combo_note = f" Đối với khối Kỹ thuật & Công nghệ, tổ hợp thế mạnh của bạn: {' và '.join(tech_notes)}."
            else:
                target_combo_note = " Đối với khối Kỹ thuật & Công nghệ, bạn chưa đăng ký đủ môn cho tổ hợp A00 hoặc A01."
        
        if target_combo_note:
            academic_comment += target_combo_note

        if comparison_notes:
            academic_comment += " " + " ".join(comparison_notes)

        return {
            "ranked_combinations": ranked_combos,
            "top_combination": top_combo,
            "top_score": top_score,
            "mean_score": round(mean_score, 2),
            "std_deviation": round(std_score, 2),
            "strongest_subject": strongest_subject,
            "weakest_subject": weakest_subject,
            "commentary": academic_comment,
            "standardized_exam_scores": exam_scores
        }
