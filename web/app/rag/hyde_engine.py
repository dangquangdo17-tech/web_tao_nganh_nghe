import re
from typing import Dict, Any, List, Optional

class HyDEEngine:
    """
    Kỹ thuật HyDE (Hypothetical Document Embeddings) thông minh và động (Dynamic HyDE).
    Tự động phân tách:
    1. Lĩnh vực/nguyện vọng thực tế của học sinh (Thời trang, Nghệ thuật, CNTT, Kinh tế, Y Dược, v.v.)
    2. Ngữ cảnh học lực/điểm số (Toán 7, Anh văn, Văn, v.v.)
    Để sinh ra văn bản hồ sơ giả định hoàn toàn tùy biến, không bị cố định vào một ngành duy nhất.
    """

    DOMAINS = [
        {
            "id": "fashion",
            "keywords": ["thời trang", "thiết kế thời trang", "may mặc", "quần áo", "trang phục", "stylist", "người mẫu", "vải", "fashion"],
            "title": "Thiết kế Thời trang & Mỹ thuật Ứng dụng (Fashion Design)",
            "related_majors": "Thiết kế Thời trang, Công nghệ May, Quản trị Kinh doanh Thời trang, Thiết kế Mỹ thuật Công nghiệp",
            "nature": "Phát triển ý tưởng bộ sưu tập, phác thảo minh họa thời trang, kỹ thuật dựng rập 2D/3D, nghiên cứu xu hướng và xử lý chất liệu vải.",
            "traits": "Năng khiếu thẩm mỹ, sự nhạy bén thị giác về phong cách, phối màu và tính thực tiễn thị trường.",
            "math_role": "Mức điểm Toán xung quanh 7.0 là nền tảng rất tốt để tính toán thông số rập, định mức vải và chi phí sản xuất may mặc. Ngành thời trang thường xét tuyển các tổ hợp D01, A00, V00, H00 hoặc xét học bạ kết hợp bài thi năng khiếu vẽ."
        },
        {
            "id": "graphic_art",
            "keywords": ["đồ họa", "thiết kế đồ họa", "ui/ux", "vẽ", "mỹ thuật", "figma", "photoshop", "kiến trúc", "nội thất", "hoạt hình", "game design"],
            "title": "Thiết kế Đồ họa, Mỹ thuật Số & Trải nghiệm Người dùng (UI/UX & Graphic Design)",
            "related_majors": "Thiết kế Đồ họa, Thiết kế UI/UX, Thiết kế Nội thất, Kiến trúc, Mỹ thuật Đa phương tiện",
            "nature": "Sáng tạo ấn phẩm truyền thông thị giác, giao diện ứng dụng web/mobile, thiết kế bao bì thương hiệu và minh họa số.",
            "traits": "Tư duy thẩm mỹ thị giác, thấu cảm hành vi người dùng, thành thạo công cụ thiết kế đồ họa.",
            "math_role": "Điểm Toán mức khá (7.0 - 7.5) kết hợp ngoại ngữ tốt là lợi thế lớn khi xét tuyển các tổ hợp D01, V00, H00 vào các trường đại học mỹ thuật và công nghệ."
        },
        {
            "id": "cs_ai",
            "keywords": ["trí tuệ nhân tạo", "ai", "machine learning", "deep learning", "khoa học máy tính", "thuật toán", "giải thuật", "toán cao cấp"],
            "title": "Khoa học Máy tính & Trí tuệ Nhân tạo (Computer Science & AI)",
            "related_majors": "Khoa học Máy tính, Trí tuệ Nhân tạo, Khoa học Dữ liệu",
            "nature": "Nghiên cứu mô hình ngôn ngữ lớn (LLM), thị giác máy tính, tối ưu hóa giải thuật và kiến trúc hệ thống tính toán phân tán.",
            "traits": "Tư duy toán học trừu tượng xuất sắc, say mê giải thuật và nghiên cứu học thuật.",
            "math_role": "Yêu cầu điểm Toán rất cao (thường từ 8.5 - 9.0 trở lên) cùng các tổ hợp A00, A01."
        },
        {
            "id": "software_dev",
            "keywords": ["phần mềm", "lập trình", "web", "mobile", "app", "ứng dụng", "coder", "developer", "máy tính", "viết code", "cntt", "it"],
            "title": "Kỹ thuật Phần mềm & Phát triển Ứng dụng (Software Engineering)",
            "related_majors": "Kỹ thuật Phần mềm, Hệ thống Thông tin, Công nghệ Thông tin Ứng dụng",
            "nature": "Xây dựng website, ứng dụng di động, giải pháp đám mây và hệ thống phần mềm doanh nghiệp.",
            "traits": "Tư duy logic thực hành, cẩn thận gỡ lỗi, tinh thần tự học công nghệ mới liên tục.",
            "math_role": "Điểm Toán mức 7.0 - 7.5 hoàn toàn đáp ứng tốt việc lập trình ứng dụng thực tế mà không bắt buộc phải học toán lý thuyết quá nặng."
        },
        {
            "id": "cybersecurity",
            "keywords": ["an ninh mạng", "bảo mật", "an toàn thông tin", "hacker", "pentest", "mật mã", "virus"],
            "title": "An toàn Thông tin & An ninh Mạng (Cybersecurity)",
            "related_majors": "An toàn Thông tin, Kỹ thuật Mạng máy tính",
            "nature": "Phòng chống tấn công mạng, kiểm thử xâm nhập bảo mật, điều tra số và quản trị hạ tầng mạng an toàn.",
            "traits": "Tư duy điều tra phản biện, cẩn trọng, kỷ luật và tuân thủ đạo đức nghề nghiệp.",
            "math_role": "Cần nền tảng Toán logic tốt (7.5 - 8.5) và tiếng Anh chuyên ngành công nghệ."
        },
        {
            "id": "data_science",
            "keywords": ["khoa học dữ liệu", "data analyst", "data science", "phân tích dữ liệu", "big data", "dữ liệu"],
            "title": "Khoa học Dữ liệu & Phân tích Kinh doanh (Data Science & Business Analytics)",
            "related_majors": "Khoa học Dữ liệu, Thống kê Kinh tế, Hệ thống Thông tin Quản lý",
            "nature": "Khai phá dữ liệu lớn, trực quan hóa biểu đồ, xây dựng mô hình dự báo hành vi thị trường.",
            "traits": "Tư duy thống kê, khả năng kể chuyện bằng dữ liệu (data storytelling).",
            "math_role": "Điểm Toán từ 7.5 - 8.5 là điểm cộng lớn cho các tổ hợp A00, A01, D01."
        },
        {
            "id": "robotics_hardware",
            "keywords": ["robot", "cơ điện tử", "tự động hóa", "máy móc", "vi mạch", "bán dẫn", "chip", "ô tô", "cơ khí", "điện tử", "lắp ráp"],
            "title": "Kỹ thuật Cơ điện tử, Robot & Vi mạch Bán dẫn (Robotics & Semiconductors)",
            "related_majors": "Kỹ thuật Robot, Vi mạch Bán dẫn, Kỹ thuật Cơ điện tử, Kỹ thuật Điều khiển",
            "nature": "Thiết kế mạch tích hợp IC, chế tạo robot tự hành, lập trình hệ thống nhúng và dây chuyền tự động.",
            "traits": "Thích tháo lắp máy móc phần cứng, tư duy không gian kỹ thuật và tính kiên trì.",
            "math_role": "Thế mạnh ở môn Toán và Vật lý là chìa khóa để trúng tuyển các tổ hợp A00, A01."
        },
        {
            "id": "int_business",
            "keywords": ["kinh doanh quốc tế", "xuất nhập khẩu", "ngoại thương", "logistics", "chuỗi cung ứng", "thương mại quốc tế", "toàn cầu"],
            "title": "Kinh doanh Quốc tế & Quản lý Chuỗi Cung ứng (International Business & SCM)",
            "related_majors": "Kinh doanh Quốc tế, Logistics, Kinh tế Đối ngoại, Thương mại Quốc tế",
            "nature": "Giao thương hàng hóa toàn cầu, đàm phán hợp đồng ngoại thương, tối ưu hóa kho vận vận tải đường biển/hàng không.",
            "traits": "Hướng ngoại, giao tiếp tự tin, nhạy bén xu thế thương mại và trình độ ngoại ngữ cao.",
            "math_role": "Các trường top đầu (FTU, NEU, UEH) xét tuyển các tổ hợp A00, A01, D01 kết hợp chứng chỉ IELTS quy đổi."
        },
        {
            "id": "marketing_media",
            "keywords": ["marketing", "tiếp thị", "quảng cáo", "pr", "truyền thông", "content", "mạng xã hội", "tiktok", "thương hiệu", "sự kiện"],
            "title": "Marketing Kỹ thuật số & Truyền thông Đa phương tiện (Digital Marketing & Media)",
            "related_majors": "Marketing, Truyền thông Đa phương tiện, Quan hệ Công chúng (PR), Thương mại Điện tử",
            "nature": "Sáng tạo chiến dịch quảng bá viral, quản trị thương hiệu, phân tích hành vi khách hàng trên các nền tảng mạng xã hội.",
            "traits": "Sáng tạo, nhạy bén trào lưu giới trẻ, thích kết nối con người và tư duy thẩm mỹ.",
            "math_role": "Phù hợp xét tuyển tổ hợp D01, A01, C00 với phổ điểm rộng từ 22 đến 27 điểm."
        },
        {
            "id": "finance_banking",
            "keywords": ["tài chính", "ngân hàng", "chứng khoán", "đầu tư", "kế toán", "kiểm toán", "fintech", "tiền"],
            "title": "Tài chính - Ngân hàng, Công nghệ Tài chính & Kế toán (Finance & Fintech)",
            "related_majors": "Tài chính - Ngân hàng, Fintech, Kế toán - Kiểm toán, Đầu tư Tài chính",
            "nature": "Quản trị dòng vốn doanh nghiệp, định giá chứng khoán, quản trị rủi ro tín dụng và thanh toán số.",
            "traits": "Nhạy bén với con số, cẩn trọng, kỷ luật và chịu được áp lực thị trường.",
            "math_role": "Điểm Toán là môn nhân hệ số hoặc tiêu chí phụ ưu tiên tại các trường khối kinh tế."
        },
        {
            "id": "medicine_pharmacy",
            "keywords": ["y khoa", "y đa khoa", "bác sĩ", "y tế", "bệnh viện", "chữa bệnh", "khám bệnh", "nha khoa", "dược", "thuốc", "dược sĩ"],
            "title": "Y Đa khoa & Dược học (Medicine & Pharmacy)",
            "related_majors": "Y Đa khoa, Dược học, Răng Hàm Mặt, Y học Cổ truyền, Điều dưỡng",
            "nature": "Khám chữa bệnh, thực hành lâm sàng, nghiên cứu bào chế dược phẩm và chăm sóc sức khỏe cộng đồng.",
            "traits": "Lòng trắc ẩn, đức hy sinh, sức bền thể lực - tinh thần và sự cẩn trọng tuyệt đối.",
            "math_role": "Xét tuyển trọng điểm khối B00 (Toán - Hóa - Sinh) và A00 (Toán - Lý - Hóa) với ngưỡng điểm chuẩn rất cao."
        },
        {
            "id": "languages",
            "keywords": ["ngôn ngữ", "tiếng anh", "ngôn ngữ anh", "dịch thuật", "biên dịch", "phiên dịch", "tiếng trung", "tiếng nhật", "tiếng hàn", "ngoại ngữ"],
            "title": "Ngôn ngữ học & Biên phiên dịch Quốc tế (Foreign Languages & Linguistics)",
            "related_majors": "Ngôn ngữ Anh, Ngôn ngữ Trung Quốc, Ngôn ngữ Hàn, Ngôn ngữ Nhật",
            "nature": "Nghiên cứu văn hóa ngữ âm, biên dịch sách báo hợp đồng, phiên dịch cabin hội nghị quốc tế và giảng dạy ngoại ngữ.",
            "traits": "Năng khiếu ngôn ngữ, trí nhớ ngắn hạn tốt, khả năng thích ứng giao thoa văn hóa.",
            "math_role": "Môn Ngoại ngữ thường được nhân hệ số 2 trong tổ hợp D01, D09, D14."
        },
        {
            "id": "journalism_social",
            "keywords": ["báo chí", "phóng viên", "truyền hình", "viết lách", "phóng sự", "xã hội", "ngoại giao", "quan hệ quốc tế"],
            "title": "Báo chí, Quan hệ Quốc tế & Khoa học Xã hội (Journalism & International Relations)",
            "related_majors": "Báo chí, Quan hệ Quốc tế, Xã hội học, Tâm lý học",
            "nature": "Sản xuất tin tức truyền hình, điều tra xã hội, đàm phán chính sách ngoại giao và tư vấn tâm lý cộng đồng.",
            "traits": "Tò mò, phản biện sắc bén, kỹ năng viết và nói thuyết phục, tinh thần dấn thân.",
            "math_role": "Thế mạnh ở các tổ hợp C00 (Văn - Sử - Địa) và D01 (Toán - Văn - Anh)."
        },
        {
            "id": "law",
            "keywords": ["luật", "pháp luật", "kinh tế luật", "luật sư", "tòa án", "pháp chế", "tranh chấp hợp đồng"],
            "title": "Luật Kinh tế & Pháp luật Quốc tế (Law & Legal Studies)",
            "related_majors": "Luật Kinh tế, Luật Quốc tế, Luật Thương mại",
            "nature": "Tư vấn pháp lý doanh nghiệp, soạn thảo hợp đồng, bảo vệ quyền lợi tố tụng tại tòa án và trọng tài thương mại.",
            "traits": "Lập luận logic chặt chẽ, tư duy bảo vệ công lý, khả năng ghi nhớ điều khoản chuẩn xác.",
            "math_role": "Xét tuyển đa dạng qua các tổ hợp A00, A01, C00, D01."
        },
        {
            "id": "pedagogy",
            "keywords": ["sư phạm", "giáo viên", "giảng dạy", "dạy học", "giáo dục", "học sinh"],
            "title": "Sư phạm & Khoa học Giáo dục (Pedagogy & Teacher Education)",
            "related_majors": "Sư phạm Toán, Sư phạm Văn, Sư phạm Tiếng Anh, Giáo dục Tiểu học",
            "nature": "Giảng dạy bộ môn, phát triển chương trình giáo dục, quản lý lớp học và tư vấn tâm lý học đường.",
            "traits": "Lòng yêu nghề, sự chuẩn mực, kiên nhẫn và khả năng truyền cảm hứng.",
            "math_role": "Miễn học phí theo Nghị định 116 và được cấp sinh hoạt phí hàng tháng."
        },
        {
            "id": "automotive",
            "keywords": ["ô tô", "xe điện", "động cơ", "kỹ thuật ô tô", "vinfast", "cơ khí ô tô", "pin lithium", "bảo dưỡng ô tô", "xe máy"],
            "title": "Kỹ thuật Ô tô & Xe điện Thông minh (Automotive & EV Engineering)",
            "related_majors": "Kỹ thuật Ô tô, Kỹ thuật Cơ khí, Điều khiển Tự động, Cơ điện tử",
            "nature": "Thiết kế hệ truyền động ô tô điện, chẩn đoán điện tử xe thông minh, tối ưu hóa hệ thống phanh lái và vận hành nhà máy sản xuất xe hơi.",
            "traits": "Đam mê máy móc cơ khí, tư duy không gian kỹ thuật và tính cẩn trọng chính xác.",
            "math_role": "Môn Toán và Vật lý là cốt lõi cho các tổ hợp A00, A01 với mức điểm từ 22 đến 26.5 điểm."
        },
        {
            "id": "hospitality",
            "keywords": ["du lịch", "khách sạn", "nhà hàng", "resort", "lữ hành", "ẩm thực", "f&b", "tour", "hướng dẫn viên", "tiếp viên hàng không"],
            "title": "Quản trị Du lịch & Khách sạn Quốc tế (Hospitality & Tourism)",
            "related_majors": "Quản trị Khách sạn, Quản trị Dịch vụ Du lịch & Lữ hành, Quản trị Nhà hàng & Dịch vụ Ăn uống",
            "nature": "Tổ chức tour du lịch khám phá, quản lý vận hành khách sạn/khu nghỉ dưỡng 5 sao, nghệ thuật ẩm thực và quản trị trải nghiệm khách hàng.",
            "traits": "Chỉ số cảm xúc EQ cao, nụ cười thân thiện, giao tiếp tự tin, thích dịch chuyển và đam mê văn hóa đa quốc gia.",
            "math_role": "Mức điểm Toán 6.5 - 7.5 kết hợp Tiếng Anh tốt mở rộng cơ hội xét tuyển các tổ hợp D01, A01, D14."
        },
        {
            "id": "pr_event",
            "keywords": ["quan hệ công chúng", "pr", "sự kiện", "tổ chức sự kiện", "khủng hoảng truyền thông", "thông cáo báo chí", "người phát ngôn"],
            "title": "Quan hệ Công chúng & Tổ chức Sự kiện (Public Relations & Event Management)",
            "related_majors": "Quan hệ Công chúng, Truyền thông Doanh nghiệp, Tổ chức Sự kiện",
            "nature": "Định vị thương hiệu tổ chức, quản trị khủng hoảng truyền thông, tổ chức các concert/sự kiện festival quy mô lớn và xây dựng mối quan hệ báo chí.",
            "traits": "Hoạt ngôn, tư duy ứng biến linh hoạt, năng động, khả năng kết nối con người và chịu áp lực thời gian.",
            "math_role": "Xét tuyển đa dạng các tổ hợp D01, C00, A01 với phổ điểm từ 24 đến 27 điểm."
        },
        {
            "id": "east_asian_lang",
            "keywords": ["tiếng trung", "tiếng hàn", "tiếng nhật", "ngôn ngữ trung", "ngôn ngữ hàn", "ngôn ngữ nhật", "hán ngữ", "hsk", "topik", "jlpt"],
            "title": "Ngôn ngữ & Văn hóa Đông Á (Tiếng Trung - Hàn - Nhật)",
            "related_majors": "Ngôn ngữ Trung Quốc, Ngôn ngữ Hàn Quốc, Ngôn ngữ Nhật Bản",
            "nature": "Thành thạo 4 kỹ năng nghe nói đọc viết, dịch thuật thương mại, đàm phán kinh doanh với các đối tác FDI lớn của Việt Nam.",
            "traits": "Năng khiếu ngôn ngữ, trí nhớ thị giác tốt, sự tỉ mỉ khi học chữ tượng hình và tinh thần cầu thị.",
            "math_role": "Tổ hợp xét tuyển phổ biến D01, D04, D06 với môn Ngoại ngữ thường được nhân hệ số 2."
        },
        {
            "id": "biotech",
            "keywords": ["công nghệ sinh học", "y sinh", "gen", "dna", "tế bào", "vi sinh", "nuôi cấy mô", "vắc xin"],
            "title": "Công nghệ Sinh học & Kỹ thuật Y sinh (Biotechnology & Biomedical)",
            "related_majors": "Công nghệ Sinh học, Kỹ thuật Y sinh, Hóa dược",
            "nature": "Nghiên cứu giải mã hệ gen, nuôi cấy mô thực vật, sản xuất chế phẩm sinh học bảo vệ môi trường và sản xuất vắc-xin thế hệ mới.",
            "traits": "Kiên nhẫn, đam mê nghiên cứu phòng thí nghiệm vô trùng, khả năng tư duy vi mô.",
            "math_role": "Xét tuyển ưu thế qua tổ hợp B00 (Toán - Hóa - Sinh) và A00 (Toán - Lý - Hóa)."
        },
        {
            "id": "veterinary",
            "keywords": ["thú y", "bác sĩ thú y", "chó mèo", "thú cưng", "pet", "chăn nuôi", "bệnh viện thú y"],
            "title": "Bác sĩ Thú y & Y học Động vật Cảnh (Veterinary Medicine)",
            "related_majors": "Thú y, Bác sĩ Thú y, Chăn nuôi Thú cưng",
            "nature": "Chẩn đoán bệnh, phẫu thuật, tiêm chủng và điều trị nội trú cho thú cưng (chó, mèo) và gia súc, phòng ngừa dịch bệnh lây từ động vật sang người.",
            "traits": "Tình yêu thương động vật sâu sắc, không sợ máu/mùi bẩn, đôi tay khéo léo và tính quyết đoán.",
            "math_role": "Xét tuyển tổ hợp B00, A00 với mức điểm chuẩn dao động từ 21 đến 26 điểm."
        },
        {
            "id": "architecture",
            "keywords": ["kiến trúc", "nội thất", "thiết kế nội thất", "kiến trúc sư", "xây dựng", "bản vẽ", "autocad", "3ds max", "không gian kiến trúc"],
            "title": "Kiến trúc Công trình & Thiết kế Nội thất (Architecture & Interior Design)",
            "related_majors": "Kiến trúc, Thiết kế Nội thất, Quy hoạch Vùng & Đô thị, Kỹ thuật Xây dựng",
            "nature": "Thiết kế phối cảnh công trình nhà ở, cao ốc, bố trí công năng không gian nội thất và vật liệu chiếu sáng thẩm mỹ.",
            "traits": "Tư duy hình học không gian 3 chiều xuất sắc, gu thẩm mỹ tinh tế, kiên nhẫn phác thảo đồ án.",
            "math_role": "Thường xét tuyển kết hợp điểm Toán (tổ hợp V00: Toán - Lý - Vẽ; H00: Văn - Năng khiếu vẽ 1 - Vẽ 2) hoặc tổ hợp D01/A00."
        },
        {
            "id": "psychology",
            "keywords": ["tâm lý", "tâm lý học", "tham vấn", "trị liệu tâm lý", "tư vấn tâm lý", "sức khỏe tinh thần", "stress", "trầm cảm"],
            "title": "Tâm lý học Ứng dụng & Tham vấn Học đường (Applied Psychology)",
            "related_majors": "Tâm lý học, Tâm lý học Giáo dục, Công tác Xã hội",
            "nature": "Thực hiện trắc nghiệm đo lường tâm lý, tham vấn giải tỏa lo âu/trầm cảm cho học sinh, can thiệp trị liệu tâm lý cá nhân và gia đình.",
            "traits": "Khả năng lắng nghe thấu cảm vô điều kiện, bảo mật thông tin, giọng nói truyền cảm ấm áp và tư duy phân tích cảm xúc.",
            "math_role": "Xét tuyển rộng rãi qua tổ hợp C00, D01, B00 với mức điểm chuẩn từ 23 đến 27 điểm."
        },
        {
            "id": "ecommerce",
            "keywords": ["thương mại điện tử", "e-commerce", "shopee", "tiktok shop", "lazada", "kinh tế số", "bán lẻ online"],
            "title": "Thương mại Điện tử & Kinh tế Số (E-Commerce)",
            "related_majors": "Thương mại Điện tử, Kinh tế Số, Marketing Số",
            "nature": "Xây dựng chiến lược bán hàng đa kênh (Omnichannel), tối ưu quảng cáo sàn TMĐT, quản lý thanh toán ví điện tử và phân tích dữ liệu mua sắm.",
            "traits": "Nhạy bén xu hướng công nghệ tiêu dùng, tư duy kinh doanh thực chiến và khả năng xử lý số liệu đơn hàng.",
            "math_role": "Xét tuyển qua tổ hợp A00, A01, D01 với phổ điểm từ 24 đến 27 điểm."
        }
    ]

    @classmethod
    def _extract_academic_mentions(cls, query: str) -> str:
        """
        Trích xuất điểm số hoặc môn học được học sinh đề cập trong câu.
        Ví dụ: 'điểm toán chỉ dự đoán khoảng 7' -> 'Toán khoảng 7.0 điểm'
        """
        math_match = re.search(r"toán[^\d]*(\d+(?:[\.,]\d+)?)", query, re.IGNORECASE)
        if math_match:
            val = math_match.group(1).replace(",", ".")
            return f"khoảng {val} điểm"
        if re.search(r"không giỏi toán|toán yếu|toán bình thường", query, re.IGNORECASE):
            return "ở mức trung bình khá"
        if re.search(r"giỏi toán|toán cao|toán 9", query, re.IGNORECASE):
            return "ở mức xuất sắc"
        return "ở mức khá"

    @classmethod
    def extract_negative_constraints(cls, query: str) -> Dict[str, Any]:
        """
        Nhận diện các từ khóa và biểu thức phủ định:
        ghét, không thích, không muốn, sợ, tránh, dị ứng, ngán, chán, không mê...
        Phân tách rõ những gì người dùng MUỐN và những gì người dùng KHÔNG MUỐN.
        """
        query_lower = query.lower()
        excluded_entities = []
        excluded_domains = []
        excluded_majors = []
        recommended_alternatives = []

        # 1. Nhận diện Lập trình / Viết code
        if re.search(r"(?:ghét|không thích|không muốn|sợ|tránh|dị ứng|ngán|chán|không mê|không có khiếu|không ưa)\s+.*?(?:code|lập trình|viết code|gõ code|coder|developer|ngồi fix bug)", query_lower) or \
           re.search(r"(?:không|đừng)\s+.*?(?:viết code|lập trình|gõ code)", query_lower):
            excluded_entities.append("Viết code chuyên sâu & Lập trình phần mềm")
            excluded_domains.extend(["software_dev", "cs_ai"])
            excluded_majors.extend(["IT-SE", "IT-CS"])
            recommended_alternatives.extend(["ecommerce", "graphic_art", "marketing_media", "data_science"])

        # 2. Nhận diện Ngồi một chỗ / Tĩnh tại / Bàn giấy
        if re.search(r"(?:ghét|không thích|không muốn|sợ|tránh|ngán|chán|không chịu được)\s+.*?(?:ngồi một chỗ|ngồi yên|ngồi cả ngày|văn phòng gò bó|bàn giấy|ngồi lì)", query_lower) or \
           "không thích ngồi một chỗ" in query_lower or "không muốn ngồi một chỗ" in query_lower or "không thích ngồi yên" in query_lower:
            excluded_entities.append("Ngồi một chỗ liên tục & Công việc bàn giấy gò bó")
            excluded_domains.extend(["software_dev", "cybersecurity", "finance_banking"])
            recommended_alternatives.extend(["int_business", "hospitality", "pr_event", "journalism_social"])

        # 3. Nhận diện Toán nặng / Giải thuật trừu tượng
        if re.search(r"(?:ghét|không thích|không muốn|sợ|tránh|dị ứng|ngán|chán|không có khiếu|không giỏi|yếu)\s+.*?(?:toán nặng|toán cao cấp|giải tích|toán khó|giải thuật)", query_lower) or \
           re.search(r"(?:sợ toán|ngán toán|không mê toán)", query_lower):
            excluded_entities.append("Toán lý thuyết trừu tượng & Giải thuật toán học nặng")
            excluded_domains.extend(["cs_ai", "robotics_hardware"])
            excluded_majors.extend(["IT-CS", "ENG-ROBOT", "ENG-SEMI"])
            recommended_alternatives.extend(["marketing_media", "languages", "graphic_art", "hospitality"])

        # 4. Nhận diện Máu / Bệnh viện / Lâm sàng
        if re.search(r"(?:ghét|không thích|không muốn|sợ|tránh|dị ứng|ngán|chán)\s+.*?(?:máu|bệnh viện|tiêm|kim tiêm|mùi thuốc|dao kéo|mổ)", query_lower) or \
           "sợ máu" in query_lower or "sợ bệnh viện" in query_lower:
            excluded_entities.append("Môi trường bệnh viện lâm sàng & Tiếp xúc máu bệnh nhân")
            excluded_domains.extend(["medicine_pharmacy"])
            excluded_majors.extend(["MED-DOC", "MED-GP"])
            recommended_alternatives.extend(["biotech", "psychology"])

        # 5. Nhận diện Kinh doanh / Bán hàng / KPI Doanh số
        if re.search(r"(?:ghét|không thích|không muốn|sợ|tránh|ngán|chán)\s+.*?(?:kinh doanh|bán hàng|sale|chạy kpi|đàm phán thương mại|buôn bán)", query_lower):
            excluded_entities.append("Áp lực doanh số, Bán hàng & Đàm phán thương mại")
            excluded_domains.extend(["int_business", "ecommerce", "marketing_media"])
            excluded_majors.extend(["ECO-IB", "ECO-BA", "ECO-MKT"])

        has_negation = len(excluded_entities) > 0
        return {
            "has_negation": has_negation,
            "excluded_entities": list(set(excluded_entities)),
            "excluded_domains": list(set(excluded_domains)),
            "excluded_majors": list(set(excluded_majors)),
            "recommended_alternatives": list(set(recommended_alternatives))
        }

    @classmethod
    def generate_hypothetical_document(cls, user_query: str) -> Dict[str, Any]:
        """
        Tạo văn bản hồ sơ giả định HyDE tùy biến và chính xác theo nguyện vọng thực của học sinh,
        có xử lý thông minh các ràng buộc phủ định (Negative Constraints).
        """
        query_lower = user_query.lower()
        math_context = cls._extract_academic_mentions(user_query)
        neg_info = cls.extract_negative_constraints(user_query)

        # Lọc bỏ các cụm từ phủ định khỏi câu để không vô tình kích hoạt từ khóa dương tính
        cleaned_query_lower = query_lower
        if neg_info["has_negation"]:
            # Tách các vế phủ định
            cleaned_query_lower = re.sub(
                r"(?:ghét|không thích|không muốn|sợ|tránh|dị ứng|ngán|chán|không mê|không có khiếu|không chịu được|không ưa|đừng)\s+[^,\.;\n]+",
                " ",
                query_lower
            )

        # 1. Tìm miền chuyên ngành (domain) phù hợp nhất theo điểm số từ khóa
        best_domain = None
        highest_score = 0

        for dom in cls.DOMAINS:
            dom_id = dom["id"]
            # Nếu domain này bị người dùng phủ định/ghét bỏ, loại trừ hoàn toàn
            if dom_id in neg_info["excluded_domains"]:
                continue

            # Đếm số từ khóa xuất hiện trên câu đã loại bỏ phủ định
            score = 0
            for kw in dom["keywords"]:
                if kw in cleaned_query_lower:
                    score += len(kw.split()) * 3 + 1

            # Nếu có gợi ý thay thế từ phủ định (ví dụ thích công nghệ nhưng ghét code -> gợi ý ecom, uiux)
            if dom_id in neg_info["recommended_alternatives"]:
                # Nếu câu gốc có nhắc đến công nghệ/máy tính
                if any(w in cleaned_query_lower for w in ["công nghệ", "máy tính", "tin học", "số", "internet", "online"]):
                    score += 8

            if score > highest_score:
                highest_score = score
                best_domain = dom

        # 2. Nếu tìm thấy domain cụ thể
        if best_domain and highest_score >= 2:
            neg_note = ""
            if neg_info["has_negation"]:
                neg_note = f"\nLưu ý đặc biệt từ nguyện vọng: Hệ thống đã ghi nhận và CHỦ ĐỘNG LOẠI TRỪ các yếu tố bạn không mong muốn ({', '.join(neg_info['excluded_entities'])}), chuyển trọng tâm sang hướng ứng dụng phù hợp nhất."

            hypo_text = f"""Hồ sơ ngành học giả định: Ngành {best_domain['title']}.
Các chuyên ngành liên quan: {best_domain['related_majors']}.
Bản chất & Môi trường đào tạo: {best_domain['nature']}
Tố chất phù hợp: {best_domain['traits']}
Phân tích học lực & Định hướng: Bạn đề cập năng lực môn Toán {math_context}. {best_domain['math_role']}{neg_note} Hệ thống khuyến nghị ưu tiên các trường có thế mạnh về lĩnh vực này để phát huy tối đa đam mê."""
            
            return {
                "original_query": user_query,
                "domain_detected": best_domain["id"],
                "hypothetical_document": hypo_text,
                "negative_constraints": neg_info
            }

        # 3. Dynamic Generative Fallback cho các câu hỏi tổng hợp hoặc sở thích khác biệt
        cleaned_words = [w for w in re.findall(r"[\w]+", cleaned_query_lower) if len(w) > 2 and w not in ["thích", "nhưng", "khoảng", "điểm", "làm", "việc", "dự", "đoán", "cho", "em"]]
        topic_preview = " ".join(cleaned_words[:5]) if cleaned_words else "phát triển toàn diện năng lực"

        neg_note = ""
        if neg_info["has_negation"]:
            neg_note = f"\nRàng buộc loại trừ: Đã loại trừ các lĩnh vực liên quan đến {', '.join(neg_info['excluded_entities'])} theo đúng yêu cầu."

        hypo_text = f"""Hồ sơ ngành học giả định tùy biến theo nguyện vọng: '{user_query}'
Lĩnh vực mục tiêu: Định hướng các ngành học liên quan đến {topic_preview}, tạo sự cân bằng giữa sở thích cá nhân và nhu cầu thị trường việc làm.{neg_note}
Đặc trưng đào tạo: Chú trọng kết hợp kiến thức chuyên môn thực hành với kỹ năng mềm và khả năng thích ứng linh hoạt.
Phân tích năng lực: Mức học lực và điểm thi dự kiến môn Toán {math_context} là tiền đề quan trọng để xây dựng chiến lược chọn tổ hợp xét tuyển an toàn và phù hợp nhất."""

        return {
            "original_query": user_query,
            "domain_detected": "custom_dynamic",
            "hypothetical_document": hypo_text,
            "negative_constraints": neg_info
        }
