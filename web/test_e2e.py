import sys
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi.testclient import TestClient
from app.main import app
from app.rag.vector_store import vector_store_instance
from app.slm.prospectus_parser import SLMProspectusParser
from app.agents.graph import counselor_graph_app
from app.agents.state import CounselorState

client = TestClient(app)

def test_1_hyde_and_vector_rag():
    print("\n--- [TEST 1] Vector RAG & HyDE Engine ---")
    query = "Em thích làm việc với máy tính nhưng điểm toán chỉ dự đoán khoảng 7"
    res = vector_store_instance.search_with_hyde(query, top_k=3)
    
    assert "hypothetical_document" in res, "HyDE document generation failed!"
    assert len(res["top_matches"]) > 0, "No major matches found!"
    print("✅ HyDE Query:", query)
    print("✅ Generated Hypothetical Document preview:", res["hypothetical_document"][:100], "...")
    print("✅ Top 1 Match:", res["top_matches"][0]["major_name"], "Score:", res["top_matches"][0]["similarity_score"])
    assert "Phần mềm" in res["top_matches"][0]["major_name"] or "Máy tính" in res["top_matches"][0]["major_name"]

def test_2_slm_prospectus_parser():
    print("\n--- [TEST 2] SLM Prospectus Parser ---")
    sample_text = """Đề án tuyển sinh Đại học Bách khoa Hà Nội 2025:
Phương thức 1: Xét tuyển theo điểm thi tốt nghiệp THPT năm 2025.
Phương thức 2: Xét tuyển theo kết quả Kỳ thi Đánh giá tư duy.
Quy chế quy đổi chứng chỉ Ngoại ngữ: IELTS 5.0 quy đổi 8.0; IELTS 6.0 quy đổi 9.0; IELTS 6.5 quy đổi 9.5; IELTS 7.0 trở lên quy đổi 10.0.
Tiêu chí phụ: Ưu tiên điểm môn Toán trong tổ hợp xét tuyển khi hòa điểm."""
    
    parsed = SLMProspectusParser.parse_prospectus(sample_text, "BKHN")
    assert len(parsed["admission_methods"]) >= 2, "Failed to extract admission methods!"
    assert "IELTS 6.5" in parsed["ielts_conversion"], "Failed to extract IELTS 6.5 conversion!"
    assert parsed["ielts_conversion"]["IELTS 6.5"] == 9.5, "IELTS 6.5 conversion score mismatch!"
    print("✅ Extracted Methods:", [m["raw_text"] for m in parsed["admission_methods"]])
    print("✅ Extracted IELTS Mapping:", parsed["ielts_conversion"])
    print("✅ Extracted Sub-criteria:", parsed["sub_criteria"])

def test_3_langgraph_multi_agent_pipeline():
    print("\n--- [TEST 3] Multi-Agent LangGraph Pipeline ---")
    input_state = CounselorState(
        exam_scores={
            "Toán": 7.2,
            "Ngữ văn": 7.0,
            "Tiếng Anh": 7.8,
            "Vật lý": 7.5,
            "Hóa học": 6.5,
            "Sinh học": 6.0
        },
        transcript_scores={"Toán": 7.8, "Tiếng Anh": 8.0},
        user_interest="Em thích làm việc với máy tính nhưng điểm toán chỉ dự đoán khoảng 7",
        ielts_score=6.5,
        priority_area="KV2-NT"
    )
    
    result = counselor_graph_app.invoke(input_state)
    
    assert "academic_analysis" in result
    assert "psychology_analysis" in result
    assert "admission_analysis" in result
    assert "safety_majors" in result
    assert "target_majors" in result
    assert "reach_majors" in result
    
    print("✅ Academic Top Combo:", result["academic_analysis"]["top_combination"], "Score:", result["academic_analysis"]["top_score"])
    print("✅ Psychology RIASEC:", result["psychology_analysis"]["primary_code"])
    print("✅ Admission Priority Added:", result["admission_analysis"]["calculated_priority"])
    print("✅ 3-Tier Counts: Safety =", len(result["safety_majors"]), ", Target =", len(result["target_majors"]), ", Reach =", len(result["reach_majors"]))
    print("✅ Top 5 Recommendations generated:", len(result["final_report"]["top_recommendations"]))

def test_4_fastapi_endpoints():
    print("\n--- [TEST 4] FastAPI REST Endpoints ---")
    
    # Test /api/holland-questions
    res_q = client.get("/api/holland-questions")
    assert res_q.status_code == 200
    assert len(res_q.json()["data"]) == 6
    print("✅ GET /api/holland-questions passed (6 questions)")

    # Test /api/consult
    payload = {
        "exam_scores": {"Toán": 8.0, "Ngữ văn": 8.0, "Tiếng Anh": 8.5},
        "transcript_scores": {"Toán": 8.2},
        "user_interest": "Em thích kinh doanh quốc tế và ngoại ngữ",
        "ielts_score": 6.5,
        "priority_area": "KV3",
        "target_region": "Tất cả",
        "target_category": "Tất cả"
    }
    # Test /api/consult với Dân tộc thiểu số (+1.0đ)
    payload_minority = {
        "exam_scores": {"Toán": 8.0, "Ngữ văn": 8.0, "Tiếng Anh": 8.5},
        "transcript_scores": {"Toán": 8.2},
        "user_interest": "Em thích kinh doanh quốc tế và ngoại ngữ",
        "ielts_score": 6.5,
        "priority_area": "KV3",
        "ethnicity": "minority",
        "target_region": "Tất cả",
        "target_category": "Tất cả"
    }
    res_m = client.post("/api/consult", json=payload_minority)
    assert res_m.status_code == 200
    adm = res_m.json()["data"]["admission_analysis"]
    assert adm["ethnicity_priority"] == 1.0, "Ethnicity priority mismatch!"
    print("✅ POST /api/consult with minority ethnicity passed (ethnicity_priority = +1.0đ)")

def test_5_subject_selection_and_ethnicity_priority():
    print("\n--- [TEST 5] Subject Selection & Ethnicity Priority ---")
    # Kiểm tra chỉ 4 môn thi
    scores_4_subs = {"Toán": 7.5, "Ngữ văn": 7.0, "Tiếng Anh": 8.0, "Vật lý": 7.5}
    state = CounselorState(
        exam_scores=scores_4_subs,
        priority_area="KV1",
        ethnicity="minority"
    )
    result = counselor_graph_app.invoke(state)
    combos = [c["combination"] for c in result["academic_analysis"]["ranked_combinations"]]
    assert "A01" in combos and "D01" in combos
    assert "A00" not in combos and "B00" not in combos
    assert result["admission_analysis"]["ethnicity_priority"] == 1.0
    assert result["admission_analysis"]["area_priority"] == 0.75
    print("✅ Subject filtering verified (Only A01, D01 evaluated)")
    print("✅ Combined priority (KV1 0.75đ + DTT 1.0đ = 1.75đ) verified")

if __name__ == "__main__":
    test_1_hyde_and_vector_rag()
    test_2_slm_prospectus_parser()
    test_3_langgraph_multi_agent_pipeline()
    test_4_fastapi_endpoints()
    test_5_subject_selection_and_ethnicity_priority()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! 🚀")

