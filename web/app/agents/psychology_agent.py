from typing import Dict, Any, List
from ..rag.vector_store import vector_store_instance
from .state import CounselorState

class PsychologyAgent:
    """
    Agent Tâm lý & Hướng nghiệp:
    Đánh giá tính cách nghề nghiệp theo mô hình Holland RIASEC và tích hợp
    kết quả HyDE Vector RAG để thấu hiểu nguyện vọng từ ngôn ngữ tự nhiên.
    """

    HOLLAND_DESCRIPTIONS = {
        "R": {"name": "Kỹ thuật - Thực tế (Realistic)", "desc": "Thích hành động, thao tác với máy móc, công cụ phần cứng, thể thao hoặc thế giới tự nhiên."},
        "I": {"name": "Nghiên cứu - Trí tuệ (Investigative)", "desc": "Thích quan sát, tìm hiểu, phân tích bản chất logic, giải quyết các bài toán trừu tượng."},
        "A": {"name": "Nghệ thuật - Sáng tạo (Artistic)", "desc": "Thích tự do thể hiện, giàu trí tưởng tượng, nhạy cảm với cái đẹp thị giác hoặc ngôn từ."},
        "S": {"name": "Xã hội - Giao tiếp (Social)", "desc": "Thích giúp đỡ, chia sẻ, giảng dạy, chữa lành hoặc làm việc tương tác trực tiếp với con người."},
        "E": {"name": "Quản lý - Lãnh đạo (Enterprising)", "desc": "Thích dẫn dắt, thuyết phục, kinh doanh, hoạch định chiến lược và theo đuổi mục tiêu lớn."},
        "C": {"name": "Nghiệp vụ - Chi tiết (Conventional)", "desc": "Thích sự ngăn nắp, kỷ luật, bảo mật, làm việc cẩn trọng với số liệu, quy trình chuẩn mực."}
    }

    DOMAIN_HOLLAND_WEIGHTS = {
        "fashion": {"A": 22, "E": 12, "R": 8},
        "graphic_art": {"A": 22, "I": 12, "R": 8},
        "cs_ai": {"I": 22, "R": 14, "C": 8},
        "software_dev": {"R": 20, "I": 14, "C": 8},
        "cybersecurity": {"R": 18, "C": 16, "I": 10},
        "data_science": {"I": 20, "C": 15, "E": 8},
        "robotics_hardware": {"R": 22, "I": 14, "C": 6},
        "automotive": {"R": 22, "I": 12, "C": 8},
        "int_business": {"E": 22, "C": 12, "S": 10},
        "ecommerce": {"E": 20, "C": 14, "I": 8},
        "marketing_media": {"E": 18, "A": 16, "S": 10},
        "pr_event": {"E": 20, "S": 15, "A": 10},
        "finance_banking": {"C": 22, "E": 14, "I": 8},
        "medicine_pharmacy": {"S": 22, "I": 18, "R": 6},
        "languages": {"A": 18, "S": 16, "E": 8},
        "east_asian_lang": {"A": 18, "S": 15, "E": 10},
        "journalism_social": {"S": 18, "A": 16, "I": 10},
        "law": {"E": 18, "C": 16, "S": 10},
        "pedagogy": {"S": 22, "A": 12, "C": 8},
        "biotech": {"I": 22, "R": 12, "S": 8},
        "veterinary": {"R": 18, "S": 16, "I": 10},
        "architecture": {"A": 20, "R": 16, "I": 8},
        "psychology": {"S": 22, "I": 15, "A": 8},
        "hospitality": {"S": 20, "E": 15, "A": 8}
    }

    DOMAIN_PSYCHOLOGY_INSIGHTS = {
        "fashion": "bạn sở hữu tư duy thẩm mỹ thị giác và khao khát thể hiện bản sắc cá nhân thông qua ngôn ngữ thiết kế, rập và chất liệu may mặc, phù hợp môi trường đào tạo xưởng may thực hành sáng tạo.",
        "graphic_art": "bạn có năng khiếu thị giác mạnh mẽ, nhạy bén với bố cục, màu sắc và trải nghiệm thị giác người dùng (UI/UX), thích biến ý tưởng trừu tượng thành sản phẩm đồ họa trực quan.",
        "cs_ai": "bạn sở hữu tư duy phân tích toán học logic sắc sảo, niềm say mê khám phá cấu trúc giải thuật trừu tượng và các mô hình học máy quy mô lớn.",
        "software_dev": "bạn tìm kiếm môi trường đào tạo cho phép phát huy tư duy thực hành và sự tự chủ, thích biến kiến thức logic thành các phần mềm, ứng dụng thực tế chạy mượt mà.",
        "cybersecurity": "bạn mang tư chất của một thám tử công nghệ: thận trọng, cẩn mật, đam mê truy tìm kẽ hở hệ thống và bảo vệ an toàn thông tin số.",
        "data_science": "bạn có xu hướng kết hợp logic toán xác suất thống kê với khả năng tư duy mô hình, thích giải mã những câu chuyện ẩn giấu đằng sau các tập dữ liệu lớn.",
        "robotics_hardware": "bạn có tố chất kỹ thuật không gian vượt trội, đam mê cơ khí chính xác, thích trực tiếp lắp ráp phần cứng, vi mạch và nhìn thấy cỗ máy tự động vận hành.",
        "automotive": "bạn có niềm say mê đặc biệt với động cơ, công nghệ ô tô và năng lượng xe điện mới, định hướng học tập qua thực hành tại các xưởng kỹ thuật ô tô hiện đại.",
        "int_business": "bạn là mẫu người hướng ngoại, tự tin giao tiếp, đam mê thương mại xuyên biên giới, logistics và các môi trường đa văn hóa năng động.",
        "ecommerce": "bạn có độ nhạy bén cao với các xu hướng tiêu dùng số, yêu thích kinh doanh thực chiến trên các sàn TMĐT và tối ưu hóa trải nghiệm khách hàng.",
        "marketing_media": "bạn mang tố chất truyền cảm hứng, óc sáng tạo nội dung viral và khả năng thấu hiểu tâm lý đám đông trên các nền tảng truyền thông hiện đại.",
        "pr_event": "bạn hoạt ngôn, năng động, có năng lượng kết nối cao và bản lĩnh xử lý tình huống linh hoạt trong các sự kiện và chiến dịch thương hiệu lớn.",
        "finance_banking": "bạn có tư duy chuẩn mực, thận trọng và kỷ luật cao khi làm việc với số liệu tài chính, thị trường vốn và các quyết định đầu tư kinh tế.",
        "medicine_pharmacy": "bạn có lòng trắc ẩn sâu sắc, tinh thần cống hiến vì sức khỏe con người và sức bền tâm lý vững vàng để theo đuổi lộ trình học tập y khoa dài hạn.",
        "languages": "bạn nhạy bén với âm điệu, cấu trúc ngữ nghĩa và giao thoa văn hóa, mong muốn trở thành cầu nối ngôn ngữ trong các hoạt động quốc tế.",
        "east_asian_lang": "bạn có tính kiên trì, khả năng ghi nhớ thị giác tốt với chữ tượng hình và khát khao làm việc với các đối tác doanh nghiệp FDI Đông Á.",
        "journalism_social": "bạn tò mò, khao khát dấn thân tìm kiếm sự thật xã hội, có khả năng diễn đạt sắc bén và tinh thần phụng sự cộng đồng.",
        "law": "bạn có tư duy lập luận phản biện sắc bén, khả năng bảo vệ lẽ phải, thượng tôn pháp luật và tinh thần bảo vệ quyền lợi hợp pháp của tổ chức, cá nhân.",
        "pedagogy": "bạn có tính kiên nhẫn, lòng yêu mến thế hệ trẻ, sự chuẩn mực trong phong thái và mong muốn truyền tải tri thức, giá trị nhân văn.",
        "biotech": "bạn kiên trì, cẩn trọng và tò mò khám phá các bí ẩn sinh học phân tử, hệ gen và công nghệ y sinh phục vụ đời sống con người.",
        "veterinary": "bạn có tình yêu thương sâu sắc với động vật, đôi bàn tay khéo léo và lòng can đảm trong chăm sóc, phẫu thuật cứu chữa thú cưng.",
        "architecture": "bạn kết hợp hoàn hảo giữa năng khiếu mỹ thuật thị giác và tư duy kết cấu không gian hình học 3 chiều của công trình xây dựng.",
        "psychology": "bạn có khả năng lắng nghe thấu cảm tự nhiên, tinh tế nhận diện cảm xúc người khác và mong muốn đồng hành hỗ trợ sức khỏe tinh thần.",
        "hospitality": "bạn ấm áp, hiếu khách, thích dịch chuyển, có chỉ số cảm xúc EQ cao và đam mê mang lại trải nghiệm dịch vụ du lịch hoàn hảo cho khách hàng."
    }

    @classmethod
    def analyze(cls, state: CounselorState) -> Dict[str, Any]:
        user_interest = state.user_interest or ""
        
        # 1. Gọi Vector RAG + HyDE Engine để tìm kiếm ngữ nghĩa theo nguyện vọng
        rag_search_result = vector_store_instance.search_with_hyde(
            user_query=user_interest if user_interest.strip() else "Em muốn tìm ngành nghề triển vọng phù hợp với năng lực học tập",
            top_k=27
        )
        domain_detected = rag_search_result.get("domain_detected", "custom_dynamic")
        neg_info = rag_search_result.get("negative_constraints", {})

        # 2. Khởi tạo điểm Holland cơ sở
        # Nếu có từ trắc nghiệm thì lấy làm nền, nếu không thì nền tảng cân bằng 10
        base_holland = state.holland_answers.copy() if state.holland_answers else {"R": 10, "I": 10, "A": 10, "S": 10, "E": 10, "C": 10}
        holland_scores = base_holland.copy()

        # Áp dụng trọng số từ domain nhận diện qua HyDE
        if domain_detected in cls.DOMAIN_HOLLAND_WEIGHTS:
            for trait, boost in cls.DOMAIN_HOLLAND_WEIGHTS[domain_detected].items():
                holland_scores[trait] = holland_scores.get(trait, 10) + boost
        else:
            # Phân tích từ khóa bổ sung nếu rơi vào fallback
            interest_lower = user_interest.lower()
            if any(w in interest_lower for w in ["máy tính", "lắp ráp", "robot", "máy móc", "kỹ thuật", "phần cứng", "ô tô"]):
                holland_scores["R"] += 18
            if any(w in interest_lower for w in ["nghiên cứu", "thuật toán", "ai", "dữ liệu", "phân tích", "khoa học", "y sinh"]):
                holland_scores["I"] += 18
            if any(w in interest_lower for w in ["vẽ", "thiết kế", "thời trang", "đồ họa", "sáng tạo", "nghệ thuật", "kiến trúc"]):
                holland_scores["A"] += 18
            if any(w in interest_lower for w in ["y học", "bác sĩ", "y khoa", "chữa bệnh", "chăm sóc", "dạy", "tâm lý", "du lịch"]):
                holland_scores["S"] += 18
            if any(w in interest_lower for w in ["kinh doanh", "quản trị", "lãnh đạo", "ngoại thương", "marketing", "luật", "pr"]):
                holland_scores["E"] += 18
            if any(w in interest_lower for w in ["tài chính", "ngân hàng", "kế toán", "an ninh mạng", "kỷ luật", "số liệu"]):
                holland_scores["C"] += 18

        # Nếu có ràng buộc phủ định, điều chỉnh điểm Holland
        if neg_info.get("has_negation"):
            excluded_domains = neg_info.get("excluded_domains", [])
            # Nếu ghét code hoặc ghét ngồi một chỗ: giảm R (kỹ thuật máy móc) và C (nghiệp vụ bàn giấy), tăng E (quản trị/kinh doanh) và S (xã hội)
            if "software_dev" in excluded_domains:
                holland_scores["R"] = max(5, holland_scores.get("R", 10) - 10)
                holland_scores["C"] = max(5, holland_scores.get("C", 10) - 6)
                holland_scores["E"] = holland_scores.get("E", 10) + 12
                holland_scores["A"] = holland_scores.get("A", 10) + 8
            if "cs_ai" in excluded_domains:
                holland_scores["I"] = max(5, holland_scores.get("I", 10) - 10)
            if "medicine_pharmacy" in excluded_domains:
                holland_scores["S"] = max(5, holland_scores.get("S", 10) - 8)

        # 3. Xác định mã Holland chủ đạo (Top 3)
        sorted_holland = sorted(holland_scores.items(), key=lambda x: x[1], reverse=True)
        primary_code = "".join([item[0] for item in sorted_holland[:3]])
        top_group_key = sorted_holland[0][0]
        top_group_info = cls.HOLLAND_DESCRIPTIONS.get(top_group_key, {"name": "Đa dạng", "desc": "Cân bằng đa lĩnh vực"})

        # 4. Sinh lời bình tâm lý tư vấn cá nhân hóa theo câu hỏi thực tế của học sinh
        insight_phrase = cls.DOMAIN_PSYCHOLOGY_INSIGHTS.get(
            domain_detected,
            "bạn tìm kiếm sự cân bằng hài hòa giữa sở thích cá nhân, khả năng ứng dụng thực tế và nhu cầu việc làm dài hạn của thị trường."
        )

        question_quote = f"'{user_interest}'" if len(user_interest) < 80 else f"'{user_interest[:77]}...'"
        
        # 5. Xây dựng khối "Hệ Thống Hiểu Bạn Thế Nào?" (AI Empathy Summary)
        identified_strengths = []
        if "E" in primary_code: identified_strengths.append("Tư duy kinh doanh & Năng lực dẫn dắt")
        if "A" in primary_code: identified_strengths.append("Óc thẩm mỹ & Sáng tạo nội dung")
        if "S" in primary_code: identified_strengths.append("Kỹ năng giao tiếp & Thấu cảm xã hội")
        if "I" in primary_code: identified_strengths.append("Tư duy phân tích & Đào sâu logic")
        if "R" in primary_code and "software_dev" not in neg_info.get("excluded_domains", []): identified_strengths.append("Kỹ thuật thực hành & Công nghệ")
        if "C" in primary_code: identified_strengths.append("Tính cẩn trọng, kỷ luật & Nhạy bén số liệu")
        if not identified_strengths: identified_strengths = ["Khả năng thích ứng linh hoạt", "Tư duy đa chiều"]

        excluded_list = neg_info.get("excluded_entities", [])
        
        if excluded_list:
            empathy_narrative = (
                f"Qua chia sẻ của bạn: *{question_quote}*, hệ thống nhận thấy bạn có thế mạnh nổi bật về **{', '.join(identified_strengths[:2])}**. "
                f"Đặc biệt, hệ thống đã ghi nhận và **CHỦ ĐỘNG LOẠI TRỪ** các yếu tố bạn không mong muốn ({', '.join(excluded_list)}) để chuyển hướng đề xuất sang các ngành ứng dụng, "
                f"giúp bạn phát huy tối đa đam mê mà không gặp phải rào cản tâm lý gò bó."
            )
        else:
            empathy_narrative = (
                f"Qua chia sẻ của bạn: *{question_quote}*, hệ thống nhận diện bạn thuộc nhóm **{top_group_info['name']}** (Mã RIASEC: **{primary_code}**), "
                f"sở hữu thế mạnh về **{', '.join(identified_strengths[:2])}**. {insight_phrase}"
            )

        psychology_comment = (
            f"{empathy_narrative} {top_group_info['desc']}"
        )

        empathy_summary = {
            "narrative": empathy_narrative,
            "identified_strengths": identified_strengths,
            "excluded_constraints": excluded_list,
            "primary_code": primary_code,
            "dominant_type": top_group_info["name"]
        }

        return {
            "holland_scores": holland_scores,
            "primary_code": primary_code,
            "dominant_type": top_group_info["name"],
            "domain_detected": domain_detected,
            "commentary": psychology_comment,
            "empathy_summary": empathy_summary,
            "negative_constraints": neg_info,
            "hypothetical_document": rag_search_result.get("hypothetical_document", ""),
            "semantic_major_matches": rag_search_result.get("top_matches", [])
        }
