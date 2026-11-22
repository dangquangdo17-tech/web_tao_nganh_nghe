import sys
import os

# Đảm bảo UTF-8 cho Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Thêm path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.slm.rule_engine import AdmissionRuleEngine

def test_admission_rule_engine():
    print("==================================================")
    print("BẮT ĐẦU KIỂM THỬ ĐỘNG CƠ QUY TẮC (RULE ENGINE)")
    print("==================================================")

    # ----------------------------------------------------
    # Case 1: HMU - Đại học Y Hà Nội (Template 1: Chuẩn 30 B00)
    # ----------------------------------------------------
    scores_hmu = {"Toán": 9.2, "Hóa học": 9.0, "Sinh học": 9.4}
    rule_hmu = AdmissionRuleEngine.resolve_rule("HMU", "MED-GEN", "Bác sĩ Đa khoa", "B00", "Xét theo điểm thi THPT", 28.5)
    res_hmu = AdmissionRuleEngine.compute_score(
        exam_scores=scores_hmu,
        rule=rule_hmu,
        combination_code="B00",
        area="KV1" # Base 0.75
    )
    print("\n[Case 1: HMU - Y Hà Nội]")
    print(f"Rule: {res_hmu['rule_name']}")
    print(f"Target Scale: {res_hmu['target_scale']}")
    print(f"Raw Score: {res_hmu['raw_score']}")
    print(f"Priority Detail: {res_hmu['priority_detail']}")
    print(f"Final Score: {res_hmu['final_score']}")

    # Kiểm tra
    expected_raw_hmu = 9.2 + 9.0 + 9.4 # 27.6
    assert abs(res_hmu["raw_score"] - expected_raw_hmu) < 0.01, f"Expected {expected_raw_hmu}, got {res_hmu['raw_score']}"
    # Raw >= 22.5 => Giảm trừ: (30 - 27.6) / 7.5 = 2.4 / 7.5 = 0.32 => 0.75 * 0.32 = 0.24
    expected_priority_hmu = 0.75 * ((30.0 - 27.6) / 7.5)
    assert abs(res_hmu["priority_points"] - round(expected_priority_hmu, 2)) < 0.02, f"Priority mismatch: {res_hmu['priority_points']} vs {expected_priority_hmu}"
    print("==> Case 1 PASS! ✓")

    # ----------------------------------------------------
    # Case 2: AOF CLC - Học viện Tài chính (Template 2: Thang 30 quy đổi Toán x 2)
    # ----------------------------------------------------
    scores_aof = {"Toán": 9.0, "Ngữ văn": 8.0, "Tiếng Anh": 8.5}
    rule_aof = AdmissionRuleEngine.resolve_rule("AOF", "ACC-AUD-CLC", "Kế toán CLC", "D01", "Chương trình chất lượng cao Toán nhân 2", 27.0)
    res_aof = AdmissionRuleEngine.compute_score(
        exam_scores=scores_aof,
        rule=rule_aof,
        combination_code="D01",
        area="KV2" # Base 0.25
    )
    print("\n[Case 2: AOF CLC - Học viện Tài chính]")
    print(f"Rule: {res_aof['rule_name']}")
    print(f"Target Scale: {res_aof['target_scale']}")
    print(f"Raw Score: {res_aof['raw_score']}")
    print(f"Formula: {res_aof['formula_desc']}")
    print(f"Final Score: {res_aof['final_score']}")

    # Toán x 2: (9.0 * 2 + 8.0 + 8.5) / 4 * 3 = 34.5 / 4 * 3 = 8.625 * 3 = 25.875 => 25.88
    expected_raw_aof = (9.0 * 2 + 8.0 + 8.5) / 4.0 * 3.0
    assert abs(res_aof["raw_score"] - round(expected_raw_aof, 2)) < 0.02, f"Expected {expected_raw_aof}, got {res_aof['raw_score']}"
    print("==> Case 2 PASS! ✓")

    # ----------------------------------------------------
    # Case 3: HANU - Đại học Hà Nội (Template 3: Thang 40 Ngoại ngữ x 2)
    # ----------------------------------------------------
    scores_hanu = {"Toán": 8.0, "Ngữ văn": 8.5, "Tiếng Anh": 9.0}
    rule_hanu = AdmissionRuleEngine.resolve_rule("HANU", "SOC-ENG", "Ngôn ngữ Anh", "D01", "Tiếng Anh nhân hệ số 2", 35.5)
    res_hanu = AdmissionRuleEngine.compute_score(
        exam_scores=scores_hanu,
        rule=rule_hanu,
        combination_code="D01",
        area="KV1" # Base 0.75
    )
    print("\n[Case 3: HANU - Đại học Hà Nội (Thang 40)]")
    print(f"Rule: {res_hanu['rule_name']}")
    print(f"Target Scale: {res_hanu['target_scale']}")
    print(f"Raw Score: {res_hanu['raw_score']}")
    print(f"Priority Detail: {res_hanu['priority_detail']}")
    print(f"Final Score: {res_hanu['final_score']}")

    # Thang 40: Tiếng Anh x 2 + Toán + Văn = 9.0 * 2 + 8.0 + 8.5 = 34.5
    expected_raw_hanu = 9.0 * 2 + 8.0 + 8.5
    assert abs(res_hanu["raw_score"] - expected_raw_hanu) < 0.01, f"Expected {expected_raw_hanu}, got {res_hanu['raw_score']}"
    assert res_hanu["target_scale"] == 40.0, f"Expected scale 40, got {res_hanu['target_scale']}"

    # Priority check: T30 = 34.5 * (30/40) = 25.875 >= 22.5
    # reduction = (30 - 25.875) / 7.5 = 4.125 / 7.5 = 0.55
    # Priority 30 = 0.75 * 0.55 = 0.4125
    # Final Priority on Scale 40 = 0.4125 * (40/30) = 0.55
    assert abs(res_hanu["priority_points"] - 0.55) < 0.02, f"Expected priority 0.55, got {res_hanu['priority_points']}"
    print("==> Case 3 PASS! ✓")

    # ----------------------------------------------------
    # Case 4: NEU - IELTS Quy đổi & Chặn Double-dipping (Template 5)
    # ----------------------------------------------------
    scores_neu = {"Toán": 9.0, "Ngữ văn": 8.0, "Tiếng Anh": 7.0}
    rule_neu = AdmissionRuleEngine.resolve_rule("NEU", "ECO-IB", "Kinh doanh Quốc tế", "D01", "Tiếng Anh >= 8.5", 28.1)
    # Thí sinh có IELTS 7.5 (quy đổi 10.0 tại NEU), và có bonus_points từ trước = 1.0
    res_neu = AdmissionRuleEngine.compute_score(
        exam_scores=scores_neu,
        rule=rule_neu,
        combination_code="D01",
        ielts_band=7.5,
        bonus_points=1.0,
        area="KV3" # Base 0
    )
    print("\n[Case 4: NEU - IELTS Quy đổi & Double-Dipping Guard]")
    print(f"Rule: {res_neu['rule_name']}")
    print(f"IELTS Replaced: {res_neu['ielts_replaced']}")
    print(f"IELTS Converted Value: {res_neu['ielts_converted_value']}")
    print(f"Raw Score: {res_neu['raw_score']}")
    print(f"Effective Bonus: {res_neu['bonus_points']}")
    print(f"Final Score: {res_neu['final_score']}")

    # Tiếng Anh 7.0 được thay thế bởi IELTS 7.5 -> 10.0
    assert res_neu["ielts_replaced"] is True
    assert res_neu["ielts_converted_value"] == 10.0
    # Raw = Toán 9.0 + Văn 8.0 + Anh (IELTS) 10.0 = 27.0
    assert abs(res_neu["raw_score"] - 27.0) < 0.01
    # Bonus bị chặn vì không cho phép double dipping (allow_stacking_with_ielts: false)
    assert res_neu["bonus_points"] == 0.0, "Double dipping must be blocked!"
    assert abs(res_neu["final_score"] - 27.0) < 0.01
    print("==> Case 4 PASS! ✓")

    print("\n==================================================")
    print("TẤT CẢ CÁC BÀI TEST TOÁN HỌC & ĐỘNG CƠ QUY TẮC ĐỀU ĐẠT CHUẨN 100%! ✓")
    print("==================================================")

if __name__ == "__main__":
    test_admission_rule_engine()
