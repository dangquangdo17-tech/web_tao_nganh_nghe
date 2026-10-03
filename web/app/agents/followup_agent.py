# -*- coding: utf-8 -*-
import re
from typing import Dict, Any, List, Optional
from .academic_agent import AcademicAgent
from .admission_agent import AdmissionAgent
from ..database.db_manager import DatabaseManager
from ..career.career_guidance import get_career_guidance

class FollowupCounselor:
    """
    Trợ lý AI tư vấn tiếp nối (Contextual Follow-up Chatbot).
    Tiếp nhận câu hỏi của học sinh kèm toàn bộ ngữ cảnh hồ sơ, điểm số và danh sách nguyện vọng.
    """

    @staticmethod
    def answer_question(
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        msg_lower = (user_message or "").strip().lower()
        context = context or {}
        
        candidate = context.get("candidate_profile", {})
        recs = context.get("recommendations", [])
        dream_matches = context.get("dream_matches", [])
        
        scores = candidate.get("scores", {})
        holland_code = candidate.get("holland_code", "")
        user_interest = candidate.get("interest", "")
        ethnicity = candidate.get("ethnicity", "kinh")
        priority_area = candidate.get("priority_area", "KV3")
        ielts = candidate.get("ielts_score")
        
        # 1. Câu hỏi về học phí / trường chi phí thấp / kinh tế khó khăn
        if any(w in msg_lower for w in ["học phí", "chi phí", "tiền học", "kinh tế khó khăn", "nghèo", "rẻ", "thấp", "hạn hẹp", "học bổng"]):
            low_tuition_unis = []
            seen_unis = set()
            
            for r in recs + dream_matches:
                u_name = r.get("university_name", "")
                u_code = r.get("university_code", "")
                tuition = r.get("tuition_range", "Chưa rõ")
                if u_code and u_code not in seen_unis:
                    seen_unis.add(u_code)
                    # Phân tích mức học phí
                    if any(c in tuition for c in ["12", "14", "15", "16", "18", "20", "22", "25", "miễn", "0 tr"]):
                        low_tuition_unis.append(f"**{u_name} ({u_code})**: Khoảng {tuition}")
            
            reply = (
                "Chào bạn! Về vấn đề **học phí và tài chính gia đình**, EduCompass AI xin chia sẻ định hướng cụ thể như sau:\n\n"
                "### 1. Các trường trong lộ trình của bạn có mức học phí vừa phải (tiết kiệm):\n"
            )
            if low_tuition_unis:
                for u in low_tuition_unis[:5]:
                    reply += f"- {u}\n"
            else:
                reply += (
                    "- Các trường Đại học Công lập truyền thống (Đại học Bách Khoa, Sư phạm, Khoa học Tự nhiên, Kinh tế Quốc dân hệ đại trà) "
                    "thường có học phí từ **15 - 28 triệu VNĐ/năm**, thấp hơn đáng kể so với hệ quốc tế hoặc tư thục (40 - 100+ triệu VNĐ/năm).\n"
                )
            
            reply += (
                "\n### 2. Chính sách hỗ trợ tài chính đặc biệt:\n"
                "- **Khối Sư phạm:** Được miễn 100% học phí và nhận hỗ trợ sinh hoạt phí 3.63 triệu VNĐ/tháng theo Nghị định 116/2020/NĐ-CP.\n"
                "- **Học bổng Khuyến khích Học tập:** Hầu hết các trường công lập đều dành 8-10% nguồn thu học phí để cấp học bổng cho sinh viên đạt điểm cao (Khá, Giỏi, Xuất sắc).\n"
                "- **Vay vốn tín dụng học sinh - sinh viên:** Ngân hàng Chính sách Xã hội cho vay lãi suất ưu đãi lên tới 4 triệu VNĐ/tháng suốt quá trình học đại học.\n\n"
                "💡 **Lời khuyên chiến lược:** Nếu điều kiện kinh tế là ưu tiên số 1, hãy đặt các trường công lập học phí thấp ở nhóm **NV Vừa sức & An toàn (NV3 - NV6)** để đảm bảo chắc chắn trúng tuyển mà không phải lo lắng gánh nặng tài chính!"
            )
            return {"reply": reply, "topic": "tuition"}

        # 2. Câu hỏi tại sao nên / không nên nộp ngành này ở trường X
        if any(w in msg_lower for w in ["tại sao", "có nên", "không nên", "vì sao", "liệu có đỗ", "khả năng đỗ"]):
            # Tìm xem có nhắc đến trường hay ngành nào trong context không
            matched_rec = None
            for r in recs + dream_matches:
                u_code = r.get("university_code", "").lower()
                u_name = r.get("university_name", "").lower()
                m_name = r.get("major_name", "").lower()
                if (u_code and u_code in msg_lower) or (u_name and any(p in msg_lower for p in u_name.split() if len(p) > 3)) or (m_name and any(p in msg_lower for p in m_name.split() if len(p) > 3)):
                    matched_rec = r
                    break

            if matched_rec:
                u_name = matched_rec.get("university_name", "")
                m_name = matched_rec.get("major_name", "")
                cand_score = matched_rec.get("candidate_score", 0)
                bench_2025 = matched_rec.get("score_2025", 0)
                delta = matched_rec.get("score_delta", cand_score - bench_2025)
                prob = matched_rec.get("pass_probability", 50)
                role = matched_rec.get("strategy_role", "")
                advice = matched_rec.get("strategic_advice", "")

                reply = (
                    f"### Phân tích chi tiết: {m_name} tại {u_name}\n\n"
                    f"- **Điểm xét tuyển của bạn:** **{cand_score:.2f} điểm**\n"
                    f"- **Điểm chuẩn năm 2025:** **{bench_2025:.2f} điểm** (Chênh lệch: **{'+' if delta >= 0 else ''}{delta:.2f} điểm**)\n"
                    f"- **Khả năng trúng tuyển dự kiến:** **{prob}%** (Xếp loại: **{role}**)\n\n"
                    f"**Nhận định từ Hội đồng Cố vấn AI:**\n"
                )
                if delta >= 1.5:
                    reply += (
                        f"👉 **NÊN NỘP!** Điểm của bạn đang vượt ngưỡng an toàn (+{delta:.2f}đ). Bạn có thể rất tự tin đặt ngành này ở **NV1 hoặc NV mục tiêu chính**.\n"
                    )
                elif delta >= -0.5:
                    reply += (
                        f"👉 **RẤT NÊN CÂN NHẮC!** Điểm của bạn đang bám rất sát điểm chuẩn ({'+' if delta >= 0 else ''}{delta:.2f}đ). "
                        f"Đây là nguyện vọng **Vừa sức lý tưởng**, hãy đặt ở vị trí **NV2 hoặc NV3**.\n"
                    )
                else:
                    reply += (
                        f"👉 **CẦN THẬN TRỌNG!** Đây là nguyện vọng thuộc nhóm **Thử thách/Ước mơ** vì điểm của bạn đang thấp hơn điểm chuẩn {abs(delta):.2f} điểm. "
                        f"Bạn vẫn có thể đặt ở **NV1 hoặc NV2** để nắm bắt cơ hội bứt phá nếu đề thi phân hóa cao, nhưng **bắt buộc phải lót thêm ít nhất 2 nguyện vọng Vừa sức và An toàn** ở các vị trí NV3 - NV5 để tránh nguy cơ trượt đại học!\n"
                    )
                if advice:
                    # Bỏ bớt thẻ HTML nếu có
                    clean_advice = re.sub(r'<[^>]+>', '', advice)
                    reply += f"\n💡 *Chiến lược:* {clean_advice}"
                return {"reply": reply, "topic": "school_evaluation"}

        # 3. Câu hỏi so sánh 2 ngành hoặc hỏi ngành nào phù hợp
        if any(w in msg_lower for w in ["so sánh", "khác gì", "khác nhau", "nên chọn ngành nào", "phân vân"]):
            reply = (
                "### Phân Tích & So Sánh Ngành Học:\n\n"
                "Khi đứng trước sự phân vân giữa các ngành học, bạn cần cân nhắc trên 3 trục chính:\n\n"
                "1. **Bản chất công việc hằng ngày:**\n"
                "   - *Khối Kỹ thuật & Công nghệ (Khoa học máy tính, Vi mạch, Robot):* Đòi hỏi tư duy logic, toán học và kỹ năng giải quyết sự cố kỹ thuật kiên nhẫn trước màn hình hoặc thiết bị.\n"
                "   - *Khối Kinh tế & Vận hành (Logistics, Kinh doanh quốc tế, Marketing):* Tập trung vào kỹ năng giao tiếp, tổ chức chuỗi cung ứng, thương lượng và nhạy bén với thị trường.\n"
                "   - *Khối Nghệ thuật & Thiết kế (Kiến trúc, Đồ họa, Nội thất):* Đòi hỏi gu thẩm mỹ thị giác, tư duy không gian 3D và sự tỉ mỉ trong từng đường nét phác thảo.\n\n"
                "2. **Đối chiếu với mã tính cách Holland của bạn:**\n"
            )
            if holland_code:
                reply += f"   - Bạn có mã Holland là **{holland_code}**. Những ngành có mã khớp với 2-3 chữ cái đầu tiên sẽ giúp bạn học tập hứng thú và ít bị áp lực chán nản sau 2 năm đại học.\n\n"
            else:
                reply += "   - Bạn nên làm bài trắc nghiệm Holland ở Bước 2 để hệ thống đo đạc chính xác mã RIASEC của bạn.\n\n"
            reply += (
                "3. **Thử nghiệm với Skill Sandbox:**\n"
                "   - Trong từng thẻ ngành của Bảng Lộ trình, hãy bấm nút **'Chi tiết nghề & Sandbox'** và thực hiện **Nhiệm vụ thử nghiệm (30-45 phút)**. "
                "Cảm xúc và sự hứng thú của bạn khi làm nhiệm vụ đó chính là câu trả lời chân thật nhất!"
            )
            return {"reply": reply, "topic": "major_comparison"}

        # 4. Câu hỏi về chiến lược xếp thứ tự nguyện vọng trên cổng Bộ GD&ĐT
        if any(w in msg_lower for w in ["nguyện vọng", "thứ tự", "xếp", "nv1", "nv2", "tỷ lệ vàng", "cổng bộ"]):
            reply = (
                "### Chiến Lược Đặt Thứ Tự Nguyện Vọng Chuẩn Bộ GD&ĐT:\n\n"
                "Theo quy chế tuyển sinh hiện hành, hệ thống của Bộ GD&ĐT sẽ xét tuyển từ **NV1 xuống NV cuối cùng**. "
                "Thí sinh chỉ trúng tuyển vào **duy nhất 1 nguyện vọng cao nhất** thỏa mãn điều kiện điểm chuẩn.\n\n"
                "**Quy tắc 'Tỷ Lệ Vàng 20 - 50 - 30' của EduCompass AI:**\n"
                "- **NV1 - NV2 (20% Thử thách/Ước mơ):** Đặt các ngành/trường bạn khao khát nhất dù điểm chuẩn năm ngoái cao hơn điểm của bạn từ 0.5 - 1.5 điểm. Không lo mất lượt vì nếu trượt NV1, NV2 vẫn được xét công bằng như người đặt NV1.\n"
                "- **NV3 - NV6 (50% Vừa sức/Mục tiêu):** Điểm chuẩn năm ngoái dao động trong khoảng $\\pm 0.5$ điểm so với điểm của bạn. Đây là nhóm có xác suất đỗ cao nhất (60 - 85%) và là trụ cột lộ trình.\n"
                "- **NV7 - NV10 (30% An toàn/Bảo hiểm):** Điểm của bạn vượt điểm chuẩn từ 1.5 - 3.0 điểm. Đảm bảo 100% cánh cửa đại học luôn mở rộng trong mọi tình huống biến động đề thi.\n\n"
                "⚠️ **Cảnh báo lỗi phổ biến:** Tuyệt đối **không đặt ngành điểm chuẩn thấp hơn lên trên ngành điểm chuẩn cao hơn mà bạn yêu thích**, "
                "vì nếu đỗ nguyện vọng trên, toàn bộ các nguyện vọng bên dưới sẽ tự động bị hủy bỏ!"
            )
            return {"reply": reply, "topic": "strategy"}

        # 5. Phản hồi thông minh tổng quát (Fallback)
        reply = (
            f"Chào bạn! Dựa trên hồ sơ của bạn (Điểm tổ hợp thế mạnh: **{max(scores.values()) if scores else 'chưa có'}đ**, "
            f"Mã tính cách: **{holland_code or 'RIASEC'}**, Sở thích: *'{user_interest or 'đang khám phá'}'*):\n\n"
            "EduCompass AI luôn sẵn sàng đồng hành cùng bạn giải đáp mọi thắc mắc:\n"
            "- 🏫 *'Tại sao nên/không nên chọn trường X?'*\n"
            "- 💰 *'Học phí trường nào dưới 20 triệu/năm?'*\n"
            "- 🎯 *'Cách xếp thứ tự NV1, NV2 tối ưu nhất?'*\n"
            "- 🧪 *'Trải nghiệm thử thách Skill Sandbox của nghề ra sao?'*\n\n"
            "Hãy đặt câu hỏi cụ thể về trường, ngành hoặc điểm số bạn quan tâm nhé!"
        )
        return {"reply": reply, "topic": "general"}


class WhatIfSimulator:
    """
    Công cụ mô phỏng giả định điểm số "Nếu - Thì" thời gian thực.
    """

    @staticmethod
    def simulate(
        baseline_scores: Dict[str, float],
        delta_scores: Optional[Dict[str, float]] = None,
        ielts_score: Optional[float] = None,
        priority_area: str = "KV3",
        ethnicity: str = "kinh",
        recommendations: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        delta_scores = delta_scores or {}
        recommendations = recommendations or []
        
        # 1. Tính toán điểm mới sau giả định
        updated_scores = dict(baseline_scores)
        for subj, delta in delta_scores.items():
            if subj in updated_scores:
                updated_scores[subj] = round(min(10.0, max(0.0, updated_scores[subj] + delta)), 2)
            else:
                updated_scores[subj] = round(min(10.0, max(0.0, 7.0 + delta)), 2)
                
        std_scores = AcademicAgent._standardize_subject_scores(updated_scores)
        prospectuses = {p["university_code"]: p for p in DatabaseManager.get_all_prospectuses(year=2025)}
        raw_english = float(std_scores.get("Tiếng Anh", 7.0))

        simulated_recs = []
        old_safety, old_target, old_reach = 0, 0, 0
        new_safety, new_target, new_reach = 0, 0, 0

        for r in recommendations:
            old_role = r.get("strategy_role", "")
            if "An toàn" in old_role:
                old_safety += 1
            elif "Vừa sức" in old_role:
                old_target += 1
            else:
                old_reach += 1

            combo = r.get("combination_code", "A00")
            uni_code = r.get("university_code", "")
            combo_subjects = AcademicAgent.COMBINATION_MAPPINGS.get(combo, ["Toán", "Vật lý", "Hóa học"])

            has_all = all(s in std_scores for s in combo_subjects)
            if has_all:
                base_score = sum(std_scores[s] for s in combo_subjects)
            else:
                existing = [std_scores[s] for s in combo_subjects if s in std_scores]
                avg_val = (sum(std_scores.values()) / len(std_scores)) if std_scores else 7.0
                base_score = sum(existing) + avg_val * (len(combo_subjects) - len(existing))

            # Điểm ưu tiên
            priority_info = AdmissionAgent.calculate_ministry_priority_score(base_score, priority_area, ethnicity)
            priority_pts = priority_info["scaled_priority"]

            # IELTS Boost
            ielts_boost = 0.0
            if ielts_score and ielts_score >= 5.0 and combo in ["A01", "D01", "D07"]:
                p_rule = prospectuses.get(uni_code)
                if p_rule and p_rule.get("ielts_conversion_map"):
                    conv_score = SLMProspectusParser.calculate_converted_score(ielts_score, p_rule["ielts_conversion_map"])
                    gain = conv_score - raw_english
                    if gain > 0:
                        ielts_boost = round(gain, 2)

            new_cand_score = round(base_score + priority_pts + ielts_boost, 2)
            bench_2025 = r.get("score_2025", 25.0)
            score_delta = round(new_cand_score - bench_2025, 2)

            # Tính lại tỷ lệ đỗ
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
                new_safety += 1
            elif pass_prob >= 60:
                tier_role = "Vừa sức (Mục tiêu cốt lõi)"
                badge_class = "target"
                new_target += 1
            else:
                tier_role = "Thử thách (Ước mơ)"
                badge_class = "reach"
                new_reach += 1

            # Xác định trạng thái thay đổi
            status_change = "unchanged"
            if "Thử thách" in old_role and ("Vừa sức" in tier_role or "An toàn" in tier_role):
                status_change = "promoted"
            elif "Vừa sức" in old_role and "An toàn" in tier_role:
                status_change = "promoted_safety"

            old_cand = round(r.get("candidate_score", new_cand_score), 2)
            old_prob = r.get("pass_probability", pass_prob)
            old_delta = r.get("score_delta", score_delta)
            score_diff = round(new_cand_score - old_cand, 2)
            prob_diff = round(pass_prob - old_prob, 1)

            # Lời diễn giải biến chuyển chi tiết cho từng nguyện vọng
            if status_change == "promoted":
                desc = (
                    f"🔥 **THĂNG HẠNG NGOẠN MỤC:** Điểm tăng +{score_diff:.2f}đ (từ {old_cand:.2f}đ ➔ {new_cand_score:.2f}đ). "
                    f"Xác suất đỗ tăng từ {old_prob}% ➔ {pass_prob}% (+{prob_diff}%), chính thức chuyển từ nhóm '{old_role}' sang nhóm '{tier_role}'!"
                )
            elif status_change == "promoted_safety":
                desc = (
                    f"🛡️ **CHUYỂN SANG CHẮC ĐỖ:** Điểm tăng +{score_diff:.2f}đ (từ {old_cand:.2f}đ ➔ {new_cand_score:.2f}đ). "
                    f"Xác suất đỗ đạt {pass_prob}% (tăng +{prob_diff}%), nâng tầm từ '{old_role}' lên nhóm '{tier_role}' an toàn tuyệt đối!"
                )
            elif score_diff > 0:
                if pass_prob >= 90:
                    desc = (
                        f"✅ **CỦNG CỐ AN TOÀN:** Điểm tăng +{score_diff:.2f}đ (từ {old_cand:.2f}đ ➔ {new_cand_score:.2f}đ). "
                        f"Tỷ lệ đỗ đạt {pass_prob}%, điểm xét tuyển vượt chuẩn +{score_delta:.2f}đ (càng vững chắc vị trí đỗ)."
                    )
                else:
                    gap_change = abs(old_delta) - abs(score_delta)
                    desc = (
                        f"📈 **RÚT NGẮN KHOẢNG CÁCH:** Điểm tăng +{score_diff:.2f}đ (từ {old_cand:.2f}đ ➔ {new_cand_score:.2f}đ). "
                        f"Khoảng cách so với điểm chuẩn 2025 rút ngắn {gap_change:.2f}đ (từ {old_delta:+.2f}đ còn {score_delta:+.2f}đ), tỷ lệ đỗ tăng từ {old_prob}% ➔ {pass_prob}%."
                    )
            else:
                desc = f"Điểm xét tuyển giữ nguyên {new_cand_score:.2f}đ, tỷ lệ đỗ {pass_prob}% ({tier_role})."

            simulated_recs.append({
                **r,
                "old_candidate_score": old_cand,
                "old_pass_probability": old_prob,
                "old_strategy_role": old_role,
                "old_score_delta": old_delta,
                "candidate_score": new_cand_score,
                "score_delta": score_delta,
                "pass_probability": pass_prob,
                "strategy_role": tier_role,
                "badge_class": badge_class,
                "status_change": status_change,
                "score_diff_from_baseline": score_diff,
                "change_description": desc
            })

        return {
            "updated_scores": updated_scores,
            "summary_before": {"safety": old_safety, "target": old_target, "reach": old_reach},
            "summary_after": {"safety": new_safety, "target": new_target, "reach": new_reach},
            "promoted_count": sum(1 for item in simulated_recs if item["status_change"] != "unchanged"),
            "simulated_recommendations": simulated_recs
        }
