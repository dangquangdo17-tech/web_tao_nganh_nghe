from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from .state import CounselorState
from .academic_agent import AcademicAgent
from .psychology_agent import PsychologyAgent
from .admission_agent import AdmissionAgent
from ..database.db_manager import DatabaseManager
from ..career.career_guidance import get_career_guidance

def academic_node(state: CounselorState) -> Dict[str, Any]:
    analysis = AcademicAgent.analyze(state)
    return {"academic_analysis": analysis}

def psychology_node(state: CounselorState) -> Dict[str, Any]:
    analysis = PsychologyAgent.analyze(state)
    return {"psychology_analysis": analysis}

def admission_node(state: CounselorState) -> Dict[str, Any]:
    analysis = AdmissionAgent.analyze(state)
    return {"admission_analysis": analysis}

def synthesizer_node(state: CounselorState) -> Dict[str, Any]:
    academic = state.academic_analysis
    psychology = state.psychology_analysis
    admission = state.admission_analysis

    ranked_combos = academic.get("ranked_combinations", [])
    combo_names = [c["combination"] for c in ranked_combos] if ranked_combos else ["A00", "A01", "D01"]
    combo_score_map = {c["combination"]: c["total_score"] for c in ranked_combos}

    priority_pts = admission.get("calculated_priority", 0.0)
    ielts_advantages = {adv["university_code"]: adv["score_gain"] for adv in admission.get("ielts_advantages", [])}

    # Semantic similarity scores từ RAG HyDE
    semantic_matches = {m["major_code"]: m["similarity_score"] for m in psychology.get("semantic_major_matches", [])}
    domain_detected = psychology.get("domain_detected", "")
    top_matches = psychology.get("semantic_major_matches", [])
    top_matched_categories = {m["category"] for m in top_matches[:5]} if top_matches else set()

    empathy_summary = psychology.get("empathy_summary", {})
    negative_constraints = psychology.get("negative_constraints", {})
    excluded_majors = set(negative_constraints.get("excluded_majors", []))

    # Xác định bộ lọc Category thông minh
    query_category = state.target_category
    if query_category and query_category != "Tất cả":
        if top_matches and top_matches[0]["similarity_score"] >= 0.25:
            top_primary_cat = top_matches[0]["category"]
            if top_primary_cat != query_category:
                query_category = None

    if query_category == "Tất cả":
        query_category = None

    # Truy vấn cơ sở dữ liệu điểm chuẩn (hỗ trợ lọc theo vùng và học phí)
    target_tuition = getattr(state, "target_tuition", "Tất cả")
    benchmarks = DatabaseManager.search_benchmarks(
        combinations=combo_names,
        min_score=15.0,
        max_score=30.0,
        region=state.target_region,
        category=query_category,
        tuition_level=target_tuition
    )

    safety_list = []
    target_list = []
    reach_list = []

    for b in benchmarks:
        uni_code = b["university_code"]
        major_code = b["major_code"]
        major_cat = b["major_category"]
        combo = b["combination_code"]
        benchmark_score_2025 = b["score_2025"]

        # Lọc bỏ nếu ngành này nằm trong danh sách phủ định do người dùng ghét/không thích
        if major_code in excluded_majors:
            continue

        # Điểm cơ sở theo tổ hợp
        base_score = combo_score_map.get(combo, academic.get("top_score", 24.0))

        # Nếu trường có quy đổi IELTS và tổ hợp có Tiếng Anh (A01, D01, D07)
        ielts_boost = 0.0
        if combo in ["A01", "D01", "D07"] and uni_code in ielts_advantages:
            ielts_boost = ielts_advantages[uni_code]

        effective_candidate_score = round(base_score + priority_pts + ielts_boost, 2)
        score_delta = round(effective_candidate_score - benchmark_score_2025, 2)

        # Tính tỷ lệ đỗ dự đoán (Pass Probability)
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

        # Chỉ số phù hợp ngữ nghĩa (Semantic Match từ RAG HyDE)
        sem_score = semantic_matches.get(major_code, 0.05)
        cat_bonus = 0.25 if (major_cat in top_matched_categories) else 0.0
        # Nếu danh mục hoàn toàn không liên quan đến nguyện vọng của học sinh, hạ thấp adjusted_sem
        if top_matched_categories and major_cat not in top_matched_categories and sem_score <= 0.15:
            adjusted_sem = 0.05
        else:
            adjusted_sem = min(1.0, sem_score + cat_bonus)

        # Tính chỉ số phù hợp tổng thể (Overall Fit Index)
        overall_fit_index = round(min(99.0, adjusted_sem * 100 * 0.65 + pass_prob * 0.35), 1)

        # Lấy thông tin hướng nghiệp chuyên sâu và tạo Explainable AI
        career_info = get_career_guidance(major_code, b["major_name"], major_cat)

        tier_badge = (
            "Thử thách (Ước mơ)" if pass_prob < 60
            else "Vừa sức (Mục tiêu cốt lõi)" if pass_prob < 90
            else "An toàn (Chắc đỗ)"
        )
        delta_str = f"+{score_delta:.2f}đ" if score_delta >= 0 else f"{score_delta:.2f}đ"
        ai_exp = (
            f"Đề xuất ngành {b['major_name']} tại {b['university_name']} ({uni_code}) vì điểm xét tuyển "
            f"của bạn ({effective_candidate_score:.2f}đ) thuộc nhóm {tier_badge} so với điểm chuẩn 2025 "
            f"({benchmark_score_2025:.2f}đ, chênh lệch {delta_str}). Lựa chọn này tối ưu hóa điểm số tổ hợp "
            f"{combo} và rất phù hợp với mã tính cách RIASEC {b['holland_code']} của bạn."
        )

        # Xác định Hệ Đào Tạo (Program Type)
        major_name_lower = b["major_name"].lower()
        sub_criteria_lower = (b.get("sub_criteria") or "").lower()
        if any(w in major_name_lower or w in sub_criteria_lower for w in ["chất lượng cao", "clc", "tiên tiến"]):
            prog_type = "Chất lượng cao (CLC)"
        elif uni_code in ["RMIT", "BUV"]:
            prog_type = "Hệ Quốc tế (100% tiếng Anh)"
        elif uni_code in ["FPT"] or "liên kết" in major_name_lower or "quốc tế" in major_name_lower:
            prog_type = "Hệ Tiên tiến / Quốc tế"
        else:
            prog_type = "Hệ Chuẩn (Đại trà)"

        # Kiểm tra cảnh báo học phí (Tuition Alert)
        t_val = DatabaseManager._parse_tuition_min(b.get("tuition_range"))
        is_tuition_alert = False
        tuition_alert_msg = ""
        if target_tuition == "under_20" and t_val > 20:
            is_tuition_alert = True
            tuition_alert_msg = f"Học phí trường này ({b.get('tuition_range', '')} tr/năm) vượt mức ngân sách tiết kiệm (< 20 tr/năm) bạn chọn."
        elif target_tuition == "20_40" and t_val > 40:
            is_tuition_alert = True
            tuition_alert_msg = f"Học phí trường này ({b.get('tuition_range', '')} tr/năm) vượt mức tiêu chuẩn (20 - 40 tr/năm) bạn chọn."
        elif t_val >= 40:
            is_tuition_alert = True
            tuition_alert_msg = f"Học phí trường này thuộc phân khúc cao ({b.get('tuition_range', '')} tr/năm, {prog_type}). Cần cân nhắc kỹ điều kiện tài chính gia đình."

        entry = {
            "benchmark_id": b["benchmark_id"],
            "university_code": b["university_code"],
            "university_name": b["university_name"],
            "university_region": b["region"],
            "university_province": b["province"],
            "tuition_range": b["tuition_range"],
            "program_type": prog_type,
            "is_tuition_alert": is_tuition_alert,
            "tuition_alert_msg": tuition_alert_msg,
            "website": b["website"],
            "major_code": b["major_code"],
            "major_name": b["major_name"],
            "major_category": b["major_category"],
            "combination_code": combo,
            "score_2023": b["score_2023"],
            "score_2024": b["score_2024"],
            "score_2025": b["score_2025"],
            "candidate_score": effective_candidate_score,
            "base_score": base_score,
            "priority_pts": priority_pts,
            "ielts_boost": ielts_boost,
            "score_delta": score_delta,
            "pass_probability": pass_prob,
            "semantic_score": round(adjusted_sem * 100, 1),
            "overall_fit_index": overall_fit_index,
            "sub_criteria": b["sub_criteria"],
            "career_prospects": b["career_prospects"],
            "career_guidance": career_info,
            "ai_explanation": ai_exp
        }

        # Phân loại vào 3 nhóm
        if pass_prob >= 90:
            safety_list.append(entry)
        elif pass_prob >= 60:
            target_list.append(entry)
        else:
            reach_list.append(entry)

    # Sắp xếp từng nhóm theo overall_fit_index giảm dần
    safety_list.sort(key=lambda x: x["overall_fit_index"], reverse=True)
    target_list.sort(key=lambda x: x["overall_fit_index"], reverse=True)
    reach_list.sort(key=lambda x: x["overall_fit_index"], reverse=True)

    # =========================================================================
    # CHIẾN LƯỢC TỶ LỆ VÀNG (20% Thử thách - 50% Phù hợp - 30% An toàn)
    # Tổng hợp danh sách Top 10 Nguyện Vọng tối ưu
    # =========================================================================
    top_recommendations = []
    used_keys = set()

    def add_rec(cand, role):
        cand_key = f"{cand['university_code']}_{cand['major_code']}_{cand['combination_code']}"
        if cand_key not in used_keys:
            top_recommendations.append({**cand, "strategy_role": role})
            used_keys.add(cand_key)
            return True
        return False

    # 1. 20% Thử thách (Ước mơ): 2 nguyện vọng đầu tiên (NV1, NV2)
    for i, item in enumerate(reach_list[:2]):
        add_rec(item, f"Nguyện vọng {len(top_recommendations)+1} (Ước mơ / Thử thách)")

    # 2. 50% Vừa sức / Phù hợp: 5 nguyện vọng trọng tâm (NV3 -> NV7)
    for i, item in enumerate(target_list[:5]):
        add_rec(item, f"Nguyện vọng {len(top_recommendations)+1} (Mục tiêu cốt lõi / Vừa sức)")

    # 3. 30% An toàn / Chắc đỗ: 3 nguyện vọng bảo hiểm (NV8 -> NV10)
    for i, item in enumerate(safety_list[:3]):
        add_rec(item, f"Nguyện vọng {len(top_recommendations)+1} (Bảo hiểm an toàn chắc đỗ)")

    # Nếu bất kỳ nhóm nào chưa đủ để đạt 10 nguyện vọng, bổ sung thông minh từ các ứng viên còn lại
    all_sorted = sorted(safety_list + target_list + reach_list, key=lambda x: x["overall_fit_index"], reverse=True)
    for cand in all_sorted:
        if len(top_recommendations) >= 10:
            break
        cand_key = f"{cand['university_code']}_{cand['major_code']}_{cand['combination_code']}"
        if cand_key not in used_keys:
            prob = cand["pass_probability"]
            role_type = "Ước mơ" if prob < 60 else "Vừa sức" if prob < 90 else "An toàn"
            add_rec(cand, f"Nguyện vọng {len(top_recommendations)+1} ({role_type} tiềm năng)")

    user_q = (state.user_interest or "").strip()
    q_preview = f"'{user_q}'" if len(user_q) < 60 else f"'{user_q[:57]}...'"
    final_report = {
        "summary": (
            f"Hội đồng tư vấn đã hoàn tất bản chiến lược tuyển sinh & nghề nghiệp cho câu hỏi: **{q_preview}**.\n\n"
            f"• **Thế mạnh học thuật:** Điểm cao nhất ở tổ hợp **{academic.get('top_combination')} ({academic.get('top_score')}đ)**, "
            f"với môn dẫn đầu **{academic.get('strongest_subject', ('Toán', 7))[0]}** đạt {academic.get('strongest_subject', ('Toán', 7))[1]}đ.\n"
            f"• **Định hướng nghề nghiệp & Tính cách:** Xác định bạn thuộc nhóm **{psychology.get('dominant_type')}** "
            f"(Mã RIASEC: **{psychology.get('primary_code')}**), thấu hiểu sở thích qua bức chân dung năng lực tương lai.\n"
            f"• **Chiến lược Tỷ Lệ Vàng:** Đã cơ cấu danh sách 10 Nguyện Vọng tối ưu gồm **20% Thử thách** (ước mơ), "
            f"**50% Vừa sức** (trọng tâm) và **30% An toàn** (chắc đỗ), đảm bảo bạn vừa chạm tới trường mơ ước vừa có bảo hiểm tuyệt đối."
        ),
        "empathy_summary": empathy_summary,
        "negative_constraints": negative_constraints,
        "top_recommendations": top_recommendations,
        "counts": {
            "safety": len(safety_list),
            "target": len(target_list),
            "reach": len(reach_list)
        }
    }

    return {
        "safety_majors": safety_list,
        "target_majors": target_list,
        "reach_majors": reach_list,
        "empathy_summary": empathy_summary,
        "final_report": final_report
    }

def create_counselor_graph():
    """
    Xây dựng đồ thị LangGraph điều phối Hội đồng Tư vấn Tuyển sinh Đa tác tử.
    """
    graph = StateGraph(CounselorState)

    graph.add_node("academic_agent", academic_node)
    graph.add_node("psychology_agent", psychology_node)
    graph.add_node("admission_agent", admission_node)
    graph.add_node("synthesizer", synthesizer_node)

    # Luồng thực thi song song hoặc tuần tự:
    # START -> academic_agent -> psychology_agent -> admission_agent -> synthesizer -> END
    graph.add_edge(START, "academic_agent")
    graph.add_edge("academic_agent", "psychology_agent")
    graph.add_edge("psychology_agent", "admission_agent")
    graph.add_edge("admission_agent", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()

# Khởi tạo instance của compiled graph
counselor_graph_app = create_counselor_graph()
