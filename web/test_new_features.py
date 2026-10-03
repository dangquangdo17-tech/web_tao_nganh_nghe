import sys
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import requests

BASE_URL = "http://127.0.0.1:1234"

print("=" * 70)
print("KIỂM THỬ TÍNH NĂNG MỚI: CHỌN MÔN THI & ƯU TIÊN DÂN TỘC THIỂU SỐ")
print("=" * 70)

# 1. Test chỉ chọn 4 môn (Toán, Văn, Anh, Lý theo chuẩn 2025)
print("\n[TEST 1] Thí sinh chọn 4 môn (Toán, Văn, Anh, Lý) - Không thi Hóa/Sinh:")
payload_4_subjects = {
    "exam_scores": {
        "Toán": 8.0,
        "Ngữ văn": 7.5,
        "Tiếng Anh": 8.5,
        "Vật lý": 8.0
    },
    "transcript_scores": {"Toán": 8.0, "Ngữ văn": 7.5},
    "user_interest": "Em thích lập trình phần mềm và công nghệ",
    "ielts_score": None,
    "priority_area": "KV3",
    "ethnicity": "kinh",
    "target_region": "Tất cả",
    "target_category": "Tất cả"
}

res1 = requests.post(f"{BASE_URL}/api/consult", json=payload_4_subjects)
assert res1.status_code == 200, f"Error: {res1.text}"
data1 = res1.json()["data"]

academic1 = data1["academic_analysis"]
combos1 = [c["combination"] for c in academic1["ranked_combinations"]]
print(f"  ✅ Các tổ hợp hợp lệ được tính: {combos1}")
# Không được có A00 (cần Hóa) hay B00 (cần Hóa + Sinh)
assert "A00" not in combos1, "Lỗi: Môn Hóa không thi nhưng vẫn tính tổ hợp A00!"
assert "B00" not in combos1, "Lỗi: Môn Sinh không thi nhưng vẫn tính tổ hợp B00!"
assert "A01" in combos1, "Lỗi: Thi Toán, Lý, Anh nhưng không tính A01!"
assert "D01" in combos1, "Lỗi: Thi Toán, Văn, Anh nhưng không tính D01!"
print("  ✅ Đã kiểm tra: Chỉ các tổ hợp gồm đúng các môn đã chọn mới được tính!")

# 2. Test So sánh Điểm ưu tiên: Dân tộc Kinh vs Dân tộc thiểu số (+1.0 điểm)
print("\n[TEST 2] So sánh Dân tộc Kinh (0đ) vs Dân tộc thiểu số (+1.0đ):")

# Thí sinh A: Dân tộc Kinh, KV1 (+0.75đ), Tổng điểm 21.0 (< 22.5 => không bị giảm)
payload_kinh = {
    "exam_scores": {"Toán": 7.0, "Vật lý": 7.0, "Hóa học": 7.0},
    "transcript_scores": {"Toán": 7.0},
    "user_interest": "Em thích kỹ thuật",
    "priority_area": "KV1",
    "ethnicity": "kinh"
}
res_kinh = requests.post(f"{BASE_URL}/api/consult", json=payload_kinh).json()["data"]
adm_kinh = res_kinh["admission_analysis"]

# Thí sinh B: Dân tộc thiểu số, KV1 (+0.75đ), Tổng điểm 21.0
payload_minority = {
    "exam_scores": {"Toán": 7.0, "Vật lý": 7.0, "Hóa học": 7.0},
    "transcript_scores": {"Toán": 7.0},
    "user_interest": "Em thích kỹ thuật",
    "priority_area": "KV1",
    "ethnicity": "minority"
}
res_minority = requests.post(f"{BASE_URL}/api/consult", json=payload_minority).json()["data"]
adm_minority = res_minority["admission_analysis"]

print(f"  • Thí sinh Kinh: Ưu tiên Dân tộc = {adm_kinh['ethnicity_priority']}đ | Khu vực = {adm_kinh['area_priority']}đ | Tổng ưu tiên = {adm_kinh['calculated_priority']}đ")
print(f"  • Thí sinh Dân tộc thiểu số: Ưu tiên Dân tộc = {adm_minority['ethnicity_priority']}đ | Khu vực = {adm_minority['area_priority']}đ | Tổng ưu tiên = {adm_minority['calculated_priority']}đ")

assert adm_kinh["ethnicity_priority"] == 0.0, "Lỗi: Người Kinh phải có điểm ưu tiên dân tộc là 0.0!"
assert adm_minority["ethnicity_priority"] == 1.0, "Lỗi: Dân tộc thiểu số phải được cộng 1.0 điểm!"
assert adm_minority["calculated_priority"] == adm_kinh["calculated_priority"] + 1.0, "Lỗi: Chênh lệch ưu tiên phải đúng bằng 1.0 điểm!"

print("  ✅ Thí sinh Dân tộc thiểu số đã được cộng đúng +1.0 điểm so với thí sinh Kinh!")

# 3. Test công thức giảm dần của Bộ GD&ĐT khi tổng điểm >= 22.5
print("\n[TEST 3] Kiểm tra công thức phân hóa điểm thi Bộ GD&ĐT (Điểm >= 22.5):")
# Tổng điểm = 25.0 -> [(30 - 25.0) / 7.5] = 5 / 7.5 = 2/3 = 0.6667
# Mức gốc: 1.0 (Dân tộc) + 0.5 (KV2-NT) = 1.5
# Điểm ưu tiên = 1.5 * (5 / 7.5) = 1.0 điểm
payload_high_score = {
    "exam_scores": {"Toán": 9.0, "Vật lý": 8.0, "Tiếng Anh": 8.0},
    "transcript_scores": {"Toán": 9.0},
    "user_interest": "Em thích trí tuệ nhân tạo",
    "priority_area": "KV2-NT",
    "ethnicity": "minority"
}
res_high = requests.post(f"{BASE_URL}/api/consult", json=payload_high_score).json()["data"]
adm_high = res_high["admission_analysis"]
print(f"  • Tổng điểm thi: 25.0đ (>= 22.5)")
print(f"  • Mức ưu tiên gốc: {adm_high['base_priority']}đ (KV: {adm_high['area_priority']}đ + DTT: {adm_high['ethnicity_priority']}đ)")
print(f"  • Điểm ưu tiên sau công thức phân hóa: {adm_high['calculated_priority']}đ (Lý thuyết: 1.0đ)")
assert adm_high["calculated_priority"] == 1.0, f"Mong đợi 1.0đ nhưng nhận được {adm_high['calculated_priority']}đ"
print("  ✅ Công thức phân hóa điểm ưu tiên Bộ GD&ĐT hoạt động chính xác tuyệt đối!")

print("\n" + "=" * 70)
print("🎉 TẤT CẢ CÁC BÀI TEST TÍNH NĂNG MỚI ĐÃ VƯỢT QUA 100%!")
print("=" * 70)
