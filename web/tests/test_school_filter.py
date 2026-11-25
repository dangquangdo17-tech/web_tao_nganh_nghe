import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def test_target_school_filter():
    client = TestClient(app)

    print("==================================================")
    print("KIỂM THỬ TÍNH NĂNG CHỈ ĐỀ XUẤT NGÀNH CỦA TRƯỜNG ĐÃ CHỌN")
    print("==================================================")

    # 1. Test với trường BKHN
    print("\n--- 1. Kiểm tra với target_school = 'BKHN' ---")
    payload_bkhn = {
        "exam_scores": {"Toán": 8.5, "Vật lý": 8.0, "Hóa học": 8.0, "Ngữ văn": 7.5, "Tiếng Anh": 8.0},
        "target_school": "BKHN",
        "user_interest": "Em thích kỹ thuật phần mềm, trí tuệ nhân tạo",
        "priority_area": "KV1"
    }
    res_bkhn = client.post("/api/consult", json=payload_bkhn)
    assert res_bkhn.status_code == 200, f"Error: {res_bkhn.text}"
    data_bkhn = res_bkhn.json()["data"]
    top_recs_bkhn = data_bkhn["final_report"]["top_recommendations"]
    assert len(top_recs_bkhn) > 0, "No recommendations returned!"
    for r in top_recs_bkhn:
        print(f"  + NV: {r['major_name']} | Trường: {r['university_code']} ({r['university_name']}) | Điểm bạn: {r['candidate_score']} | Chuẩn: {r['score_2025']}")
        assert r["university_code"] == "BKHN", f"Expected BKHN but got {r['university_code']}!"
    print("==> BKHN PASS: 100% các ngành gợi ý đều thuộc BKHN! ✓")

    # 2. Test với trường PTIT
    print("\n--- 2. Kiểm tra với target_school = 'PTIT' ---")
    payload_ptit = {
        "exam_scores": {"Toán": 8.0, "Vật lý": 7.5, "Hóa học": 7.5, "Ngữ văn": 7.0, "Tiếng Anh": 8.0},
        "target_school": "PTIT",
        "user_interest": "Công nghệ thông tin",
        "priority_area": "KV2"
    }
    res_ptit = client.post("/api/consult", json=payload_ptit)
    assert res_ptit.status_code == 200
    top_recs_ptit = res_ptit.json()["data"]["final_report"]["top_recommendations"]
    assert len(top_recs_ptit) > 0
    for r in top_recs_ptit:
        print(f"  + NV: {r['major_name']} | Trường: {r['university_code']} ({r['university_name']})")
        assert r["university_code"] == "PTIT", f"Expected PTIT but got {r['university_code']}!"
    print("==> PTIT PASS: 100% các ngành gợi ý đều thuộc PTIT! ✓")

    # 3. Test với target_school = 'ALL' (Gợi ý mở rộng toàn quốc)
    print("\n--- 3. Kiểm tra với target_school = 'ALL' ---")
    payload_all = {
        "exam_scores": {"Toán": 8.0, "Vật lý": 7.5, "Hóa học": 7.5, "Ngữ văn": 7.0, "Tiếng Anh": 8.0},
        "target_school": "ALL",
        "user_interest": "Công nghệ thông tin"
    }
    res_all = client.post("/api/consult", json=payload_all)
    assert res_all.status_code == 200
    top_recs_all = res_all.json()["data"]["final_report"]["top_recommendations"]
    unis = {r["university_code"] for r in top_recs_all}
    print(f"  + Các trường xuất hiện khi chọn ALL: {unis}")
    assert len(unis) >= 1, "Should have recommendations"
    print("==> ALL PASS! ✓")

    print("\n>>> TẤT CẢ CÁC BÀI TEST LỌC ĐỀ XUẤT THEO TRƯỜNG ĐỀU THÀNH CÔNG RỰC RỠ! <<<")

if __name__ == "__main__":
    test_target_school_filter()
