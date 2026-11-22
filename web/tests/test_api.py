import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def test_api_endpoints():
    client = TestClient(app)

    print("--- 1. Kiểm tra GET /api/admission/rules ---")
    res = client.get("/api/admission/rules")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    rules_data = res.json()
    assert "templates" in rules_data
    assert "T1_STANDARD_30" in rules_data["templates"]
    assert "T3_SCALE_40" in rules_data["templates"]
    print("GET /api/admission/rules PASS! ✓")

    print("--- 2. Kiểm tra GET /api/admission/rules/HANU ---")
    res_hanu = client.get("/api/admission/rules/HANU")
    assert res_hanu.status_code == 200
    assert res_hanu.json()["status"] == "success"
    print("GET /api/admission/rules/HANU PASS! ✓")

    print("--- 3. Kiểm tra POST /api/school-check cho HANU ---")
    payload_hanu = {
        "school_code": "HANU",
        "exam_scores": {"Toán": 8.0, "Ngữ văn": 8.5, "Tiếng Anh": 9.0},
        "transcript_gpa": 8.2,
        "priority_area": "KV1",
        "ethnicity": "kinh"
    }
    res_check = client.post("/api/school-check", json=payload_hanu)
    assert res_check.status_code == 200, f"Expected 200, got {res_check.status_code}"
    data = res_check.json()
    assert data["status"] == "success"
    assert "tiers" in data
    safe_comp_risk = data["tiers"]["safe"] + data["tiers"]["competitive"] + data["tiers"]["risky"]
    assert len(safe_comp_risk) > 0
    # Check that language major is on scale 40
    lang_majors = [m for m in safe_comp_risk if m["major_code"] in ["SOC-ENG", "SOC-CHINESE", "SOC-KOREAN", "SOC-JAPANESE"]]
    assert len(lang_majors) > 0
    for lm in lang_majors:
        assert lm["target_scale"] == 40.0, f"Expected scale 40, got {lm['target_scale']}"
    # Check that tourism is on scale 30
    tour_majors = [m for m in safe_comp_risk if m["major_code"] == "TOUR-HOSP"]
    if tour_majors:
        assert tour_majors[0]["target_scale"] == 30.0, f"Expected scale 30 for TOUR-HOSP, got {tour_majors[0]['target_scale']}"
    print("POST /api/school-check HANU PASS! ✓")

    print("--- 4. Kiểm tra POST /api/school-check cho HMU ---")
    payload_hmu = {
        "school_code": "HMU",
        "exam_scores": {"Toán": 9.2, "Hóa học": 9.0, "Sinh học": 9.4},
        "priority_area": "KV1"
    }
    res_hmu = client.post("/api/school-check", json=payload_hmu)
    assert res_hmu.status_code == 200
    data_hmu = res_hmu.json()
    assert data_hmu["status"] == "success"
    all_hmu = data_hmu["tiers"]["safe"] + data_hmu["tiers"]["competitive"] + data_hmu["tiers"]["risky"]
    for m in all_hmu:
        assert m["target_scale"] == 30.0
    print("POST /api/school-check HMU PASS! ✓")

    print("\n>>> TẤT CẢ API ĐÃ KIỂM THỬ THÀNH CÔNG VÀ CHẠY MƯỢT MÀ! <<<")

if __name__ == "__main__":
    test_api_endpoints()
