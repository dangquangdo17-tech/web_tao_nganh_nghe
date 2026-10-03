# -*- coding: utf-8 -*-
from typing import Dict, Any, List, Optional
import re

CAREER_GUIDANCE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "IT-CS": {
        "entry_roles": ["Kỹ sư Trí tuệ Nhân tạo (AI Engineer)", "Kỹ sư Học máy (Machine Learning Engineer)", "Kỹ sư Dữ liệu lớn (Big Data Engineer)", "Chuyên viên Nghiên cứu Thuật toán AI"],
        "daily_work": "Nghiên cứu kiến trúc mô hình học sâu (Deep Learning), huấn luyện và tinh chỉnh mô hình AI (Fine-tuning LLMs), tối ưu hóa thuật toán xử lý dữ liệu quy mô lớn và xây dựng hệ thống gợi ý thông minh.",
        "starting_salary": "12 - 18 triệu VNĐ/tháng (Fresher)",
        "mid_salary": "28 - 50 triệu VNĐ/tháng (sau 2-3 năm)",
        "labor_market_outlook": "Thị trường cực kỳ khát nhân lực chất lượng cao trong kỷ nguyên Generative AI, xe tự hành và thị giác máy tính. Yêu cầu nền tảng Toán giải tích, Đại số tuyến tính và Xác suất thống kê vững chắc.",
        "skill_sandbox": {
            "course_name": "CS50 AI: Nhập môn Trí tuệ Nhân tạo với Python (Harvard edX) & Google Machine Learning Crash Course",
            "tryout_task": "Mở Google Colab (chạy Python online miễn phí), chạy thử một mô hình học máy đơn giản nhận diện chữ số viết tay từ 0 đến 9 trên tập dữ liệu chuẩn MNIST, rồi tự vẽ một chữ số bằng chuột xem AI đoán đúng bao nhiêu %.",
            "self_assessment_criteria": [
                "Bạn say mê các môn Toán (Đại số, Xác suất, Hình học giải tích) và luôn tò mò muốn biết cách máy tính có thể 'suy nghĩ' hoặc 'học'.",
                "Bạn thích quan sát các hiện tượng phức tạp và cố gắng tìm ra quy luật, công thức toán học ẩn giấu đằng sau dữ liệu.",
                "Bạn hứng thú với các công nghệ AI mới (ChatGPT, Midjourney, xe tự lái) và muốn tự tay tạo ra những cỗ máy thông minh như vậy.",
                "Bạn có tính kiên nhẫn cao, sẵn sàng đọc tài liệu kỹ thuật tiếng Anh và đào sâu bản chất toán học của thuật toán thay vì chỉ dùng sẵn thư viện."
            ],
            "self_assessment": "Nếu bạn đam mê giải các bài toán logic hóc búa và thích nhìn thế giới qua lăng kính mô hình toán học, ngành Khoa học Máy tính & AI sinh ra là dành cho bạn!"
        },
        "work_distribution": [
            {"task": "Nghiên cứu kiến trúc mô hình & Thuật toán", "percent": 40},
            {"task": "Lập trình, Huấn luyện mô hình & Gỡ lỗi", "percent": 35},
            {"task": "Xử lý & Chuẩn hóa dữ liệu lớn", "percent": 15},
            {"task": "Họp nhóm Agile & Báo cáo kỹ thuật", "percent": 10}
        ],
        "pressure_challenges": [
            "Công nghệ AI thay đổi theo từng tuần; áp lực tự học và đọc tài liệu nghiên cứu (Arxiv) liên tục để không bị tụt hậu.",
            "Các bài toán tối ưu thuật toán và học sâu đòi hỏi tư duy trừu tượng cực cao; việc tìm ra lỗi logic có thể mất nhiều ngày.",
            "Thời gian ngồi làm việc trước máy tính liên tục từ 8–10 tiếng, dễ gặp các vấn đề về cột sống và thị giác."
        ],
        "mini_case_study": {
            "scenario": "Bạn là Kỹ sư AI tại một sàn TMĐT lớn. Vào ngày Siêu Sale 11/11, mô hình gợi ý sản phẩm bỗng dưng liên tục đề xuất đồ chơi trẻ em cho khách hàng tìm mua laptop công nghệ, làm giảm 35% doanh thu giờ đầu tiên.",
            "questions": [
                {
                    "q": "Hành động đầu tiên khẩn cấp nhất bạn sẽ làm để xử lý sự cố là gì?",
                    "options": [
                        "Kích hoạt cơ chế Fallback (gợi ý top sản phẩm bán chạy nhất) để chặn đà sụt giảm doanh thu, sau đó mới cô lập dữ liệu lỗi để điều tra.",
                        "Tiếp tục để hệ thống chạy và lập tức mở mã nguồn Python lên huấn luyện lại mô hình mới từ đầu.",
                        "Gửi email báo cáo ban giám đốc và chờ chỉ đạo tiếp theo trước khi can thiệp máy chủ."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Tư duy kỹ sư công nghệ chuyên nghiệp luôn ưu tiên bảo vệ tính liên tục của hệ thống kinh doanh (System Resilience & Fail-safe) trước khi truy tìm nguyên nhân kỹ thuật."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Kỹ sư Trí tuệ Nhân tạo (AI Engineer)",
            "skill_tree": {
                "year_1_2": "Nền tảng Toán giải tích, Đại số tuyến tính, Xác suất thống kê; Lập trình Python nâng cao, Cấu trúc dữ liệu & Giải thuật, Git, Cơ sở dữ liệu SQL.",
                "year_3": "Học máy (Scikit-Learn), Học sâu (PyTorch/TensorFlow), Xử lý ngôn ngữ tự nhiên (NLP), Thị giác máy tính; Chứng chỉ AWS Certified Machine Learning; IELTS 6.5+.",
                "year_4": "Kiến trúc LLMs, RAG, Triển khai mô hình (MLOps, Docker, FastAPI); Thực tập tại VinAI, FPT Software, Viettel AI; Đồ án tốt nghiệp ứng dụng AI vào bài toán thực tiễn."
            },
            "top_specialized_unis": [
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Viện CNTT & TT số 1 miền Bắc, mạng lưới phòng lab AI liên kết Naver, VinAI, Samsung."},
                {"code": "UIT", "name": "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", "strength": "Khoa Khoa học Máy tính mạnh, chuyên sâu AI & Data Science, đối tác Intel, FPT."},
                {"code": "UET", "name": "Trường Đại học Công nghệ - ĐHQGHN", "strength": "Đào tạo nghiên cứu thuật toán đỉnh cao, đội ngũ giảng viên giàu công bố quốc tế."},
                {"code": "HCMUT", "name": "Trường Đại học Bách khoa - ĐHQG-HCM", "strength": "Truyền thống kỹ thuật công nghệ hàng đầu phương Nam, mạng lưới cựu sinh viên công nghệ hùng mạnh."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 18,
            "risk_level": "Rất thấp",
            "ai_augmented_skills": [
                "Làm chủ các công cụ hỗ trợ sinh mã (GitHub Copilot, Cursor) để tăng tốc độ phát triển mô hình gấp 3 lần.",
                "Kỹ năng Fine-tuning mô hình ngôn ngữ lớn (LLMs) và thiết kế hệ thống RAG chuyên biệt cho doanh nghiệp.",
                "Tư duy phản biện, thẩm định đạo đức dữ liệu và kiểm thử an toàn thuật toán AI (AI Safety & Alignment)."
            ],
            "national_priority": "Chiến lược Quốc gia về Nghiên cứu, Phát triển và Ứng dụng Trí tuệ Nhân tạo đến năm 2030 (QĐ 127/QĐ-TTg)"
        },
        "average_starting_salary": 15.5,
        "employment_rate": 98.6,
        "english_exit_req": "IELTS 6.0 hoặc VSTEP B2"
    },

    "IT-SE": {
        "entry_roles": ["Lập trình viên Web/App Frontend (React/Vue/Flutter)", "Lập trình viên Hệ thống Backend (Node/Python/Java/Golang)", "Kỹ sư Đảm bảo Chất lượng Phần mềm (QA/QC Automation)", "Kỹ sư DevOps sơ cấp"],
        "daily_work": "Tham gia họp Agile/Scrum đầu ngày, phân tích yêu cầu tính năng, viết mã nguồn sạch (Clean Code), viết Unit Test, rà soát mã nguồn cùng đồng nghiệp (Code Review) và sửa lỗi phần mềm (Debug).",
        "starting_salary": "9 - 14 triệu VNĐ/tháng (Fresher)",
        "mid_salary": "22 - 38 triệu VNĐ/tháng (sau 2-3 năm)",
        "labor_market_outlook": "Nhu cầu tuyển dụng luôn dẫn đầu ngành công nghệ. Doanh nghiệp đặc biệt ưu tiên sinh viên có sản phẩm thực tế đưa lên GitHub và khả năng giao tiếp tiếng Anh tốt.",
        "skill_sandbox": {
            "course_name": "CS50: Introduction to Computer Science (Harvard University) & FreeCodeCamp Web Development",
            "tryout_task": "Lên trang Replit.com hoặc VSCode, tự viết một chương trình Python nhỏ 30 dòng mô phỏng trò chơi: 'Đoán số bí mật từ 1 đến 100' có đếm số lần đoán và gợi ý 'Cao hơn / Thấp hơn' cho người chơi.",
            "self_assessment_criteria": [
                "Bạn thích cảm giác tự tay tạo ra một công cụ hoặc ứng dụng có thể chạy được trên máy tính hay điện thoại.",
                "Khi gặp lỗi (Bug), thay vì nản lòng bỏ cuộc, bạn cảm thấy tò mò muốn 'truy tìm thủ phạm' đến cùng.",
                "Bạn thích lối sống ngăn nắp, làm việc có cấu trúc logic rõ ràng và biết chia một bài toán lớn thành các bước nhỏ.",
                "Bạn thích tự học mày mò các mẹo công nghệ trên mạng và thích khám phá các ứng dụng mới mỗi ngày."
            ],
            "self_assessment": "Nếu bạn thấy hạnh phúc khi những dòng lệnh của mình biến thành một sản phẩm thực tế chạy mượt mà, bạn có 95% tố chất của một Kỹ sư Phần mềm xuất sắc!"
        },
        "work_distribution": [
            {"task": "Viết mã nguồn & Xây dựng tính năng phần mềm", "percent": 45},
            {"task": "Kiểm thử mã nguồn, Sửa lỗi & Code Review", "percent": 25},
            {"task": "Tham gia họp Agile/Scrum & Phân tích yêu cầu", "percent": 15},
            {"task": "Soạn tài liệu kỹ thuật & Cấu hình CI/CD", "percent": 15}
        ],
        "pressure_challenges": [
            "Thời hạn bàn giao (Deadline / Sprint release) thường rất gấp gáp; sẵn sàng tăng ca (OT) khi hệ thống gặp lỗi vào lúc nửa đêm.",
            "Yêu cầu từ khách hàng hoặc ban kinh doanh thường xuyên thay đổi khiến phải đập đi xây lại tính năng nhiều lần.",
            "Áp lực duy trì chất lượng mã nguồn sạch (Clean Code) trong khi bị ép về mặt tiến độ thời gian."
        ],
        "mini_case_study": {
            "scenario": "Bạn là lập trình viên Backend cho một ứng dụng ngân hàng số. Sau bản cập nhật mới lúc 20h tối, 5% người dùng gửi khiếu nại rằng họ bị trừ tiền trong tài khoản nhưng người thụ hưởng không nhận được tiền.",
            "questions": [
                {
                    "q": "Quy trình ứng phó kỹ thuật chuẩn mực đầu tiên là gì?",
                    "options": [
                        "Kích hoạt quy trình Rollback (khôi phục phiên bản trước), tạm khóa luồng giao dịch bị lỗi, kiểm tra nhật ký lỗi (Server Logs) và đối soát giao dịch ngân hàng.",
                        "Xóa bỏ cơ sở dữ liệu để người dùng không thấy số dư bị trừ nữa.",
                        "Tắt điện thoại và đợi đến sáng hôm sau lên văn phòng xử lý."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Nguyên tắc vàng của kỹ sư phần mềm là đảm bảo an toàn tài chính và dữ liệu khách hàng qua quy trình Rollback và kiểm tra đối soát nhật ký hệ thống."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Kỹ sư Phần mềm (Full-Stack / Backend Engineer)",
            "skill_tree": {
                "year_1_2": "Lập trình C/C++, Java hoặc Python; Nền tảng OOP, Cấu trúc dữ liệu & Giải thuật; Cơ sở dữ liệu quan hệ (PostgreSQL/MySQL), Git & GitHub.",
                "year_3": "Kiến trúc Microservices, RESTful API, Docker, Redis; Lập trình Frontend (React/Vue) hoặc Backend chuyên sâu (Node.js/Spring Boot); Chứng chỉ AWS Solutions Architect; IELTS 6.0+.",
                "year_4": "Hệ thống phân tán, CI/CD, Kubernetes, Thiết kế hệ thống chịu tải cao; Thực tập tại FPT, VNG, VNPT, Shopee; Hoàn thành đồ án tốt nghiệp với sản phẩm chạy thực tế."
            },
            "top_specialized_unis": [
                {"code": "FPT", "name": "Trường Đại học FPT", "strength": "100% sinh viên làm việc tại doanh nghiệp từ năm 3, chương trình chuẩn quốc tế, mạng lưới đối tác phần mềm toàn cầu."},
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Nền tảng kỹ thuật và tư duy thuật toán cực kỳ vững chắc, cựu sinh viên nắm giữ nhiều vị trí CTO/Lead Engineer."},
                {"code": "UIT", "name": "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", "strength": "Đào tạo bài bản theo quy trình kiểm thử phần mềm quốc tế, tỷ lệ sinh viên có việc làm trước khi tốt nghiệp trên 95%."},
                {"code": "PTIT", "name": "Học viện Công nghệ Bưu chính Viễn thông", "strength": "Rất mạnh về kỹ thuật mạng, ứng dụng đa nền tảng và hệ sinh thái phần mềm viễn thông."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 28,
            "risk_level": "Trung bình",
            "ai_augmented_skills": [
                "Sử dụng AI để tự động sinh Unit Test và tài liệu API (Swagger/OpenAPI).",
                "Kỹ năng kiểm tra mã nguồn tự động (Automated Code Review) và phân tích lỗ hổng bảo mật cùng AI.",
                "Tập trung vào tư duy thiết kế kiến trúc hệ thống (System Architecture) - phần việc AI chưa thể tự quyết định."
            ],
            "national_priority": "Chương trình Chuyển đổi số Quốc gia đến năm 2025, định hướng đến năm 2030 (QĐ 749/QĐ-TTg)"
        },
        "average_starting_salary": 13.0,
        "employment_rate": 98.4,
        "english_exit_req": "IELTS 6.0 hoặc TOEIC 650+"
    },

    "IT-CYBER": {
        "entry_roles": ["Chuyên viên Giám sát & Phân tích An ninh Mạng (SOC Analyst Tier 1)", "Chuyên viên Kiểm thử Xâm nhập & Đánh giá Lỗ hổng (Junior Pentester)", "Chuyên viên Bảo mật Ứng dụng (AppSec Specialist)"],
        "daily_work": "Giám sát nhật ký (logs) hệ thống mạng theo thời gian thực để phát hiện hành vi tấn công, quét lỗ hổng bảo mật của website/máy chủ, mô phỏng các kịch bản tấn công giả lập và phối hợp ứng cứu sự cố an ninh.",
        "starting_salary": "10 - 15 triệu VNĐ/tháng (Fresher)",
        "mid_salary": "25 - 45 triệu VNĐ/tháng",
        "labor_market_outlook": "Mọi ngân hàng, sàn thương mại điện tử, cơ quan chính phủ đều bắt buộc có đội ngũ an ninh thông tin theo luật định. Nhân sự có chứng chỉ CEH, Security+, OSCP luôn được săn đón với mức lương cao.",
        "skill_sandbox": {
            "course_name": "Nhập môn An ninh Mạng (Cisco Networking Academy) & Luyện kỹ năng CTF trên OverTheWire",
            "tryout_task": "Vào trang web OverTheWire.org (thử thách Bandit Level 0 - 3), sử dụng cửa sổ dòng lệnh Terminal để kết nối SSH vào máy chủ Linux và tìm mật mã ẩn giấu trong các tệp tin hệ thống.",
            "self_assessment_criteria": [
                "Bạn có tính cách cẩn trọng, tỉ mỉ, luôn để ý đến các nguy cơ bảo mật như mật khẩu yếu, đường link lừa đảo (phishing).",
                "Bạn có tính tò mò muốn 'bẻ khóa', tìm hiểu ngóc ngách xem một hệ thống hoạt động như thế nào và có lỗ hổng gì.",
                "Bạn có đạo đức tốt, thích đóng vai trò người bảo vệ sự an toàn cho tài sản số của người khác.",
                "Bạn không ngại làm việc với giao diện dòng lệnh đen trắng (Terminal) và các cấu hình mạng phức tạp."
            ],
            "self_assessment": "Nếu bạn yêu thích cảm giác làm 'hiệp sĩ gác cổng không gian mạng' và mê mẩn những câu đố hóc búa, An ninh mạng là sân chơi tuyệt vời dành cho bạn!"
        },
        "work_distribution": [
            {"task": "Giám sát nhật ký (Logs), Phân tích cảnh báo tấn công mạng", "percent": 40},
            {"task": "Quét lỗ hổng bảo mật & Thực hiện kiểm thử xâm nhập (Pentest)", "percent": 30},
            {"task": "Thiết lập tường lửa, Phân quyền & Cấu hình chính sách an ninh", "percent": 20},
            {"task": "Báo cáo tuân thủ an toàn thông tin & Đào tạo nhận thức bảo mật", "percent": 10}
        ],
        "pressure_challenges": [
            "Tâm lý luôn trong trạng thái trực chiến; sự cố an ninh có thể xảy ra bất kỳ lúc nào kể cả ngày nghỉ lễ, Tết.",
            "Gánh nặng trách nhiệm pháp lý rất cao khi rò rỉ dữ liệu nhạy cảm của hàng triệu khách hàng.",
            "Phải liên tục đối đầu với các tin tặc (Hackers) sử dụng các mã độc mới chưa từng được phát hiện (Zero-day)."
        ],
        "mini_case_study": {
            "scenario": "Vào lúc 2 giờ sáng, hệ thống cảnh báo SOC phát hiện lưu lượng truy cập bất thường từ một địa chỉ IP lạ đang cố gắng trích xuất cơ sở dữ liệu khách hàng qua một lỗ hổng SQL Injection trên trang web thanh toán.",
            "questions": [
                {
                    "q": "Biện pháp phòng thủ ngay lập tức bạn nên thực hiện là gì?",
                    "options": [
                        "Chặn ngay lập tức IP nguồn trên Web Application Firewall (WAF), cô lập máy chủ bị tấn công khỏi mạng nội bộ để bảo vệ các máy chủ khác và lưu lại toàn bộ gói tin để điều tra pháp y số.",
                        "Gửi email cho tin tặc yêu cầu họ dừng lại.",
                        "Đợi đến 8 giờ sáng khi đội ngũ lập trình web đi làm để nhờ họ sửa lỗ hổng."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Nguyên tắc phản ứng sự cố (Incident Response): Ngăn chặn lây lan (Containment) và thu thập bằng chứng pháp y (Forensics) là ưu tiên số 1 của chuyên viên an ninh mạng."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Chuyên viên An toàn Thông tin (Security Analyst / Pentester)",
            "skill_tree": {
                "year_1_2": "Kiến trúc mạng máy tính (TCP/IP), Hệ điều hành Linux/Windows Server, Lập trình kịch bản Python/Bash, Mật mã học cơ bản.",
                "year_3": "Kiểm thử xâm nhập (OWASP Top 10, Kali Linux, Metasploit), Giám sát SOC (SIEM, Wireshark, Splunk); Chứng chỉ quốc tế CompTIA Security+, CEH; IELTS 6.0+.",
                "year_4": "Phân tích mã độc, Ứng cứu sự cố an ninh (Incident Response), Chứng chỉ OSCP; Thực tập tại các ngân hàng, VNPT Cyber Immunity, Viettel Cyber Security."
            },
            "top_specialized_unis": [
                {"code": "PTIT", "name": "Học viện Công nghệ Bưu chính Viễn thông", "strength": "Được Bộ TT&TT giao nhiệm vụ đào tạo nguồn nhân lực trọng điểm về an toàn thông tin quốc gia."},
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Đội ngũ sinh viên đạt giải thưởng cao tại các cuộc thi an ninh mạng quốc tế (WhiteHat, Cyber SEA Game)."},
                {"code": "UIT", "name": "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", "strength": "Phòng thực hành thao trường mạng (Cyber Range) hiện đại bậc nhất khu vực phía Nam."},
                {"code": "UET", "name": "Trường Đại học Công nghệ - ĐHQGHN", "strength": "Mạnh về mật mã học, bảo mật hệ thống nhúng và mạng không dây."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 15,
            "risk_level": "Rất thấp",
            "ai_augmented_skills": [
                "Ứng dụng AI để phân tích hàng triệu dòng nhật ký hệ thống mỗi giây nhằm phát hiện hành vi dị thường.",
                "Nghiên cứu các cuộc tấn công lừa đảo thế hệ mới ứng dụng Deepfake và AI để xây dựng hàng rào phòng thủ.",
                "Kiểm thử bảo mật cho chính các ứng dụng và mô hình AI của doanh nghiệp (AI Red Teaming)."
            ],
            "national_priority": "Chiến lược An toàn Không gian mạng Quốc gia (QĐ 964/QĐ-TTg)"
        },
        "average_starting_salary": 14.5,
        "employment_rate": 99.1,
        "english_exit_req": "IELTS 6.0 hoặc VSTEP B2"
    },

    "IT-DS": {
        "entry_roles": ["Chuyên viên Phân tích Dữ liệu (Data Analyst)", "Chuyên viên Trực quan hóa Dữ liệu (BI Specialist)", "Kỹ sư Dữ liệu Sơ cấp (Junior Data Engineer)"],
        "daily_work": "Viết câu lệnh SQL trích xuất dữ liệu từ cơ sở dữ liệu lớn, làm sạch và xử lý dữ liệu khuyết thiếu bằng Python/Pandas, thiết kế bảng điều khiển trực quan (Dashboard trên Power BI/Tableau) phục vụ quyết định kinh doanh.",
        "starting_salary": "10 - 15 triệu VNĐ/tháng",
        "mid_salary": "22 - 38 triệu VNĐ/tháng",
        "labor_market_outlook": "Doanh nghiệp trong mọi lĩnh vực (bán lẻ, viễn thông, ngân hàng, y tế) đều chuyển đổi số dựa trên dữ liệu. Vị trí phân tích dữ liệu đang có tốc độ tăng trưởng tuyển dụng hàng đầu.",
        "skill_sandbox": {
            "course_name": "Google Data Analytics Professional Certificate & Nhập môn SQL căn bản (W3Schools)",
            "tryout_task": "Tải một bảng dữ liệu Excel về doanh số bán hàng của một chuỗi đồ uống, dùng tính năng Pivot Table và biểu đồ tròn/cột để tìm ra: Top 3 món trà sữa mang lại lợi nhuận cao nhất và ngày nào trong tuần có lượng khách đột biến.",
            "self_assessment_criteria": [
                "Bạn thích các con số thống kê và luôn muốn nhìn vào dữ liệu thực tế trước khi đưa ra kết luận thay vì cảm tính.",
                "Bạn thấy thích thú khi nhìn các biểu đồ trực quan, infographic màu sắc thể hiện xu hướng một cách rõ ràng.",
                "Bạn vừa có tư duy logic toán học, vừa có khả năng thấu hiểu góc nhìn kinh doanh để giải thích ý nghĩa con số.",
                "Bạn yêu thích việc sắp xếp bảng biểu, phân loại thông tin ngăn nắp và có hệ thống."
            ],
            "self_assessment": "Nếu bạn có niềm đam mê biến những con số vô hồn thành những câu chuyện chiến lược có sức thuyết phục, bạn sẽ tiến rất xa trong ngành Data Science!"
        },
        "work_distribution": [
            {"task": "Viết truy vấn SQL & Xử lý dữ liệu bằng Python", "percent": 45},
            {"task": "Thiết kế bảng điều khiển trực quan (Power BI / Tableau)", "percent": 25},
            {"task": "Phân tích xu hướng kinh doanh & Tìm kiếm Insights", "percent": 20},
            {"task": "Thuyết trình kết quả cho ban giám đốc", "percent": 10}
        ],
        "pressure_challenges": [
            "Dữ liệu thực tế thường bị bẩn, thiếu sót và phân tán ở nhiều hệ thống khác nhau; tốn tới 70% công sức chỉ để làm sạch dữ liệu.",
            "Áp lực phải đưa ra các đề xuất kinh doanh chính xác có thể kiểm chứng được qua doanh thu thực tế.",
            "Phải làm việc ở giữa hai thế giới: Kỹ thuật dữ liệu phức tạp và ngôn ngữ kinh doanh bình dân của các sếp."
        ],
        "mini_case_study": {
            "scenario": "Bạn là chuyên viên phân tích dữ liệu cho một chuỗi siêu thị. Dữ liệu cho thấy doanh số bán tã trẻ em tăng vọt vào các buổi chiều thứ Sáu, và một tỷ lệ lớn người mua tã cũng mua kèm bia lon.",
            "questions": [
                {
                    "q": "Bạn sẽ đề xuất chiến lược kinh doanh nào cho ban giám đốc siêu thị?",
                    "options": [
                        "Bố trí quầy bia lon ngay cạnh quầy tã trẻ em và tạo combo khuyến mãi chung vào chiều thứ Sáu để kích thích hành vi mua sắm của các ông bố trẻ sau giờ tan làm.",
                        "Lập tức cấm bán bia cùng tã vì không có mối liên quan nào.",
                        "Nghĩ rằng dữ liệu bị sai và xóa bỏ các dòng giao dịch đó."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Tư duy phân tích dữ liệu là biến các mối tương quan ẩn giấu trong hành vi khách hàng thành cơ hội gia tăng doanh thu cụ thể cho doanh nghiệp."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Chuyên viên Phân tích Dữ liệu (Data Analyst / BI Specialist)",
            "skill_tree": {
                "year_1_2": "Toán thống kê mô tả & Thống kê suy luận, Excel nâng cao, Ngôn ngữ truy vấn SQL (Subqueries, Window Functions), Trực quan hóa dữ liệu cơ bản.",
                "year_3": "Phân tích dữ liệu bằng Python (Pandas, Seaborn), Thiết kế Data Warehouse, Làm chủ công cụ Power BI hoặc Tableau; Chứng chỉ Microsoft Power BI Data Analyst (PL-300); IELTS 6.0+.",
                "year_4": "A/B Testing, Mô hình dự báo chuỗi thời gian, Phân tích chỉ số kinh doanh (LTV, CAC, Churn Rate); Thực tập tại các ngân hàng, sàn TMĐT hoặc tập đoàn bán lẻ."
            },
            "top_specialized_unis": [
                {"code": "NEU", "name": "Trường Đại học Kinh tế Quốc dân", "strength": "Viện CNTT & Kinh tế số dẫn đầu về đào tạo phân tích dữ liệu ứng dụng trực tiếp trong kinh doanh và tài chính."},
                {"code": "HCMUS", "name": "Trường ĐH Khoa học Tự nhiên - ĐHQG-HCM", "strength": "Thế mạnh tuyệt đối về toán học thống kê và nền tảng khoa học dữ liệu gốc."},
                {"code": "UEH", "name": "Đại học Kinh tế TP. Hồ Chí Minh", "strength": "Khoa Toán - Thống kê đào tạo rất thực tế, mạng lưới đối tác tài chính ngân hàng sâu rộng."},
                {"code": "PTIT", "name": "Học viện Công nghệ Bưu chính Viễn thông", "strength": "Đào tạo bài bản cả về hạ tầng dữ liệu lớn (Big Data) và công nghệ trực quan hóa."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 32,
            "risk_level": "Trung bình",
            "ai_augmented_skills": [
                "Sử dụng AI để tự động sinh câu truy vấn SQL phức tạp và làm sạch dữ liệu tự động.",
                "Kỹ năng kể chuyện bằng dữ liệu (Data Storytelling) để truyền cảm hứng cho người ra quyết định - điều AI không thể thay thế.",
                "Khả năng hiểu sâu bối cảnh thị trường và tư duy kinh doanh nhạy bén."
            ],
            "national_priority": "Chiến lược Dữ liệu Quốc gia đến năm 2030 (QĐ 142/QĐ-TTg)"
        },
        "average_starting_salary": 13.5,
        "employment_rate": 97.9,
        "english_exit_req": "IELTS 6.0 hoặc VSTEP B2"
    },

    "ENG-SEMI": {
        "entry_roles": ["Kỹ sư Thiết kế Vi mạch Số (Digital IC Design / RTL)", "Kỹ sư Kiểm thử Vi mạch (Verification Engineer)", "Kỹ sư Thiết kế Vật lý Vi mạch (Physical Layout Design)"],
        "daily_work": "Sử dụng ngôn ngữ mô tả phần cứng Verilog/SystemVerilog để thiết kế các khối chức năng của chip, chạy hàng triệu kịch bản mô phỏng kiểm tra lỗi logic, tối ưu hóa diện tích khuôn silicon và mức tiêu thụ điện năng của vi mạch.",
        "starting_salary": "14 - 20 triệu VNĐ/tháng (Thuộc nhóm cao nhất trong các ngành kỹ thuật)",
        "mid_salary": "30 - 65 triệu VNĐ/tháng",
        "labor_market_outlook": "Chiến lược quốc gia về bán dẫn cùng sự hiện diện của Synopsys, Marvell, Qualcomm, Amkor, Viettel tạo ra 'cơn khát' kỹ sư vi mạch với chế độ đãi ngộ vượt bậc.",
        "skill_sandbox": {
            "course_name": "Nhập môn Thiết kế Mạch Số & Ngôn ngữ Verilog (EDX/Coursera & CircuitVerse)",
            "tryout_task": "Vào trang CircuitVerse.org, dùng các cổng logic cơ bản (AND, OR, XOR) để lắp ráp và mô phỏng hoạt động của một bộ cộng 1-bit (Full Adder), kiểm tra bảng chân lý xem kết quả cộng 1 + 1 có ra nhị phân 10 (2) hay không.",
            "self_assessment_criteria": [
                "Bạn có đức tính cực kỳ tỉ mỉ và kiên nhẫn; bạn hiểu rằng một lỗi thiết kế chip siêu nhỏ có thể làm hỏng hàng triệu USD tiền sản xuất.",
                "Bạn yêu thích môn Vật lý (phần Bán dẫn, Dòng điện trong chất bán dẫn) và Toán logic (Đại số Boole).",
                "Bạn thích làm việc với những hệ thống tinh vi ở cấp độ nano và muốn đóng góp vào công nghệ cốt lõi của thế giới (smartphone, máy tính, AI chip).",
                "Bạn có khả năng tập trung cao độ, chịu khó đọc hiểu tài liệu chuẩn quốc tế bằng tiếng Anh."
            ],
            "self_assessment": "Nếu bạn muốn dấn thân vào ngành công nghệ mũi nhọn có thu nhập nghìn đô và vị thế toàn cầu, Vi mạch Bán dẫn là lựa chọn xứng đáng nhất!"
        },
        "work_distribution": [
            {"task": "Viết mã mô tả phần cứng (Verilog/VHDL) & Thiết kế logic", "percent": 45},
            {"task": "Mô phỏng kiểm thử lỗi vi mạch (Verification & Simulation)", "percent": 35},
            {"task": "Thiết kế vật lý (Physical Layout) & Tối ưu diện tích chip", "percent": 15},
            {"task": "Họp phối hợp kỹ thuật với nhóm thiết kế đa quốc gia", "percent": 5}
        ],
        "pressure_challenges": [
            "Mỗi con chip sản xuất thử nghiệm (Tape-out) tốn từ vài trăm nghìn đến hàng triệu USD; chỉ một lỗi logic nhỏ có thể làm phế toàn bộ mẻ chip.",
            "Quy trình kiểm thử đòi hỏi hàng triệu kịch bản mô phỏng kiểm tra gắt gao; tính tỉ mỉ và kiên nhẫn phải ở mức tuyệt đối.",
            "Tài liệu kỹ thuật và tiêu chuẩn bán dẫn 100% bằng tiếng Anh với các thuật ngữ chuyên sâu cực kỳ phức tạp."
        ],
        "mini_case_study": {
            "scenario": "Trong quá trình chạy mô phỏng kiểm thử khối xử lý số học (ALU) cho một vi điều khiển 32-bit, bạn phát hiện có 1 trường hợp tràn số (Overflow) hiếm gặp chỉ xảy ra khi thực hiện phép tính nhân với 2 số âm lớn liên tiếp.",
            "questions": [
                {
                    "q": "Thái độ làm việc chuẩn mực của kỹ sư thiết kế vi mạch là gì?",
                    "options": [
                        "Lập tức ghi nhận lỗi, viết kịch bản tái hiện lỗi (Corner Case) và sửa đổi logic mã Verilog để đảm bảo không một lỗi nào lọt qua khâu sản xuất.",
                        "Bỏ qua vì nghĩ trường hợp này rất hiếm khi người dùng thực tế gặp phải.",
                        "Đổ lỗi cho phần mềm mô phỏng bị trục trặc."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Tư duy không khoan nhượng với sai sót (Zero-tolerance for defects) là phẩm chất số 1 của kỹ sư bán dẫn vì chi phí sửa chữa chip sau khi xuất xưởng là không thể đảo ngược."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Kỹ sư Thiết kế Vi mạch (IC Design / Verification Engineer)",
            "skill_tree": {
                "year_1_2": "Vật lý bán dẫn, Lý thuyết mạch điện tử, Đại số Boole và Thiết kế logic số; Lập trình C/C++ và ngôn ngữ kịch bản Linux (Bash/Tcl/Python).",
                "year_3": "Ngôn ngữ mô tả phần cứng Verilog/SystemVerilog, Kiến trúc máy tính nâng cao (RISC-V/ARM), Kiểm thử vi mạch theo chuẩn UVM; Làm quen với phần mềm Synopsys / Cadence; IELTS 6.5+.",
                "year_4": "Thiết kế vật lý (Synthesis, Place & Route), Tối ưu công suất (Low-power design); Thực tập tại Marvell, Synopsys, Qualcomm, Amkor, Viettel; Tham gia dự án thiết kế chip mẫu (Tape-out)."
            },
            "top_specialized_unis": [
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Trung tâm nghiên cứu vi mạch bán dẫn quốc gia, hợp tác trực tiếp với Synopsys, Cadence, Foxconn."},
                {"code": "HCMUT", "name": "Trường Đại học Bách khoa - ĐHQG-HCM", "strength": "Cái nôi đào tạo kỹ sư thiết kế vi mạch hàng đầu phương Nam, cựu sinh viên chiếm tỷ lệ lớn tại các hãng chip tại TP.HCM."},
                {"code": "UET", "name": "Trường Đại học Công nghệ - ĐHQGHN", "strength": "Đào tạo xuất sắc về vật lý kỹ thuật, bán dẫn và vi hệ thống (MEMS)."},
                {"code": "DUT", "name": "Trường ĐH Bách khoa - ĐH Đà Nẵng", "strength": "Được chính phủ quy hoạch thành trung tâm đào tạo nhân lực bán dẫn trọng điểm khu vực miền Trung."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 12,
            "risk_level": "Rất thấp",
            "ai_augmented_skills": [
                "Ứng dụng AI vào các công cụ EDA để tự động hóa khâu tối ưu vị trí linh kiện (Floorplanning) và chạy dây (Routing).",
                "Sử dụng mô hình ngôn ngữ hỗ trợ sinh kịch bản kiểm thử (Testbench Generation).",
                "Thiết kế các kiến trúc vi mạch chuyên dụng tăng tốc tính toán cho mô hình AI (AI Accelerators / NPU)."
            ],
            "national_priority": "Chiến lược Phát triển Công nghiệp Bán dẫn Việt Nam đến năm 2030 (QĐ 1018/QĐ-TTg)"
        },
        "average_starting_salary": 17.5,
        "employment_rate": 99.5,
        "english_exit_req": "IELTS 6.5 hoặc VSTEP B2"
    },

    "ENG-ROBOT": {
        "entry_roles": ["Kỹ sư Lập trình Điều khiển PLC & Tự động hóa", "Kỹ sư Thiết kế Hệ thống Cơ điện tử & Robot", "Kỹ sư Hệ thống Nhúng & Vi điều khiển (Embedded Engineer)"],
        "daily_work": "Lập trình điều khiển cánh tay robot công nghiệp, thiết kế mạch phần cứng vi điều khiển (STM32/ESP32), tích hợp cảm biến và động cơ servo, bảo trì vận hành dây chuyền sản xuất tự động trong nhà máy.",
        "starting_salary": "10 - 14 triệu VNĐ/tháng",
        "mid_salary": "20 - 35 triệu VNĐ/tháng",
        "labor_market_outlook": "Cách mạng công nghiệp 4.0 và làn sóng nhà máy thông minh (Smart Factory) của Samsung, Foxconn, Lego tại Việt Nam thúc đẩy nhu cầu kỹ sư tự động hóa tăng vọt.",
        "skill_sandbox": {
            "course_name": "Lập trình Vi mạch Arduino & Mô phỏng Mạch Điện tử trên Tinkercad Circuits",
            "tryout_task": "Vào trang web Tinkercad.com (mục Circuits), kéo thả một bo mạch Arduino Uno, 1 cảm biến khoảng cách siêu âm và 1 đèn LED, rồi viết 15 dòng mã C/C++ để đèn LED tự động chớp nháy khi phát hiện vật cản dưới 30cm.",
            "self_assessment_criteria": [
                "Từ nhỏ bạn đã thích tháo lắp đồ chơi điện tử, tò mò xem các bánh răng, mô tơ và mạch điện bên trong hoạt động ra sao.",
                "Bạn không chỉ thích viết code trên máy tính mà thích nhìn thấy sản phẩm vật lý ngoài đời thực chuyển động theo ý mình.",
                "Bạn học khá các môn Vật lý (phần Điện xoay chiều, Cơ học) và thích các dự án STEM/chế tạo khoa học.",
                "Bạn có tính cẩn thận, chịu khó cầm mỏ hàn, tua-vít và kiên nhẫn đo đạc kiểm tra từng mối nối linh kiện."
            ],
            "self_assessment": "Nếu bạn luôn mơ ước chế tạo ra những cỗ máy thông minh phục vụ con người, ngành Kỹ thuật Robot & Cơ điện tử chính là bệ phóng cho bạn!"
        },
        "work_distribution": [
            {"task": "Lập trình điều khiển cánh tay robot & Lập trình PLC", "percent": 40},
            {"task": "Thiết kế mạch phần cứng, Vi điều khiển & Lắp ráp cảm biến", "percent": 30},
            {"task": "Kiểm tra vận hành dây chuyền & Xử lý sự cố máy móc tại nhà máy", "percent": 20},
            {"task": "Soạn thảo tài liệu hướng dẫn vận hành & An toàn lao động", "percent": 10}
        ],
        "pressure_challenges": [
            "Môi trường làm việc thực tế thường ở các nhà xưởng công nghiệp (ồn ào, bụi bặm, nhiệt độ cao).",
            "Sự cố dây chuyền sản xuất tự động dừng lại gây thiệt hại hàng trăm triệu đồng mỗi giờ, đòi hỏi kỹ sư phải xử lý sự cố thần tốc.",
            "Phải tích hợp đồng thời 3 lĩnh vực: Cơ khí chính xác, Mạch điện tử và Phần mềm điều khiển."
        ],
        "mini_case_study": {
            "scenario": "Dây chuyền đóng gói bánh kẹo tự động tại nhà máy bỗng nhiên bị lệch cánh tay hút chân không, khiến 10% gói bánh bị bẹp vỏ trước khi vào thùng carton.",
            "questions": [
                {
                    "q": "Bạn sẽ tiến hành kiểm tra theo thứ tự nào?",
                    "options": [
                        "Kiểm tra áp suất van hút chân không và cảm biến định vị quang học xem có bị bụi bẩn che khuất không, sau đó kiểm tra thông số tọa độ gắp trên phần mềm điều khiển PLC.",
                        "Dùng búa gõ mạnh vào cánh tay robot xem có hoạt động lại không.",
                        "Yêu cầu công nhân dừng ăn cơm và chờ hết ca làm việc."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Tư duy kỹ sư cơ điện tử là kiểm tra từ phần cứng vật lý (khí nén, cảm biến) trước khi can thiệp vào thuật toán phần mềm."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Kỹ sư Robot & Tự động hóa (Automation & Robotics Engineer)",
            "skill_tree": {
                "year_1_2": "Cơ học kỹ thuật, Vật lý điện từ, Thiết kế 3D SolidWorks, Lập trình C/C++ vi điều khiển cơ bản (Arduino, STM32).",
                "year_3": "Lập trình PLC (Siemens, Mitsubishi), Hệ thống khí nén - thủy lực, Xử lý ảnh công nghiệp (OpenCV), Giao thức mạng công nghiệp (Modbus, Profinet); IELTS 5.5+.",
                "year_4": "Hệ điều hành Robot (ROS), Tích hợp Robot công nghiệp (ABB, KUKA, Universal Robots); Thực tập tại Samsung, Lego, VinFast, Foxconn."
            },
            "top_specialized_unis": [
                {"code": "HCMUTE", "name": "Trường ĐH Sư phạm Kỹ thuật TP.HCM", "strength": "Cực kỳ mạnh về đào tạo thực hành cơ điện tử và robot công nghiệp, phòng lab tự động hóa hàng đầu."},
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Đội ngũ nghiên cứu cơ điện tử hàng đầu, sinh viên nhiều năm vô địch Robocon toàn quốc và châu Á."},
                {"code": "HaUI", "name": "Trường Đại học Công nghiệp Hà Nội", "strength": "Mạng lưới đối tác doanh nghiệp sản xuất FDI phong phú, tỷ lệ sinh viên có việc làm ngay khi tốt nghiệp rất cao."},
                {"code": "HCMUT", "name": "Trường Đại học Bách khoa - ĐHQG-HCM", "strength": "Đào tạo kỹ sư cơ điện tử toàn diện cả về nghiên cứu lý thuyết lẫn ứng dụng công nghiệp."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 16,
            "risk_level": "Rất thấp",
            "ai_augmented_skills": [
                "Tích hợp thị giác máy tính AI (Computer Vision) giúp cánh tay robot nhận diện và phân loại sản phẩm linh hoạt.",
                "Áp dụng học máy dự đoán bảo trì hỏng hóc máy móc (Predictive Maintenance) trước khi sự cố xảy ra.",
                "Lập trình xe tự hành AGV/AMR điều hướng thông minh trong kho hàng nhà máy."
            ],
            "national_priority": "Quy hoạch phát triển Công nghiệp Chế biến, Chế tạo và Tự động hóa đến năm 2030"
        },
        "average_starting_salary": 12.5,
        "employment_rate": 98.0,
        "english_exit_req": "TOEIC 550+ hoặc VSTEP B1"
    },

    "ENG-AUTO": {
        "entry_roles": ["Kỹ sư R&D Thiết kế Hệ thống Ô tô/Xe điện", "Kỹ sư Hiệu chỉnh & Chẩn đoán Điện tử Ô tô", "Kỹ sư Giám sát Dây chuyền Lắp ráp Ô tô", "Cố vấn Dịch vụ Kỹ thuật Ô tô"],
        "daily_work": "Sử dụng phần mềm CAD/CATIA dựng mô hình cơ khí xe hơi, phân tích mô phỏng khí động học, kiểm tra hoạt động của bộ điều khiển động cơ (ECU) và hệ thống quản lý pin xe điện (BMS), chẩn đoán mã lỗi thông qua thiết bị quét OBD-II.",
        "starting_salary": "9.5 - 14 triệu VNĐ/tháng",
        "mid_salary": "20 - 35 triệu VNĐ/tháng",
        "labor_market_outlook": "Cuộc cách mạng chuyển đổi sang xe điện (EV) và xe thông minh của VinFast, Hyundai, Toyota mở ra cơ hội việc làm khổng lồ cho kỹ sư am hiểu tích hợp giữa cơ khí truyền thống và hệ thống điều khiển điện tử.",
        "skill_sandbox": {
            "course_name": "Nguyên lý Cấu tạo Ô tô & Nhập môn Thiết kế Cơ khí 3D (SolidWorks Foundation)",
            "tryout_task": "Tìm hiểu sơ đồ cấu tạo một khối pin xe điện hoặc động cơ đốt trong 4 kỳ, vẽ lại sơ đồ truyền động từ nguồn năng lượng đến bánh xe và giải thích vai trò của bộ vi sai khi xe vào cua.",
            "self_assessment_criteria": [
                "Bạn có niềm đam mê đặc biệt với xe cộ: bạn nhận diện được các dòng xe ngoài đường, thích tìm hiểu thông số mã lực, mô-men xoắn và công nghệ an toàn.",
                "Bạn không ngại lấm lem dầu mỡ, thích cầm cờ-lê, tua-vít tự tay sửa chữa xe máy, xe đạp hay các thiết bị cơ khí.",
                "Bạn có tư duy hình học không gian 3D tốt và học khá môn Vật lý (Cơ học và Nhiệt học).",
                "Bạn hào hứng với các công nghệ xe điện, pin lithium và tính năng tự hành (ADAS)."
            ],
            "self_assessment": "Nếu tiếng động cơ và những chiếc xe hiện đại làm tim bạn đập nhanh, Kỹ thuật Ô tô chính là nơi biến niềm đam mê của bạn thành sự nghiệp vững vàng!"
        },
        "work_distribution": [
            {"task": "Chẩn đoán hệ thống điện tử & Kiểm tra pin/động cơ", "percent": 40},
            {"task": "Thiết kế cơ khí 3D (CAD/CATIA) & Mô phỏng", "percent": 30},
            {"task": "Thử nghiệm thực địa & Kiểm tra an toàn xe", "percent": 20},
            {"task": "Soạn quy trình bảo dưỡng & Làm việc với khách hàng", "percent": 10}
        ],
        "pressure_challenges": [
            "Công việc thường xuyên tiếp xúc với dầu mỡ, phụ tùng nặng và tiếng ồn trong xưởng bảo dưỡng hoặc nhà máy.",
            "Trách nhiệm an toàn tính mạng cực kỳ lớn; một lỗi siết ốc hay phanh xe có thể gây nguy hiểm cho người lái.",
            "Áp lực chuyển giao công nghệ cấp tốc từ động cơ đốt trong truyền thống sang hệ thống điện áp cao của xe điện (EV)."
        ],
        "mini_case_study": {
            "scenario": "Một chiếc xe điện sau khi sạc nhanh tại trạm sạc báo đèn cảnh báo lỗi nhiệt độ pin (Battery Overheat) và tự động giới hạn tốc độ xe dưới 30km/h để bảo vệ an toàn.",
            "questions": [
                {
                    "q": "Bạn sẽ tiến hành kiểm tra bước nào trước tiên bằng máy chẩn đoán?",
                    "options": [
                        "Đọc mã lỗi DTC từ bộ điều khiển BMS, kiểm tra mức nước làm mát pin và hoạt động của bơm tuần hoàn nhiệt độ.",
                        "Thay ngay toàn bộ khối pin mới mà không cần kiểm tra cảm biến.",
                        "Khuyên khách hàng cứ tiếp tục lái xe với tốc độ tối đa."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Quy trình chẩn đoán điện tử ô tô hiện đại luôn bắt đầu từ việc đọc dữ liệu thời gian thực của cảm biến (Live Data) trước khi tháo lắp vật lý."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Kỹ sư Ô tô & Xe điện Thông minh (Automotive / EV Engineer)",
            "skill_tree": {
                "year_1_2": "Vẽ kỹ thuật cơ khí, Sức bền vật liệu, Nhiệt động lực học; Cấu tạo gầm, động cơ và hệ thống truyền lực ô tô.",
                "year_3": "Hệ thống điện - điện tử ô tô, Mạng CAN-bus, Quản trị pin xe điện (BMS), Lập trình vi điều khiển ô tô; IELTS 5.5+.",
                "year_4": "Hệ thống an toàn chủ động ADAS, Xe tự hành, Chẩn đoán chuyên sâu OBD-II; Thực tập tại VinFast, Thaco, Toyota, Hyundai."
            },
            "top_specialized_unis": [
                {"code": "HCMUTE", "name": "Trường ĐH Sư phạm Kỹ thuật TP.HCM", "strength": "Xưởng thực hành ô tô hiện đại hàng đầu cả nước, đối tác chiến lược của VinFast, Toyota."},
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Viện Cơ khí Động lực đào tạo chuyên sâu về nghiên cứu động cơ, khí động học và xe điện."},
                {"code": "UTC", "name": "Trường Đại học Giao thông Vận tải", "strength": "Bề dày truyền thống về đầu máy toa xe, ô tô và phương tiện giao thông thông minh."},
                {"code": "HaUI", "name": "Trường Đại học Công nghiệp Hà Nội", "strength": "Cực kỳ mạnh về đào tạo kỹ sư công nghệ ô tô thực chiến, tỷ lệ việc làm cao."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 22,
            "risk_level": "Thấp",
            "ai_augmented_skills": [
                "Lập trình thuật toán tự hành ADAS và thị giác máy tính nhận diện làn đường, vật cản.",
                "Sử dụng AI phân tích dữ liệu xe từ xa (Telematics) để dự đoán thời điểm bảo dưỡng định kỳ.",
                "Tối ưu hóa chiến lược quản lý năng lượng pin xe điện bằng học máy."
            ],
            "national_priority": "Chiến lược Phát triển Ngành Công nghiệp Ô tô Việt Nam đến năm 2030, tầm nhìn 2045"
        },
        "average_starting_salary": 12.0,
        "employment_rate": 97.5,
        "english_exit_req": "TOEIC 550+ hoặc VSTEP B1"
    },

    "ENG-ARCH": {
        "entry_roles": ["Kiến trúc sư Thiết kế Ý tưởng (Concept Architect)", "Nhà Thiết kế Nội thất & Không gian Sống (Interior Designer)", "Chuyên viên Diễn họa 3D Kiến trúc (3D Visualizer)", "Giám sát Tác giả & Quản lý Dự án Thi công"],
        "daily_work": "Lắng nghe nhu cầu khách hàng, phác thảo ý tưởng không gian bằng tay, sử dụng phần mềm AutoCAD/Revit/SketchUp dựng mô hình 3D, phối vật liệu - màu sắc - ánh sáng, xuất bản vẽ kỹ thuật thi công và đi thực địa giám sát công trình.",
        "starting_salary": "9 - 13 triệu VNĐ/tháng (Fresher)",
        "mid_salary": "20 - 38 triệu VNĐ/tháng (tăng mạnh với các hợp đồng thiết kế độc lập)",
        "labor_market_outlook": "Tốc độ đô thị hóa nhanh và nhu cầu nâng cao chất lượng không gian sống (nhà ở, quán cafe, khách sạn, văn phòng) khiến nhu cầu tuyển dụng kiến trúc sư và nhà thiết kế nội thất có gu thẩm mỹ cao luôn dồi dào.",
        "skill_sandbox": {
            "course_name": "Nhập môn Phác thảo Bố cục Kiến trúc & Vẽ Mặt bằng Nội thất Cơ bản (Floorplanner/SketchUp)",
            "tryout_task": "Lấy một tờ giấy A4 hoặc dùng công cụ online miễn phí (Floorplanner.com), đo đạc và phác thảo mặt bằng phòng ngủ 15m² của bạn: bố trí lại vị trí giường ngủ, bàn học, tủ quần áo và cửa sổ sao cho đón được ánh sáng tự nhiên tốt nhất và lối đi lại thông thoáng nhất.",
            "self_assessment_criteria": [
                "Bạn có thói quen quan sát cách bài trí không gian, ánh sáng, màu sắc mỗi khi bước vào một quán cà phê, nhà hàng hay một ngôi nhà mới.",
                "Bạn có khả năng hình dung không gian 3D tốt (khi nhìn vào một sơ đồ phẳng 2D, bạn tưởng tượng ngay ra căn phòng thực tế trông như thế nào).",
                "Bạn vừa có năng khiếu mỹ thuật, yêu cái đẹp, vừa có tư duy thực tế về tính tiện dụng, an toàn và kích thước tỷ lệ.",
                "Bạn có tính kiên nhẫn cao, sẵn sàng ngồi hàng giờ vẽ tay, làm mô hình giấy và thoải mái tiếp thu góp ý để chỉnh sửa bản vẽ nhiều lần."
            ],
            "self_assessment": "Nếu bạn luôn khao khát kiến tạo nên những không gian sống tiện nghi, truyền cảm hứng và lưu dấu ấn cá nhân qua từng công trình, ngành Kiến trúc & Nội thất sinh ra dành cho bạn!"
        },
        "work_distribution": [
            {"task": "Dựng hình 3D (SketchUp/Revit/3ds Max) & Render phối cảnh", "percent": 40},
            {"task": "Khai triển hồ sơ bản vẽ kỹ thuật thi công (AutoCAD)", "percent": 30},
            {"task": "Gặp gỡ khách hàng, Khảo sát hiện trạng & Giám sát công trình", "percent": 20},
            {"task": "Lựa chọn vật liệu, Lập dự toán chi phí thi công", "percent": 10}
        ],
        "pressure_challenges": [
            "Áp lực 'sửa bản vẽ theo ý khách hàng' nhiều lần đến kiệt sức; khách hàng thường muốn thay đổi thiết kế vào phút chót.",
            "Mùa chạy đồ án tốt nghiệp và bàn giao hồ sơ thi công thường xuyên phải thức trắng đêm (thức khuya là đặc thù ngành kiến trúc).",
            "Vừa phải bay bổng nghệ thuật, vừa phải tuân thủ nghiêm ngặt quy chuẩn xây dựng, phòng cháy chữa cháy và kết cấu chịu lực."
        ],
        "mini_case_study": {
            "scenario": "Khách hàng muốn làm một giếng trời lớn ở giữa phòng khách nhà phố 4 tầng, nhưng kỹ sư kết cấu cảnh báo vị trí đó sẽ cắt ngang dầm chính chịu lực của ngôi nhà.",
            "questions": [
                {
                    "q": "Bạn xử lý mâu thuẫn này thế nào để vừa đẹp vừa an toàn?",
                    "options": [
                        "Phối hợp với kỹ sư kết cấu để dịch chuyển giếng trời sang ô sàn bên cạnh hoặc bố trí lại hệ dầm chịu lực phụ, vừa lấy sáng tự nhiên vừa đảm bảo 100% độ an toàn kết cấu.",
                        "Cứ đập bỏ dầm chính theo ý khách hàng mà không cần quan tâm kết cấu.",
                        "Mắng khách hàng là không biết gì về kiến trúc và từ chối thiết kế."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Kiến trúc sư giỏi là người biết dung hòa giữa thẩm mỹ không gian và các giới hạn kỹ thuật kết cấu an toàn bằng giải pháp sáng tạo."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Kiến trúc sư Công trình & Nội thất (Architect / Interior Designer)",
            "skill_tree": {
                "year_1_2": "Hình họa, Vẽ mỹ thuật chì/màu, Lịch sử kiến trúc, Nguyên lý thiết kế kiến trúc dân dụng, AutoCAD 2D.",
                "year_3": "Dựng hình 3D (SketchUp, Revit BIM, 3ds Max, Lumion), Cấu tạo kiến trúc & Vật liệu xây dựng; Đồ án nhà ở, công trình công cộng; IELTS 5.5+.",
                "year_4": "Quy chuẩn PCCC, Thiết kế bền vững, Quản lý dự án kiến trúc; Thực tập tại các văn phòng kiến trúc (Vo Trong Nghia Architects, MIA Design Studio, Baumschlager Eberle)."
            },
            "top_specialized_unis": [
                {"code": "HAU", "name": "Trường Đại học Kiến trúc Hà Nội", "strength": "Cái nôi đào tạo kiến trúc sư hàng đầu miền Bắc, bề dày giải thưởng Loa Thành xuất sắc."},
                {"code": "UAH", "name": "Trường Đại học Kiến trúc TP. Hồ Chí Minh", "strength": "Top 1 phương Nam về kiến trúc, nội thất và quy hoạch đô thị, môi trường sáng tạo bùng nổ."},
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Khoa Kiến trúc kết hợp xuất sắc giữa nghệ thuật tạo hình và nền tảng kỹ thuật công trình vững chắc."},
                {"code": "DUT", "name": "Trường ĐH Bách khoa - ĐH Đà Nẵng", "strength": "Trung tâm đào tạo kiến trúc sư cảnh quan và công trình nhiệt đới lớn nhất miền Trung."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 30,
            "risk_level": "Trung bình",
            "ai_augmented_skills": [
                "Sử dụng AI sinh ảnh (Midjourney, Stable Diffusion) để tìm kiếm ý tưởng phối cảnh sơ phác (Moodboard) trong 5 phút.",
                "Ứng dụng Generative Design trong Revit để tự động tối ưu hóa hướng nắng, hướng gió và tiết kiệm năng lượng công trình.",
                "Nâng cao năng lực thẩm mỹ, thấu cảm tâm lý khách hàng và kiểm soát chi tiết thi công thực tế."
            ],
            "national_priority": "Quy hoạch Đô thị Xanh và Phát triển Công trình Bền vững Quốc gia"
        },
        "average_starting_salary": 11.5,
        "employment_rate": 96.5,
        "english_exit_req": "TOEIC 500+ hoặc VSTEP B1"
    },

    "ECO-IB": {
        "entry_roles": ["Chuyên viên Xuất Nhập khẩu (Import-Export Specialist)", "Chuyên viên Quản trị Đơn hàng Quốc tế (Merchandiser)", "Chuyên viên Phát triển Thị trường Toàn cầu (Global Market Development)"],
        "daily_work": "Tìm kiếm đối tác mua bán nước ngoài, soạn thảo và đàm phán hợp đồng ngoại thương, mở L/C thanh toán quốc tế, làm việc với hãng tàu và hải quan để hoàn tất thủ tục thông quan hàng hóa xuất nhập khẩu.",
        "starting_salary": "9.5 - 14 triệu VNĐ/tháng",
        "mid_salary": "22 - 38 triệu VNĐ/tháng",
        "labor_market_outlook": "Việt Nam là một trong những nền kinh tế có độ mở thương mại lớn nhất thế giới. Các tập đoàn đa quốc gia và doanh nghiệp FDI liên tục săn đón nhân sự thông thạo ngoại ngữ và luật thương mại quốc tế.",
        "skill_sandbox": {
            "course_name": "Nhập môn Điều kiện Thương mại Quốc tế Incoterms 2020 & Soạn thảo Hợp đồng Ngoại thương",
            "tryout_task": "Chọn một mặt hàng thế mạnh của Việt Nam (như cà phê, sầu riêng, hạt điều), lập một checklist gồm 5 bước cốt lõi từ khâu đóng gói, kiểm dịch, làm thủ tục hải quan đến vận chuyển để xuất khẩu 1 container hàng sang châu Âu.",
            "self_assessment_criteria": [
                "Bạn có tính cách năng động, thích giao lưu kết nối với những người đến từ các nền văn hóa khác nhau.",
                "Bạn yêu thích môn Tiếng Anh (hoặc ngoại ngữ khác) và muốn sử dụng ngoại ngữ hàng ngày trong công việc.",
                "Bạn nhạy bén với tin tức thời sự kinh tế thế giới, tỷ giá ngoại tệ và các hiệp định thương mại.",
                "Bạn có khả năng đàm phán, thương lượng khéo léo và biết cách bảo vệ lợi ích của tổ chức trong các thỏa thuận."
            ],
            "self_assessment": "Nếu bạn khao khát đưa sản phẩm Việt Nam vươn tầm thế giới và làm việc trong môi trường đa văn hóa chuyên nghiệp, Kinh doanh Quốc tế là bệ phóng hoàn hảo!"
        },
        "work_distribution": [
            {"task": "Soạn thảo chứng từ xuất nhập khẩu (B/L, Invoice, Packing List, C/O)", "percent": 40},
            {"task": "Giao tiếp, Đàm phán giá & Điều khoản với đối tác nước ngoài", "percent": 30},
            {"task": "Làm việc với Hải quan, Hãng tàu & Kho hàng", "percent": 20},
            {"task": "Theo dõi thanh toán quốc tế (L/C, T/T) & Đối soát chi phí", "percent": 10}
        ],
        "pressure_challenges": [
            "Chênh lệch múi giờ với đối tác Mỹ/châu Âu; thường xuyên phải kiểm tra email và phản hồi đối tác vào ban đêm.",
            "Rủi ro chậm trễ tàu biển, tắc biên hoặc hàng hóa bị giữ lại kiểm dịch; thiệt hại tiền lưu kho (Demurrage) tính theo từng ngày.",
            "Biến động tỷ giá hối đoái và chi phí cước tàu container quốc tế có thể làm đảo lộn lợi nhuận hợp đồng."
        ],
        "mini_case_study": {
            "scenario": "Một lô hàng 2 container dệt may xuất khẩu sang Đức đến cảng Hamburg nhưng bị hải quan sở tại giữ lại vì thiếu giấy chứng nhận xuất xứ form EUR.1 để được hưởng thuế suất 0% theo hiệp định EVFTA.",
            "questions": [
                {
                    "q": "Bạn sẽ xử lý tình huống phát sinh này ra sao?",
                    "options": [
                        "Liên hệ khẩn cấp với Bộ Công Thương xin cấp bổ sung C/O điện tử (e-C/O) gửi hỏa tốc cho đại lý tại Đức để thông quan, giảm tối đa phí lưu bãi.",
                        "Bỏ luôn 2 container hàng để khỏi tốn công xử lý.",
                        "Tranh cãi với hải quan Đức và yêu cầu họ tự tìm hiểu luật."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Chuyên viên xuất nhập khẩu giỏi luôn nắm vững quy tắc xuất xứ hiệp định thương mại và phản ứng nhanh nhạy với các thủ tục chứng từ điện tử quốc tế."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Chuyên viên Kinh doanh Quốc tế & Xuất Nhập Khẩu",
            "skill_tree": {
                "year_1_2": "Kinh tế vi mô/vĩ mô, Tiếng Anh thương mại, Luật thương mại quốc tế, Nguyên lý quản trị kinh doanh.",
                "year_3": "Incoterms 2020, Vận tải & Bảo hiểm quốc tế, Thanh toán quốc tế (UCP 600, L/C), Thủ tục hải quan điện tử VNACCS/VCIS; IELTS 6.5+.",
                "year_4": "Đàm phán ngoại thương, Quản trị chuỗi cung ứng toàn cầu; Thực tập tại các tập đoàn logistics quốc tế (DHL, Maersk, Kuehne+Nagel) hoặc doanh nghiệp xuất nhập khẩu."
            },
            "top_specialized_unis": [
                {"code": "FTU", "name": "Trường Đại học Ngoại thương", "strength": "Thương hiệu số 1 cả nước về Kinh doanh quốc tế, mạng lưới cựu sinh viên toàn cầu, tiếng Anh vượt trội."},
                {"code": "NEU", "name": "Trường Đại học Kinh tế Quốc dân", "strength": "Khoa Kinh doanh quốc tế đào tạo bài bản, rất mạnh về tư duy chiến lược thương mại."},
                {"code": "UEH", "name": "Đại học Kinh tế TP. Hồ Chí Minh", "strength": "Đầu tàu đào tạo kinh tế đối ngoại phía Nam, kết nối sâu rộng với các hiệp hội xuất nhập khẩu."},
                {"code": "DAV", "name": "Học viện Ngoại giao", "strength": "Thế mạnh về đàm phán ngoại giao kinh tế và luật pháp thương mại quốc tế."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 25,
            "risk_level": "Thấp",
            "ai_augmented_skills": [
                "Ứng dụng AI tự động quét và đối chiếu tính hợp lệ của bộ chứng từ xuất nhập khẩu.",
                "Sử dụng công cụ dịch thuật AI chuyên ngành kết hợp thẩm định ngữ cảnh pháp lý hợp đồng.",
                "Kỹ năng đàm phán trực tiếp và xây dựng mối quan hệ tin cậy giữa các nền văn hóa (Human-to-Human trust)."
            ],
            "national_priority": "Chiến lược Xuất Nhập khẩu Hàng hóa đến năm 2030 (QĐ 493/QĐ-TTg)"
        },
        "average_starting_salary": 12.5,
        "employment_rate": 98.2,
        "english_exit_req": "IELTS 6.5 hoặc TOEIC 750+"
    },

    "ECO-LOG": {
        "entry_roles": ["Chuyên viên Điều độ & Khai thác Đội xe Vận tải", "Chuyên viên Vận hành Kho Bãi (Warehouse Operations)", "Chuyên viên Kế hoạch Cung ứng (Supply Chain Planner)", "Nhân viên Giao nhận Hiện trường (Customs Field Staff)"],
        "daily_work": "Lên kế hoạch vận chuyển hàng hóa tối ưu tuyến đường, quản lý mức tồn kho an toàn, giám sát việc bốc dỡ hàng tại cảng biển/sân bay, xử lý nhanh các sự cố tắc nghẽn giao hàng hoặc chậm trễ thông quan.",
        "starting_salary": "9 - 13.5 triệu VNĐ/tháng",
        "mid_salary": "20 - 35 triệu VNĐ/tháng",
        "labor_market_outlook": "Sự bùng nổ của thương mại điện tử (Shopee, Lazada, TikTok Shop) và định hướng đưa Việt Nam thành trung tâm logistics khu vực khiến nhu cầu nhân sự chuỗi cung ứng luôn ở mức rất cao.",
        "skill_sandbox": {
            "course_name": "Quản lý Chuỗi Cung ứng Căn bản (MITx MicroMasters Supply Chain) & Kỹ năng Tối ưu Vận hành",
            "tryout_task": "Lập một bảng tính Excel giải bài toán điều phối: Sắp xếp 120 thùng hàng từ kho trung tâm tại Hà Nội giao đến 5 cửa hàng bán lẻ trong nội thành trong 1 buổi sáng sao cho quãng đường xe tải đi là ngắn nhất và không bị trễ giờ mở cửa.",
            "self_assessment_criteria": [
                "Bạn có đầu óc tổ chức khoa học, giỏi sắp xếp đồ đạc, đồ dùng ngăn nắp và luôn có thói quen lập kế hoạch trước khi hành động.",
                "Bạn có khả năng phản ứng nhanh và giữ được bình tĩnh khi kế hoạch bị xáo trộn hoặc phát sinh sự cố bất ngờ.",
                "Bạn thích tìm ra cách làm việc nhanh hơn, tiết kiệm thời gian và chi phí hơn cho mọi người xung quanh.",
                "Bạn không ngại di chuyển thực tế đến kho bãi, cảng biển và thích làm việc với các hệ thống quy trình chặt chẽ."
            ],
            "self_assessment": "Nếu bạn có tư duy chiến lược thực tế, yêu thích sự chuyển động nhịp nhàng của dòng chảy hàng hóa toàn cầu, Logistics là con đường lý tưởng!"
        },
        "work_distribution": [
            {"task": "Điều phối vận tải, Quản lý đơn hàng & Theo dõi lộ trình (Tracking)", "percent": 45},
            {"task": "Kiểm soát tồn kho, Lập kế hoạch cung ứng (Planning)", "percent": 25},
            {"task": "Làm việc tại hiện trường kho bãi, Cảng biển / Sân bay", "percent": 20},
            {"task": "Đàm phán giá cước & Đánh giá hiệu quả nhà cung cấp (KPI)", "percent": 10}
        ],
        "pressure_challenges": [
            "Thời gian giao hàng là sinh mạng (On-Time In-Full); tắc đường, thời tiết xấu hoặc hỏng xe đòi hỏi xử lý tình huống tức thì.",
            "Mùa cao điểm lễ Tết lượng hàng tăng gấp 3–4 lần, áp lực kho quá tải và làm việc ca kíp liên tục.",
            "Phải cân đối bài toán khó: Giảm tối đa chi phí lưu kho nhưng không bao giờ được để đứt gãy nguồn cung sản phẩm."
        ],
        "mini_case_study": {
            "scenario": "Một nhà máy lắp ráp ô tô sẽ phải dừng toàn bộ dây chuyền sản xuất sau 12 giờ nữa nếu lô linh kiện chip điện tử từ cảng Hải Phòng không được giao đến nhà máy kịp thời do đường cao tốc bị sạt lở vì mưa bão.",
            "questions": [
                {
                    "q": "Quyết định xử lý khủng hoảng chuỗi cung ứng của bạn là gì?",
                    "options": [
                        "Ngay lập tức điều phối chuyển đổi phương tiện sang đường sắt hoặc thuê dịch vụ xe tải nhỏ chạy đường tránh liên tỉnh, đồng thời cập nhật thời gian đến từng giờ cho nhà máy.",
                        "Chờ hết mưa bão thông đường mới tính tiếp.",
                        "Thông báo đóng cửa nhà máy 3 ngày."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Người làm logistics xuất sắc luôn có sẵn kế hoạch dự phòng (Contingency Plan) và tư duy hành động linh hoạt để bảo vệ dòng chảy cung ứng."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Chuyên viên Quản lý Chuỗi Cung ứng & Logistics (Supply Chain Specialist)",
            "skill_tree": {
                "year_1_2": "Nguyên lý Logistics, Quản trị mua hàng, Thống kê ứng dụng, Excel nâng cao & Phân tích dữ liệu chuỗi cung ứng.",
                "year_3": "Quản trị kho hàng (WMS), Quản trị vận tải (TMS), Dự báo nhu cầu (Demand Forecasting); Chứng chỉ quốc tế CSCP hoặc FIATA; IELTS 6.0+.",
                "year_4": "Mô phỏng chuỗi cung ứng (AnyLogic), Tối ưu chi phí logistics; Thực tập tại Shopee Xpress, Lazada Logistics, Viettel Post, Tân Cảng Sài Gòn."
            },
            "top_specialized_unis": [
                {"code": "UTC", "name": "Trường Đại học Giao thông Vận tải", "strength": "Đầu ngành đào tạo Logistics, tổ chức vận tải đường sắt, đường bộ và cảng biển tại miền Bắc."},
                {"code": "UTH", "name": "Trường ĐH Giao thông Vận tải TP.HCM", "strength": "Thế mạnh số 1 phía Nam về Logistics hàng hải, khai thác cảng và chuỗi cung ứng quốc tế."},
                {"code": "FTU", "name": "Trường Đại học Ngoại thương", "strength": "Đào tạo chuyên sâu Logistics và Chuỗi cung ứng quốc tế theo chuẩn FIATA, tiếng Anh xuất sắc."},
                {"code": "TMU", "name": "Trường Đại học Thương mại", "strength": "Khoa Logistics đào tạo rất sát thực tế thương mại bán lẻ và chuỗi cung ứng số."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 24,
            "risk_level": "Thấp",
            "ai_augmented_skills": [
                "Ứng dụng thuật toán AI tối ưu hóa lộ trình giao hàng (Route Optimization) tiết kiệm 20% nhiên liệu.",
                "Sử dụng học máy để dự báo nhu cầu tồn kho chính xác theo mùa vụ và thời tiết.",
                "Vận hành hệ thống quản lý kho tự động với robot gắp hàng tự động (Automated Warehouse)."
            ],
            "national_priority": "Kế hoạch Hành động Nâng cao Năng lực Cạnh tranh và Phát triển Dịch vụ Logistics Việt Nam"
        },
        "average_starting_salary": 12.0,
        "employment_rate": 98.5,
        "english_exit_req": "TOEIC 650+ hoặc VSTEP B2"
    },

    "ECO-MKT": {
        "entry_roles": ["Chuyên viên Chạy Quảng cáo Số (Digital Ads Executive)", "Chuyên viên Sáng tạo Nội dung (Content Creator / Copywriter)", "Chuyên viên Chăm sóc Cộng đồng & Mạng xã hội (Social Media Executive)"],
        "daily_work": "Lên ý tưởng chiến dịch truyền thông, viết bài viết hấp dẫn trên mạng xã hội, xây dựng kịch bản video ngắn bắt trend, cài đặt và theo dõi hiệu quả các chiến dịch quảng cáo (Facebook Ads, Google Ads, TikTok Ads).",
        "starting_salary": "8.5 - 13 triệu VNĐ/tháng",
        "mid_salary": "18 - 32 triệu VNĐ/tháng",
        "labor_market_outlook": "Không một doanh nghiệp nào có thể tồn tại mà không tiếp thị sản phẩm đến khách hàng. Sinh viên có khả năng sáng tạo nội dung số, hiểu thuật toán mạng xã hội và tư duy dữ liệu luôn có mức thu nhập hấp dẫn.",
        "skill_sandbox": {
            "course_name": "Google Digital Garage & Khóa học Sáng tạo Nội dung Truyền thông Tiếp thị (HubSpot Academy)",
            "tryout_task": "Viết một kịch bản video ngắn 45 giây cho TikTok giới thiệu một chiếc bình giữ nhiệt thân thiện môi trường dành cho học sinh, tuân thủ đúng công thức Hook (gây chú ý 3 giây đầu) - Body (nêu 2 lợi ích vượt trội) - CTA (kêu gọi bình luận/mua hàng).",
            "self_assessment_criteria": [
                "Bạn luôn bắt trend nhanh trên TikTok/Facebook, tò mò tại sao một video lại lên xu hướng và hàng triệu người bấm xem.",
                "Bạn có khả năng thấu hiểu tâm lý người khác, biết cách nói chuyện hay viết bài chạm đến cảm xúc của đám đông.",
                "Bạn tràn ngập ý tưởng mới lạ, ghét sự rập khuôn và luôn muốn thử nghiệm những cách làm mới.",
                "Bạn thích quan sát các mẫu quảng cáo ngoài đời và tự phân tích xem điểm hay/dở của mẫu quảng cáo đó."
            ],
            "self_assessment": "Nếu bạn muốn biến sự sáng tạo không giới hạn thành doanh thu và tầm ảnh hưởng thực tế, Digital Marketing là mảnh đất màu mỡ cho bạn tỏa sáng!"
        },
        "work_distribution": [
            {"task": "Sáng tạo nội dung (Content, Kịch bản video, Copywriting)", "percent": 35},
            {"task": "Cài đặt, Tối ưu & Phân tích số liệu quảng cáo (Ads & Analytics)", "percent": 35},
            {"task": "Nghiên cứu thị trường, Hành vi đối thủ & Bắt trend MXH", "percent": 20},
            {"task": "Họp phối hợp phòng Sales, Thiết kế & Đối tác KOC/KOL", "percent": 10}
        ],
        "pressure_challenges": [
            "Áp lực chỉ số KPI doanh số, giá trên mỗi khách hàng tiềm năng (CPL/CPA) và hiệu quả sinh lời trên chi phí quảng cáo (ROAS).",
            "Thuật toán của Facebook/TikTok/Google thay đổi liên tục, tài khoản quảng cáo có thể bị khóa bất cứ lúc nào.",
            "Cạn kiệt ý tưởng sáng tạo (Creative Burnout) khi phải sản xuất nội dung mới hàng ngày."
        ],
        "mini_case_study": {
            "scenario": "Một chiến dịch quảng cáo TikTok Ads của công ty bạn chi hết 10 triệu đồng nhưng chỉ thu về 2 đơn hàng, chi phí để có 1 khách mua hàng cao gấp 5 lần giá trị sản phẩm.",
            "questions": [
                {
                    "q": "Bạn phân tích và điều chỉnh chiến dịch như thế nào?",
                    "options": [
                        "Xem lại tỷ lệ xem hết 3 giây đầu của video để đổi đoạn Hook hấp dẫn hơn, kiểm tra lại trang đích (Landing page) xem nút mua hàng có bị lỗi không, và thu hẹp tệp đối tượng khách hàng mục tiêu.",
                        "Bơm thêm 50 triệu nữa để tiếp tục chạy quảng cáo đó.",
                        "Đăng đàn lên mạng than thở rằng thuật toán TikTok quá bất công."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Người làm Digital Marketing thành công là người biết 'nói chuyện bằng số liệu' để tối ưu hóa từng điểm chạm trong phễu chuyển đổi khách hàng."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Chuyên viên Digital Marketing & Quản trị Thương hiệu",
            "skill_tree": {
                "year_1_2": "Nghiên cứu hành vi người tiêu dùng, Viết quảng cáo (Copywriting), Thiết kế cơ bản (Canva/Photoshop), Quản trị mạng xã hội.",
                "year_3": "Chạy quảng cáo đa kênh (Meta Ads, Google Ads, TikTok Ads), SEO/SEM, Email Marketing Automation; Chứng chỉ Google Ads / Meta Certified Digital Marketing Associate; IELTS 6.0+.",
                "year_4": "Chiến lược thương hiệu, Đo lường chỉ số ROI/ROAS, Phân bổ ngân sách tiếp thị; Thực tập tại các Agency truyền thông (Ogilvy, Dentsu) hoặc phòng Marketing doanh nghiệp."
            },
            "top_specialized_unis": [
                {"code": "NEU", "name": "Trường Đại học Kinh tế Quốc dân", "strength": "Khoa Marketing lâu đời nhất Việt Nam, mạng lưới cựu sinh viên nắm giữ nhiều vị trí Giám đốc Marketing (CMO)."},
                {"code": "TMU", "name": "Trường Đại học Thương mại", "strength": "Cực kỳ mạnh về Marketing thực chiến, Thương mại điện tử và hành vi tiêu dùng."},
                {"code": "UEH", "name": "Đại học Kinh tế TP. Hồ Chí Minh", "strength": "Môi trường năng động, kết nối sâu rộng với các tập đoàn hàng tiêu dùng nhanh (Unilever, P&G, Nestlé)."},
                {"code": "RMIT", "name": "Đại học Quốc tế RMIT Việt Nam", "strength": "Chuẩn đào tạo quốc tế, sinh viên sở hữu tư duy toàn cầu và khả năng sáng tạo chiến dịch đột phá."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 35,
            "risk_level": "Trung bình",
            "ai_augmented_skills": [
                "Sử dụng AI tạo ảnh/video/bài viết (Midjourney, ChatGPT) để sản xuất hàng loạt biến thể quảng cáo A/B Testing.",
                "Phân tích cảm xúc mạng xã hội (Social Listening & Sentiment Analysis) bằng AI.",
                "Chiến lược định vị thương hiệu và sáng tạo cảm xúc chạm đến trái tim con người."
            ],
            "national_priority": "Phát triển Kinh tế Số và Thương mại Dịch vụ Hiện đại"
        },
        "average_starting_salary": 11.5,
        "employment_rate": 97.2,
        "english_exit_req": "IELTS 6.0 hoặc TOEIC 650+"
    },

    "ECO-FIN": {
        "entry_roles": ["Chuyên viên Phân tích Tài chính Doanh nghiệp (Financial Analyst)", "Chuyên viên Phân tích Đầu tư Chứng khoán (Equity Research)", "Chuyên viên Quản trị Rủi ro Ngân hàng (Risk Management)", "Chuyên viên Tư vấn Tài chính Cá nhân (Wealth Management)"],
        "daily_work": "Thu thập và xử lý báo cáo tài chính, xây dựng mô hình định giá DCF/P/E, dự phóng dòng tiền doanh nghiệp, phân tích biến động thị trường cổ phiếu/trái phiếu và lập báo cáo khuyến nghị đầu tư.",
        "starting_salary": "11 - 16 triệu VNĐ/tháng (Fresher)",
        "mid_salary": "25 - 55 triệu VNĐ/tháng (thưởng hiệu quả danh mục đầu tư rất cao)",
        "labor_market_outlook": "Thị trường tài chính, chứng khoán và công nghệ tài chính (FinTech) tại Việt Nam đang phát triển mạnh mẽ. Nhu cầu nhân sự sở hữu chứng chỉ CFA, CPA và kỹ năng mô hình tài chính luôn vượt trội.",
        "skill_sandbox": {
            "course_name": "Financial Markets (Yale University on Coursera) & Financial Modeling in Excel",
            "tryout_task": "Mở báo cáo tài chính kiểm toán năm gần nhất của Vinamilk (VNM), dùng Excel tính toán 3 chỉ số cốt lõi: Biên lợi nhuận gộp, ROE và Tỷ lệ nợ/Vốn chủ sở hữu để đánh giá sức khỏe tài chính doanh nghiệp.",
            "self_assessment_criteria": [
                "Bạn nhạy cảm với các con số, thị trường chứng khoán, lãi suất và tin tức tài chính kinh tế vĩ mô.",
                "Bạn thích phân tích logic, đọc hiểu bản chất hoạt động kinh doanh ẩn sau các bảng cân đối kế toán.",
                "Bạn có sự cẩn trọng, kỷ luật cao trong quản lý rủi ro và ra quyết định đầu tư dựa trên dữ liệu.",
                "Bạn chịu được áp lực thị trường biến động và kiên định với phương pháp luận khoa học."
            ],
            "self_assessment": "Nếu bạn có tư duy phân tích nhạy bén và đam mê làm chủ dòng tiền, Tài chính & Đầu tư là con đường thăng tiến không giới hạn!"
        },
        "work_distribution": [
            {"task": "Xây dựng mô hình tài chính & Định giá doanh nghiệp", "percent": 40},
            {"task": "Thu thập dữ liệu BCTC, Phân tích chỉ số & Báo cáo", "percent": 30},
            {"task": "Theo dõi biến động thị trường, Tin tức vĩ mô & Ngành", "percent": 20},
            {"task": "Họp trao đổi khách hàng & Thuyết trình khuyến nghị đầu tư", "percent": 10}
        ],
        "pressure_challenges": [
            "Áp lực thời gian hoàn thành báo cáo phân tích trước giờ thị trường mở cửa giao dịch.",
            "Trách nhiệm lớn đối với tính chính xác của mô hình định giá khi doanh nghiệp ra quyết định mua bán sáp nhập (M&A) hàng trăm tỷ.",
            "Cần duy trì việc ôn luyện các kỳ thi chứng chỉ quốc tế khắc nghiệt (CFA, FRM)."
        ],
        "mini_case_study": {
            "scenario": "Một doanh nghiệp bán lẻ lớn báo cáo lợi nhuận sau thuế tăng 50%, nhưng dòng tiền thuần từ hoạt động kinh doanh (CFO) lại âm nặng do hàng tồn kho và khoản phải thu tăng đột biến.",
            "questions": [
                {
                    "q": "Góc nhìn chuyên gia phân tích tài chính cảnh báo điều gì?",
                    "options": [
                        "Lợi nhuận có thể là 'lợi nhuận trên giấy tờ', doanh nghiệp có nguy cơ thiếu thanh khoản ngắn hạn và phải đi vay nợ bù đắp.",
                        "Doanh nghiệp sắp trở thành tập đoàn giàu nhất thế giới.",
                        "Bỏ qua số liệu dòng tiền vì chỉ cần lợi nhuận sau thuế dương là tốt."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Nguyên tắc 'Cash is King': Dòng tiền hoạt động kinh doanh thực tế mới là thước đo sức khỏe thật sự của một doanh nghiệp."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Chuyên viên Phân tích Tài chính & Đầu tư (Financial Analyst / CFA)",
            "skill_tree": {
                "year_1_2": "Kinh tế lượng, Toán tài chính, Nguyên lý kế toán, Tài chính doanh nghiệp; Kỹ năng Excel tài chính chuyên sâu.",
                "year_3": "Phân tích báo cáo tài chính nâng cao, Định giá cổ phiếu/trái phiếu, Thị trường phái sinh; Luyện thi chứng chỉ CFA Level 1; IELTS 6.5+.",
                "year_4": "M&A, Quản trị danh mục đầu tư, Mô hình định giá tài sản; Thực tập tại các công ty chứng khoán (SSI, VNDirect), Quỹ đầu tư (Dragon Capital, VinaCapital), Ngân hàng (Vietcombank, MB, Techcombank)."
            },
            "top_specialized_unis": [
                {"code": "NEU", "name": "Trường Đại học Kinh tế Quốc dân", "strength": "Viện Ngân hàng - Tài chính số 1 miền Bắc, mạng lưới đối tác rộng lớn với các định chế tài chính."},
                {"code": "FTU", "name": "Trường Đại học Ngoại thương", "strength": "Khoa Tài chính - Ngân hàng đào tạo chuẩn quốc tế, sinh viên đoạt nhiều giải quán quân CFA Research Challenge."},
                {"code": "AOF", "name": "Học viện Tài chính", "strength": "Bề dày truyền thống đào tạo chuyên gia tài chính công, kế toán kiểm toán và thẩm định giá hàng đầu."},
                {"code": "UEH", "name": "Đại học Kinh tế TP. Hồ Chí Minh", "strength": "Cái nôi đào tạo chuyên gia tài chính ngân hàng tại trung tâm tài chính lớn nhất cả nước."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 28,
            "risk_level": "Trung bình",
            "ai_augmented_skills": [
                "Ứng dụng AI tự động bóc tách số liệu báo cáo tài chính và tổng hợp tin tức thị trường tức thời.",
                "Sử dụng thuật toán học máy phân tích dữ liệu phi cấu trúc để dự báo xu hướng dòng tiền.",
                "Tư duy chiến lược, trực giác kinh doanh và kỹ năng phỏng vấn chuyên sâu lãnh đạo doanh nghiệp."
            ],
            "national_priority": "Chiến lược Phát triển Thị trường Chứng khoán và Trung tâm Tài chính Quốc tế Việt Nam"
        },
        "average_starting_salary": 13.5,
        "employment_rate": 98.0,
        "english_exit_req": "IELTS 6.5 hoặc TOEIC 750+"
    },

    "MED-GP": {
        "entry_roles": ["Bác sĩ Đa khoa Nội trú", "Bác sĩ Đa khoa Tuyến cơ sở & Bệnh viện đa khoa", "Bác sĩ Chăm sóc Sức khỏe Ban đầu", "Bác sĩ Trị liệu & Tư vấn Y khoa"],
        "daily_work": "Khám bệnh lâm sàng, hỏi bệnh sử, chỉ định xét nghiệm và chẩn đoán hình ảnh, phân tích kết quả cận lâm sàng, thiết lập phác đồ điều trị, theo dõi diễn tiến sức khỏe bệnh nhân và tư vấn phòng bệnh.",
        "starting_salary": "10 - 15 triệu VNĐ/tháng (khởi điểm), tăng nhanh khi có CCHN và hoàn thành Bác sĩ Chuyên khoa / Nội trú",
        "mid_salary": "30 - 65 triệu VNĐ/tháng",
        "labor_market_outlook": "Nhu cầu bác sĩ chất lượng cao luôn thiếu hụt trên toàn quốc. Hệ thống y tế tư nhân và công lập phát triển mạnh mẽ mở ra cơ hội việc làm 100% cho sinh viên tốt nghiệp y khoa.",
        "skill_sandbox": {
            "course_name": "Nhập môn Giải phẫu & Sinh lý Người (Anatomy & Physiology - Khan Academy / Coursera)",
            "tryout_task": "Tìm hiểu chu kỳ tim và cơ chế tuần hoàn máu của con người, vẽ lại sơ đồ dòng máu qua 4 ngăn tim và giải thích vì sao khi tập thể dục nhịp tim lại tăng lên.",
            "self_assessment_criteria": [
                "Bạn có lòng trắc ẩn, tình yêu thương con người và mong muốn chữa lành nỗi đau của người bệnh.",
                "Bạn học giỏi các môn Sinh học, Hóa học và có trí nhớ tốt với khối lượng kiến thức đồ sộ.",
                "Bạn có tinh thần kiên cường, sức khỏe dẻo dai, chịu được áp lực trực đêm và cảnh tượng máu me, vết thương.",
                "Bạn sẵn sàng học tập suốt đời, vì y học liên tục cập nhật các phác đồ và tiến bộ mới."
            ],
            "self_assessment": "Nếu bạn mang trái tim nhân ái và khát vọng cống hiến cứu người, nghề Y là thiên chức cao quý và thiêng liêng nhất!"
        },
        "work_distribution": [
            {"task": "Khám lâm sàng, Khai thác bệnh sử & Ra quyết định điều trị", "percent": 45},
            {"task": "Phân tích kết quả cận lâm sàng (X-quang, CT, Xét nghiệm máu)", "percent": 25},
            {"task": "Theo dõi người bệnh tại buồng bệnh & Xử trí ca cấp cứu", "percent": 20},
            {"task": "Ghi chép bệnh án & Hội chẩn cùng chuyên gia liên chuyên khoa", "percent": 10}
        ],
        "pressure_challenges": [
            "Thời gian đào tạo dài nhất (6 năm đại học + 18 tháng thực hành lấy chứng chỉ hành nghề hoặc 3 năm Bác sĩ Nội trú).",
            "Trực đêm cấp cứu liên tục 24h, áp lực ranh giới mong manh giữa sự sống và cái chết của bệnh nhân.",
            "Khối lượng kiến thức y khoa khổng lồ, đòi hỏi trí nhớ bền bỉ và sự tập trung tuyệt đối."
        ],
        "mini_case_study": {
            "scenario": "Một bệnh nhân 55 tuổi vào phòng cấp cứu với triệu chứng đau tức ngực dữ dội lan lên hàm dưới và cánh tay trái, vã mồ hôi, huyết áp tụt.",
            "questions": [
                {
                    "q": "Xử trí y khoa khẩn cấp chuẩn mực đầu tiên là gì?",
                    "options": [
                        "Lập tức đo điện tâm đồ (ECG) 12 chuyển đạo trong vòng 10 phút, thở oxy, mắc monitor theo dõi và chuẩn bị kíp can thiệp tim mạch khẩn vì nghi ngờ nhồi máu cơ tim cấp.",
                        "Kê thuốc giảm đau dạ dày và cho bệnh nhân về nhà nghỉ ngơi.",
                        "Chờ người nhà bệnh nhân đến đông đủ mới khám."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Y đức và sự nhạy bén lâm sàng: Cấp cứu tim mạch chạy đua từng phút 'Thời gian là cơ tim, thời gian là sự sống'."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Bác sĩ Đa khoa (General Practitioner / Medical Doctor)",
            "skill_tree": {
                "year_1_2": "Giải phẫu học, Sinh lý học, Hóa sinh y học, Mô phôi, Vi sinh - Ký sinh trùng; Y đức và Kỹ năng giao tiếp với người bệnh.",
                "year_3": "Giải phẫu bệnh, Dược lý học, Triệu chứng học Nội khoa - Ngoại khoa; Thực tập lâm sàng tại các bệnh viện thực hành; Ngoại ngữ chuyên ngành y khoa.",
                "year_4": "Bệnh học Nội khoa, Ngoại khoa, Sản phụ khoa, Nhi khoa; Tham gia trực cấp cứu, phụ mổ; Thi Bác sĩ Nội trú hoặc thực hành 18 tháng lấy CCHN."
            },
            "top_specialized_unis": [
                {"code": "HMU", "name": "Trường Đại học Y Hà Nội", "strength": "Trường y lâu đời và uy tín nhất cả nước, gắn liền với các bệnh viện tuyến cuối: Bạch Mai, Việt Đức, Phụ sản TW."},
                {"code": "UMP", "name": "Đại học Y Dược TP. Hồ Chí Minh", "strength": "Đầu tàu y khoa phương Nam, liên kết chặt chẽ với Chợ Rẫy, Thống Nhất, Từ Dũ, Nhi Đồng 1."},
                {"code": "HMED", "name": "Trường Đại học Y Dược - Đại học Huế", "strength": "Trung tâm đào tạo y khoa trọng điểm của miền Trung - Tây Nguyên với bệnh viện trường quy mô lớn."},
                {"code": "PNTU", "name": "Trường ĐH Y khoa Phạm Ngọc Thạch", "strength": "Mạnh về đào tạo thực hành y tế cơ sở và hệ thống bệnh viện chuyên khoa chất lượng cao tại TP.HCM."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 8,
            "risk_level": "Rất thấp",
            "ai_augmented_skills": [
                "Ứng dụng AI phân tích hình ảnh X-quang, CT, MRI phát hiện tổn thương sớm với độ chính xác cao.",
                "Sử dụng trợ lý AI tra cứu nhanh tương tác thuốc và cập nhật phác đồ điều trị quốc tế.",
                "Tình cảm, sự thấu cảm, đôi bàn tay phẫu thuật và y đức chữa lành - những giá trị AI không bao giờ thay thế được."
            ],
            "national_priority": "Quy hoạch Mạng lưới Cơ sở Y tế Thời kỳ 2021-2030, tầm nhìn 2050 (QĐ 201/QĐ-TTg)"
        },
        "average_starting_salary": 12.0,
        "employment_rate": 99.8,
        "english_exit_req": "IELTS 6.0 hoặc VSTEP B2 Y khoa"
    },

    "MED-PHARM": {
        "entry_roles": ["Dược sĩ Bệnh viện / Lâm sàng (Clinical Pharmacist)", "Dược sĩ Nghiên cứu & Phát triển Thuốc (R&D Pharmacist)", "Dược sĩ Quản lý Đăng ký Thuốc (Regulatory Affairs)", "Dược sĩ Quản lý Chuỗi Nhà thuốc & Kinh doanh Dược"],
        "daily_work": "Thẩm định đơn thuốc, kiểm tra tương tác thuốc, tư vấn sử dụng thuốc an toàn cho bác sĩ và bệnh nhân, nghiên cứu bào chế thuốc mới, kiểm tra chất lượng dược phẩm và làm thủ tục cấp phép lưu hành.",
        "starting_salary": "10 - 15 triệu VNĐ/tháng",
        "mid_salary": "22 - 45 triệu VNĐ/tháng",
        "labor_market_outlook": "Ngành công nghiệp dược phẩm Việt Nam đang bùng nổ với làn sóng nâng cấp chuẩn EU-GMP, WHO-GMP và sự mở rộng của các chuỗi bán lẻ dược phẩm (Long Châu, An Khang, Pharmacity).",
        "skill_sandbox": {
            "course_name": "Nhập môn Hóa Dược & Dược lý Học Đại cương (Understanding Drugs - FutureLearn)",
            "tryout_task": "Đọc tờ hướng dẫn sử dụng của thuốc hạ sốt Paracetamol, tìm hiểu cơ chế giảm đau, liều tối đa an toàn trong 24h đối với người lớn và cảnh báo nguy cơ ngộ độc gan khi dùng quá liều.",
            "self_assessment_criteria": [
                "Bạn rất yêu thích môn Hóa học (Hóa hữu cơ, Hóa phân tích) và Sinh học.",
                "Bạn có tính cẩn thận, chính xác tuyệt đối; bạn hiểu rằng một miligram sai sót có thể ảnh hưởng đến tính mạng.",
                "Bạn thích nghiên cứu các hợp chất tự nhiên, dược liệu cây thuốc và công nghệ sinh học nano.",
                "Bạn có đạo đức nghề nghiệp trong sáng và tinh thần trách nhiệm với sức khỏe cộng đồng."
            ],
            "self_assessment": "Nếu bạn say mê nghiên cứu hóa sinh và muốn tạo ra những viên thuốc kỳ diệu cứu chữa con người, Dược học là lựa chọn hoàn hảo!"
        },
        "work_distribution": [
            {"task": "Nghiên cứu công thức, Bào chế & Kiểm nghiệm chất lượng thuốc", "percent": 40},
            {"task": "Dược lâm sàng, Tư vấn sử dụng thuốc & Thẩm định đơn", "percent": 30},
            {"task": "Hồ sơ đăng ký lưu hành thuốc & Đảm bảo chuẩn GMP", "percent": 20},
            {"task": "Quản lý tồn trữ thuốc, Chuỗi cung ứng dược phẩm", "percent": 10}
        ],
        "pressure_challenges": [
            "Yêu cầu độ chính xác tuyệt đối trong định lượng, pha chế và kiểm nghiệm hoạt chất.",
            "Quy trình cấp phép và kiểm tra tiêu chuẩn chất lượng dược phẩm vô cùng khắt khe.",
            "Phải liên tục cập nhật thông tin về tương tác thuốc và cảnh giác dược (Pharmacovigilance)."
        ],
        "mini_case_study": {
            "scenario": "Bác sĩ kê đơn kết hợp kháng sinh Ciprofloxacin với viên sắt cho bệnh nhân viêm đường tiết niệu có thiếu máu nhẹ.",
            "questions": [
                {
                    "q": "Phát hiện của Dược sĩ lâm sàng trong đơn thuốc này là gì?",
                    "options": [
                        "Ion sắt tạo phức chelate không tan với Ciprofloxacin làm giảm hấp thu kháng sinh, cần tư vấn uống cách nhau ít nhất 2 giờ.",
                        "Hai thuốc này uống chung sẽ làm tăng tác dụng kháng sinh gấp đôi.",
                        "Kê thêm 5 loại thuốc bổ khác để tăng doanh thu."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Dược sĩ lâm sàng là 'chốt chặn an toàn' cuối cùng bảo vệ người bệnh khỏi các tương tác thuốc bất lợi."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Dược sĩ Lâm sàng & Quản lý Dược (Clinical / Industrial Pharmacist)",
            "skill_tree": {
                "year_1_2": "Hóa đại cương, Hóa hữu cơ, Sinh học tế bào, Giải phẫu sinh lý; Hóa phân tích, Thực vật dược.",
                "year_3": "Hóa dược, Dược lý học, Bào chế & Sinh dược học, Dược liệu học; Kiểm nghiệm thuốc theo Dược điển; IELTS 6.0+.",
                "year_4": "Dược lâm sàng, Quản lý & Kinh tế dược, Pháp chế dược; Thực tập tại các nhà máy đạt chuẩn EU-GMP (Dược Hậu Giang, Traphaco, Imexpharm) hoặc khoa Dược bệnh viện lớn."
            },
            "top_specialized_unis": [
                {"code": "HMU", "name": "Trường Đại học Dược Hà Nội", "strength": "Trường dược danh giá số 1 Việt Nam, cái nôi nghiên cứu hóa dược, bào chế và kiểm nghiệm thuốc."},
                {"code": "UMP", "name": "Đại học Y Dược TP. Hồ Chí Minh", "strength": "Khoa Dược đầu ngành phía Nam, đào tạo xuất sắc cả về dược lâm sàng lẫn công nghiệp dược."},
                {"code": "HMED", "name": "Trường Đại học Y Dược - Đại học Huế", "strength": "Thế mạnh về dược liệu tự nhiên, nghiên cứu phát triển thuốc từ nguồn thảo dược miền Trung."},
                {"code": "CTU", "name": "Trường Đại học Cần Thơ", "strength": "Khoa Y Dược đào tạo nguồn nhân lực dược phẩm chất lượng cao cho vùng Đồng bằng sông Cửu Long."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 18,
            "risk_level": "Rất thấp",
            "ai_augmented_skills": [
                "Ứng dụng AI mô phỏng gắn kết phân tử (Molecular Docking) đẩy nhanh quá trình tìm kiếm hoạt chất thuốc mới.",
                "Hệ thống phần mềm cảnh báo tương tác thuốc và liều lượng tự động trong bệnh viện.",
                "Tư vấn dược lâm sàng cá thể hóa theo gen người bệnh (Pharmacogenomics)."
            ],
            "national_priority": "Chiến lược Quốc gia Phát triển Ngành Dược Việt Nam giai đoạn đến năm 2030 (QĐ 376/QĐ-TTg)"
        },
        "average_starting_salary": 12.5,
        "employment_rate": 99.0,
        "english_exit_req": "IELTS 6.0 hoặc TOEIC 650+"
    },

    "DES-UIUX": {
        "entry_roles": ["Chuyên viên Thiết kế Trải nghiệm Người dùng (UX Designer)", "Chuyên viên Thiết kế Giao diện Ứng dụng (UI Designer)", "Chuyên viên Thiết kế Sản phẩm Số (Product Designer)", "Chuyên viên Nghiên cứu Người dùng (User Researcher)"],
        "daily_work": "Nghiên cứu hành vi người dùng, vẽ sơ đồ luồng trải nghiệm (User Flow), dựng khung xương sản phẩm (Wireframe), thiết kế giao diện chi tiết pixel-perfect trên Figma, làm việc chặt chẽ với lập trình viên và kiểm thử trải nghiệm sản phẩm số.",
        "starting_salary": "10 - 15 triệu VNĐ/tháng",
        "mid_salary": "22 - 42 triệu VNĐ/tháng",
        "labor_market_outlook": "Thời đại ứng dụng di động và siêu ứng dụng đòi hỏi trải nghiệm người dùng mượt mà. Vị trí Product Designer có gu thẩm mỹ kết hợp tư duy công nghệ luôn được săn đón tại các công ty công nghệ lớn và fintech.",
        "skill_sandbox": {
            "course_name": "Google UX Design Professional Certificate & Figma for Beginners",
            "tryout_task": "Mở phần mềm Figma (online miễn phí), thiết kế 2 màn hình điện thoại đơn giản cho một ứng dụng đặt món ăn: Màn hình 1 liệt kê món ăn kèm giá và nút 'Thêm vào giỏ', Màn hình 2 là giỏ hàng với nút 'Thanh toán' to rõ ràng.",
            "self_assessment_criteria": [
                "Bạn có sự nhạy cảm thẩm mỹ cao về màu sắc, kiểu chữ (typography) và bố cục thị giác cân đối.",
                "Bạn có khả năng thấu cảm cao: bạn luôn để ý xem người khác có gặp khó khăn gì khi dùng điện thoại hay ứng dụng công nghệ không.",
                "Bạn thích sự giao thoa giữa nghệ thuật sáng tạo và công nghệ số.",
                "Bạn thích giải quyết các bài toán tiện ích: làm thế nào để một thao tác phức tạp trở nên đơn giản chỉ bằng 1 cú chạm."
            ],
            "self_assessment": "Nếu bạn đam mê thiết kế những giao diện ứng dụng đẹp mắt, tiện dụng mà hàng triệu người chạm vào mỗi ngày, UI/UX Design là mảnh đất dành riêng cho bạn!"
        },
        "work_distribution": [
            {"task": "Thiết kế giao diện UI (Figma, Design System, Auto Layout)", "percent": 45},
            {"task": "Nghiên cứu UX, Phỏng vấn người dùng & Dựng Wireframe", "percent": 25},
            {"task": "Làm mẫu thử tương tác (Interactive Prototyping) & Usability Test", "percent": 15},
            {"task": "Phối hợp bàn giao thiết kế cho đội ngũ lập trình viên Frontend", "percent": 15}
        ],
        "pressure_challenges": [
            "Thường xuyên phải tiếp nhận phản hồi đóng góp và chỉnh sửa giao diện nhiều vòng từ ban quản trị sản phẩm.",
            "Phải cân bằng giữa yếu tố thẩm mỹ nghệ thuật và tính khả thi kỹ thuật khi lập trình viên triển khai mã nguồn.",
            "Áp lực tối ưu tỷ lệ chuyển đổi (Conversion Rate) của ứng dụng thông qua thiết kế."
        ],
        "mini_case_study": {
            "scenario": "Một ứng dụng ngân hàng số nhận được đánh giá 1 sao hàng loạt trên App Store vì người dùng lớn tuổi liên tục chuyển khoản nhầm tiền do nút 'Xác nhận chuyển' và nút 'Hủy' có màu sắc và vị trí quá giống nhau.",
            "questions": [
                {
                    "q": "Giải pháp thiết kế UI/UX tối ưu nhất bạn đề xuất là gì?",
                    "options": [
                        "Làm nút 'Xác nhận' màu xanh đậm nổi bật với kích thước lớn ở phía dưới, nút 'Hủy' để dạng chữ xám mờ không nền, và bổ sung màn hình tóm tắt thông tin người nhận trước khi nhập OTP.",
                        "Gửi email mắng người dùng là không chú ý khi chuyển tiền.",
                        "Xóa bỏ hoàn toàn nút Xác nhận."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Nguyên tắc thiết kế UX lấy con người làm trung tâm (Human-Centered Design): Thiết kế phải chủ động ngăn ngừa sai sót của người dùng bằng phân cấp thị giác rõ ràng."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": "Thiết kế Trải nghiệm & Giao diện Số (UI/UX Product Designer)",
            "skill_tree": {
                "year_1_2": "Nguyên lý thị giác, Màu sắc, Typography, Tư duy thiết kế (Design Thinking); Thành thạo công cụ Figma, Adobe Illustrator cơ bản.",
                "year_3": "Nghiên cứu người dùng (User Research, Empathy Map), Xây dựng Design System, Thiết kế tương tác Micro-interactions; Hoàn thiện Portfolio trên Behance; IELTS 6.0+.",
                "year_4": "Kiểm thử trải nghiệm (Usability Testing), Đo lường UX Metrics, Nền tảng HTML/CSS cơ bản để giao tiếp với lập trình viên; Thực tập tại các công ty công nghệ (VNG, MoMo, Shopee, FPT)."
            },
            "top_specialized_unis": [
                {"code": "MTCN", "name": "Trường ĐH Mỹ thuật Công nghiệp", "strength": "Cái nôi mỹ thuật ứng dụng hàng đầu miền Bắc, sinh viên có nền tảng bố cục và tư duy tạo hình rất vững."},
                {"code": "UIT", "name": "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", "strength": "Khoa Kỹ thuật Phần mềm đào tạo UI/UX gắn liền với công nghệ thực tế, sinh viên hiểu sâu về khả năng lập trình."},
                {"code": "RMIT", "name": "Đại học Quốc tế RMIT Việt Nam", "strength": "Đào tạo Digital Design chuẩn quốc tế, tư duy sản phẩm toàn cầu và mạng lưới quan hệ rộng mở."},
                {"code": "FPT", "name": "Trường Đại học FPT", "strength": "Chương trình Thiết kế Mỹ thuật số gắn liền với các dự án thực tế của các công ty phần mềm."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 30,
            "risk_level": "Trung bình",
            "ai_augmented_skills": [
                "Sử dụng AI tạo wireframe tự động và sinh biến thể giao diện nhanh gấp 5 lần (Figma AI, Relume).",
                "Tập trung vào thấu cảm tâm lý người dùng sâu sắc và thiết kế trải nghiệm cảm xúc độc đáo.",
                "Xây dựng kiến trúc thông tin phức tạp và chiến lược sản phẩm số toàn diện."
            ],
            "national_priority": "Chương trình Phát triển Công nghiệp Văn hóa và Kinh tế Sáng tạo Số Quốc gia"
        },
        "average_starting_salary": 13.0,
        "employment_rate": 97.8,
        "english_exit_req": "IELTS 6.0 hoặc TOEIC 650+"
    }
}

def get_all_target_roles() -> List[Dict[str, Any]]:
    """
    Trả về danh sách tất cả các chức danh nghề nghiệp mục tiêu kèm thông tin chi tiết
    phục vụ tính năng 'Đi từ nghề ngược về ngành' (Reverse Career Mapping).
    """
    roles = []
    seen = set()
    for code, info in CAREER_GUIDANCE_KNOWLEDGE_BASE.items():
        rcm = info.get("reverse_career_map", {})
        target = rcm.get("target_role")
        if target and target not in seen:
            seen.add(target)
            roles.append({
                "code": code,
                "title": target,
                "major_code": code,
                "target_role": target,
                "major_category": info.get("major_category", "Đại học"),
                "skill_tree": rcm.get("skill_tree", {}),
                "top_specialized_unis": rcm.get("top_specialized_unis", []),
                "starting_salary": info.get("starting_salary", "10 - 15 triệu/tháng"),
                "salary_range": info.get("starting_salary", "10 - 15 triệu/tháng"),
                "ai_impact": info.get("ai_impact", {}),
                "employment_rate": info.get("employment_rate", 97.0),
                "english_exit_req": info.get("english_exit_req", "IELTS 6.0")
            })
    return roles

def get_career_guidance(major_code: str, major_name: str, major_category: str) -> Dict[str, Any]:
    """
    Trả về bộ thông tin nghề nghiệp chuyên sâu, Reality Check và Skill Sandbox cho ngành học.
    """
    if major_code in CAREER_GUIDANCE_KNOWLEDGE_BASE:
        return CAREER_GUIDANCE_KNOWLEDGE_BASE[major_code]

    # Khớp thông minh theo từ khóa
    m_lower = (major_name or "").lower()
    mapping = {
        "máy tính": "IT-CS", "trí tuệ nhân tạo": "IT-CS", "ai": "IT-CS",
        "phần mềm": "IT-SE", "công nghệ thông tin": "IT-SE",
        "an toàn thông tin": "IT-CYBER", "an ninh mạng": "IT-CYBER",
        "dữ liệu": "IT-DS", "data": "IT-DS",
        "bán dẫn": "ENG-SEMI", "vi mạch": "ENG-SEMI",
        "robot": "ENG-ROBOT", "cơ điện tử": "ENG-ROBOT", "tự động hóa": "ENG-ROBOT",
        "ô tô": "ENG-AUTO", "xe điện": "ENG-AUTO",
        "kiến trúc": "ENG-ARCH", "nội thất": "ENG-ARCH",
        "quốc tế": "ECO-IB", "xuất nhập khẩu": "ECO-IB",
        "logistics": "ECO-LOG", "chuỗi cung ứng": "ECO-LOG",
        "marketing": "ECO-MKT", "tiếp thị": "ECO-MKT"
    }

    for kw, target_code in mapping.items():
        if kw in m_lower and target_code in CAREER_GUIDANCE_KNOWLEDGE_BASE:
            return CAREER_GUIDANCE_KNOWLEDGE_BASE[target_code]

    # Fallback mặc định
    return {
        "entry_roles": [f"Chuyên viên {major_name}", "Kỹ sư sơ cấp", "Trợ lý chuyên môn"],
        "daily_work": f"Thực hiện các nghiệp vụ chuyên môn ngành {major_name}, lập báo cáo công việc và phối hợp làm việc nhóm.",
        "starting_salary": "9 - 13 triệu VNĐ/tháng",
        "mid_salary": "18 - 30 triệu VNĐ/tháng",
        "labor_market_outlook": "Nhu cầu ổn định theo sự phát triển kinh tế xã hội.",
        "skill_sandbox": {
            "course_name": f"Nhập môn Nền tảng {major_name}",
            "tryout_task": f"Tìm hiểu nguyên lý vận hành cốt lõi của ngành {major_name} và lập bản tóm tắt 3 điểm quan trọng nhất.",
            "self_assessment_criteria": [
                "Bạn có sự yêu thích và ham học hỏi trong lĩnh vực này.",
                "Bạn có tinh thần trách nhiệm và kỷ luật trong công việc."
            ],
            "self_assessment": "Ngành này mở ra nhiều cơ hội phát triển nếu bạn kiên trì theo đuổi!"
        },
        "work_distribution": [
            {"task": "Nghiệp vụ chuyên môn cốt lõi", "percent": 50},
            {"task": "Họp nhóm, Phối hợp & Báo cáo", "percent": 30},
            {"task": "Nghiên cứu tài liệu & Tự học công nghệ mới", "percent": 20}
        ],
        "pressure_challenges": [
            "Áp lực cạnh tranh tuyển dụng và yêu cầu kỹ năng thực tế ngày càng cao.",
            "Cần duy trì khả năng tự học liên tục để đáp ứng yêu cầu chuyển đổi số."
        ],
        "mini_case_study": {
            "scenario": f"Bạn đang tham gia một dự án quan trọng về {major_name} và phát hiện một sai sót nhỏ có thể làm chậm tiến độ bàn giao 1 ngày.",
            "questions": [
                {
                    "q": "Bạn sẽ ứng xử ra sao?",
                    "options": [
                        "Chủ động thông báo ngay cho trưởng nhóm, đề xuất giải pháp khắc phục cụ thể để mọi người cùng phối hợp.",
                        "Giấu đi và hy vọng không ai phát hiện.",
                        "Đổ lỗi cho người khác."
                    ],
                    "correct_index": 0,
                    "mindset_analysis": "Tính chính trực và tinh thần trách nhiệm là chìa khóa thăng tiến trong mọi ngành nghề."
                }
            ]
        },
        "reverse_career_map": {
            "target_role": f"Chuyên viên {major_name}",
            "skill_tree": {
                "year_1_2": "Nền tảng đại cương, ngoại ngữ, kỹ năng tin học và kỹ năng mềm.",
                "year_3": "Kiến thức chuyên ngành sâu, chứng chỉ nghề nghiệp, kỹ năng phân tích.",
                "year_4": "Thực tập tại doanh nghiệp, hoàn thành đồ án tốt nghiệp."
            },
            "top_specialized_unis": [
                {"code": "BKHN", "name": "Đại học Bách Khoa Hà Nội", "strength": "Đào tạo kỹ thuật hàng đầu."},
                {"code": "NEU", "name": "Trường Đại học Kinh tế Quốc dân", "strength": "Đào tạo kinh tế quản trị hàng đầu."}
            ]
        },
        "ai_impact": {
            "automation_risk_percent": 25,
            "risk_level": "Thấp",
            "ai_augmented_skills": [
                "Làm chủ các công cụ AI hỗ trợ công việc chuyên môn.",
                "Phát triển tư duy phản biện và giải quyết vấn đề phức tạp."
            ],
            "national_priority": "Quy hoạch phát triển nguồn nhân lực quốc gia"
        },
        "average_starting_salary": 11.5,
        "employment_rate": 96.5,
        "english_exit_req": "TOEIC 550+ hoặc VSTEP B1"
    }

def calculate_education_roi(
    uni_code: str,
    major_code: Optional[str] = None,
    living_city: str = "Hà Nội",
    program_type: str = "standard",
    study_years: float = 4.0,
    custom_tuition: Optional[float] = None,
    custom_living_cost: Optional[float] = None,
    savings_rate: float = 0.4,
    scholarship_pct: float = 0.0,
    **kwargs
) -> Dict[str, Any]:
    """
    Tính toán chi tiết bài toán đầu tư học tập (Education ROI Calculator) cho BẤT KỲ trường đại học nào.
    """
    # 1. Bảng học phí cơ sở (triệu VNĐ/năm) cho các trường đại học toàn quốc (Chuẩn 2025)
    UNI_TUITION_BASE = {
        "BKHN": {"name": "Đại học Bách Khoa Hà Nội", "standard": 30.0, "high_quality": 45.0, "international": 75.0, "city": "Hà Nội", "years": 5.0},
        "UET": {"name": "Trường ĐH Công nghệ - ĐHQGHN", "standard": 28.5, "high_quality": 42.0, "international": 65.0, "city": "Hà Nội", "years": 4.5},
        "NEU": {"name": "Trường ĐH Kinh tế Quốc dân", "standard": 26.0, "high_quality": 40.0, "international": 70.0, "city": "Hà Nội", "years": 4.0},
        "FTU": {"name": "Trường ĐH Ngoại thương", "standard": 28.0, "high_quality": 48.0, "international": 80.0, "city": "Hà Nội", "years": 4.0},
        "HMU": {"name": "Trường ĐH Y Hà Nội", "standard": 45.0, "high_quality": 55.0, "international": 80.0, "city": "Hà Nội", "years": 6.0},
        "PTIT": {"name": "Học viện Công nghệ Bưu chính Viễn thông", "standard": 27.0, "high_quality": 38.0, "international": 60.0, "city": "Hà Nội", "years": 4.5},
        "DAV": {"name": "Học viện Ngoại giao", "standard": 25.0, "high_quality": 42.0, "international": 65.0, "city": "Hà Nội", "years": 4.0},
        "AOF": {"name": "Học viện Tài chính", "standard": 25.0, "high_quality": 40.0, "international": 65.0, "city": "Hà Nội", "years": 4.0},
        "TMU": {"name": "Trường Đại học Thương mại", "standard": 26.0, "high_quality": 38.0, "international": 60.0, "city": "Hà Nội", "years": 4.0},
        "HNUE": {"name": "Trường ĐH Sư phạm Hà Nội", "standard": 0.0, "high_quality": 0.0, "international": 30.0, "city": "Hà Nội", "years": 4.0, "pedagogy_support": 3.63},
        "HAU": {"name": "Trường ĐH Kiến trúc Hà Nội", "standard": 24.0, "high_quality": 36.0, "international": 55.0, "city": "Hà Nội", "years": 5.0},
        "MTCN": {"name": "Trường ĐH Mỹ thuật Công nghiệp", "standard": 20.0, "high_quality": 32.0, "international": 50.0, "city": "Hà Nội", "years": 4.0},
        "HANU": {"name": "Trường Đại học Hà Nội", "standard": 26.0, "high_quality": 40.0, "international": 65.0, "city": "Hà Nội", "years": 4.0},
        "AJC": {"name": "Học viện Báo chí & Tuyên truyền", "standard": 22.0, "high_quality": 38.0, "international": 55.0, "city": "Hà Nội", "years": 4.0},
        "HaUI": {"name": "Trường ĐH Công nghiệp Hà Nội", "standard": 24.0, "high_quality": 35.0, "international": 50.0, "city": "Hà Nội", "years": 4.0},
        "UTC": {"name": "Trường ĐH Giao thông Vận tải", "standard": 22.0, "high_quality": 32.0, "international": 48.0, "city": "Hà Nội", "years": 4.5},
        "VNUA": {"name": "Học viện Nông nghiệp Việt Nam", "standard": 20.0, "high_quality": 30.0, "international": 45.0, "city": "Hà Nội", "years": 4.5},
        "FPT": {"name": "Trường Đại học FPT", "standard": 75.0, "high_quality": 95.0, "international": 120.0, "city": "Hà Nội", "years": 4.0},

        # Miền Trung
        "DUT": {"name": "Trường ĐH Bách khoa - ĐH Đà Nẵng", "standard": 26.0, "high_quality": 38.0, "international": 55.0, "city": "Đà Nẵng", "years": 4.5},
        "DUE": {"name": "Trường ĐH Kinh tế - ĐH Đà Nẵng", "standard": 24.0, "high_quality": 36.0, "international": 55.0, "city": "Đà Nẵng", "years": 4.0},
        "HMED": {"name": "Trường ĐH Y Dược - ĐH Huế", "standard": 40.0, "high_quality": 52.0, "international": 70.0, "city": "Thừa Thiên Huế", "years": 6.0},
        "UTE_DN": {"name": "Trường ĐH Sư phạm Kỹ thuật - ĐH Đà Nẵng", "standard": 22.0, "high_quality": 32.0, "international": 45.0, "city": "Đà Nẵng", "years": 4.0},
        "HUL": {"name": "Trường ĐH Ngoại ngữ - ĐH Huế", "standard": 20.0, "high_quality": 30.0, "international": 45.0, "city": "Thừa Thiên Huế", "years": 4.0},
        "HUAF": {"name": "Trường ĐH Nông Lâm - ĐH Huế", "standard": 18.0, "high_quality": 28.0, "international": 40.0, "city": "Thừa Thiên Huế", "years": 4.5},
        "NTU": {"name": "Trường Đại học Nha Trang", "standard": 20.0, "high_quality": 30.0, "international": 45.0, "city": "Khánh Hòa", "years": 4.0},
        "QNU": {"name": "Trường Đại học Quy Nhơn", "standard": 18.0, "high_quality": 28.0, "international": 40.0, "city": "Bình Định", "years": 4.0},
        "VINH": {"name": "Trường Đại học Vinh", "standard": 20.0, "high_quality": 30.0, "international": 45.0, "city": "Nghệ An", "years": 4.0},
        "TDU": {"name": "Trường Đại học Tây Nguyên", "standard": 18.0, "high_quality": 28.0, "international": 40.0, "city": "Đắk Lắk", "years": 4.5},
        "DTU": {"name": "Trường Đại học Duy Tân", "standard": 38.0, "high_quality": 55.0, "international": 85.0, "city": "Đà Nẵng", "years": 4.0},

        # Miền Nam
        "HCMUT": {"name": "Trường ĐH Bách khoa - ĐHQG-HCM", "standard": 35.0, "high_quality": 50.0, "international": 80.0, "city": "TP. Hồ Chí Minh", "years": 4.5},
        "UIT": {"name": "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", "standard": 35.0, "high_quality": 48.0, "international": 75.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "UEH": {"name": "Đại học Kinh tế TP. Hồ Chí Minh", "standard": 32.0, "high_quality": 48.0, "international": 80.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "UMP": {"name": "Đại học Y Dược TP. Hồ Chí Minh", "standard": 55.0, "high_quality": 75.0, "international": 110.0, "city": "TP. Hồ Chí Minh", "years": 6.0},
        "USSH_HCM": {"name": "Trường ĐH KHXH&NV - ĐHQG-HCM", "standard": 24.0, "high_quality": 38.0, "international": 60.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "HCMUS": {"name": "Trường ĐH Khoa học Tự nhiên - ĐHQG-HCM", "standard": 30.0, "high_quality": 45.0, "international": 70.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "UAH": {"name": "Trường ĐH Kiến trúc TP. Hồ Chí Minh", "standard": 28.0, "high_quality": 42.0, "international": 65.0, "city": "TP. Hồ Chí Minh", "years": 5.0},
        "HCMUTE": {"name": "Trường ĐH Sư phạm Kỹ thuật TP.HCM", "standard": 28.0, "high_quality": 40.0, "international": 60.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "NLU": {"name": "Trường ĐH Nông Lâm TP. Hồ Chí Minh", "standard": 22.0, "high_quality": 34.0, "international": 50.0, "city": "TP. Hồ Chí Minh", "years": 4.5},
        "CTU": {"name": "Trường Đại học Cần Thơ", "standard": 20.0, "high_quality": 32.0, "international": 48.0, "city": "Cần Thơ", "years": 4.0},
        "PNTU": {"name": "Trường ĐH Y khoa Phạm Ngọc Thạch", "standard": 45.0, "high_quality": 60.0, "international": 90.0, "city": "TP. Hồ Chí Minh", "years": 6.0},
        "TDTU": {"name": "Trường Đại học Tôn Đức Thắng", "standard": 32.0, "high_quality": 48.0, "international": 75.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "RMIT": {"name": "Đại học Quốc tế RMIT Việt Nam", "standard": 320.0, "high_quality": 350.0, "international": 380.0, "city": "TP. Hồ Chí Minh", "years": 3.5},
        "TLU": {"name": "Trường Đại học Thủy lợi", "standard": 22.0, "high_quality": 32.0, "international": 48.0, "city": "Hà Nội", "years": 4.5},
        "EPU": {"name": "Trường Đại học Điện lực", "standard": 22.0, "high_quality": 32.0, "international": 45.0, "city": "Hà Nội", "years": 4.0},
        "HUMG": {"name": "Trường ĐH Mỏ - Địa chất", "standard": 20.0, "high_quality": 30.0, "international": 42.0, "city": "Hà Nội", "years": 4.5},
        "HUIT": {"name": "Trường ĐH Công Thương TP.HCM", "standard": 24.0, "high_quality": 35.0, "international": 50.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "UTH": {"name": "Trường ĐH Giao thông Vận tải TP.HCM", "standard": 22.0, "high_quality": 32.0, "international": 48.0, "city": "TP. Hồ Chí Minh", "years": 4.0},
        "SGU": {"name": "Trường Đại học Sài Gòn", "standard": 20.0, "high_quality": 32.0, "international": 48.0, "city": "TP. Hồ Chí Minh", "years": 4.0}
    }

    # Chi phí sinh hoạt hàng tháng ước tính (triệu VNĐ/tháng)
    LIVING_COST_MAP = {
        "Hà Nội": 4.5,
        "TP. Hồ Chí Minh": 5.0,
        "Đà Nẵng": 3.5,
        "Cần Thơ": 3.0,
        "Thừa Thiên Huế": 2.8,
        "Khánh Hòa": 3.2,
        "Bình Định": 2.8,
        "Nghệ An": 2.6,
        "Đắk Lắk": 2.5,
        "Khác": 2.8
    }

    u_data = UNI_TUITION_BASE.get(uni_code.upper(), {
        "name": f"Trường Đại học ({uni_code})",
        "standard": 25.0, "high_quality": 40.0, "international": 65.0,
        "city": living_city,
        "years": 4.0
    })

    # Xác định số năm học thực tế
    actual_years = study_years if study_years > 0 else u_data.get("years", 4.0)

    # Xác định mức học phí hàng năm
    if custom_tuition is not None and custom_tuition > 0:
        annual_tuition = custom_tuition
    else:
        annual_tuition = u_data.get(program_type, u_data.get("standard", 25.0))

    total_tuition = round(annual_tuition * actual_years, 2)

    # Chi phí sinh hoạt
    if custom_living_cost is not None and custom_living_cost > 0:
        monthly_living = custom_living_cost
    else:
        city_key = living_city if living_city in LIVING_COST_MAP else u_data.get("city", "Hà Nội")
        monthly_living = LIVING_COST_MAP.get(city_key, 3.5)

    annual_living = round(monthly_living * 12, 2)
    total_living = round(annual_living * actual_years, 2)
    total_cost = round(total_tuition + total_living, 2)

    # Mức lương khởi điểm
    cg = CAREER_GUIDANCE_KNOWLEDGE_BASE.get(major_code or "IT-CS", {})
    avg_salary = cg.get("average_starting_salary", 12.0)
    monthly_savings = round(avg_salary * savings_rate, 2)
    annual_savings = round(monthly_savings * 12, 2)

    if annual_savings > 0:
        payback_years = round(total_cost / annual_savings, 1)
        payback_months = round(total_cost / monthly_savings, 0)
    else:
        payback_years = 0
        payback_months = 0

    # Xử lý học phí giảm trừ học bổng nếu có
    scholarship_pct = kwargs.get("scholarship_pct", 0) or 0
    if scholarship_pct > 0:
        annual_tuition = round(annual_tuition * (1 - scholarship_pct / 100.0), 2)
        total_tuition = round(annual_tuition * actual_years, 2)
        total_cost = round(total_tuition + total_living, 2)
        if annual_savings > 0:
            payback_years = round(total_cost / annual_savings, 1)
            payback_months = round(total_cost / monthly_savings, 0)

    # Học bổng và hỗ trợ tài chính
    aid_notes = []
    if u_data.get("pedagogy_support"):
        aid_notes.append("Miễn 100% học phí và nhận hỗ trợ sinh hoạt phí 3.63 triệu VNĐ/tháng theo Nghị định 116/2020/NĐ-CP.")
    aid_notes.append("Chính sách vay vốn Ngân hàng Chính sách Xã hội tối đa 4.0 triệu VNĐ/tháng (lãi suất ưu đãi 6.6%/năm).")
    aid_notes.append(f"Quỹ học bổng Khuyến khích học tập trích tối thiểu 8% từ nguồn thu học phí của {u_data.get('name')}.")
    if annual_tuition >= 60.0:
        aid_notes.append("Học bổng tài năng đầu vào từ 30% - 100% học phí dành cho thí sinh có giải HSG quốc gia hoặc IELTS cao.")

    return {
        "university_code": uni_code.upper(),
        "university_name": u_data.get("name"),
        "city": u_data.get("city", living_city),
        "program_type": program_type,
        "study_years": actual_years,
        "annual_tuition": annual_tuition,
        "total_tuition": total_tuition,
        "total_tuition_4y": total_tuition,
        "monthly_living_cost": monthly_living,
        "annual_living_cost": annual_living,
        "total_living_cost": total_living,
        "total_living_cost_4y": total_living,
        "total_cost": total_cost,
        "grand_total_investment": total_cost,
        "average_starting_salary": avg_salary,
        "estimated_starting_salary": avg_salary,
        "monthly_savings": monthly_savings,
        "estimated_monthly_savings": monthly_savings,
        "payback_period_years": payback_years,
        "payback_period_months": int(payback_months),
        "financial_aid_suggestions": aid_notes,
        "scholarship_advice": aid_notes[0] if aid_notes else "Có nhiều cơ hội học bổng đầu vào.",
        "student_loan_note": aid_notes[1] if len(aid_notes) > 1 else "Chính sách vay vốn sinh viên 4 tr/tháng."
    }

def analyze_parent_student_alignment(
    student_answers: Dict[str, Any],
    parent_answers: Dict[str, Any],
    target_majors: List[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Phân tích độ đồng thuận giữa kỳ vọng của Phụ huynh và Học sinh (Parent & Student Alignment).
    Tạo báo cáo tóm tắt giải thích chuyên sâu dành riêng cho phụ huynh (Parent Summary Report).
    """
    s_ans = student_answers or kwargs.get("student_scores", {}) or {}
    p_ans = parent_answers or kwargs.get("parent_scores", {}) or {}

    s_stab = s_ans.get("stability_vs_income", s_ans.get("stability", 3))
    p_stab = p_ans.get("stability_vs_income", p_ans.get("stability", 3))

    s_loc = s_ans.get("location", 3)
    p_loc = p_ans.get("location", 3)

    s_brand = s_ans.get("brand_vs_major", s_ans.get("brand", 3))
    p_brand = p_ans.get("brand_vs_major", p_ans.get("brand", 3))

    s_cost = s_ans.get("cost_vs_investment", s_ans.get("cost", 3))
    p_cost = p_ans.get("cost_vs_investment", p_ans.get("cost", 3))

    # Chuẩn hóa nếu thang điểm là 10 thay vì 5
    if any(v > 5 for v in [s_stab, p_stab, s_loc, p_loc, s_brand, p_brand, s_cost, p_cost]):
        diff_sum = abs(s_stab - p_stab) + abs(s_loc - p_loc) + abs(s_brand - p_brand) + abs(s_cost - p_cost)
        alignment_percent = max(15, int(100 - (diff_sum / 36) * 100))
    else:
        diff_sum = abs(s_stab - p_stab) + abs(s_loc - p_loc) + abs(s_brand - p_brand) + abs(s_cost - p_cost)
        alignment_percent = max(15, int(100 - (diff_sum / 16) * 100))

    common_ground = []
    conflict_points = []

    # 1. Ổn định vs Thu nhập
    diff_stab = abs(s_stab - p_stab)
    stab_labels = {
        1: "Rất chuộng ổn định (công chức/nhà nước)",
        2: "Ưu tiên ổn định vừa phải",
        3: "Cân bằng giữa ổn định và thu nhập",
        4: "Sẵn sàng chịu áp lực để thu nhập cao",
        5: "Đam mê khởi nghiệp / Thu nhập đột phá"
    }
    if diff_stab <= (2 if s_stab > 5 else 1):
        common_ground.append({
            "axis": "stability",
            "axis_label": "Độ ổn định & Thu nhập",
            "average_score": round((s_stab + p_stab) / 2, 1),
            "description": "Cả hai bên đều có quan điểm tương đồng về mức độ ưu tiên giữa tính ổn định công việc và tiềm năng thu nhập."
        })
    else:
        conflict_points.append({
            "axis": "stability",
            "axis_label": "Độ ổn định & Thu nhập",
            "student_score": s_stab,
            "parent_score": p_stab,
            "advice": "Phụ huynh ưu tiên công việc ổn định, lâu dài trong khi học sinh muốn thử sức với các ngành nghề mới có thu nhập bứt phá."
        })

    # 2. Vị trí địa lý
    diff_loc = abs(s_loc - p_loc)
    loc_labels = {
        1: "Nhất định muốn học gần gia đình",
        2: "Thích học trong tỉnh/vùng lân cận",
        3: "Tùy thuộc vào trường nào tốt hơn",
        4: "Muốn lên thành phố lớn tự lập",
        5: "Muốn vươn xa toàn cầu / Du học"
    }
    if diff_loc <= (2 if s_loc > 5 else 1):
        common_ground.append({
            "axis": "location",
            "axis_label": "Vị trí địa lý",
            "average_score": round((s_loc + p_loc) / 2, 1),
            "description": "Đồng thuận về địa điểm học tập (gần gia đình hoặc sẵn sàng cho con học xa nhà để tự lập)."
        })
    else:
        conflict_points.append({
            "axis": "location",
            "axis_label": "Vị trí địa lý",
            "student_score": s_loc,
            "parent_score": p_loc,
            "advice": "Phụ huynh mong muốn con học tập gần nhà để tiện chăm sóc, trong khi học sinh khao khát đến các đô thị lớn để tìm kiếm cơ hội bứt phá."
        })

    # 3. Danh tiếng trường vs Ngành đam mê
    diff_brand = abs(s_brand - p_brand)
    brand_labels = {
        1: "Trường top 1 danh giá là trên hết",
        2: "Ưu tiên thương hiệu trường truyền thống",
        3: "Cân đối cả trường và ngành",
        4: "Miễn đúng ngành yêu thích, trường nào cũng được",
        5: "Tuyệt đối chỉ học đúng ngành đam mê"
    }
    if diff_brand <= (2 if s_brand > 5 else 1):
        common_ground.append({
            "axis": "brand",
            "axis_label": "Danh tiếng trường vs Đam mê",
            "average_score": round((s_brand + p_brand) / 2, 1),
            "description": "Thống nhất quan điểm giữa việc chọn tên tuổi của trường đại học và việc chọn ngành con thực sự yêu thích."
        })
    else:
        conflict_points.append({
            "axis": "brand",
            "axis_label": "Danh tiếng trường vs Đam mê",
            "student_score": s_brand,
            "parent_score": p_brand,
            "advice": "Phụ huynh coi trọng danh tiếng trường truyền thống (Bách Khoa, Kinh tế, Y Dược) trong khi con chú trọng vào đúng ngành đam mê."
        })

    # 4. Học phí & Đầu tư tài chính
    diff_cost = abs(s_cost - p_cost)
    cost_labels = {
        1: "Tiết kiệm tối đa, học phí thấp nhất",
        2: "Học phí công lập truyền thống",
        3: "Mức học phí tự chủ vừa phải",
        4: "Sẵn sàng đầu tư chương trình chất lượng cao",
        5: "Đầu tư mạnh mẽ chuẩn quốc tế"
    }
    if diff_cost <= (2 if s_cost > 5 else 1):
        common_ground.append({
            "axis": "cost",
            "axis_label": "Học phí & Khả năng tài chính",
            "average_score": round((s_cost + p_cost) / 2, 1),
            "description": "Gia đình đã có sự đồng thuận về mức học phí và lộ trình đầu tư tài chính cho khóa học."
        })
    else:
        conflict_points.append({
            "axis": "cost",
            "axis_label": "Học phí & Khả năng tài chính",
            "student_score": s_cost,
            "parent_score": p_cost,
            "advice": "Cần thảo luận kỹ hơn về bài toán tài chính: Phụ huynh lo ngại áp lực học phí cao của các chương trình tự chủ/chất lượng cao."
        })

    # Tạo bảng đối chiếu chi tiết 4 trục sự đồng thuận gia đình
    axis_comparisons = [
        {
            "axis_id": "stability",
            "axis_name": "1. Ổn Định Việc Làm vs Tiềm Năng Thu Nhập",
            "student_score": s_stab,
            "student_text": stab_labels.get(int(s_stab), f"{s_stab}/5"),
            "parent_score": p_stab,
            "parent_text": stab_labels.get(int(p_stab), f"{p_stab}/5"),
            "gap": diff_stab,
            "status": "Đồng thuận rất cao" if diff_stab <= 1 else ("Lệch nhẹ (cần trao đổi)" if diff_stab == 2 else "Khác biệt lớn (cần đối thoại sâu)"),
            "status_class": "badge-success" if diff_stab <= 1 else ("badge-warning" if diff_stab == 2 else "badge-danger"),
            "advice": "Phụ huynh lo lắng cho sự ổn định lâu dài, trong khi con có khát vọng bứt phá trong kỷ nguyên số. Hãy thống nhất: Đặt các trường công lập uy tín ở nhóm NV vừa sức để đảm bảo nền móng vững chắc."
        },
        {
            "axis_id": "location",
            "axis_name": "2. Vị Trí Địa Lý (Gần Nhà vs Đô Thị Lớn)",
            "student_score": s_loc,
            "student_text": loc_labels.get(int(s_loc), f"{s_loc}/5"),
            "parent_score": p_loc,
            "parent_text": loc_labels.get(int(p_loc), f"{p_loc}/5"),
            "gap": diff_loc,
            "status": "Đồng thuận rất cao" if diff_loc <= 1 else ("Lệch nhẹ (cần trao đổi)" if diff_loc == 2 else "Khác biệt lớn (cần đối thoại sâu)"),
            "status_class": "badge-success" if diff_loc <= 1 else ("badge-warning" if diff_loc == 2 else "badge-danger"),
            "advice": "Nếu con học xa nhà tại Hà Nội hay TP.HCM, gia đình nên lên kế hoạch chi tiết về ký túc xá an toàn và kỹ năng sống tự lập trong năm đầu."
        },
        {
            "axis_id": "brand",
            "axis_name": "3. Thương Hiệu Trường vs Đúng Ngành Đam Mê",
            "student_score": s_brand,
            "student_text": brand_labels.get(int(s_brand), f"{s_brand}/5"),
            "parent_score": p_brand,
            "parent_text": brand_labels.get(int(p_brand), f"{p_brand}/5"),
            "gap": diff_brand,
            "status": "Đồng thuận rất cao" if diff_brand <= 1 else ("Lệch nhẹ (cần trao đổi)" if diff_brand == 2 else "Khác biệt lớn (cần đối thoại sâu)"),
            "status_class": "badge-success" if diff_brand <= 1 else ("badge-warning" if diff_brand == 2 else "badge-danger"),
            "advice": "Thương hiệu trường lớn mang lại mạng lưới cựu sinh viên rộng, nhưng đúng ngành đam mê mới giúp con kiên trì học tập và đạt kết quả xuất sắc."
        },
        {
            "axis_id": "cost",
            "axis_name": "4. Học Phí & Khả Năng Tài Chính Gia Đình",
            "student_score": s_cost,
            "student_text": cost_labels.get(int(s_cost), f"{s_cost}/5"),
            "parent_score": p_cost,
            "parent_text": cost_labels.get(int(p_cost), f"{p_cost}/5"),
            "gap": diff_cost,
            "status": "Đồng thuận rất cao" if diff_cost <= 1 else ("Lệch nhẹ (cần trao đổi)" if diff_cost == 2 else "Khác biệt lớn (cần đối thoại sâu)"),
            "status_class": "badge-success" if diff_cost <= 1 else ("badge-warning" if diff_cost == 2 else "badge-danger"),
            "advice": "Cần tính toán tổng mức đầu tư 4 năm (bao gồm cả sinh hoạt phí ~4-5 tr/tháng) và xem xét các gói học bổng khuyến khích học tập hoặc vay vốn sinh viên lãi suất ưu đãi."
        }
    ]

    # Ngành con hướng tới
    target_major_name = (target_majors[0] if target_majors else kwargs.get("student_target_major")) or "Công nghệ Thông tin / Kỹ thuật Số"

    # Sinh bản báo cáo tóm tắt dành cho phụ huynh (Parent Summary Report)
    level_str = "Rất cao (Đồng thuận hoàn hảo)" if alignment_percent >= 80 else ("Khá tốt (Đồng thuận cơ bản)" if alignment_percent >= 60 else "Cần đối thoại thêm để tìm tiếng nói chung")

    parent_report = f"""### BẢN TÓM TẮT DÀNH RIÊNG CHO PHỤ HUYNH (PARENT SUMMARY REPORT)
**Kính gửi Quý Phụ huynh,**

Hội đồng Cố vấn Tuyển sinh & Hướng nghiệp EduCompass AI trân trọng gửi tới Quý Phụ huynh bản phân tích tâm lý và chiến lược chọn ngành dựa trên khảo sát đồng thuận gia đình:

#### 1. Mức Độ Đồng Thuận Hiện Tại: **{alignment_percent}%** ({level_str})
{f"- ✅ **Điểm chung vững chắc:** {common_ground[0]['description']}" if common_ground else ''}
{f"- 💡 **Điểm cần trao đổi thêm:** {conflict_points[0]['advice']}" if conflict_points else '- Gia đình có sự thấu hiểu rất cao, các mục tiêu chọn trường đang rất hòa hợp.'}

#### 2. Giải Mã Tiềm Năng Ngành "{target_major_name}" Bằng Ngôn Ngữ Dễ Hiểu:
Nhiều phụ huynh thường lo lắng khi con chọn các ngành công nghệ hay kinh tế mới. Xin phụ huynh hoàn toàn an tâm:
- **Ngành này ra trường làm gì:** Sinh viên tốt nghiệp không chỉ ngồi lập trình hay gõ máy tính, mà là người xây dựng các giải pháp số hóa, tối ưu hóa quy trình kinh doanh, tài chính và tự động hóa cho các tập đoàn lớn, ngân hàng và doanh nghiệp FDI.
- **Thu nhập thực tế:** Mức lương khởi điểm của cử nhân/kỹ sư ngành này đạt từ **12 - 18 triệu VNĐ/tháng** (cao hơn mặt bằng chung 30-50%). Sau 3 năm, mức thu nhập có thể đạt **25 - 45 triệu VNĐ/tháng**.
- **Tính an toàn lâu dài:** Đây là các lĩnh vực cốt lõi được Chính phủ ưu tiên phát triển quốc gia đến năm 2030, cơ hội việc làm luôn rộng mở và không sợ bão hòa.

#### 3. Bảng Phân Tích Rủi Ro Thực Tế & Cách Khắc Phục Để Phụ Huynh An Tâm:
- **Rủi ro 1: Ngành học đòi hỏi tự học cao và công nghệ đổi mới liên tục.**
  -> *Giải pháp:* Ngay từ năm 1-2, các trường đại học hàng đầu đều đào tạo nền tảng Toán - Tin - Ngoại ngữ rất vững chắc. Sinh viên nắm vững gốc rễ sẽ làm chủ mọi công nghệ mới dễ dàng.
- **Rủi ro 2: Áp lực thi cử và điểm chuẩn đầu vào cao.**
  -> *Giải pháp:* EduCompass AI áp dụng Chiến lược Tỷ lệ Vàng (20% Thử thách - 50% Vừa sức - 30% An toàn), bảo đảm 100% con có bến đỗ đại học công lập uy tín.
- **Rủi ro 3: Chi phí học tập và sinh hoạt tại thành phố lớn.**
  -> *Giải pháp:* Nhà trường có quỹ học bổng khuyến khích học tập trích 8% học phí, các gói hỗ trợ ký túc xá và chính sách vay vốn sinh viên ưu đãi 6.6%/năm.

#### 4. Lộ Trình 4 Năm Đại Học Cụ Thể (Con sẽ học và làm gì?):
- **Năm 1–2:** Học các môn đại cương nền tảng (Toán, Triết học, Ngoại ngữ IELTS 6.0+) và rèn luyện kỹ năng mềm (làm việc nhóm, tư duy phản biện).
- **Năm 3:** Học sâu vào chuyên ngành, thi các chứng chỉ chuyên môn quốc tế (AWS, CFA, Google Data, PMP) và tham gia dự án thực tế.
- **Năm 4:** Đi thực tập có lương tại doanh nghiệp đối tác, hoàn thành khóa luận tốt nghiệp và nhận lời mời làm việc chính thức trước khi nhận bằng.

#### 5. Khung 4 Câu Hỏi Gợi Mở Để Cha Mẹ Trò Chuyện Cởi Mở Cùng Con:
1. "Con thích nhất điều gì khi hình dung về một ngày làm việc trong ngành này sau 4 năm nữa?"
2. "Bố mẹ rất muốn ủng hộ ước mơ của con, con đã chuẩn bị tâm lý cho những môn học khó và khối lượng bài tập lớn chưa?"
3. "Về chi phí học tập và sinh hoạt, gia đình mình cùng lên kế hoạch chi tiêu thế nào để vừa vặn nhất?"
4. "Nếu điểm thi có chênh lệch so với dự kiến, con đã có phương án trường dự phòng nào mà con vẫn thấy vui vẻ theo học chưa?"
"""

    return {
        "alignment_percent": alignment_percent,
        "overall_alignment_pct": alignment_percent,
        "alignment_level": level_str,
        "common_ground": common_ground,
        "conflict_points": conflict_points,
        "axis_comparisons": axis_comparisons,
        "parent_report": parent_report,
        "parent_summary_report": {
            "title": "Bản Tóm Tắt Định Hướng Dành Cho Phụ Huynh (Parent Summary Report)",
            "target_major": target_major_name,
            "reassurance_message": "Hội đồng Cố vấn Tuyển sinh EduCompass AI thấu hiểu sâu sắc tấm lòng và những nỗi lo lắng chính đáng của Quý Phụ huynh khi đứng trước bước ngoặt quan trọng của con. Báo cáo này được thiết kế để giải tỏa những băn khoăn, giúp gia đình có cùng một tiếng nói chung ấm áp và đồng hành vững chắc cùng con.",
            "plain_explanation": f"Ngành '{target_major_name}' là lĩnh vực đào tạo sinh viên trở thành chuyên gia giải quyết các vấn đề thực tiễn bằng tư duy logic và công nghệ hiện đại. Con không chỉ học lý thuyết sách vở mà được thực hành giải các bài toán thực tế của doanh nghiệp từ năm thứ hai.",
            "market_demand_salary": "Mức thu nhập khởi điểm dự kiến từ 12 - 18 triệu VNĐ/tháng, tăng lên 25 - 45 triệu VNĐ/tháng sau 3-5 năm tích lũy kinh nghiệm.",
            "risk_analysis": [
                {
                    "risk": "Công nghệ thay đổi nhanh chóng, kiến thức có thể bị lỗi thời",
                    "solution": "Chương trình đại học chú trọng dạy phương pháp tư duy và nền tảng cốt lõi, giúp sinh viên tự học và thích nghi trọn đời."
                },
                {
                    "risk": "Áp lực thi cử và điểm chuẩn trường top cạnh tranh gay gắt",
                    "solution": "Áp dụng chiến lược xếp 10 nguyện vọng theo Tỷ lệ Vàng: 20% Mơ ước - 50% Vừa sức - 30% An toàn, triệt tiêu hoàn toàn rủi ro trượt đại học."
                },
                {
                    "risk": "Gánh nặng học phí và sinh hoạt phí xa nhà",
                    "solution": "Minh bạch bài toán tài chính với Bộ tính ROI, tận dụng học bổng doanh nghiệp và chính sách vay vốn sinh viên ưu đãi."
                }
            ],
            "four_year_roadmap": [
                {
                    "stage": "Năm 1–2: Nền tảng & Kỹ năng",
                    "content": "Xây chắc nền móng Toán, Ngoại ngữ chuẩn hóa (IELTS 6.0+) và kỹ năng giao tiếp, làm việc nhóm."
                },
                {
                    "stage": "Năm 3: Chuyên môn & Chứng chỉ quốc tế",
                    "content": "Chinh phục các chứng chỉ ngành nghề được công nhận toàn cầu và tham gia nghiên cứu, làm dự án môn học."
                },
                {
                    "stage": "Năm 4: Thực tập & Tốt nghiệp",
                    "content": "Thực tập toàn thời gian tại các tập đoàn đối tác, nhận lương thực tập và ký hợp đồng lao động trước khi ra trường."
                }
            ],
            "family_dialogue_guide": [
                "Con hãy chia sẻ cho bố mẹ biết lý do con yêu thích ngành học này nhất là gì?",
                "Nếu học xa nhà, con đã chuẩn bị những kỹ năng tự lập nào cho bản thân?",
                "Bố mẹ luôn tin tưởng và ủng hộ con, chúng ta hãy cùng chọn ra 2 trường vừa sức để con yên tâm thi cử nhé!",
                "Con có cần bố mẹ hỗ trợ gì thêm trong giai đoạn ôn thi nước rút này không?"
            ],
            "next_step_action": "In bản báo cáo này ra giấy A4, cùng ngồi lại trong bữa cơm gia đình để lắng nghe và thấu hiểu nguyện vọng của con."
        }
    }

