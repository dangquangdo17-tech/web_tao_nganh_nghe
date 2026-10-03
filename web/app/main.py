import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .database.schema import init_db
from .database.seed_data import seed_database
from .database.db_manager import DatabaseManager
from .rag.vector_store import vector_store_instance
from .slm.prospectus_parser import SLMProspectusParser
from .slm.school_evaluator import SchoolEvaluator
from .agents.state import CounselorState
from .agents.graph import counselor_graph_app

# Đảm bảo CSDL được khởi tạo và nạp dữ liệu
init_db()
seed_database()

app = FastAPI(
    title="Trợ lý RAG & Đa Tác Tử Tư Vấn Tuyển Sinh Đại Học",
    description="Hệ thống tư vấn chọn ngành, chọn trường dựa trên điểm thi tốt nghiệp, học lực, RAG HyDE và Multi-Agent LangGraph.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.middleware.base import BaseHTTPMiddleware
class NoCacheStaticMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.endswith((".js", ".css", ".html")) or request.url.path == "/":
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheStaticMiddleware)

# 1. Endpoint Tư Vấn Tuyển Sinh Đa Tác Tử Toàn Diện (Multi-Agent Admission Pipeline)
@app.post("/api/consult")
async def consult_admission(state: CounselorState):
    try:
        # Thực thi đồ thị LangGraph
        result = counselor_graph_app.invoke(state)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 2. Endpoint Khám phá Ngành Nghề với RAG & HyDE
class HyDEQueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/api/hyde-search")
async def search_hyde(req: HyDEQueryRequest):
    try:
        res = vector_store_instance.search_with_hyde(user_query=req.query, top_k=req.top_k)
        return {
            "status": "success",
            "data": res
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Endpoint SLM Phân tích Đề án Tuyển sinh
class ProspectusParseRequest(BaseModel):
    text: str
    university_code: Optional[str] = ""

@app.post("/api/prospectus/parse")
async def parse_prospectus(req: ProspectusParseRequest):
    try:
        parsed = SLMProspectusParser.parse_prospectus(req.text, req.university_code or "")
        return {
            "status": "success",
            "data": parsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Endpoint Lấy danh sách trường và đề án mẫu
@app.get("/api/universities")
async def get_universities(region: Optional[str] = None):
    try:
        unis = DatabaseManager.get_all_universities(region=region)
        return {
            "status": "success",
            "data": unis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/prospectus/{uni_code}")
async def get_university_prospectus(uni_code: str):
    p = DatabaseManager.get_prospectus(uni_code.upper())
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề án tuyển sinh cho trường này.")
    return {
        "status": "success",
        "data": p
    }

# 4b. Thẩm định & Phỏng vấn Chuyên sâu theo Trường Đại học Mơ ước
class SchoolCheckRequest(BaseModel):
    school_code: str
    exam_scores: Dict[str, float]
    transcript_gpa: Optional[float] = 7.5
    ielts_score: Optional[float] = None
    tsa_score: Optional[float] = None
    apt_score: Optional[float] = None
    hsa_score: Optional[float] = None
    priority_area: Optional[str] = "KV3"
    ethnicity: Optional[str] = "kinh"

@app.post("/api/school-check")
async def evaluate_school(req: SchoolCheckRequest):
    try:
        res = SchoolEvaluator.evaluate_school_admission(
            school_code=req.school_code,
            exam_scores=req.exam_scores,
            transcript_gpa=req.transcript_gpa or 7.5,
            ielts_score=req.ielts_score,
            tsa_score=req.tsa_score,
            apt_score=req.apt_score,
            hsa_score=req.hsa_score,
            priority_area=req.priority_area or "KV3",
            ethnicity=req.ethnicity or "kinh"
        )
        return res
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/school-sample-score/{school_code}")
async def get_school_sample_score(school_code: str):
    try:
        sample = SchoolEvaluator.get_sample_score_for_school(school_code)
        persona = SchoolEvaluator.get_school_persona(school_code)
        return {
            "status": "success",
            "school_code": school_code,
            "sample_scores": sample,
            "persona": persona
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SchoolInterviewStartRequest(BaseModel):
    school_code: str
    student_data: Optional[Dict[str, Any]] = None
    target_major_code: Optional[str] = None

@app.post("/api/school-interview/start")
async def start_school_interview(req: SchoolInterviewStartRequest):
    try:
        session = SchoolEvaluator.start_mock_interview(
            school_code=req.school_code,
            student_data=req.student_data or {},
            target_major_code=req.target_major_code
        )
        return {
            "status": "success",
            "data": session
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

class SchoolInterviewTurnRequest(BaseModel):
    session_id: str
    school_code: str
    turn_index: int
    user_answer: str
    target_major_name: Optional[str] = "Ngành mục tiêu"

@app.post("/api/school-interview/turn")
async def process_school_interview_turn(req: SchoolInterviewTurnRequest):
    try:
        turn_res = SchoolEvaluator.process_interview_turn(
            session_id=req.session_id,
            school_code=req.school_code,
            turn_index=req.turn_index,
            user_answer=req.user_answer,
            target_major_name=req.target_major_name or "Ngành mục tiêu"
        )
        return {
            "status": "success",
            "data": turn_res
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 5. Bộ câu hỏi Trắc nghiệm Nhanh Holland RIASEC (6 câu tình huống)
@app.get("/api/holland-questions")
async def get_holland_questions():
    questions = [
        {
            "id": "q_r",
            "trait": "R",
            "title": "Nhóm Kỹ thuật - Thực tế (Realistic)",
            "scenario": "Trong một buổi hoạt động nhóm hoặc dự án trường học, bạn hứng thú nhất với việc:",
            "options": [
                {"text": "Tự tay lắp ráp mô hình phần cứng, đấu nối mạch điện tử, hoặc sửa chữa thiết bị hỏng.", "points": 15},
                {"text": "Ngồi quan sát người khác làm hoặc chỉ hứng thú khi có người hướng dẫn chi tiết.", "points": 5}
            ]
        },
        {
            "id": "q_i",
            "trait": "I",
            "title": "Nhóm Nghiên cứu - Trí tuệ (Investigative)",
            "scenario": "Khi gặp một hiện tượng khó hiểu hoặc bài toán hóc búa, xu hướng tự nhiên của bạn là:",
            "options": [
                {"text": "Đào sâu tìm hiểu nguyên nhân gốc rễ, đọc tài liệu chuyên sâu hoặc mày mò tìm giải thuật tối ưu.", "points": 15},
                {"text": "Chờ xem đáp án hoặc hỏi người khác cho nhanh để đỡ mất thời gian.", "points": 5}
            ]
        },
        {
            "id": "q_a",
            "trait": "A",
            "title": "Nhóm Nghệ thuật - Sáng tạo (Artistic)",
            "scenario": "Khi chuẩn bị một bài thuyết trình hoặc sản phẩm truyền thông, bạn quan tâm nhất đến:",
            "options": [
                {"text": "Thiết kế slide bắt mắt, chọn phối màu ấn tượng, sáng tạo nội dung độc đáo và kể chuyện lôi cuốn.", "points": 15},
                {"text": "Chỉ cần đủ chữ và thông tin cần thiết, không quá câu nệ về mặt hình thức thẩm mỹ.", "points": 5}
            ]
        },
        {
            "id": "q_s",
            "trait": "S",
            "title": "Nhóm Xã hội - Giúp đỡ (Social)",
            "scenario": "Khi bạn bè trong lớp gặp khúc mắc trong học tập hoặc áp lực tâm lý:",
            "options": [
                {"text": "Sẵn sàng dành hàng giờ để lắng nghe, an ủi, hướng dẫn giảng giải bài tập và hỗ trợ bạn bè.", "points": 15},
                {"text": "Cảm thấy ái ngại và thường để bạn tự giải quyết vấn đề cá nhân.", "points": 5}
            ]
        },
        {
            "id": "q_e",
            "trait": "E",
            "title": "Nhóm Quản trị - Lãnh đạo (Enterprising)",
            "scenario": "Nếu trường tổ chức hội chợ kinh doanh hoặc cuộc thi khởi nghiệp học sinh:",
            "options": [
                {"text": "Xung phong làm nhóm trưởng, lên kế hoạch kinh doanh, phân chia nhiệm vụ và đàm phán bán hàng.", "points": 15},
                {"text": "Thích làm thành viên thực thi chỉ đâu đánh đó, không muốn chịu trách nhiệm lãnh đạo.", "points": 5}
            ]
        },
        {
            "id": "q_c",
            "trait": "C",
            "title": "Nhóm Nghiệp vụ - Quy củ (Conventional)",
            "scenario": "Trong thói quen quản lý đồ đạc, lịch trình và bảng số liệu:",
            "options": [
                {"text": "Rất cẩn thận, thích lập danh sách việc cần làm rõ ràng, ghi chép thu chi chi tiết và tuân thủ kỷ luật.", "points": 15},
                {"text": "Thích làm việc tùy hứng, linh hoạt theo cảm xúc, ít khi lập kế hoạch chi tiết.", "points": 5}
            ]
        }
    ]
    return {
        "status": "success",
        "data": questions
    }

# 6. Endpoint Tra Cứu & Đánh Giá Trường Mơ Ước (Dream University Evaluation)
class DreamMajorEvaluationRequest(BaseModel):
    keyword: str
    user_interest: Optional[str] = ""
    exam_scores: Dict[str, float]
    transcript_scores: Optional[Dict[str, float]] = None
    ielts_score: Optional[float] = None
    priority_area: Optional[str] = "KV3"
    ethnicity: Optional[str] = "kinh"

@app.post("/api/evaluate-dream-major")
async def evaluate_dream_major(req: DreamMajorEvaluationRequest):
    try:
        import re
        from .agents.academic_agent import AcademicAgent
        from .agents.admission_agent import AdmissionAgent
        from .career.career_guidance import get_career_guidance

        search_kw = req.keyword.strip() if req.keyword else ""
        user_interest = req.user_interest.strip() if req.user_interest else ""

        # 1. Tính toán độ tương đồng với mô tả sở thích (HyDE Vector RAG)
        sem_map = {}
        top_categories = set()
        top_major_codes = []
        if user_interest:
            try:
                hyde_res = vector_store_instance.search_with_hyde(user_interest, top_k=15)
                sem_map = {m["major_code"]: m["similarity_score"] for m in hyde_res.get("top_matches", [])}
                top_categories = {m["category"] for m in hyde_res.get("top_matches", [])[:3]}
                top_major_codes = [m["major_code"] for m in hyde_res.get("top_matches", []) if m.get("similarity_score", 0) >= 0.20]
                if not top_major_codes:
                    top_major_codes = [m["major_code"] for m in hyde_res.get("top_matches", [])[:4]]
            except Exception as ex:
                print("HyDE search in dream university error:", ex)

        # 2. Tìm kiếm điểm chuẩn theo từ khóa trường/ngành hoặc theo top mã ngành sở thích
        benchmarks = []
        if search_kw:
            benchmarks = DatabaseManager.search_dream_benchmarks(keyword=search_kw, limit=35)
        
        if not benchmarks and top_major_codes:
            benchmarks = DatabaseManager.search_dream_benchmarks(major_codes=top_major_codes, limit=35)

        if not benchmarks and not search_kw:
            benchmarks = DatabaseManager.search_dream_benchmarks(limit=35)

        if not benchmarks:
            return {
                "status": "success",
                "data": {
                    "keyword": req.keyword,
                    "user_interest": user_interest,
                    "matches": []
                }
            }

        # 2. Chuẩn hóa điểm thi
        std_scores = AcademicAgent._standardize_subject_scores(req.exam_scores or {})
        ielts = req.ielts_score
        raw_english = float(std_scores.get("Tiếng Anh", 7.0))

        # Khảo sát quy đổi IELTS của các trường
        prospectuses = {p["university_code"]: p for p in DatabaseManager.get_all_prospectuses(year=2025)}

        evaluated = []
        u_int_lower = user_interest.lower()

        for b in benchmarks:
            uni_code = b["university_code"]
            combo = b["combination_code"]
            combo_subjects = AcademicAgent.COMBINATION_MAPPINGS.get(combo, ["Toán", "Vật lý", "Hóa học"])

            # Kiểm tra thí sinh có thi đủ tổ hợp này không
            has_all_subjects = all(s in std_scores for s in combo_subjects)
            missing_subjects = [s for s in combo_subjects if s not in std_scores]

            if has_all_subjects:
                base_score = sum(std_scores[s] for s in combo_subjects)
            else:
                existing = [std_scores[s] for s in combo_subjects if s in std_scores]
                avg_val = (sum(std_scores.values()) / len(std_scores)) if std_scores else 7.0
                base_score = sum(existing) + avg_val * len(missing_subjects)

            # Tính điểm ưu tiên
            priority_info = AdmissionAgent.calculate_ministry_priority_score(
                base_score, req.priority_area or "KV3", req.ethnicity or "kinh"
            )
            priority_pts = priority_info["scaled_priority"]

            # IELTS Boost
            ielts_boost = 0.0
            if ielts and ielts >= 5.0 and combo in ["A01", "D01", "D07"]:
                p_rule = prospectuses.get(uni_code)
                if p_rule and p_rule.get("ielts_conversion_map"):
                    conv_score = SLMProspectusParser.calculate_converted_score(ielts, p_rule["ielts_conversion_map"])
                    gain = conv_score - raw_english
                    if gain > 0:
                        ielts_boost = round(gain, 2)

            effective_score = round(base_score + priority_pts + ielts_boost, 2)
            benchmark_2025 = b["score_2025"]
            score_delta = round(effective_score - benchmark_2025, 2)

            # Tính tỷ lệ đỗ
            if score_delta >= 2.0:
                pass_prob = min(98, round(92 + (score_delta - 2.0) * 2, 1))
            elif score_delta >= 1.5:
                pass_prob = round(90 + (score_delta - 1.5) * 4, 1)
            elif score_delta >= 0.0:
                pass_prob = round(70 + score_delta * 13.3, 1)
            elif score_delta >= -0.5:
                pass_prob = round(60 + (score_delta + 0.5) * 20, 1)
            elif score_delta >= -1.5:
                pass_prob = max(15, round(45 + (score_delta + 0.5) * 30, 1))
            else:
                pass_prob = max(5, round(15 - abs(score_delta + 1.5) * 5, 1))

            if pass_prob >= 90:
                tier_role = "An toàn (Chắc đỗ)"
                badge_class = "safety"
                advice = f"Điểm của bạn ({effective_score}đ) vượt ngưỡng an toàn so với điểm chuẩn 2025 (+{score_delta}đ). Bạn có thể tự tin đặt làm NV1 hoặc NV mục tiêu chính!"
            elif pass_prob >= 60:
                tier_role = "Vừa sức (Mục tiêu cốt lõi)"
                badge_class = "target"
                delta_str = f"+{score_delta}đ" if score_delta >= 0 else f"{score_delta}đ"
                advice = f"Điểm của bạn ({effective_score}đ) đang nằm sát ngưỡng chuẩn 2025 ({delta_str}). Rất nên đặt ở vị trí NV1 - NV3 trong lộ trình xét tuyển!"
            else:
                tier_role = "Thử thách (Ước mơ)"
                badge_class = "reach"
                gap = abs(score_delta)
                advice = f"Đây là nhóm Thử thách/Ước mơ (còn thiếu khoảng {gap:.2f} điểm để an toàn). Nên đặt ở NV1 hoặc NV2 để giữ cơ hội bứt phá, nhưng bắt buộc lót thêm các NV vừa sức phía sau!"

            # 3. Tính điểm ưu tiên sở thích nghề nghiệp (Interest Match)
            sem_score = sem_map.get(b["major_code"], 0.0)
            direct_word_match = False
            if u_int_lower:
                m_name_lower = b["major_name"].lower()
                words = [w for w in re.findall(r"[\w]+", m_name_lower) if len(w) > 2 and w not in ["ngành", "kỹ", "thuật", "học"]]
                direct_word_match = any(w in u_int_lower for w in words)
                if direct_word_match:
                    sem_score += 0.35
                if b["major_category"] in top_categories:
                    sem_score += 0.15

            is_interest_match = (sem_score >= 0.22) or direct_word_match

            if is_interest_match and user_interest:
                short_q = user_interest[:40] + "..." if len(user_interest) > 40 else user_interest
                advice = f"✨ <strong>Khớp với sở thích bạn mô tả:</strong> Ngành này rất đúng với nguyện vọng <em>'{short_q}'</em> của bạn. " + advice

            career_info = get_career_guidance(b["major_code"], b["major_name"], b["major_category"])

            evaluated.append({
                **b,
                "candidate_score": effective_score,
                "base_score": round(base_score, 2),
                "priority_pts": priority_pts,
                "ielts_boost": ielts_boost,
                "score_delta": score_delta,
                "pass_probability": pass_prob,
                "strategy_role": tier_role,
                "badge_class": badge_class,
                "has_all_subjects": has_all_subjects,
                "missing_subjects": missing_subjects,
                "is_interest_match": is_interest_match,
                "interest_match_score": round(sem_score, 3),
                "career_guidance": career_info,
                "strategic_advice": advice
            })

        # SẮP XẾP ƯU TIÊN: Các ngành khớp với sở thích nghề nghiệp của người dùng đứng ĐẦU TIÊN!
        evaluated.sort(
            key=lambda x: (
                1 if x["is_interest_match"] else 0,
                x["interest_match_score"],
                x["pass_probability"],
                x["score_2025"]
            ),
            reverse=True
        )

        return {
            "status": "success",
            "data": {
                "keyword": req.keyword,
                "user_interest": user_interest,
                "matches": evaluated[:15]
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 7. Endpoint Trợ Lý Chatbot Tư Vấn Ngữ Cảnh Tiếp Nối (Follow-up AI Chatbot)
class ChatFollowupRequest(BaseModel):
    message: str
    consultation_context: Optional[Dict[str, Any]] = None

@app.post("/api/chat-followup")
async def chat_followup(req: ChatFollowupRequest):
    try:
        from .agents.followup_agent import FollowupCounselor
        res = FollowupCounselor.answer_question(req.message, req.consultation_context)
        return {
            "status": "success",
            "data": res
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 8. Endpoint Mô Phỏng "Nếu - Thì" (What-if Analysis Simulation)
class WhatIfRequest(BaseModel):
    baseline_scores: Dict[str, float]
    delta_scores: Optional[Dict[str, float]] = None
    ielts_score: Optional[float] = None
    priority_area: Optional[str] = "KV3"
    ethnicity: Optional[str] = "kinh"
    current_recommendations: List[Dict[str, Any]] = []

@app.post("/api/simulate-what-if")
async def simulate_what_if(req: WhatIfRequest):
    try:
        from .agents.followup_agent import WhatIfSimulator
        res = WhatIfSimulator.simulate(
            baseline_scores=req.baseline_scores,
            delta_scores=req.delta_scores,
            ielts_score=req.ielts_score,
            priority_area=req.priority_area or "KV3",
            ethnicity=req.ethnicity or "kinh",
            recommendations=req.current_recommendations
        )
        return {
            "status": "success",
            "data": res
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 9. Endpoint Lấy Danh Mục Nghề Mục Tiêu (Reverse Career Mapping)
@app.get("/api/target-roles")
@app.get("/api/reverse-career-roles")
async def get_reverse_career_roles():
    try:
        from .career.career_guidance import get_all_target_roles
        roles = get_all_target_roles()
        return {"status": "success", "data": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/target-roles/{role_code}")
async def get_target_role_detail(role_code: str):
    try:
        from .career.career_guidance import CAREER_GUIDANCE_KNOWLEDGE_BASE
        if role_code in CAREER_GUIDANCE_KNOWLEDGE_BASE:
            item = CAREER_GUIDANCE_KNOWLEDGE_BASE[role_code]
            return {"status": "success", "data": item}
        raise HTTPException(status_code=404, detail=f"Không tìm thấy nghề mục tiêu với mã {role_code}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 10. Endpoint Tính Toán Học Phí & Hoàn Vốn Toàn Bộ Các Trường (Education ROI Calculator)
class EducationROIRequest(BaseModel):
    university_code: str
    major_code: Optional[str] = None
    major_name: Optional[str] = None
    city: Optional[str] = None
    living_city: Optional[str] = "Hà Nội"
    program_type: Optional[str] = "standard"
    study_years: Optional[float] = 4.0
    custom_tuition: Optional[float] = None
    custom_living_cost: Optional[float] = None
    custom_monthly_living: Optional[float] = None
    savings_rate: Optional[float] = 0.4
    scholarship_pct: Optional[float] = 0.0

@app.post("/api/education-roi/calculate")
async def calculate_roi_endpoint(req: EducationROIRequest):
    try:
        from .career.career_guidance import calculate_education_roi
        # Normalize program type
        pt = (req.program_type or "standard").lower().strip()
        if "quốc tế" in pt or "international" in pt:
            norm_pt = "international"
        elif "chất lượng cao" in pt or "clc" in pt or "high_quality" in pt:
            norm_pt = "high_quality"
        else:
            norm_pt = "standard"

        city_val = req.city or req.living_city or "Hà Nội"
        living_cost_val = req.custom_monthly_living if req.custom_monthly_living is not None else req.custom_living_cost

        res = calculate_education_roi(
            uni_code=req.university_code,
            major_code=req.major_code,
            living_city=city_val,
            program_type=norm_pt,
            study_years=req.study_years or 4.0,
            custom_tuition=req.custom_tuition,
            custom_living_cost=living_cost_val,
            savings_rate=req.savings_rate or 0.4,
            scholarship_pct=req.scholarship_pct or 0.0
        )
        return {"status": "success", "data": res}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 11. Endpoint Cầu Nối Đồng Thuận Gia Đình - Học Sinh (Parent & Student Alignment)
class AlignmentRequest(BaseModel):
    student_answers: Optional[Dict[str, Any]] = None
    parent_answers: Optional[Dict[str, Any]] = None
    student_scores: Optional[Dict[str, Any]] = None
    parent_scores: Optional[Dict[str, Any]] = None
    target_majors: Optional[List[str]] = []
    student_target_major: Optional[str] = None

@app.post("/api/parent-student-alignment")
async def parent_student_alignment_endpoint(req: AlignmentRequest):
    try:
        from .career.career_guidance import analyze_parent_student_alignment
        s_ans = req.student_scores or req.student_answers or {}
        p_ans = req.parent_scores or req.parent_answers or {}
        majors = req.target_majors or ([req.student_target_major] if req.student_target_major else [])

        res = analyze_parent_student_alignment(
            student_answers=s_ans,
            parent_answers=p_ans,
            target_majors=majors
        )
        return {"status": "success", "data": res}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 12. Endpoint So Sánh Đối Đầu 2 Ngành / 2 Trường (Head-to-Head Comparison)
class CompareMajorsRequest(BaseModel):
    major_code_a: Optional[str] = None
    university_code_a: Optional[str] = "BKHN"
    major_code_b: Optional[str] = None
    university_code_b: Optional[str] = "NEU"
    major_a_name: Optional[str] = None
    major_b_name: Optional[str] = None
    candidate_score: Optional[float] = 24.5

@app.post("/api/compare-majors")
async def compare_majors_endpoint(req: CompareMajorsRequest):
    try:
        name_a = req.major_a_name or req.major_code_a or "Công nghệ thông tin"
        name_b = req.major_b_name or req.major_code_b or "Quản trị kinh doanh"
        uni_a = req.university_code_a or "BKHN"
        uni_b = req.university_code_b or "NEU"

        bm_a = DatabaseManager.search_dream_benchmarks(keyword=name_a, limit=5)
        bm_b = DatabaseManager.search_dream_benchmarks(keyword=name_b, limit=5)

        first_bm_a = bm_a[0] if bm_a else {}
        first_bm_b = bm_b[0] if bm_b else {}

        code_a = req.major_code_a or first_bm_a.get("major_code", "IT-CS")
        code_b = req.major_code_b or first_bm_b.get("major_code", "ECO-BA")

        from .career.career_guidance import get_career_guidance, calculate_education_roi
        cg_a = get_career_guidance(code_a, name_a, first_bm_a.get("major_category", "Công nghệ"))
        cg_b = get_career_guidance(code_b, name_b, first_bm_b.get("major_category", "Kinh tế"))

        roi_a = calculate_education_roi(uni_a, code_a)
        roi_b = calculate_education_roi(uni_b, code_b)

        score_2025_a = first_bm_a.get("score_2025", 26.5)
        score_2025_b = first_bm_b.get("score_2025", 25.5)

        item_a = {
            "university_code": uni_a.upper(),
            "university_name": roi_a.get("university_name", f"Trường {uni_a}"),
            "major_code": code_a,
            "major_name": name_a,
            "major_category": first_bm_a.get("major_category", "Công nghệ thông tin"),
            "benchmark_2025": score_2025_a,
            "benchmark_2024": first_bm_a.get("score_2024", round(score_2025_a - 0.5, 2)),
            "benchmark_2023": first_bm_a.get("score_2023", round(score_2025_a - 0.8, 2)),
            "score_2023": first_bm_a.get("score_2023", round(score_2025_a - 0.8, 2)),
            "score_2024": first_bm_a.get("score_2024", round(score_2025_a - 0.5, 2)),
            "score_2025": score_2025_a,
            "tuition_annual": roi_a.get("annual_tuition", 30),
            "tuition_total_4y": roi_a.get("total_tuition", 120),
            "total_cost": roi_a.get("total_cost", 280),
            "payback_years": roi_a.get("payback_period_years", 3.5),
            "payback_period_years": roi_a.get("payback_period_years", 3.5),
            "starting_salary": cg_a.get("starting_salary", "12 - 18 tr/tháng"),
            "average_starting_salary": 14.5,
            "employment_rate": cg_a.get("employment_rate", 98.0),
            "english_exit_req": cg_a.get("english_exit_req", "IELTS 6.0"),
            "ai_risk": cg_a.get("ai_impact", {}).get("automation_risk_percent", 15),
            "ai_risk_pct": cg_a.get("ai_impact", {}).get("automation_risk_percent", 15),
            "ai_risk_level": cg_a.get("ai_impact", {}).get("risk_level", "Thấp")
        }

        item_b = {
            "university_code": uni_b.upper(),
            "university_name": roi_b.get("university_name", f"Trường {uni_b}"),
            "major_code": code_b,
            "major_name": name_b,
            "major_category": first_bm_b.get("major_category", "Kinh tế"),
            "benchmark_2025": score_2025_b,
            "benchmark_2024": first_bm_b.get("score_2024", round(score_2025_b - 0.4, 2)),
            "benchmark_2023": first_bm_b.get("score_2023", round(score_2025_b - 0.7, 2)),
            "score_2023": first_bm_b.get("score_2023", round(score_2025_b - 0.7, 2)),
            "score_2024": first_bm_b.get("score_2024", round(score_2025_b - 0.4, 2)),
            "score_2025": score_2025_b,
            "tuition_annual": roi_b.get("annual_tuition", 28),
            "tuition_total_4y": roi_b.get("total_tuition", 112),
            "total_cost": roi_b.get("total_cost", 270),
            "payback_years": roi_b.get("payback_period_years", 3.8),
            "payback_period_years": roi_b.get("payback_period_years", 3.8),
            "starting_salary": cg_b.get("starting_salary", "10 - 15 tr/tháng"),
            "average_starting_salary": 12.5,
            "employment_rate": cg_b.get("employment_rate", 96.5),
            "english_exit_req": cg_b.get("english_exit_req", "IELTS 6.0"),
            "ai_risk": cg_b.get("ai_impact", {}).get("automation_risk_percent", 35),
            "ai_risk_pct": cg_b.get("ai_impact", {}).get("automation_risk_percent", 35),
            "ai_risk_level": cg_b.get("ai_impact", {}).get("risk_level", "Trung bình")
        }

        cand_score = req.candidate_score or 24.5
        rec_advice = f"Với mức điểm dự kiến {cand_score}đ: "
        if cand_score >= score_2025_a:
            rec_advice += f"Bạn hoàn toàn đủ năng lực trúng tuyển vào {name_a} tại trường mục tiêu. Hãy đặt nguyện vọng 1!"
        elif cand_score >= score_2025_b:
            rec_advice += f"Ngành {name_b} là lựa chọn an toàn và vừa sức hơn, trong khi {name_a} có thể đặt làm nguyện vọng thử thách."
        else:
            rec_advice += f"Cả hai ngành đều đòi hỏi bạn cần nỗ lực bứt phá thêm từ 1 - 2 điểm trong kỳ thi sắp tới."

        comparison_summary = {
            "overview_summary": f"So sánh giữa {name_a} và {name_b}: {name_a} có thu nhập khởi điểm và tỷ lệ việc làm cao hơn, đồng thời rủi ro tự động hóa AI thấp hơn; {name_b} có phổ điểm chuẩn dễ tiếp cận hơn.",
            "recommended_choice_advice": rec_advice
        }

        return {
            "status": "success",
            "data": {
                "major_a": item_a,
                "major_b": item_b,
                "item_a": item_a,
                "item_b": item_b,
                "comparison": comparison_summary
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 13. Endpoint: Reality Check & Một Ngày Làm Nghề (15 Profiles)
@app.get("/api/reality-check-profiles")
def get_reality_check_profiles():
    try:
        from app.career.career_guidance import CAREER_GUIDANCE_KNOWLEDGE_BASE
        profiles = []
        name_map = {
            "IT-CS": "Khoa học Máy tính & Trí tuệ Nhân tạo (AI)",
            "IT-SE": "Kỹ thuật Phần mềm & Phát triển Ứng dụng",
            "IT-CYBER": "An toàn Thông tin & An ninh Mạng",
            "IT-DS": "Khoa học Dữ liệu & Phân tích Kinh doanh",
            "ENG-SEMI": "Thiết kế Vi mạch & Công nghệ Bán dẫn",
            "ENG-ROBOT": "Robotics & Kỹ thuật Tự động hóa",
            "ENG-AUTO": "Kỹ thuật Ô tô & Phương tiện Thông minh",
            "ENG-ARCH": "Kiến trúc Công trình & Quy hoạch Đô thị",
            "ECO-IB": "Kinh doanh Quốc tế & Đàm phán Thương mại",
            "ECO-LOG": "Quản lý Chuỗi Cung ứng & Logistics",
            "ECO-MKT": "Digital Marketing & Truyền thông Tương tác",
            "ECO-FIN": "Tài chính - Ngân hàng & Phân tích Đầu tư (CFA)",
            "MED-GP": "Bác sĩ Đa khoa & Y học Lâm sàng",
            "MED-PHARM": "Dược học & Nghiên cứu Dược phẩm",
            "DES-UIUX": "Thiết kế Giao diện & Trải nghiệm Người dùng (UI/UX)"
        }
        for code, data in CAREER_GUIDANCE_KNOWLEDGE_BASE.items():
            profiles.append({
                "code": code,
                "title": name_map.get(code, code),
                "entry_roles": data.get("entry_roles", []),
                "daily_work": data.get("daily_work", ""),
                "starting_salary": data.get("starting_salary", ""),
                "mid_salary": data.get("mid_salary", ""),
                "labor_market_outlook": data.get("labor_market_outlook", ""),
                "work_distribution": data.get("work_distribution", []),
                "pressure_challenges": data.get("pressure_challenges", []),
                "mini_case_study": data.get("mini_case_study", {}),
                "ai_impact": data.get("ai_impact", {}),
                "skill_sandbox": data.get("skill_sandbox", {})
            })
        return {"status": "success", "data": profiles}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 14. Serve Frontend Static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

