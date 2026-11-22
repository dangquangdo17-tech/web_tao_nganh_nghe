import json
import os
import re
from typing import Dict, Any, List, Optional, Tuple

class AdmissionRuleEngine:
    """
    Động cơ quy tắc tuyển sinh Đại học (Rule Engine):
    - Chuẩn hóa 5 templates: T1 (Chuẩn 30), T2 (Thang 30 quy đổi), T3 (Thang 40), T4 (Thang 100), T5 (Quy đổi IELTS).
    - Pipeline 4 bước chuẩn hóa tính toán điểm thô, điểm ưu tiên theo quy chế Bộ GD&ĐT (giảm trừ từ 22.5),
      chặn ăn 2 lần điểm IELTS (Double-dipping guard), và chốt thang điểm nhất quán.
    """

    _rules_cache: Optional[Dict[str, Any]] = None

    COMBO_MAP = {
        "A00": ["Toán", "Vật lý", "Hóa học"],
        "A01": ["Toán", "Vật lý", "Tiếng Anh"],
        "A02": ["Toán", "Vật lý", "Sinh học"],
        "B00": ["Toán", "Hóa học", "Sinh học"],
        "B08": ["Toán", "Sinh học", "Tiếng Anh"],
        "C00": ["Ngữ văn", "Lịch sử", "Địa lý"],
        "C01": ["Ngữ văn", "Toán", "Vật lý"],
        "C03": ["Ngữ văn", "Toán", "Lịch sử"],
        "C04": ["Ngữ văn", "Toán", "Địa lý"],
        "D01": ["Toán", "Ngữ văn", "Tiếng Anh"],
        "D07": ["Toán", "Hóa học", "Tiếng Anh"],
        "D08": ["Toán", "Sinh học", "Tiếng Anh"],
        "D09": ["Toán", "Lịch sử", "Tiếng Anh"],
        "D10": ["Toán", "Địa lý", "Tiếng Anh"],
        "D14": ["Ngữ văn", "Lịch sử", "Tiếng Anh"],
        "D15": ["Ngữ văn", "Địa lý", "Tiếng Anh"],
        "D78": ["Ngữ văn", "Tiếng Anh", "Lịch sử"],
        "D90": ["Toán", "Khoa học tự nhiên", "Tiếng Anh"]
    }

    AREA_MAP = {
        "KV1": 0.75,
        "KV2-NT": 0.5,
        "KV2": 0.25,
        "KV3": 0.0
    }

    @classmethod
    def get_rules_config(cls, force_reload: bool = False) -> Dict[str, Any]:
        """Tải cấu hình rules từ file admission_rules.json (kèm cache)"""
        if cls._rules_cache is not None and not force_reload:
            return cls._rules_cache

        json_path = os.path.join(os.path.dirname(__file__), "admission_rules.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                cls._rules_cache = json.load(f)
        except Exception as e:
            # Fallback an toàn nếu file có sự cố
            cls._rules_cache = {
                "templates": {
                    "T1_STANDARD_30": {
                        "template_id": "T1_STANDARD_30",
                        "target_scale": 30.0,
                        "normalization": "unweighted_30",
                        "formula_desc": "Điểm thô = M1 + M2 + M3",
                        "allow_stacking_with_ielts": False
                    }
                },
                "default_ielts_map": {"5.0": 8.0, "5.5": 8.5, "6.0": 9.0, "6.5": 9.5, "7.0": 10.0},
                "school_overrides": {}
            }
        return cls._rules_cache

    @classmethod
    def get_combo_subjects(cls, combo: str) -> List[str]:
        """Trả về 3 môn trong tổ hợp xét tuyển"""
        c = combo.strip().upper()
        return cls.COMBO_MAP.get(c, ["Toán", "Ngữ văn", "Tiếng Anh"])

    @classmethod
    def resolve_rule(
        cls,
        school_code: str,
        major_code: str,
        major_name: str = "",
        combination_code: str = "A00",
        sub_criteria: str = "",
        benchmark_score: float = 25.0,
        prospectus_ielts_map: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Tìm quy tắc tính điểm tối ưu nhất cho (Trường + Ngành + Tổ hợp + Tiêu chí phụ).
        Nếu không có cấu hình cứng, tự động suy luận thông minh từ Tiêu chí phụ và Thang điểm.
        """
        config = cls.get_rules_config()
        school_code_clean = (school_code or "").strip().upper()
        major_code_clean = (major_code or "").strip()
        criteria_lower = (sub_criteria or "").lower()
        major_lower = (major_name or "").lower()

        # 1. Kiểm tra School Overrides
        overrides = config.get("school_overrides", {})
        if school_code_clean in overrides:
            school_entry = overrides[school_code_clean]
            rules_list = school_entry.get("rules", [])

            # Ưu tiên 1: Match chính xác major_code
            for rule in rules_list:
                if "applicable_majors" in rule and major_code_clean in rule["applicable_majors"]:
                    rule_copy = dict(rule)
                    if prospectus_ielts_map and "ielts_conversion_table" not in rule_copy:
                        rule_copy["ielts_conversion_table"] = prospectus_ielts_map
                    return rule_copy

            # Ưu tiên 2: Match theo keywords có kiểm tra tính tương thích thang điểm
            for rule in rules_list:
                # Nếu rule thang 40 nhưng benchmark <= 31.0 và không có "nhân hệ số 2", bỏ qua rule này
                if rule.get("target_scale") == 40.0 and benchmark_score <= 31.0 and not ("nhân hệ số 2" in criteria_lower or "thang 40" in criteria_lower):
                    continue

                keywords = rule.get("applicable_keywords", [])
                if keywords:
                    for kw in keywords:
                        kw_lower = kw.lower()
                        if kw_lower in criteria_lower or kw_lower in major_lower:
                            rule_copy = dict(rule)
                            if prospectus_ielts_map and "ielts_conversion_table" not in rule_copy:
                                rule_copy["ielts_conversion_table"] = prospectus_ielts_map
                            return rule_copy

            # Ưu tiên 3: Fallback rule mặc định của trường (tương thích với benchmark_score)
            for rule in rules_list:
                if benchmark_score > 31.0 and rule.get("target_scale") != 40.0:
                    continue
                if benchmark_score <= 31.0 and rule.get("target_scale") == 40.0:
                    continue
                if not rule.get("applicable_majors") and not rule.get("applicable_keywords"):
                    rule_copy = dict(rule)
                    if prospectus_ielts_map and "ielts_conversion_table" not in rule_copy:
                        rule_copy["ielts_conversion_table"] = prospectus_ielts_map
                    return rule_copy

        # 2. Dynamic Rule Resolver: Tự động phân tích sub_criteria & benchmark score
        # Phân tích xem có hệ số nhân 2 không
        is_scale_40 = False
        is_weighted_norm_30 = False
        is_scale_100 = False
        main_subject = None

        if "thang 40" in criteria_lower or benchmark_score > 32.0:
            is_scale_40 = True
        elif "nhân hệ số 2" in criteria_lower or "hệ số 2" in criteria_lower or "môn chính" in criteria_lower:
            if "quy về 30" in criteria_lower or "(toán*2)/4" in criteria_lower or "(môn chính*2)/4" in criteria_lower or benchmark_score <= 30.5:
                is_weighted_norm_30 = True
            else:
                is_scale_40 = True
        elif "thang 100" in criteria_lower or "tsa" in criteria_lower or "đánh giá tư duy" in criteria_lower or benchmark_score > 50.0:
            is_scale_100 = True

        # Xác định môn chính
        if is_scale_40 or is_weighted_norm_30:
            if any(w in criteria_lower for w in ["tiếng anh", "ngoại ngữ", "anh"]):
                main_subject = "Tiếng Anh"
            elif any(w in criteria_lower for w in ["toán", "toán học"]):
                main_subject = "Toán"
            elif any(w in criteria_lower for w in ["văn", "ngữ văn"]):
                main_subject = "Ngữ văn"
            elif any(w in criteria_lower for w in ["hóa", "hóa học"]):
                main_subject = "Hóa học"
            elif any(w in criteria_lower for w in ["sinh", "sinh học"]):
                main_subject = "Sinh học"
            else:
                # Mặc định theo mã ngành hoặc tổ hợp
                if combination_code.startswith("D"):
                    main_subject = "Tiếng Anh"
                else:
                    main_subject = "Toán"

        # Quyết định Template
        ielts_table = prospectus_ielts_map or config.get("default_ielts_map", {})

        if is_scale_100:
            template = config.get("templates", {}).get("T4_SCALE_100", {})
            return {
                "rule_id": f"{school_code_clean}_TSA_100",
                "rule_name": f"{school_code_clean} - Đánh giá tư duy / Năng lực (Thang 100)",
                "template_id": "T4_SCALE_100",
                "target_scale": 100.0,
                "normalization": "scale_100",
                "formula_desc": "Điểm thô = Điểm bài thi TSA / ĐGNL (Thang 100, Điểm ưu tiên x 10/3)",
                "allow_ielts_replacement": False,
                "allow_stacking_with_ielts": False
            }
        elif is_scale_40:
            template = config.get("templates", {}).get("T3_SCALE_40", {})
            return {
                "rule_id": f"{school_code_clean}_{major_code_clean}_SCALE_40",
                "rule_name": f"{school_code_clean} - Thang 40 ({main_subject} nhân hệ số 2)",
                "template_id": "T3_SCALE_40",
                "target_scale": 40.0,
                "normalization": "scale_40",
                "main_subject": main_subject,
                "main_subject_weight": 2.0,
                "formula_desc": f"Điểm thô = {main_subject} x 2 + M2 + M3 (Thang 40, Điểm ưu tiên x 4/3)",
                "allow_ielts_replacement": True,
                "allow_stacking_with_ielts": False,
                "ielts_conversion_table": ielts_table
            }
        elif is_weighted_norm_30:
            template = config.get("templates", {}).get("T2_WEIGHTED_NORM_30", {})
            return {
                "rule_id": f"{school_code_clean}_{major_code_clean}_WEIGHTED_30",
                "rule_name": f"{school_code_clean} - Thang 30 quy đổi ({main_subject} hệ số 2)",
                "template_id": "T2_WEIGHTED_NORM_30",
                "target_scale": 30.0,
                "normalization": "weighted_norm_30",
                "main_subject": main_subject,
                "main_subject_weight": 2.0,
                "formula_desc": f"Điểm thô = ({main_subject} x 2 + M2 + M3) / 4 x 3",
                "allow_ielts_replacement": True,
                "allow_stacking_with_ielts": False,
                "ielts_conversion_table": ielts_table
            }
        else:
            template = config.get("templates", {}).get("T1_STANDARD_30", {})
            return {
                "rule_id": f"{school_code_clean}_STANDARD_30",
                "rule_name": f"{school_code_clean} - Chuẩn 30 không nhân hệ số",
                "template_id": "T1_STANDARD_30",
                "target_scale": 30.0,
                "normalization": "unweighted_30",
                "formula_desc": "Điểm thô = M1 + M2 + M3",
                "allow_ielts_replacement": True,
                "allow_stacking_with_ielts": False,
                "ielts_conversion_table": ielts_table
            }

    @classmethod
    def convert_ielts(cls, ielts_band: Optional[float], ielts_table: Dict[str, float]) -> float:
        """Quy đổi band điểm IELTS sang thang điểm 10 theo bảng của Rule"""
        if not ielts_band or ielts_band < 4.0 or not ielts_table:
            return 0.0

        # Chuẩn hóa bảng tra cứu sang float key
        numeric_table: List[Tuple[float, float]] = []
        for k, v in ielts_table.items():
            # Hỗ trợ cả key "5.5" lẫn "IELTS 5.5" hoặc "IELTS 7.0+"
            m = re.search(r"(\d+(\.\d+)?)", str(k))
            if m:
                numeric_table.append((float(m.group(1)), float(v)))

        if not numeric_table:
            return 8.0 if ielts_band >= 5.0 else 0.0

        # Sắp xếp band giảm dần
        numeric_table.sort(key=lambda x: x[0], reverse=True)

        for min_band, score in numeric_table:
            if ielts_band >= min_band:
                return score

        return 0.0

    @classmethod
    def calculate_moet_priority(
        cls,
        raw_score: float,
        target_scale: float = 30.0,
        area: str = "KV3",
        ethnicity: str = "kinh",
        priority_object: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Tính điểm ưu tiên chuẩn Quy chế Bộ GD&ĐT:
        - Mức điểm ưu tiên cơ sở = Điểm khu vực + Điểm đối tượng chính sách.
        - Quy đổi điểm thô về thang 30: T30 = raw_score * (30 / target_scale).
        - Nếu T30 >= 22.5: ĐƯT_30 = Base * (30 - T30) / 7.5.
        - Quy đổi ĐƯT về đúng target_scale: ĐƯT_final = ĐƯT_30 * (target_scale / 30).
        """
        area_pts = cls.AREA_MAP.get(area.strip().upper(), 0.0)
        
        # Đối tượng chính sách: dân tộc thiểu số hoặc UT1/UT2
        eth_pts = 0.0
        eth_lower = (ethnicity or "").lower().strip()
        if eth_lower in ["minority", "dân tộc thiểu số", "dan_toc_thieu_so", "dtts", "dân tộc ít người"]:
            eth_pts = 1.0
        elif priority_object == "UT1":
            eth_pts = 2.0
        elif priority_object == "UT2":
            eth_pts = 1.0

        base_priority = area_pts + eth_pts

        if base_priority <= 0:
            return {
                "base_priority": 0.0,
                "priority_30": 0.0,
                "final_priority": 0.0,
                "is_reduced": False,
                "reduction_ratio": 1.0
            }

        # Quy đổi điểm thô về thang 30 để kiểm tra mốc 22.5
        scale_ratio = 30.0 / target_scale if target_scale > 0 else 1.0
        t30 = raw_score * scale_ratio

        if t30 >= 22.5:
            # Áp dụng công thức giảm trừ tuyến tính từ 22.5 đến 30.0
            reduction_ratio = max(0.0, (30.0 - t30) / 7.5)
            priority_30 = base_priority * reduction_ratio
            is_reduced = True
        else:
            reduction_ratio = 1.0
            priority_30 = base_priority
            is_reduced = False

        # Quy đổi điểm ưu tiên về đúng target_scale
        final_priority = priority_30 * (target_scale / 30.0)

        return {
            "base_priority": round(base_priority, 3),
            "priority_30": round(priority_30, 3),
            "final_priority": round(final_priority, 2),
            "is_reduced": is_reduced,
            "reduction_ratio": round(reduction_ratio, 3),
            "t30_equivalent": round(t30, 2)
        }

    @classmethod
    def compute_score(
        cls,
        exam_scores: Dict[str, float],
        rule: Dict[str, Any],
        combination_code: str = "A00",
        area: str = "KV3",
        ethnicity: str = "kinh",
        ielts_band: Optional[float] = None,
        bonus_points: float = 0.0,
        tsa_score: Optional[float] = None,
        apt_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Quy trình 4 bước chuẩn hóa (Calculation Pipeline):
        Bước 1: Quy đổi chứng chỉ & Điểm môn trong tổ hợp.
        Bước 2: Tính Điểm thô (Raw Weighted Score) theo Template & Normalization.
        Bước 3: Tính Điểm ưu tiên MOET có giảm trừ từ 22.5 và scale về target_scale.
        Bước 4: Kiểm tra chống ăn 2 lần IELTS (Double-dipping guard), cộng điểm thưởng và chốt điểm cuối cùng.
        """
        target_scale = float(rule.get("target_scale", 30.0))
        normalization = rule.get("normalization", "unweighted_30")
        allow_ielts_replacement = rule.get("allow_ielts_replacement", True)
        allow_stacking_with_ielts = rule.get("allow_stacking_with_ielts", False)
        ielts_table = rule.get("ielts_conversion_table") or {}

        # -------------------------------------------------------------
        # BƯỚC 1: QUY ĐỔI CHỨNG CHỈ & ĐIỂM MÔN
        # -------------------------------------------------------------
        combo_subjects = cls.get_combo_subjects(combination_code)
        subject_scores_raw = {}
        subject_scores_effective = {}
        ielts_replaced = False
        ielts_converted_value = 0.0

        for subj in combo_subjects:
            score = exam_scores.get(subj, 0.0)
            subject_scores_raw[subj] = score

            # Kiểm tra thay thế môn Tiếng Anh bằng IELTS
            if subj == "Tiếng Anh" and allow_ielts_replacement and ielts_band and ielts_band >= 4.0:
                conv = cls.convert_ielts(ielts_band, ielts_table)
                if conv > score:
                    subject_scores_effective[subj] = conv
                    ielts_replaced = True
                    ielts_converted_value = conv
                else:
                    subject_scores_effective[subj] = score
            else:
                subject_scores_effective[subj] = score

        # -------------------------------------------------------------
        # BƯỚC 2: TÍNH ĐIỂM THÔ (RAW WEIGHTED SCORE)
        # -------------------------------------------------------------
        main_subject = rule.get("main_subject")
        main_weight = float(rule.get("main_subject_weight", 2.0))

        if normalization == "scale_100":
            # Thang 100 (TSA Bách Khoa hoặc ĐGNL)
            if tsa_score is not None and tsa_score > 0:
                raw_score = float(tsa_score)
            elif apt_score is not None and apt_score > 0:
                # ĐGNL ĐHQG thang 1200 quy về 100
                raw_score = round(float(apt_score) / 12.0, 2)
            else:
                # Ước lượng từ 3 môn THPT sang thang 100: (S1 + S2 + S3) / 3 * 10
                raw_score = round(sum(subject_scores_effective.values()) / 3.0 * 10.0, 2)

        elif normalization == "scale_40":
            # Thang 40: Môn chính nhân 2 + 2 môn còn lại
            total_weighted = 0.0
            for subj, sc in subject_scores_effective.items():
                w = main_weight if (main_subject and subj == main_subject) else 1.0
                total_weighted += sc * w
            raw_score = total_weighted

        elif normalization == "weighted_norm_30":
            # Thang 30 quy đổi: (Môn chính x 2 + M2 + M3) / 4 x 3
            total_weighted = 0.0
            total_weights = 0.0
            for subj, sc in subject_scores_effective.items():
                w = main_weight if (main_subject and subj == main_subject) else 1.0
                total_weighted += sc * w
                total_weights += w
            if total_weights > 0:
                raw_score = (total_weighted / total_weights) * 3.0
            else:
                raw_score = sum(subject_scores_effective.values())

        else:
            # unweighted_30: M1 + M2 + M3 chuẩn
            raw_score = sum(subject_scores_effective.values())

        raw_score = round(raw_score, 2)

        # -------------------------------------------------------------
        # BƯỚC 3: ĐIỂM ƯU TIÊN MOET (Áp dụng giảm trừ từ 22.5)
        # -------------------------------------------------------------
        priority_info = cls.calculate_moet_priority(
            raw_score=raw_score,
            target_scale=target_scale,
            area=area,
            ethnicity=ethnicity
        )
        final_priority = priority_info["final_priority"]

        # -------------------------------------------------------------
        # BƯỚC 4: ĐIỂM THƯỞNG & CHỐT ĐIỂM CUỐI CÙNG (CHỐNG ĂN 2 LẦN)
        # -------------------------------------------------------------
        effective_bonus = float(bonus_points)
        # Nếu đã quy đổi môn tiếng Anh bằng IELTS và rule không cho phép cộng dồn
        if ielts_replaced and not allow_stacking_with_ielts:
            # Loại bỏ điểm thưởng ngoại ngữ trùng lặp
            effective_bonus = 0.0

        total_final = raw_score + final_priority + effective_bonus
        # Clamp tối đa không vượt quá target_scale
        final_score = round(min(target_scale, max(0.0, total_final)), 2)

        return {
            "rule_id": rule.get("rule_id", "DEFAULT_RULE"),
            "rule_name": rule.get("rule_name", "Quy chế chuẩn"),
            "target_scale": target_scale,
            "normalization": normalization,
            "formula_desc": rule.get("formula_desc", "M1 + M2 + M3"),
            "raw_score": raw_score,
            "priority_points": final_priority,
            "priority_detail": priority_info,
            "bonus_points": effective_bonus,
            "final_score": final_score,
            "ielts_replaced": ielts_replaced,
            "ielts_converted_value": ielts_converted_value,
            "subject_scores_raw": subject_scores_raw,
            "subject_scores_effective": subject_scores_effective,
            "combo_subjects": combo_subjects
        }
