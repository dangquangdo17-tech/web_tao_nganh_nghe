# Knowledge base of major profiles for Vector RAG
from typing import List, Dict, Any

MAJOR_KNOWLEDGE_DOCS: List[Dict[str, Any]] = [
    {
        "code": "IT-CS",
        "name": "Khoa học Máy tính & Trí tuệ Nhân tạo (Computer Science & AI)",
        "category": "Công nghệ thông tin",
        "holland": "IRC",
        "keywords": ["máy tính", "thuật toán", "ai", "trí tuệ nhân tạo", "machine learning", "deep learning", "toán cao cấp", "lập trình", "python", "dữ liệu", "logic", "nghiên cứu"],
        "content": """Ngành Khoa học Máy tính & Trí tuệ Nhân tạo tập trung nghiên cứu bản chất của tính toán, lý thuyết thuật toán, kiến trúc xử lý dữ liệu quy mô lớn và mô hình hóa trí thông minh nhân tạo (LLM, Computer Vision, NLP). 
Phù hợp với học sinh có tư duy toán học xuất sắc (Điểm Toán >= 8.5 - 9.0), thích đào sâu bản chất vấn đề, không ngại các chứng minh toán lý thuyết và thuật toán phức tạp. 
Cơ hội nghề nghiệp: Kỹ sư AI/ML tại các tập đoàn công nghệ lớn, Kỹ sư nghiên cứu giải thuật (Algorithm Engineer), Chuyên gia phân tích dữ liệu chuyên sâu."""
    },
    {
        "code": "IT-SE",
        "name": "Kỹ thuật Phần mềm (Software Engineering)",
        "category": "Công nghệ thông tin",
        "holland": "RIC",
        "keywords": ["phần mềm", "lập trình", "web", "mobile", "app", "ứng dụng", "coder", "developer", "backend", "frontend", "game", "máy tính"],
        "content": """Kỹ thuật Phần mềm là ngành học ứng dụng thực tiễn, đào tạo kỹ năng thiết kế, xây dựng, kiểm thử và vận hành các phần mềm, ứng dụng di động, website và hệ thống doanh nghiệp. 
Đặc biệt thích hợp cho những bạn yêu thích máy tính, công nghệ nhưng điểm Toán ở mức khá (khoảng 7.0 - 8.0) hoặc không muốn đi quá sâu vào toán trừu tượng. Điểm quan trọng nhất là tư duy logic thực hành, tính cẩn thận, khả năng tự học công nghệ mới và làm việc nhóm.
Cơ hội nghề nghiệp: Lập trình viên Fullstack, Mobile Developer (iOS/Android), Kỹ sư DevOps, Trưởng nhóm phát triển sản phẩm."""
    },
    {
        "code": "IT-CYBER",
        "name": "An toàn Thông tin & An ninh Mạng (Cybersecurity)",
        "category": "Công nghệ thông tin",
        "holland": "RIC",
        "keywords": ["an ninh mạng", "hacker", "bảo mật", "mật mã", "mạng máy tính", "virus", "phòng thủ", "điều tra số", "hệ thống"],
        "content": """Ngành An toàn Thông tin đào tạo chuyên gia bảo vệ hệ thống mạng, hạ tầng máy chủ, phòng chống mã độc, kiểm thử lỗ hổng bảo mật và phản ứng sự cố an ninh mạng.
Phù hợp với người có tính tò mò, tư duy phản biện, kiên trì điều tra, tuân thủ đạo đức nghề nghiệp nghiêm ngặt. Yêu cầu nắm vững nguyên lý hoạt động của hệ điều hành và mạng máy tính.
Cơ hội nghề nghiệp: Chuyên viên Pentest, Giám sát an ninh mạng (SOC Analyst), Kỹ sư an toàn thông tin ngân hàng và cơ quan chính phủ."""
    },
    {
        "code": "IT-DS",
        "name": "Khoa học Dữ liệu (Data Science)",
        "category": "Công nghệ thông tin",
        "holland": "IRC",
        "keywords": ["dữ liệu", "thống kê", "data analyst", "data science", "biểu đồ", "kinh doanh", "dự báo", "toán xác suất", "sql", "python"],
        "content": """Khoa học Dữ liệu là sự giao thoa hoàn hảo giữa Toán thống kê, Công nghệ thông tin và Kiến thức nghiệp vụ kinh tế. Ngành này biến những khối dữ liệu khổng lồ thành thông tin chiến lược hỗ trợ ra quyết định.
Phù hợp với học sinh thích các con số, biểu đồ, tò mò về xu hướng hành vi con người và thị trường. Điểm Toán từ 7.5 - 8.5 là một lợi thế lớn.
Cơ hội nghề nghiệp: Data Analyst, Data Engineer, Chuyên viên phân tích hành vi khách hàng, Tư vấn giải pháp dữ liệu số."""
    },
    {
        "code": "ENG-ROBOT",
        "name": "Kỹ thuật Robot & Cơ điện tử (Robotics & Mechatronics)",
        "category": "Khoa học Kỹ thuật",
        "holland": "RIC",
        "keywords": ["robot", "cơ điện tử", "tự động hóa", "máy móc", "phần cứng", "mạch điện", "lắp ráp", "chế tạo", "cơ khí", "vật lý"],
        "content": """Kỹ thuật Robot và Cơ điện tử kết hợp cơ khí chính xác, điều khiển điện tử thông minh và trí tuệ nhân tạo để thiết kế các cỗ máy tự động, cánh tay robot và dây chuyền sản xuất thông minh.
Phù hợp với các bạn trẻ đam mê tháo lắp máy móc, thích làm việc với phần cứng, có khả năng tư duy không gian tốt và thế mạnh ở môn Vật lý và Toán học.
Cơ hội nghề nghiệp: Kỹ sư R&D Robot, Kỹ sư lập trình hệ thống nhúng (Embedded Systems), Trưởng ca vận hành tự động hóa nhà máy thông minh."""
    },
    {
        "code": "ENG-SEMI",
        "name": "Kỹ thuật Vi mạch & Bán dẫn (Semiconductor Engineering)",
        "category": "Khoa học Kỹ thuật",
        "holland": "IRE",
        "keywords": ["bán dẫn", "vi mạch", "chip", "phần cứng", "vật lý chất rắn", "điện tử", "intel", "nvidia", "fdi", "công nghệ cao"],
        "content": """Kỹ thuật Vi mạch và Bán dẫn là ngành chiến lược quốc gia, chuyên về thiết kế các con chip bán dẫn (IC Design), kiểm thử vật lý vi mạch và sản xuất linh kiện điện tử tinh vi.
Đòi hỏi sự tỉ mỉ, kiên nhẫn cực cao, kiến thức sâu về vật lý lượng tử, điện từ học và kỹ năng sử dụng công cụ thiết kế vi mạch chuyên dụng.
Cơ hội nghề nghiệp: Kỹ sư thiết kế vi mạch RTL, Kỹ sư kiểm thử Chip (Verification Engineer) tại các tập đoàn toàn cầu như Marvell, Synopsys, FPT Semiconductor, Qualcomm."""
    },
    {
        "code": "ECO-IB",
        "name": "Kinh doanh Quốc tế & Xuất nhập khẩu (International Business)",
        "category": "Kinh tế & Quản lý",
        "holland": "ECS",
        "keywords": ["kinh doanh quốc tế", "xuất nhập khẩu", "toàn cầu", "ngoại thương", "tiếng anh", "giao tiếp", "hợp đồng", "logistics", "ngoại giao kinh tế"],
        "content": """Kinh doanh Quốc tế trang bị kiến thức về thương mại toàn cầu, thanh toán quốc tế, logistics đường biển, chiến lược marketing thâm nhập thị trường nước ngoài và đàm phán hợp đồng thương mại.
Cực kỳ thích hợp cho các bạn năng động, tự tin, giỏi ngoại ngữ (IELTS từ 6.5 trở lên là lợi thế cực lớn), thích giao lưu văn hóa và đam mê môi trường làm việc đa quốc gia.
Cơ hội nghề nghiệp: Chuyên viên mua hàng toàn cầu (Global Procurement), Quản lý chuỗi cung ứng, Chuyên viên thương mại đối ngoại, Đại diện kinh doanh hãng quốc tế."""
    },
    {
        "code": "ECO-MKT",
        "name": "Marketing Kỹ thuật số & Truyền thông Thương hiệu (Digital Marketing)",
        "category": "Kinh tế & Quản lý",
        "holland": "EAS",
        "keywords": ["marketing", "truyền thông", "quảng cáo", "sáng tạo", "content", "mạng xã hội", "tiktok", "facebook", "sự kiện", "thương hiệu"],
        "content": """Marketing Kỹ thuật số là nghệ thuật và khoa học kết nối sản phẩm với người tiêu dùng qua các kênh trực tuyến, sáng tạo nội dung viral, quảng cáo Google/Meta và xây dựng hình ảnh thương hiệu.
Dành cho người yêu thích sự đổi mới liên tục, nhạy bén với xu hướng của giới trẻ, thích sáng tạo nội dung, có mắt thẩm mỹ và tư duy thấu hiểu tâm lý khách hàng.
Cơ hội nghề nghiệp: Chuyên viên Digital Marketing, Quản lý tài khoản quảng cáo (Account Executive), Giám đốc chiến dịch truyền thông, Content Strategist."""
    },
    {
        "code": "ECO-FIN",
        "name": "Tài chính - Ngân hàng & Fintech (Finance & Banking)",
        "category": "Kinh tế & Quản lý",
        "holland": "CEI",
        "keywords": ["tài chính", "ngân hàng", "chứng khoán", "đầu tư", "tiền tệ", "fintech", "kế toán", "con số", "báo cáo tài chính"],
        "content": """Tài chính - Ngân hàng chuyên sâu về dòng vốn doanh nghiệp, thị trường chứng khoán, quản trị rủi ro tín dụng và các công nghệ tài chính mới như thanh toán ví điện tử, ngân hàng số.
Phù hợp với học sinh thích các con số, cẩn trọng, kỷ luật, có óc quan sát thị trường và khả năng giữ bình tĩnh trước áp lực biến động thị trường.
Cơ hội nghề nghiệp: Chuyên viên phân tích đầu tư chứng khoán, Quản lý tài sản (Wealth Management), Thẩm định tín dụng ngân hàng, Chuyên viên Fintech."""
    },
    {
        "code": "ECO-LOG",
        "name": "Logistics & Quản lý Chuỗi Cung ứng (Logistics & SCM)",
        "category": "Kinh tế & Quản lý",
        "holland": "ECR",
        "keywords": ["logistics", "kho bãi", "vận tải", "chuỗi cung ứng", "giao nhận", "cảng biển", "tối ưu", "hàng hóa", "điều phối"],
        "content": """Logistics & Quản lý Chuỗi Cung ứng là mạch máu vận hành nền kinh tế, đảm bảo hàng hóa được vận chuyển từ nơi sản xuất đến tay người tiêu dùng một cách nhanh nhất với chi phí tối ưu nhất.
Phù hợp với người có óc tổ chức, sắp xếp logic, xử lý tình huống phát sinh nhanh, chịu được áp lực thời gian và nhịp độ làm việc liên tục.
Cơ hội nghề nghiệp: Trưởng phòng Điều độ vận tải, Quản lý kho hàng thương mại điện tử (Shopee, Lazada), Chuyên viên Forwarder cảng biển quốc tế."""
    },
    {
        "code": "MED-DOC",
        "name": "Y Đa khoa (General Medicine)",
        "category": "Y Dược",
        "holland": "ISR",
        "keywords": ["bác sĩ", "y đa khoa", "y học", "bệnh viện", "chữa bệnh", "sức khỏe", "sinh học", "hóa học", "cứu người", "khám bệnh"],
        "content": """Y Đa khoa là ngành học đòi hỏi sự cam kết học tập lâu dài (6 năm đại học + 18 tháng thực hành lâm sàng), đào tạo bác sĩ có kiến thức y khoa toàn diện, kỹ năng chẩn đoán và điều trị bệnh.
Yêu cầu học lực xuất sắc (Khối B00 từ 27+ điểm), sức khỏe thể chất bền bỉ, tâm lý vững vàng và đặc biệt là lòng trắc ẩn, sự tận tâm với nỗi đau của người bệnh.
Cơ hội nghề nghiệp: Bác sĩ điều trị tại bệnh viện tuyến Trung ương, tỉnh/thành phố, Giảng viên trường y, Bác sĩ tại các phòng khám quốc tế."""
    },
    {
        "code": "MED-PHARM",
        "name": "Dược học (Pharmacy)",
        "category": "Y Dược",
        "holland": "IRC",
        "keywords": ["dược", "thuốc", "bào chế", "hóa học", "dược sĩ", "nhà thuốc", "kiểm nghiệm", "y tế"],
        "content": """Dược học nghiên cứu thuốc từ nguồn gốc tự nhiên và tổng hợp hóa học, tương tác thuốc trong cơ thể người, quy trình bào chế và quản lý chất lượng thuốc.
Thích hợp cho học sinh yêu thích môn Hóa học và Sinh học, tính cẩn trọng cao, ngăn nắp và có trách nhiệm với sức khỏe cộng đồng.
Cơ hội nghề nghiệp: Dược sĩ lâm sàng bệnh viện, Nghiên cứu R&D sản xuất thuốc, Trình dược viên chuyên nghiệp, Chủ chuỗi nhà thuốc đạt chuẩn GPP."""
    },
    {
        "code": "SOC-ENG",
        "name": "Ngôn ngữ Anh & Biên phiên dịch (English Studies)",
        "category": "Xã hội & Nhân văn",
        "holland": "ASE",
        "keywords": ["ngôn ngữ anh", "tiếng anh", "phiên dịch", "biên dịch", "văn hóa", "giảng dạy", "đối ngoại", "giao tiếp"],
        "content": """Ngôn ngữ Anh không chỉ dạy giao tiếp mà trang bị kiến thức sâu sắc về ngôn ngữ học, văn hóa các nước nói tiếng Anh, kỹ năng biên phiên dịch văn bản và dịch cabin trực tiếp.
Dành cho người có năng khiếu ngôn ngữ, phản xạ nghe nói tốt, trí nhớ ngắn hạn linh hoạt và mong muốn làm việc trong môi trường ngoại giao hoặc doanh nghiệp toàn cầu.
Cơ hội nghề nghiệp: Biên phiên dịch viên chuyên nghiệp, Chuyên viên đối ngoại quốc tế, Giáo viên/giảng viên IELTS, Điều phối viên dự án phi chính phủ (NGO)."""
    },
    {
        "code": "SOC-JOUR",
        "name": "Báo chí & Truyền thông Đa phương tiện (Journalism & Media)",
        "category": "Xã hội & Nhân văn",
        "holland": "ASE",
        "keywords": ["báo chí", "truyền thông", "phóng viên", "viết lách", "nhiếp ảnh", "podcast", "biên tập", "tin tức", "xã hội"],
        "content": """Báo chí & Truyền thông Đa phương tiện đào tạo kỹ năng phát hiện đề tài xã hội, phỏng vấn, viết bài báo điều tra, ghi hình, dựng phóng sự đa phương tiện và dẫn chương trình.
Phù hợp với học sinh năng nổ, thích di chuyển, đam mê viết lách, tò mò khám phá các góc cạnh cuộc sống và có tinh thần phụng sự công chúng.
Cơ hội nghề nghiệp: Phóng viên, Biên tập viên đài truyền hình/báo điện tử, Chuyên viên PR doanh nghiệp, Nhà sản xuất nội dung số."""
    },
    {
        "code": "ART-DES",
        "name": "Thiết kế Đồ họa & UI/UX (Graphic & UI/UX Design)",
        "category": "Nghệ thuật & Thiết kế",
        "holland": "ARE",
        "keywords": ["thiết kế", "đồ họa", "ui/ux", "vẽ", "mỹ thuật", "sáng tạo", "figma", "photoshop", "giao diện", "nghệ thuật", "hình ảnh"],
        "content": """Thiết kế Đồ họa & UI/UX là cầu nối giữa nghệ thuật thị giác và công nghệ ứng dụng, tạo nên các ấn phẩm truyền thông mãn nhãn và giao diện ứng dụng web/mobile tiện dụng cho hàng triệu người.
Phù hợp với học sinh có mắt thẩm mỹ, yêu thích vẽ vời, sáng tạo thị giác nhưng cũng muốn ứng dụng trong ngành công nghệ hiện đại mà không bắt buộc phải viết mã code phức tạp.
Cơ hội nghề nghiệp: UI/UX Designer tại các công ty công nghệ, Art Director tại các agency sáng tạo, Họa sĩ minh họa 2D/3D tự do."""
    },
    {
        "code": "ART-FASH",
        "name": "Thiết kế Thời trang & Mỹ thuật Ứng dụng (Fashion Design)",
        "category": "Nghệ thuật & Thiết kế",
        "holland": "ARE",
        "keywords": ["thời trang", "thiết kế thời trang", "may mặc", "stylist", "quần áo", "trang phục", "vải", "người mẫu", "mỹ thuật", "sáng tạo", "fashion"],
        "content": """Ngành Thiết kế Thời trang đào tạo chuyên môn về phát triển ý tưởng bộ sưu tập, phác thảo minh họa trang phục (Fashion Illustration), kỹ thuật dựng rập, xử lý chất liệu vải và kinh doanh thời trang.
Phù hợp với người có năng khiếu thẩm mỹ, đam mê xu hướng trang phục, phong cách sống, sự nhạy bén màu sắc và tư duy ứng dụng thương mại.
Cơ hội nghề nghiệp: Nhà thiết kế thời trang (Fashion Designer), Stylist định hình phong cách, Giám đốc sáng tạo thương hiệu thời trang, Chuyên viên quản lý sản xuất may mặc."""
    },
    {
        "code": "ECO-ECOM",
        "name": "Thương mại Điện tử & Kinh tế Số (E-Commerce)",
        "category": "Kinh tế & Quản lý",
        "holland": "ECS",
        "keywords": ["thương mại điện tử", "e-commerce", "shopee", "tiktok shop", "kinh tế số", "bán lẻ", "digital", "online"],
        "content": """Thương mại Điện tử kết hợp kinh doanh bán lẻ và nền tảng công nghệ số, quản trị gian hàng sàn thương mại điện tử, tối ưu hóa trải nghiệm mua sắm và luồng thanh toán số.
Phù hợp với học sinh thích buôn bán trực tuyến, nắm bắt nhanh các trào lưu mua sắm số, có tư duy logic và kỹ năng dữ liệu kinh doanh.
Cơ hội nghề nghiệp: E-Commerce Specialist, Quản lý sàn TMĐT (Shopee, Lazada, TikTok Shop), Chuyên viên phát triển kinh doanh số."""
    },
    {
        "code": "EDU-PED",
        "name": "Sư phạm & Khoa học Giáo dục (Pedagogy & Education)",
        "category": "Xã hội & Nhân văn",
        "holland": "SAE",
        "keywords": ["sư phạm", "giáo viên", "giảng dạy", "dạy học", "giáo dục", "học sinh", "truyền cảm hứng", "nhà trường"],
        "content": """Ngành Sư phạm đào tạo nghiệp vụ giảng dạy chuyên sâu các môn học, tâm lý giáo dục học sinh, phương pháp sư phạm hiện đại và ứng dụng công nghệ giáo dục (EdTech).
Đòi hỏi sự kiên nhẫn, lòng yêu trẻ, kỹ năng truyền đạt lôi cuốn, giọng nói truyền cảm và chuẩn mực đạo đức nhà giáo. Được nhà nước hỗ trợ học phí và sinh hoạt phí theo Nghị định 116.
Cơ hội nghề nghiệp: Giáo viên trường công/tư thục chất lượng cao, Chuyên gia phát triển chương trình EdTech, Giảng viên đại học."""
    },
    {
        "code": "LAW-INT",
        "name": "Luật Kinh tế & Luật Quốc tế (International Economic Law)",
        "category": "Xã hội & Nhân văn",
        "holland": "ECS",
        "keywords": ["luật", "pháp luật", "kinh tế", "tranh chấp", "hợp đồng", "tư vấn pháp lý", "phản biện", "lập luận", "công lý"],
        "content": """Luật Kinh tế & Luật Quốc tế đào tạo kỹ năng phân tích điều khoản luật pháp, soạn thảo hợp đồng thương mại, giải quyết tranh chấp kinh doanh và bảo vệ quyền lợi doanh nghiệp.
Phù hợp với người có tư duy logic sắc bén, khả năng ăn nói lưu loát, trí nhớ tốt và sự kiên định trong việc bảo vệ công lý và lợi ích hợp pháp.
Cơ hội nghề nghiệp: Luật sư thương mại, Chuyên viên pháp chế doanh nghiệp (Legal Counsel), Công chứng viên, Thư ký tòa án."""
    },
    {
        "code": "ENG-AUTO",
        "name": "Kỹ thuật Ô tô & Xe điện Thông minh (Automotive & EV Engineering)",
        "category": "Khoa học Kỹ thuật",
        "holland": "RIC",
        "keywords": ["ô tô", "xe điện", "kỹ thuật ô tô", "động cơ", "vinfast", "cơ khí", "tự động hóa", "pin lithium", "bảo dưỡng"],
        "content": """Kỹ thuật Ô tô & Xe điện đào tạo chuyên môn về cấu trúc động cơ đốt trong và hệ thống truyền động điện (EV), điều khiển tự hành, chẩn đoán điện tử và quản lý chuỗi bảo dưỡng sửa chữa ô tô.
Phù hợp với học sinh say mê xe cộ, yêu thích cơ khí chính xác, mạch điện tử và mong muốn tham gia vào làn sóng chuyển đổi xe xanh toàn cầu.
Cơ hội nghề nghiệp: Kỹ sư R&D Ô tô/Xe điện tại VinFast, Toyota, Thaco; Kỹ sư chẩn đoán lỗi tại đại lý 3S; Giám đốc xưởng dịch vụ kỹ thuật."""
    },
    {
        "code": "TOUR-HOSP",
        "name": "Quản trị Du lịch & Khách sạn Quốc tế (Hospitality & Tourism)",
        "category": "Kinh tế & Quản lý",
        "holland": "ESC",
        "keywords": ["du lịch", "khách sạn", "nhà hàng", "resort", "hướng dẫn viên", "lữ hành", "ẩm thực", "dịch vụ", "tour", "tiếp viên"],
        "content": """Quản trị Khách sạn & Du lịch trang bị kỹ năng vận hành chuỗi khu nghỉ dưỡng 5 sao, thiết kế tour trải nghiệm quốc tế, lễ tân cao cấp, nghệ thuật ẩm thực và quản trị nhân sự dịch vụ.
Thích hợp cho người năng động, nụ cười thân thiện, khả năng ngoại ngữ lưu loát, chỉ số cảm xúc EQ cao và thích di chuyển khám phá.
Cơ hội nghề nghiệp: Giám đốc tiền sảnh (Front Office Manager), Quản lý dịch vụ F&B tại khách sạn 5 sao (Marriott, InterContinental), Điều hành tour quốc tế."""
    },
    {
        "code": "SOC-PR",
        "name": "Quan hệ Công chúng & Truyền thông Doanh nghiệp (Public Relations - PR)",
        "category": "Xã hội & Nhân văn",
        "holland": "EAS",
        "keywords": ["quan hệ công chúng", "pr", "sự kiện", "tổ chức sự kiện", "khủng hoảng truyền thông", "thông cáo báo chí", "người phát ngôn", "truyền thông"],
        "content": """Ngành Quan hệ Công chúng (PR) đào tạo kỹ năng xây dựng uy tín thương hiệu, xử lý khủng hoảng truyền thông, tổ chức họp báo, sự kiện quy mô lớn và kết nối với các cơ quan báo chí.
Phù hợp với học sinh có tài ăn nói, hoạt ngôn, xử lý tình huống nhanh nhạy, ngoại hình sáng và tư duy chiến lược xã hội.
Cơ hội nghề nghiệp: Chuyên viên PR & Truyền thông nội bộ, Chuyên gia quản lý sự kiện (Event Planner), Người phát ngôn doanh nghiệp."""
    },
    {
        "code": "SOC-LANG-EAST",
        "name": "Ngôn ngữ & Văn hóa Đông Á (Tiếng Trung - Hàn - Nhật)",
        "category": "Xã hội & Nhân văn",
        "holland": "ASE",
        "keywords": ["tiếng trung", "tiếng hàn", "tiếng nhật", "ngôn ngữ trung", "ngôn ngữ hàn", "ngôn ngữ nhật", "fdi", "dịch thuật", "thương mại"],
        "content": """Chuyên sâu về văn phạm, khẩu ngữ, thương mại và văn hóa các cường quốc kinh tế Đông Á (Trung Quốc, Hàn Quốc, Nhật Bản). Đón đầu dòng vốn FDI khổng lồ đầu tư vào Việt Nam.
Phù hợp với người yêu thích văn hóa Đông Á, có năng khiếu bắt chước âm thanh, trí nhớ hình ảnh tốt để học chữ tượng hình Hán tự/Kanji/Hangul.
Cơ hội nghề nghiệp: Thông dịch viên cấp cao tại các tập đoàn Samsung, LG, Foxconn, Toyota; Chuyên viên xúc tiến thương mại quốc tế."""
    },
    {
        "code": "BIO-TECH",
        "name": "Công nghệ Sinh học & Kỹ thuật Y sinh (Biotechnology & Biomedical)",
        "category": "Khoa học Kỹ thuật",
        "holland": "IRE",
        "keywords": ["công nghệ sinh học", "y sinh", "gen", "tế bào", "dna", "vi sinh", "sinh học", "nuôi cấy mô", "vắc xin"],
        "content": """Nghiên cứu ứng dụng công nghệ gen, liệu pháp tế bào gốc, sản xuất vắc-xin, xử lý ô nhiễm môi trường và nông nghiệp hữu cơ công nghệ cao.
Đòi hỏi sự tỉ mỉ, đam mê thực nghiệm trong phòng lab vô trùng, khả năng phân tích vi sinh và thế mạnh ở môn Sinh học, Hóa học.
Cơ hội nghề nghiệp: Kỹ sư xét nghiệm di truyền gen, Chuyên viên R&D dược phẩm sinh học, Giám định viên công nghệ sinh học nông nghiệp."""
    },
    {
        "code": "AGRI-VET",
        "name": "Bác sĩ Thú y & Chăm sóc Thú cưng (Veterinary Medicine)",
        "category": "Khoa học Kỹ thuật",
        "holland": "RIS",
        "keywords": ["thú y", "bác sĩ thú y", "chó mèo", "thú cưng", "pet", "chăn nuôi", "bệnh viện thú y", "sinh học"],
        "content": """Đào tạo bác sĩ chẩn đoán, phẫu thuật, tiêm phòng và điều trị bệnh cho động vật cảnh (thú cưng) và gia súc gia cầm, quản lý an toàn dịch bệnh động vật.
Thị trường chăm sóc thú cưng tại các đô thị đang bùng nổ, mở ra cơ hội kinh doanh phòng khám thú y tư nhân cực kỳ phát triển.
Cơ hội nghề nghiệp: Bác sĩ trưởng phòng khám thú y thú cưng, Chuyên gia dinh dưỡng động vật, Kiểm dịch viên thú y xuất nhập khẩu."""
    },
    {
        "code": "ENG-ARCH",
        "name": "Kiến trúc Công trình & Thiết kế Nội thất (Architecture & Interior Design)",
        "category": "Nghệ thuật & Thiết kế",
        "holland": "AIR",
        "keywords": ["kiến trúc", "nội thất", "thiết kế nội thất", "kiến trúc sư", "nhà ở", "bản vẽ", "autocad", "3ds max", "không gian", "xây dựng"],
        "content": """Giao thoa đỉnh cao giữa kỹ thuật kết cấu xây dựng và nghệ thuật không gian sống, tạo nên các công trình biểu tượng và không gian nội thất tiện nghi.
Đòi hỏi năng khiếu vẽ hình học không gian, sự nhạy cảm ánh sáng vật liệu và khả năng làm chủ các phần mềm đồ họa mô phỏng 3D chuyên sâu.
Cơ hội nghề nghiệp: Kiến trúc sư công trình, Nhà thiết kế nội thất dân dụng/khách sạn, Giám sát thiết kế thi công hoàn thiện."""
    },
    {
        "code": "PSYCH-APP",
        "name": "Tâm lý học Ứng dụng & Tham vấn Học đường (Applied Psychology)",
        "category": "Xã hội & Nhân văn",
        "holland": "SIA",
        "keywords": ["tâm lý", "tâm lý học", "tham vấn", "trị liệu", "tâm thần", "sức khỏe tinh thần", "lắng nghe", "tư vấn tâm lý"],
        "content": """Nghiên cứu hành vi, cảm xúc con người, phương pháp đánh giá trắc nghiệm tâm lý và kỹ năng trị liệu tham vấn tâm lý cho thanh thiếu niên và người trưởng thành.
Đòi hỏi khả năng lắng nghe thấu cảm không phán xét, bảo mật thông tin tuyệt đối và đức tính kiên nhẫn sâu sắc.
Cơ hội nghề nghiệp: Chuyên viên tư vấn tâm lý học đường, Chuyên gia quản trị nhân sự & đào tạo tâm lý doanh nghiệp, Trị liệu viên tâm lý."""
    }
]
