import json
from .schema import get_connection, init_db

def seed_database(force_refresh: bool = False):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Kiểm tra xem đã có đủ dữ liệu mới chưa (ít nhất 55 trường và 40 ngành)
    cursor.execute("SELECT COUNT(*) FROM universities")
    uni_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM majors")
    maj_count = cursor.fetchone()[0]

    if uni_count >= 55 and maj_count >= 40 and not force_refresh:
        conn.close()
        return

    # Nếu chưa đủ dữ liệu hoặc force_refresh, làm mới CSDL để cập nhật các trường và ngành mới
    cursor.execute("DELETE FROM prospectus_rules")
    cursor.execute("DELETE FROM admission_benchmarks")
    cursor.execute("DELETE FROM majors")
    cursor.execute("DELETE FROM universities")

    # 1. Danh sách Trường Đại học Đầy Đủ Ba Miền (Chuẩn hóa & mở rộng theo Tuyensinhso.vn)
    universities = [
        # --- MIỀN BẮC (24 trường) ---
        ("BKHN", "Đại học Bách khoa Hà Nội", "Bắc", "Hà Nội", "Công lập", "25 - 45", "https://hust.edu.vn", "Top 1 Kỹ thuật & Công nghệ miền Bắc, đào tạo chuyên sâu và áp lực học tập cao."),
        ("UET", "Trường Đại học Công nghệ - ĐHQGHN", "Bắc", "Hà Nội", "Công lập", "20 - 35", "https://uet.vnu.edu.vn", "Trường công nghệ mũi nhọn thuộc ĐHQGHN, thế mạnh CNTT, AI và Bán dẫn."),
        ("NEU", "Trường Đại học Kinh tế Quốc dân", "Bắc", "Hà Nội", "Công lập", "22 - 38", "https://neu.edu.vn", "Trường đầu ngành kinh tế, tài chính và quản trị tại miền Bắc."),
        ("FTU", "Trường Đại học Ngoại thương (Cơ sở Hà Nội)", "Bắc", "Hà Nội", "Công lập", "25 - 45", "https://ftu.edu.vn", "Thương hiệu hàng đầu về Kinh tế đối ngoại, năng động, chuẩn quốc tế."),
        ("HMU", "Trường Đại học Y Hà Nội", "Bắc", "Hà Nội", "Công lập", "27 - 55", "https://hmu.edu.vn", "Cơ sở đào tạo y khoa danh giá bậc nhất Việt Nam, điểm chuẩn luôn ở mức đỉnh."),
        ("PTIT", "Học viện Công nghệ Bưu chính Viễn thông", "Bắc", "Hà Nội", "Công lập", "24 - 32", "https://ptit.edu.vn", "Thế mạnh lớn về Viễn thông, CNTT, Đa phương tiện và An toàn thông tin."),
        ("DAV", "Học viện Ngoại giao", "Bắc", "Hà Nội", "Công lập", "24 - 35", "https://dav.edu.vn", "Cái nôi ngoại giao, Quan hệ quốc tế, Luật quốc tế, Truyền thông và Ngôn ngữ ngoại giao."),
        ("AOF", "Học viện Tài chính", "Bắc", "Hà Nội", "Công lập", "20 - 30", "https://hvtc.edu.vn", "Cái nôi đào tạo chuyên gia Tài chính - Ngân hàng, Kế toán - Kiểm toán hàng đầu miền Bắc."),
        ("HLU", "Trường Đại học Luật Hà Nội", "Bắc", "Hà Nội", "Công lập", "22 - 32", "https://hlu.edu.vn", "Trường đại học trọng điểm quốc gia về đào tạo pháp luật, đầu ngành Luật tại Việt Nam."),
        ("UEB", "Trường Đại học Kinh tế - ĐHQGHN", "Bắc", "Hà Nội", "Công lập", "30 - 45", "https://ueb.edu.vn", "Thành viên ĐHQGHN, đào tạo Kinh tế quốc tế, Quản trị kinh doanh chuẩn quốc tế."),
        ("ULIS", "Trường Đại học Ngoại ngữ - ĐHQGHN", "Bắc", "Hà Nội", "Công lập", "22 - 38", "https://ulis.vnu.edu.vn", "Trung tâm đào tạo ngoại ngữ, sư phạm ngoại ngữ và quốc tế học hàng đầu Việt Nam."),
        ("TMU", "Trường Đại học Thương mại", "Bắc", "Hà Nội", "Công lập", "22 - 32", "https://tmu.edu.vn", "Đào tạo Thương mại điện tử, Marketing, Logistics và Quản trị kinh doanh."),
        ("HNUE", "Trường Đại học Sư phạm Hà Nội", "Bắc", "Hà Nội", "Công lập", "0 - 15 (Miễn học phí theo NĐ 116)", "https://hnue.edu.vn", "Trường sư phạm trọng điểm quốc gia, môi trường sư phạm chuẩn mực."),
        ("HAU", "Trường Đại học Kiến trúc Hà Nội", "Bắc", "Hà Nội", "Công lập", "18 - 28", "https://hau.edu.vn", "Cơ sở đào tạo Kiến trúc sư, Thiết kế nội thất và Thiết kế thời trang hàng đầu miền Bắc."),
        ("MTCN", "Trường Đại học Mỹ thuật Công nghiệp", "Bắc", "Hà Nội", "Công lập", "16 - 25", "https://mythuatcongnghiep.edu.vn", "Trung tâm đào tạo Thiết kế Thời trang, Đồ họa và Mỹ thuật ứng dụng danh tiếng."),
        ("HANU", "Trường Đại học Hà Nội", "Bắc", "Hà Nội", "Công lập", "20 - 32", "https://hanu.edu.vn", "Thế mạnh đào tạo ngoại ngữ Anh, Trung, Hàn, Nhật, Tây Ban Nha và Du lịch quốc tế."),
        ("AJC", "Học viện Báo chí & Tuyên truyền", "Bắc", "Hà Nội", "Công lập", "18 - 28", "https://ajc.hcma.vn", "Cái nôi báo chí truyền thông, quan hệ công chúng (PR) và truyền hình cả nước."),
        ("HaUI", "Trường Đại học Công nghiệp Hà Nội", "Bắc", "Hà Nội", "Công lập", "19 - 28", "https://haui.edu.vn", "Thế mạnh đào tạo thực hành Kỹ thuật Ô tô, Điện tử, Cơ khí và Du lịch khách sạn."),
        ("UTC", "Trường Đại học Giao thông Vận tải", "Bắc", "Hà Nội", "Công lập", "18 - 26", "https://utc.edu.vn", "Đầu ngành về Logistics, Kỹ thuật Ô tô, Cầu đường và Đường sắt cao tốc."),
        ("HPMU", "Trường Đại học Y Dược Hải Phòng", "Bắc", "Hải Phòng", "Công lập", "28 - 48", "https://hpmu.edu.vn", "Cơ sở đào tạo Y đa khoa, Răng Hàm Mặt, Dược học và Y học biển uy tín miền Bắc."),
        ("KMA", "Học viện Kỹ thuật Mật mã", "Bắc", "Hà Nội", "Công lập", "18 - 25", "https://actvn.edu.vn", "Cơ sở đầu ngành về An toàn thông tin, Mật mã học, Lập trình nhúng và CNTT."),
        ("HOU", "Trường Đại học Mở Hà Nội", "Bắc", "Hà Nội", "Công lập", "18 - 26", "https://hou.edu.vn", "Đại học công lập đa ngành về Luật, Kinh tế, CNTT, Thiết kế và Ngôn ngữ chi phí hợp lý."),
        ("VNUA", "Học viện Nông nghiệp Việt Nam", "Bắc", "Hà Nội", "Công lập", "16 - 24", "https://vnua.edu.vn", "Đào tạo Bác sĩ Thú y, Công nghệ Sinh học và Nông nghiệp công nghệ cao trọng điểm."),
        ("FPT", "Trường Đại học FPT", "Bắc", "Hà Nội", "Tư thục", "60 - 90", "https://fpt.edu.vn", "Chương trình thực tiễn, đào tạo bằng tiếng Anh, 100% sinh viên thực tập doanh nghiệp."),

        # --- MIỀN TRUNG (11 trường) ---
        ("DUT", "Trường Đại học Bách khoa - ĐH Đà Nẵng", "Trung", "Đà Nẵng", "Công lập", "22 - 32", "https://dut.udn.vn", "Trung tâm đào tạo kỹ thuật công nghệ lớn nhất miền Trung."),
        ("DUE", "Trường Đại học Kinh tế - ĐH Đà Nẵng", "Trung", "Đà Nẵng", "Công lập", "20 - 30", "https://due.udn.vn", "Trường kinh tế hàng đầu khu vực miền Trung và Tây Nguyên."),
        ("HMED", "Trường Đại học Y Dược - ĐH Huế", "Trung", "Thừa Thiên Huế", "Công lập", "26 - 50", "https://huemed-univ.edu.vn", "Trung tâm y tế và đào tạo bác sĩ, dược sĩ uy tín khu vực miền Trung."),
        ("UTE_DN", "Trường ĐH Sư phạm Kỹ thuật - ĐH Đà Nẵng", "Trung", "Đà Nẵng", "Công lập", "18 - 26", "https://ute.udn.vn", "Thế mạnh Kỹ thuật Ô tô, Cơ điện tử và Kỹ thuật điều khiển tự động."),
        ("HUL", "Trường Đại học Ngoại ngữ - ĐH Huế", "Trung", "Thừa Thiên Huế", "Công lập", "16 - 25", "https://hucfl.edu.vn", "Đào tạo Ngôn ngữ Anh, Trung, Hàn, Nhật và Quốc tế học miền Trung."),
        ("HUAF", "Trường Đại học Nông Lâm - ĐH Huế", "Trung", "Thừa Thiên Huế", "Công lập", "15 - 22", "https://huaf.edu.vn", "Thế mạnh đào tạo Bác sĩ Thú y, Chăn nuôi và Công nghệ sinh học thủy sản."),
        ("NTU", "Trường Đại học Nha Trang", "Trung", "Khánh Hòa", "Công lập", "16 - 25", "https://ntu.edu.vn", "Thế mạnh Quản trị Du lịch - Khách sạn biển, Kỹ thuật Hàng hải và Thủy sản."),
        ("QNU", "Trường Đại học Quy Nhơn", "Trung", "Bình Định", "Công lập", "15 - 24", "https://qnu.edu.vn", "Trung tâm đào tạo Sư phạm, Khoa học dữ liệu và Du lịch Nam Trung Bộ."),
        ("VINH", "Trường Đại học Vinh", "Trung", "Nghệ An", "Công lập", "16 - 25", "https://vinhuni.edu.vn", "Đại học đa ngành trọng điểm khu vực Bắc Trung Bộ."),
        ("TDU", "Trường Đại học Tây Nguyên", "Trung", "Đắk Lắk", "Công lập", "15 - 25", "https://ttn.edu.vn", "Đào tạo Y đa khoa, Thú y, Nông lâm nghiệp lớn nhất Tây Nguyên."),
        ("DTU", "Trường Đại học Duy Tân", "Trung", "Đà Nẵng", "Tư thục", "30 - 55", "https://duytan.edu.vn", "Đại học tư thục uy tín miền Trung, mạnh về Y Dược, Du lịch và CNTT."),

        # --- MIỀN NAM (19 trường) ---
        ("HCMUT", "Trường Đại học Bách khoa - ĐHQG-HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "30 - 50", "https://hcmut.edu.vn", "Đại học kỹ thuật danh tiếng bậc nhất miền Nam."),
        ("UIT", "Trường Đại học Công nghệ Thông tin - ĐHQG-HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "32 - 45", "https://uit.edu.vn", "Chuyên sâu hoàn toàn về Khoa học máy tính, AI, Kỹ thuật dữ liệu."),
        ("UEH", "Đại học Kinh tế TP. Hồ Chí Minh", "Nam", "TP. Hồ Chí Minh", "Công lập", "28 - 48", "https://ueh.edu.vn", "Đại học đa ngành về Kinh tế, Quản lý công và Đổi mới sáng tạo phía Nam."),
        ("UMP", "Đại học Y Dược TP. Hồ Chí Minh", "Nam", "TP. Hồ Chí Minh", "Công lập", "35 - 70", "https://ump.edu.vn", "Biểu tượng y khoa phương Nam, chất lượng đào tạo bác sĩ, răng hàm mặt đầu ngành."),
        ("HUB", "Trường Đại học Ngân hàng TP. Hồ Chí Minh", "Nam", "TP. Hồ Chí Minh", "Công lập", "24 - 36", "https://hub.edu.vn", "Đầu ngành về Tài chính - Ngân hàng, Fintech và Kinh tế số tại phương Nam."),
        ("UFM", "Trường Đại học Tài chính - Marketing", "Nam", "TP. Hồ Chí Minh", "Công lập", "25 - 40", "https://ufm.edu.vn", "Top 1 phương Nam về Marketing, Kinh doanh thương mại, Logistics và Thẩm định giá."),
        ("HCMUE", "Trường Đại học Sư phạm TP. Hồ Chí Minh", "Nam", "TP. Hồ Chí Minh", "Công lập", "0 - 15 (Miễn học phí theo NĐ 116)", "https://hcmue.edu.vn", "Trường đại học sư phạm trọng điểm phía Nam, uy tín bậc nhất về đào tạo giáo viên."),
        ("USSH_HCM", "Trường ĐH Khoa học Xã hội & Nhân văn - ĐHQG-HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "18 - 30", "https://hcmussh.edu.vn", "Hàng đầu về Báo chí truyền thông, Tâm lý học, Ngôn ngữ học miền Nam."),
        ("HCMUS", "Trường Đại học Khoa học Tự nhiên - ĐHQG-HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "26 - 40", "https://hcmus.edu.vn", "Cái nôi khoa học cơ bản, Khoa học dữ liệu, Sinh học và Công nghệ bán dẫn."),
        ("UAH", "Trường Đại học Kiến trúc TP. Hồ Chí Minh", "Nam", "TP. Hồ Chí Minh", "Công lập", "24 - 38", "https://uah.edu.vn", "Top 1 miền Nam về Kiến trúc, Thiết kế Thời trang, Nội thất và Mỹ thuật đô thị."),
        ("HCMUTE", "Trường ĐH Sư phạm Kỹ thuật TP.HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "26 - 36", "https://hcmute.edu.vn", "Đầu tàu Kỹ thuật Ô tô, Robot, Cơ điện tử, Công nghệ may và Điện tử."),
        ("NLU", "Trường Đại học Nông Lâm TP. Hồ Chí Minh", "Nam", "TP. Hồ Chí Minh", "Công lập", "18 - 28", "https://hcmuaf.edu.vn", "Đào tạo Bác sĩ Thú y, Công nghệ Sinh học, Cảnh quan và Lâm nghiệp hàng đầu."),
        ("CTU", "Trường Đại học Cần Thơ", "Nam", "Cần Thơ", "Công lập", "17 - 26", "https://ctu.edu.vn", "Trung tâm đào tạo lớn nhất ĐBSCL về Nông nghiệp, Thủy sản, Sư phạm và CNTT."),
        ("CTUMP", "Trường Đại học Y Dược Cần Thơ", "Nam", "Cần Thơ", "Công lập", "35 - 55", "https://ctump.edu.vn", "Trung tâm đào tạo bác sĩ, dược sĩ và nhân lực y tế trọng điểm vùng ĐBSCL."),
        ("PNTU", "Trường Đại học Y khoa Phạm Ngọc Thạch", "Nam", "TP. Hồ Chí Minh", "Công lập", "32 - 55", "https://pnt.edu.vn", "Đào tạo Y đa khoa, Dược học, Điều dưỡng tuyến đầu TP.HCM."),
        ("TDTU", "Trường Đại học Tôn Đức Thắng", "Nam", "TP. Hồ Chí Minh", "Công lập", "26 - 42", "https://tdtu.edu.vn", "Cơ sở vật chất chuẩn quốc tế 5 sao, mạnh về Thiết kế đồ họa, Du lịch, CNTT và Dược."),
        ("RMIT", "Đại học Quốc tế RMIT Việt Nam", "Nam", "TP. Hồ Chí Minh", "Tư thục", "280 - 350", "https://rmit.edu.vn", "Môi trường quốc tế 100%, chuẩn giáo dục Australia, bằng cấp toàn cầu."),

        # --- TRƯỜNG PHÂN KHÚC ĐIỂM CHUẨN VỪA SỨC (18 - 23 ĐIỂM) ---
        ("TLU", "Trường Đại học Thủy lợi", "Bắc", "Hà Nội", "Công lập", "18 - 28", "https://tlu.edu.vn", "Thế mạnh lớn về CNTT, Kỹ thuật Phần mềm, Kỹ thuật Ô tô, Logistics và Xây dựng."),
        ("EPU", "Trường Đại học Điện lực", "Bắc", "Hà Nội", "Công lập", "18 - 26", "https://epu.edu.vn", "Thế mạnh về Kỹ thuật Điện, Năng lượng, Tự động hóa và CNTT."),
        ("HUMG", "Trường Đại học Mỏ - Địa chất", "Bắc", "Hà Nội", "Công lập", "15 - 24", "https://humg.edu.vn", "Đào tạo CNTT, Kỹ thuật Điều khiển & Tự động hóa, Ô tô và Kỹ thuật Địa chất."),
        ("HUIT", "Trường Đại học Công Thương TP.HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "18 - 28", "https://huit.edu.vn", "Thế mạnh về Kỹ thuật Phần mềm, Cơ điện tử, Công nghệ Thực phẩm và Marketing."),
        ("UTH", "Trường ĐH Giao thông Vận tải TP.HCM", "Nam", "TP. Hồ Chí Minh", "Công lập", "18 - 26", "https://ut.edu.vn", "Đầu ngành về Logistics, Quản lý Cảng, Kỹ thuật Ô tô và CNTT phía Nam."),
        ("SGU", "Trường Đại học Sài Gòn", "Nam", "TP. Hồ Chí Minh", "Công lập", "16 - 25", "https://sgu.edu.vn", "Đào tạo Sư phạm, CNTT, Kỹ thuật Điện tử và Quản trị Kinh doanh uy tín tại TP.HCM.")
    ]

    cursor.executemany("""
    INSERT INTO universities (code, name, region, province, type, tuition_range, website, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, universities)

    # 2. Danh mục Ngành Đào tạo Chuẩn Quốc Gia (Dựa trên Tuyensinhso.vn - 44 ngành trọng điểm)
    majors = [
        # --- NHÓM MÁY TÍNH & CNTT ---
        ("IT-CS", "Khoa học Máy tính & Trí tuệ Nhân tạo", "Công nghệ thông tin", "IRC", 
         "Nghiên cứu cấu trúc dữ liệu, thuật toán máy học, deep learning và kiến trúc hệ thống AI quy mô lớn.", 
         "Kỹ sư AI, Chuyên viên Machine Learning, Nhà khoa học dữ liệu, Thuật toán cao cấp.", "Tư duy logic trừu tượng, kiên trì gỡ lỗi, đam mê toán học.", "18 - 35 triệu/tháng"),

        ("IT-SE", "Kỹ thuật Phần mềm (Software Engineering)", "Công nghệ thông tin", "RIC", 
         "Xây dựng ứng dụng di động, web, hệ thống backend và dịch vụ đám mây với quy trình Agile/DevOps hiện đại.", 
         "Lập trình viên Fullstack, Mobile App Developer, Solution Architect, DevOps Engineer.", "Thích biến ý tưởng thành sản phẩm, tư duy giải quyết vấn đề.", "15 - 30 triệu/tháng"),

        ("IT-CYBER", "An toàn Thông tin & An ninh Mạng", "Công nghệ thông tin", "RIC", 
         "Bảo vệ mạng lưới dữ liệu, kiểm thử xâm nhập (Penetration Testing), phòng chống tấn công mạng và mật mã học.", 
         "Chuyên viên SOC, Kỹ sư An ninh mạng, Pentester, Tư vấn bảo mật ngân hàng.", "Cẩn trọng, nguyên tắc, óc phân tích điều tra.", "16 - 32 triệu/tháng"),

        ("IT-DS", "Khoa học Dữ liệu (Data Science)", "Công nghệ thông tin", "IRC", 
         "Khai phá dữ liệu lớn (Big Data), thống kê phân tích và xây dựng mô hình dự báo kinh doanh thông minh (BI).", 
         "Data Analyst, Data Engineer, Trưởng nhóm phân tích dữ liệu kinh doanh.", "Tư duy toán thống kê, khả năng kể chuyện bằng dữ liệu.", "16 - 30 triệu/tháng"),

        ("IT-MIS", "Hệ thống Thông tin Quản lý & Chuyển đổi Số (MIS)", "Công nghệ thông tin", "CIE", 
         "Cầu nối giữa kinh doanh và công nghệ, phân tích luồng nghiệp vụ (Business Analysis - BA), quản trị hệ thống ERP/CRM số.", 
         "Business Analyst (IT BA), Chuyên viên triển khai ERP SAP/Oracle, Quản trị hệ thống dữ liệu doanh nghiệp.", "Tư duy logic kết hợp khả năng giao tiếp, thích giải quyết bài toán vận hành.", "15 - 30 triệu/tháng"),

        # --- NHÓM KỸ THUẬT & CÔNG NGHỆ ---
        ("ENG-ROBOT", "Kỹ thuật Robot & Cơ điện tử", "Khoa học Kỹ thuật", "RIC", 
         "Tích hợp cơ khí chính xác, điều khiển điện tử và trí tuệ nhân tạo để chế tạo robot tự hành và dây chuyền tự động.", 
         "Kỹ sư tự động hóa, Thiết kế hệ thống nhúng (Embedded), Lập trình vi điều khiển PLC.", "Khéo tay, thích lắp ráp phần cứng, tư duy không gian.", "14 - 26 triệu/tháng"),

        ("ENG-SEMI", "Kỹ thuật Vi mạch & Bán dẫn (Semiconductor)", "Khoa học Kỹ thuật", "IRE", 
         "Thiết kế vi mạch tích hợp (IC Design), kiểm thử vật lý bán dẫn và quy trình sản xuất chip thế hệ mới.", 
         "Kỹ sư thiết kế vi mạch (RTL, Physical Design), Chuyên viên kiểm thử chip tại Marvell, Synopsys.", "Tập trung cao độ, kiến thức vật lý điện tử vững.", "18 - 40 triệu/tháng"),

        ("ENG-EE", "Kỹ thuật Điện - Điện tử & Năng lượng Tái tạo", "Khoa học Kỹ thuật", "RIC", 
         "Thiết kế hệ thống truyền tải điện lưới thông minh (Smart Grid), điện gió/mặt trời, trạm sạc xe điện và tự động hóa công nghiệp.", 
         "Kỹ sư hệ thống điện tại EVN, Kỹ sư thiết kế tủ bảng điện Schneider, Kỹ sư pin mặt trời/xe điện.", "Tư duy logic kỹ thuật, cẩn trọng an toàn điện, thích thực hành.", "14 - 28 triệu/tháng"),

        ("ENG-AUTO", "Kỹ thuật Ô tô & Xe điện Thông minh", "Khoa học Kỹ thuật", "RIC", 
         "Nghiên cứu động cơ đốt trong, hệ truyền động điện xe thông minh (EV), chẩn đoán điện tử và dây chuyền lắp ráp.", 
         "Kỹ sư R&D Ô tô/Xe điện tại VinFast, Toyota, Thaco; Trưởng xưởng dịch vụ kỹ thuật.", "Đam mê xe cộ, tư duy không gian kỹ thuật, tính cẩn trọng.", "14 - 28 triệu/tháng"),

        ("ENG-CIVIL", "Kỹ thuật Xây dựng & Kết cấu Hạ tầng Đô thị", "Khoa học Kỹ thuật", "RIC", 
         "Tính toán kết cấu bê tông cốt thép, giám sát thi công cầu đường, tòa nhà cao tầng và quy hoạch công trình giao thông.", 
         "Kỹ sư kết cấu, Chỉ huy trưởng công trường Coteccons/Vingroup, Chuyên viên thẩm định dự án.", "Sức khỏe dẻo dai, tư duy hình học không gian, tinh thần trách nhiệm.", "13 - 28 triệu/tháng"),

        ("FOOD-CHEM", "Công nghệ Hóa học, Thực phẩm & Dược mỹ phẩm", "Khoa học Kỹ thuật", "IRE", 
         "Nghiên cứu công thức thực phẩm dinh dưỡng, chiết xuất dược mỹ phẩm tự nhiên và quản lý dây chuyền sản xuất vi sinh.", 
         "Chuyên viên R&D thực phẩm tại Unilever, Vinamilk, CP; Kỹ sư quản lý chất lượng QA/QC.", "Đam mê hóa sinh thực nghiệm, khứu giác vị giác nhạy bén, cẩn thận.", "12 - 26 triệu/tháng"),

        ("BIO-TECH", "Công nghệ Sinh học & Kỹ thuật Y sinh", "Khoa học Kỹ thuật", "IRE", 
         "Nghiên cứu ứng dụng công nghệ gen, liệu pháp tế bào gốc, sản xuất vắc-xin và chế phẩm sinh học bảo vệ môi trường.", 
         "Kỹ sư xét nghiệm di truyền gen, Chuyên viên R&D dược phẩm sinh học, Giám định viên vi sinh.", "Đam mê phòng thí nghiệm vô trùng, khả năng tư duy vi mô.", "13 - 26 triệu/tháng"),

        ("AGRI-VET", "Bác sĩ Thú y & Chăm sóc Thú cưng", "Khoa học Kỹ thuật", "RIS", 
         "Chẩn đoán bệnh, phẫu thuật, tiêm chủng và điều trị nội trú cho động vật cảnh thú cưng và gia súc gia cầm.", 
         "Bác sĩ trưởng phòng khám thú y thú cưng, Chuyên gia dinh dưỡng vật nuôi, Kiểm dịch viên.", "Tình yêu thương động vật, không sợ máu/mùi bẩn, khéo tay.", "13 - 30 triệu/tháng"),

        # --- NHÓM KINH DOANH, TÀI CHÍNH & QUẢN LÝ ---
        ("ACC-AUD", "Kế toán & Kiểm toán Chuyên nghiệp (Auditing)", "Kinh tế & Quản lý", "CEI", 
         "Đào tạo nghiệp vụ kế toán tài chính, kiểm toán báo cáo tài chính quốc tế (IFRS), thuế và chuẩn mực kế toán kiểm toán.", 
         "Kiểm toán viên Big4 (PwC, Deloitte, EY, KPMG), Kế toán trưởng, Chuyên viên tư vấn thuế.", "Tỉ mỉ, kỷ luật cao, yêu thích số liệu, trung thực.", "14 - 32 triệu/tháng"),

        ("BUS-ADMIN", "Quản trị Kinh doanh & Khởi nghiệp Đổi mới", "Kinh tế & Quản lý", "ECS", 
         "Đào tạo kỹ năng quản trị chiến lược, điều hành doanh nghiệp, phân tích thị trường và quản lý dự án khởi nghiệp.", 
         "Giám đốc điều hành (CEO), Trưởng phòng kinh doanh, Chuyên viên quản trị dự án, Khởi nghiệp.", "Tư duy lãnh đạo, giao tiếp đàm phán, nhạy bén kinh doanh.", "13 - 35 triệu/tháng"),

        ("ECO-IB", "Kinh doanh Quốc tế & Xuất nhập khẩu", "Kinh tế & Quản lý", "ECS", 
         "Nghiên cứu chuỗi cung ứng toàn cầu, đàm phán hợp đồng ngoại thương, chiến lược thâm nhập thị trường quốc tế.", 
         "Chuyên viên Xuất nhập khẩu (Forwarder), Quản lý chuỗi cung ứng quốc tế, Phát triển thị trường.", "Ngoại ngữ lưu loát, hướng ngoại, giao tiếp tự tin.", "14 - 28 triệu/tháng"),

        ("ECO-INT", "Kinh tế Quốc tế & Kinh tế Đối ngoại", "Kinh tế & Quản lý", "ECS", 
         "Phân tích chính sách vĩ mô toàn cầu, dòng chảy vốn FDI, thương mại tự do (FTA, WTO) và thị trường tài chính thế giới.", 
         "Chuyên viên phân tích vĩ mô, Chuyên viên nghiên cứu thị trường quốc tế, Quản lý xúc tiến thương mại.", "Tư duy bao quát vĩ mô, giỏi ngoại ngữ và nhạy bén thời cuộc thế giới.", "15 - 32 triệu/tháng"),

        ("ECO-MKT", "Marketing Kỹ thuật số & Truyền thông Tiếp thị", "Kinh tế & Quản lý", "EAS", 
         "Sáng tạo chiến dịch quảng cáo đa kênh (SEO/SEM, Content, Social Media), phân tích hành vi người tiêu dùng.", 
         "Digital Marketing Lead, Content Creator, Brand Manager, Media Planner.", "Tư duy sáng tạo, nhạy bén xu hướng MXH, thích giao tiếp.", "12 - 25 triệu/tháng"),

        ("ECO-FIN", "Tài chính - Ngân hàng & Fintech", "Kinh tế & Quản lý", "CEI", 
         "Quản lý danh mục đầu tư chứng khoán, định giá doanh nghiệp, bảo hiểm và ứng dụng thanh toán điện tử số.", 
         "Chuyên viên Phân tích đầu tư, Giao dịch viên ngân hàng, Chuyên gia định phí rủi ro, Chuyên viên Fintech.", "Nhạy bén với con số, cẩn trọng, kỷ luật và chịu áp lực.", "15 - 35 triệu/tháng"),

        ("ECO-LOG", "Logistics & Quản lý Chuỗi Cung ứng", "Kinh tế & Quản lý", "ECR", 
         "Tối ưu hóa vận chuyển hàng hóa, quản lý kho bãi thông minh, dự báo nhu cầu lưu thông sản phẩm toàn cầu.", 
         "Chuyên viên Điều độ vận tải, Quản lý kho hàng Shopee/Lazada, Forwarder cảng biển.", "Tư duy hệ thống, khả năng sắp xếp logic, xử lý sự cố nhanh.", "13 - 26 triệu/tháng"),

        ("ECO-ECOM", "Thương mại Điện tử & Kinh tế Số", "Kinh tế & Quản lý", "ECS", 
         "Vận hành gian hàng trực tuyến, tối ưu hóa trải nghiệm mua sắm số, quản trị logistics bán lẻ và marketing sàn.", 
         "Chuyên viên E-Commerce, Quản lý sàn TMĐT (Shopee/TikTok Shop), Trưởng nhóm Digital Sales.", "Nhạy bén xu hướng mua sắm số, tư duy kinh doanh thực chiến.", "13 - 26 triệu/tháng"),

        ("TOUR-HOSP", "Quản trị Du lịch & Khách sạn Quốc tế", "Kinh tế & Quản lý", "ESC", 
         "Vận hành chuỗi khu nghỉ dưỡng 5 sao, thiết kế tour trải nghiệm quốc tế, lễ tân cao cấp và nghệ thuật ẩm thực.", 
         "Giám đốc tiền sảnh resort, Quản lý F&B chuỗi khách sạn 5 sao, Điều hành tour quốc tế.", "Chỉ số EQ cao, nụ cười thân thiện, giao tiếp tự tin, giỏi ngoại ngữ.", "12 - 28 triệu/tháng"),

        # --- NHÓM SỨC KHỎE & Y DƯỢC ---
        ("MED-DOC", "Y đa khoa (Bác sĩ Chữa bệnh)", "Y Dược", "ISR", 
         "Chẩn đoán, điều trị, phẫu thuật và chăm sóc sức khỏe cộng đồng trong các bệnh viện tuyến đầu.", 
         "Bác sĩ chuyên khoa tại các bệnh viện công/tư, Viện nghiên cứu y học, Giảng viên trường y.", "Lòng trắc ẩn, đức hy sinh, sức bền thể lực và tâm lý.", "15 - 45 triệu/tháng"),

        ("MED-DENT", "Bác sĩ Răng - Hàm - Mặt (Dentistry)", "Y Dược", "ISR", 
         "Chẩn đoán, phẫu thuật chỉnh nha, phục hình răng sứ, cấy ghép Implant và điều trị bệnh lý răng hàm mặt.", 
         "Bác sĩ Răng Hàm Mặt tại bệnh viện trung ương, Chủ phòng khám nha khoa thẩm mỹ cao cấp.", "Khéo tay, tỉ mỉ tuyệt đối, sức bền cơ bắp, thấu hiểu bệnh nhân.", "25 - 60 triệu/tháng"),

        ("MED-PHARM", "Dược học (Pharmacology)", "Y Dược", "IRC", 
         "Nghiên cứu phát triển thuốc, bào chế dược phẩm, kiểm nghiệm chất lượng và dược lâm sàng bệnh viện.", 
         "Dược sĩ bệnh viện, Nghiên cứu R&D sản xuất thuốc, Trình dược viên chuyên nghiệp.", "Tỉ mỉ, chính xác tuyệt đối, đam mê hóa học và sinh học.", "14 - 30 triệu/tháng"),

        ("MED-NURS", "Điều dưỡng & Kỹ thuật Phục hồi Chức năng", "Y Dược", "SIC", 
         "Chăm sóc bệnh nhân toàn diện, thực hiện y lệnh, vật lý trị liệu phục hồi chức năng và cấp cứu tuyến đầu.", 
         "Điều dưỡng trưởng bệnh viện, Chuyên viên phục hồi chức năng, Cơ hội làm việc tại Nhật Bản, Đức, Úc.", "Lòng trắc ẩn, ân cần, sức khỏe tốt, chịu được áp lực ca trực.", "10 - 25 triệu/tháng"),

        # --- NHÓM PHÁP LUẬT ---
        ("LAW-INT", "Luật Kinh tế & Luật Thương mại Quốc tế", "Pháp luật", "ECS", 
         "Giải quyết tranh chấp hợp đồng kinh doanh, tư vấn sáp nhập doanh nghiệp (M&A) và sở hữu trí tuệ.", 
         "Luật sư doanh nghiệp, Chuyên viên Pháp chế (In-house Legal), Trọng tài thương mại.", "Lập luận chặt chẽ, tư duy phản biện, đàm phán xuất sắc.", "15 - 32 triệu/tháng"),

        ("LAW-CIVIL", "Luật học, Luật Dân sự & Tư pháp Hình sự", "Pháp luật", "ECS", 
         "Nghiên cứu hệ thống pháp luật nhà nước, tố tụng hình sự, tranh chấp dân sự đất đai và bảo vệ quyền công dân.", 
         "Thẩm phán, Kiểm sát viên, Luật sư tranh tụng tòa án, Chuyên viên pháp lý cơ quan nhà nước.", "Lập luận logic thép, bản lĩnh vững vàng, bảo vệ công lý và liêm chính.", "14 - 30 triệu/tháng"),

        # --- NHÓM BÁO CHÍ, TRUYỀN THÔNG & QUAN HỆ CÔNG CHÚNG ---
        ("SOC-JOUR", "Báo chí & Truyền thông Đa phương tiện", "Xã hội & Nhân văn", "ASE", 
         "Sản xuất nội dung truyền hình, podcast, viết phóng sự báo điện tử, biên kịch và quan hệ công chúng (PR).", 
         "Nhà báo số, Chuyên viên PR & Tổ chức sự kiện, Copywriter, Biên tập viên nội dung.", "Tò mò, phản biện sắc bén, khả năng viết lách lôi cuốn.", "12 - 24 triệu/tháng"),

        ("SOC-PR", "Quan hệ Công chúng & Tổ chức Sự kiện (PR)", "Xã hội & Nhân văn", "EAS", 
         "Xây dựng uy tín thương hiệu tổ chức, xử lý khủng hoảng truyền thông, tổ chức sự kiện lớn và kết nối báo chí.", 
         "Chuyên viên PR & Truyền thông nội bộ, Chuyên gia quản lý sự kiện (Event Planner), Người phát ngôn.", "Hoạt ngôn, tư duy ứng biến linh hoạt, năng động.", "13 - 28 triệu/tháng"),

        ("SOC-MULTI", "Truyền thông Đa phương tiện & Kỹ xảo Đồ họa Số", "Xã hội & Nhân văn", "ARE", 
         "Sản xuất video viral, kỹ xảo điện ảnh 3D/VFX, quản trị kênh YouTube/TikTok triệu view và sáng tạo nội dung số.", 
         "Creative Director, Video Producer, Motion Graphic Designer, Chuyên gia sáng tạo nội dung đa nền tảng.", "Tư duy thị giác sáng tạo, nhạy bén xu hướng viral, thành thạo đồ họa.", "14 - 30 triệu/tháng"),

        ("SOC-IR", "Quan hệ Quốc tế & Ngoại giao Toàn cầu", "Xã hội & Nhân văn", "EAS", 
         "Nghiên cứu địa chính trị, luật pháp quốc tế, lễ tân ngoại giao, đàm phán hiệp định đa phương và đối ngoại nhân dân.", 
         "Chuyên viên ngoại giao Bộ Ngoại giao, Đại sứ quán, Cán bộ tổ chức quốc tế (UN, ASEAN), Điều phối viên NGO.", "Tư duy phản biện sắc bén, hiểu biết văn hóa sâu rộng, hoạt ngôn.", "15 - 35 triệu/tháng"),

        # --- NHÓM NHÂN VĂN & NGÔN NGỮ ---
        ("SOC-ENG", "Ngôn ngữ Anh & Biên phiên dịch Quốc tế", "Xã hội & Nhân văn", "ASE", 
         "Nắm vững văn hóa, ngữ âm, dịch thuật hội nghị cabin cao cấp và tiếng Anh thương mại quốc tế.", 
         "Biên phiên dịch viên ngoại giao, Giảng viên tiếng Anh/IELTS, Chuyên viên đối ngoại.", "Nhạy bén ngôn từ, trí nhớ ngắn hạn tốt, phản xạ nghe nói linh hoạt.", "12 - 25 triệu/tháng"),

        ("SOC-CHINESE", "Ngôn ngữ & Thương mại Trung Quốc", "Xã hội & Nhân văn", "ASE", 
         "Thành thạo HSK 6, dịch thuật hội nghị và thương mại song phương Việt - Trung trong chuỗi cung ứng toàn cầu.", 
         "Biên phiên dịch tiếng Trung cấp cao, Chuyên viên mua hàng nhập khẩu, Quản lý dự án FDI Trung Quốc.", "Trí nhớ thị giác tốt, phản xạ ngôn ngữ linh hoạt, thích giao thoa văn hóa.", "14 - 32 triệu/tháng"),

        ("SOC-KOREAN", "Ngôn ngữ & Văn hóa Hàn Quốc", "Xã hội & Nhân văn", "ASE", 
         "Đào tạo TOPIK 5-6, văn hóa doanh nghiệp Hàn Quốc, thông dịch cabin và xúc tiến đầu tư các tập đoàn Chaebol.", 
         "Thông dịch viên cấp cao tập đoàn Samsung, LG, Lotte; Chuyên viên nhân sự FDI Hàn Quốc.", "Năng khiếu ngữ điệu, đam mê văn hóa nghệ thuật xứ Hàn, chỉn chu.", "14 - 30 triệu/tháng"),

        ("SOC-JAPANESE", "Ngôn ngữ & Văn hóa Nhật Bản", "Xã hội & Nhân văn", "ASE", 
         "Đào tạo JLPT N1-N2, văn hóa Omotenashi, tiếng Nhật kinh tế IT (Bridge SE) và dịch thuật doanh nghiệp Nhật Bản.", 
         "Kỹ sư cầu nối IT tiếng Nhật (BrSE), Thông dịch viên Toyota, Honda, Canon; Cán bộ JICA.", "Kiên trì bền bỉ, nguyên tắc, tôn trọng quy chuẩn và tỉ mỉ.", "15 - 35 triệu/tháng"),

        ("SOC-LANG-EAST", "Ngôn ngữ & Văn hóa Đông Á (Đông phương học)", "Xã hội & Nhân văn", "ASE", 
         "Chuyên sâu văn phạm, thương mại và văn hóa các cường quốc Đông Á. Đón đầu dòng vốn FDI đầu tư vào VN.", 
         "Thông dịch viên, Chuyên viên nghiên cứu khu vực học, Chuyên viên xúc tiến đầu tư.", "Năng khiếu ngôn ngữ, trí nhớ thị giác tốt học chữ Hán tự/Kanji.", "14 - 30 triệu/tháng"),

        ("PSYCH-APP", "Tâm lý học Ứng dụng & Tham vấn Học đường", "Xã hội & Nhân văn", "SIA", 
         "Nghiên cứu hành vi cảm xúc con người, đo lường trắc nghiệm tâm lý và tham vấn giải tỏa lo âu trầm cảm.", 
         "Chuyên viên tư vấn tâm lý học đường, Chuyên gia đào tạo tâm lý nhân sự doanh nghiệp.", "Lắng nghe thấu cảm vô điều kiện, kiên nhẫn sâu sắc.", "12 - 25 triệu/tháng"),

        # --- NHÓM KHOA HỌC GIÁO DỤC & SƯ PHẠM ---
        ("EDU-PED", "Sư phạm & Khoa học Giáo dục (Chung)", "Khoa học Giáo dục", "SAE", 
         "Nghiên cứu phương pháp giảng dạy hiện đại, tâm lý học sinh, thiết kế bài giảng số EdTech và quản lý lớp học.", 
         "Giáo viên trường công lập/quốc tế chất lượng cao, Chuyên gia EdTech. Miễn 100% học phí theo NĐ 116.", "Yêu trẻ, kiên nhẫn, khả năng truyền đạt lôi cuốn.", "10 - 22 triệu/tháng"),

        ("EDU-MATH", "Sư phạm Toán học & Giáo dục STEM", "Khoa học Giáo dục", "IRC", 
         "Phương pháp giảng dạy Toán tư duy hiện đại, tích hợp mô hình STEM/EdTech, luyện thi học sinh giỏi quốc gia.", 
         "Giáo viên Toán trường chuyên, trường chất lượng cao; Chuyên gia phát triển chương trình toán EdTech. Miễn học phí NĐ 116.", "Tư duy toán học sắc bén, kiên nhẫn giải thích, yêu thích truyền lửa tri thức.", "12 - 28 triệu/tháng"),

        ("EDU-LIT", "Sư phạm Ngữ văn & Giáo dục Khai phóng", "Khoa học Giáo dục", "ASE", 
         "Phương pháp đọc hiểu văn bản hiện đại, phát triển kỹ năng viết sáng tạo, tư duy phản biện ngôn từ và đạo đức nhân cách.", 
         "Giáo viên Ngữ văn trường chuyên, trường quốc tế; Biên tập viên sách giáo dục. Miễn học phí NĐ 116.", "Tâm hồn nhân văn phong phú, giọng nói truyền cảm, khả năng truyền cảm hứng.", "12 - 25 triệu/tháng"),

        # --- NHÓM KIẾN TRÚC, NGHỆ THUẬT & THIẾT KẾ ---
        ("ENG-ARCH", "Kiến trúc Công trình & Thiết kế Nội thất", "Nghệ thuật & Thiết kế", "AIR", 
         "Giao thoa giữa kỹ thuật kết cấu xây dựng và nghệ thuật không gian sống, thiết kế phối cảnh nhà ở cao ốc và nội thất.", 
         "Kiến trúc sư công trình, Nhà thiết kế nội thất dân dụng/khách sạn, Giám sát thiết kế.", "Tư duy hình học 3D, gu thẩm mỹ tinh tế, kiên nhẫn vẽ đồ án.", "15 - 32 triệu/tháng"),

        ("ART-DES", "Thiết kế Đồ họa & Thiết kế UI/UX", "Nghệ thuật & Thiết kế", "ARE", 
         "Kết hợp thẩm mỹ thị giác, tạo mẫu giao diện ứng dụng web/app, thiết kế thương hiệu và trải nghiệm sản phẩm số.", 
         "UI/UX Designer, Product Designer, Art Director, Họa sĩ minh họa số.", "Thẩm mỹ màu sắc tốt, đồng cảm với người dùng, dùng tốt Figma/Adobe.", "14 - 28 triệu/tháng"),

        ("ART-FASH", "Thiết kế Thời trang & Mỹ thuật Ứng dụng", "Nghệ thuật & Thiết kế", "ARE", 
         "Phát triển ý tưởng bộ sưu tập, phác thảo minh họa trang phục thời trang, kỹ thuật dựng rập may và xu hướng thời trang.", 
         "Nhà thiết kế thời trang (Fashion Designer), Stylist, Giám đốc sáng tạo thương hiệu may mặc.", "Năng khiếu thẩm mỹ, cảm thụ màu sắc, đam mê phong cách trang phục.", "12 - 30 triệu/tháng")
    ]

    cursor.executemany("""
    INSERT INTO majors (code, name, category, holland_code, description, career_prospects, suitable_traits, expected_salary_range)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, majors)

    # Lấy ID của các trường và các ngành để tạo bảng điểm chuẩn
    cursor.execute("SELECT id, code FROM universities")
    uni_map = {row["code"]: row["id"] for row in cursor.fetchall()}

    cursor.execute("SELECT id, code FROM majors")
    major_map = {row["code"]: row["id"] for row in cursor.fetchall()}

    # 3. Dữ liệu Điểm chuẩn tuyển sinh THPT thực tế (2023, 2024, 2025)
    # Format: (uni_code, major_code, combo, score_2023, score_2024, score_2025, quota, sub_criteria)
    benchmarks_data = [
        # === MIỀN BẮC ===
        # BKHN - Đại học Bách khoa Hà Nội
        ("BKHN", "IT-CS", "A00", 29.42, 29.25, 29.40, 300, "Toán >= 9.2, TTNV <= 2"),
        ("BKHN", "IT-CS", "A01", 28.90, 28.80, 28.95, 150, "Toán >= 9.0"),
        ("BKHN", "IT-SE", "A00", 28.60, 28.45, 28.50, 250, "Toán >= 8.8"),
        ("BKHN", "IT-CYBER", "A00", 27.90, 27.75, 27.85, 120, "Toán >= 8.4"),
        ("BKHN", "ENG-ROBOT", "A00", 26.85, 26.70, 26.80, 180, "Toán >= 8.2"),
        ("BKHN", "ENG-SEMI", "A00", 27.50, 27.80, 28.10, 150, "Toán >= 8.6"),
        ("BKHN", "ENG-SEMI", "A01", 27.10, 27.40, 27.70, 80, "Toán >= 8.4"),
        ("BKHN", "ENG-AUTO", "A00", 26.40, 26.65, 26.80, 200, "Toán >= 8.2"),
        ("BKHN", "ENG-EE", "A00", 27.20, 27.50, 27.75, 350, "Toán >= 8.6"),
        ("BKHN", "ENG-CIVIL", "A00", 23.50, 23.80, 24.00, 200, "Toán >= 7.5"),
        ("BKHN", "FOOD-CHEM", "A00", 25.80, 26.10, 26.35, 250, "Hóa học >= 8.2"),

        # UET - ĐHQGHN
        ("UET", "IT-CS", "A00", 28.50, 28.65, 28.70, 160, "Toán >= 8.8"),
        ("UET", "IT-SE", "A00", 28.20, 28.30, 28.40, 140, "Toán >= 8.6"),
        ("UET", "IT-DS", "A01", 27.80, 27.90, 28.05, 100, "Toán >= 8.6, Tiếng Anh >= 8.0"),
        ("UET", "ENG-SEMI", "A00", 26.50, 27.10, 27.50, 100, "Toán >= 8.4"),
        ("UET", "ENG-AUTO", "A00", 25.80, 26.20, 26.50, 120, "Toán >= 8.0"),

        # NEU - Kinh tế Quốc dân
        ("NEU", "ECO-IB", "A01", 27.80, 28.00, 28.15, 180, "Tiếng Anh >= 8.5"),
        ("NEU", "ECO-IB", "D01", 27.65, 27.90, 28.10, 220, "Toán >= 8.4"),
        ("NEU", "ECO-MKT", "D01", 27.55, 27.80, 27.95, 200, "Tiếng Anh >= 8.2"),
        ("NEU", "ECO-FIN", "A00", 27.10, 27.35, 27.45, 250, "Toán >= 8.6"),
        ("NEU", "ACC-AUD", "A00", 27.80, 28.10, 28.30, 300, "Toán >= 8.8"),
        ("NEU", "ACC-AUD", "D01", 27.60, 27.90, 28.15, 300, "Toán >= 8.6"),
        ("NEU", "BUS-ADMIN", "D01", 27.40, 27.70, 27.90, 350, "Toán >= 8.4"),
        ("NEU", "IT-MIS", "A00", 27.10, 27.40, 27.60, 200, "Toán >= 8.4"),
        ("NEU", "ECO-LOG", "A01", 27.40, 27.60, 27.75, 150, "Toán >= 8.4"),
        ("NEU", "ECO-ECOM", "A01", 27.50, 27.80, 28.00, 150, "Tiếng Anh >= 8.2"),
        ("NEU", "TOUR-HOSP", "D01", 26.50, 26.80, 27.00, 180, "Tiếng Anh >= 8.0"),

        # FTU - Ngoại thương Hà Nội
        ("FTU", "ECO-IB", "A00", 28.30, 28.50, 28.60, 250, "Toán >= 9.0"),
        ("FTU", "ECO-IB", "A01", 28.10, 28.30, 28.45, 200, "Tiếng Anh >= 8.8"),
        ("FTU", "ECO-IB", "D01", 28.00, 28.20, 28.35, 300, "Tiếng Anh >= 8.6"),
        ("FTU", "ECO-INT", "A00", 28.40, 28.60, 28.75, 250, "Toán >= 9.0"),
        ("FTU", "ECO-FIN", "D01", 27.70, 27.90, 28.05, 200, "Toán >= 8.4"),
        ("FTU", "ACC-AUD", "D01", 27.80, 28.10, 28.25, 200, "Toán >= 8.6"),
        ("FTU", "BUS-ADMIN", "D01", 27.90, 28.20, 28.35, 250, "Toán >= 8.6"),
        ("FTU", "LAW-INT", "D01", 27.50, 27.70, 27.80, 100, "Ngữ văn >= 8.0"),

        # AOF - Học viện Tài chính (ĐẦY ĐỦ CÁC NGÀNH)
        ("AOF", "ACC-AUD", "A00", 26.20, 26.50, 26.70, 400, "Toán >= 8.6"),
        ("AOF", "ACC-AUD", "A01", 26.00, 26.30, 26.50, 300, "Toán >= 8.4"),
        ("AOF", "ACC-AUD", "D01", 26.10, 26.40, 26.60, 350, "Tiếng Anh >= 8.0"),
        ("AOF", "ECO-FIN", "A00", 25.80, 26.00, 26.20, 500, "Toán >= 8.2"),
        ("AOF", "ECO-FIN", "D01", 25.60, 25.90, 26.10, 400, "Toán >= 8.0"),
        ("AOF", "IT-MIS", "A00", 25.40, 25.70, 25.90, 200, "Toán >= 8.2"),
        ("AOF", "BUS-ADMIN", "D01", 25.70, 26.00, 26.25, 300, "Tiếng Anh >= 7.8"),
        ("AOF", "ECO-LOG", "A01", 26.10, 26.35, 26.50, 200, "Toán >= 8.4"),

        # DAV - Học viện Ngoại giao (ĐẦY ĐỦ CÁC NGÀNH)
        ("DAV", "SOC-IR", "A01", 27.20, 27.60, 27.90, 150, "Tiếng Anh >= 8.8"),
        ("DAV", "SOC-IR", "D01", 27.50, 27.80, 28.10, 200, "Tiếng Anh >= 9.0"),
        ("DAV", "SOC-IR", "C00", 28.20, 28.50, 28.80, 80, "Ngữ văn >= 8.8"),
        ("DAV", "SOC-JOUR", "D01", 27.80, 28.20, 28.45, 120, "Truyền thông quốc tế, Tiếng Anh >= 8.8"),
        ("DAV", "ECO-INT", "A01", 26.80, 27.20, 27.40, 150, "Tiếng Anh >= 8.6"),
        ("DAV", "LAW-INT", "D01", 26.90, 27.30, 27.50, 100, "Luật quốc tế, Tiếng Anh >= 8.4"),
        ("DAV", "SOC-ENG", "D01", 26.70, 27.00, 27.20, 180, "Tiếng Anh nhân hệ số 2"),

        # HLU - Đại học Luật Hà Nội
        ("HLU", "LAW-CIVIL", "C00", 27.50, 28.00, 28.35, 300, "Ngữ văn >= 8.5"),
        ("HLU", "LAW-CIVIL", "A00", 25.80, 26.20, 26.50, 250, "Toán >= 8.2"),
        ("HLU", "LAW-CIVIL", "D01", 26.20, 26.60, 26.90, 350, "Tiếng Anh >= 8.0"),
        ("HLU", "LAW-INT", "A01", 26.80, 27.20, 27.50, 200, "Tiếng Anh >= 8.6"),
        ("HLU", "LAW-INT", "D01", 27.00, 27.40, 27.70, 250, "Tiếng Anh >= 8.6"),

        # UEB - ĐHQGHN
        ("UEB", "ECO-INT", "A01", 26.50, 26.90, 27.20, 180, "Tiếng Anh >= 8.5"),
        ("UEB", "ECO-INT", "D01", 26.80, 27.20, 27.50, 200, "Tiếng Anh >= 8.6"),
        ("UEB", "BUS-ADMIN", "A01", 26.20, 26.60, 26.90, 220, "Toán >= 8.2"),
        ("UEB", "ECO-FIN", "A01", 26.40, 26.80, 27.10, 200, "Toán >= 8.4"),

        # ULIS - ĐHQGHN
        ("ULIS", "SOC-ENG", "D01", 35.50, 36.00, 36.50, 300, "Tiếng Anh nhân hệ số 2, >= 8.5"),
        ("ULIS", "SOC-CHINESE", "D01", 35.80, 36.30, 36.80, 250, "Ngoại ngữ nhân hệ số 2, >= 8.5"),
        ("ULIS", "SOC-KOREAN", "D01", 35.50, 36.00, 36.40, 200, "Ngoại ngữ nhân hệ số 2"),
        ("ULIS", "SOC-JAPANESE", "D01", 35.20, 35.70, 36.10, 200, "Ngoại ngữ nhân hệ số 2"),
        ("ULIS", "EDU-PED", "D01", 36.50, 37.00, 37.50, 150, "Sư phạm Tiếng Anh, nhân hệ số 2"),

        # HMU - Đại học Y Hà Nội
        ("HMU", "MED-DOC", "B00", 27.73, 27.80, 28.15, 400, "TTNV 1-2, Toán >= 8.8"),
        ("HMU", "MED-DENT", "B00", 27.50, 27.70, 28.00, 80, "Răng - Hàm - Mặt đỉnh cao, Toán >= 8.8"),
        ("HMU", "MED-PHARM", "A00", 26.20, 26.35, 26.50, 150, "Hóa học >= 8.5"),
        ("HMU", "MED-NURS", "B00", 23.50, 23.90, 24.20, 150, "Điều dưỡng BV Bạch Mai/Việt Đức"),

        # PTIT - Học viện Bưu chính Viễn thông
        ("PTIT", "IT-CS", "A00", 26.60, 26.75, 26.90, 200, "Toán >= 8.2"),
        ("PTIT", "IT-SE", "A00", 26.55, 26.65, 26.70, 350, "Toán >= 8.0"),
        ("PTIT", "IT-SE", "A01", 26.30, 26.40, 26.50, 200, "Tiếng Anh >= 7.5"),
        ("PTIT", "IT-CYBER", "A00", 26.10, 26.20, 26.35, 180, "Toán >= 7.8"),
        ("PTIT", "ENG-EE", "A00", 25.20, 25.50, 25.75, 250, "Điện tử viễn thông"),
        ("PTIT", "SOC-MULTI", "D01", 25.80, 26.10, 26.30, 200, "Truyền thông đa phương tiện"),
        ("PTIT", "SOC-JOUR", "D01", 25.40, 25.60, 25.80, 150, "Ngữ văn >= 7.5"),
        ("PTIT", "ECO-MKT", "D01", 25.80, 26.00, 26.15, 200, "Toán >= 8.0"),
        ("PTIT", "ECO-ECOM", "D01", 26.00, 26.25, 26.40, 150, "Toán >= 7.8"),

        # HAU - Kiến trúc Hà Nội
        ("HAU", "ENG-ARCH", "A00", 23.50, 23.80, 24.20, 250, "Toán >= 7.5"),
        ("HAU", "ENG-ARCH", "D01", 24.00, 24.30, 24.60, 150, "Tiếng Anh >= 7.0"),
        ("HAU", "ART-FASH", "D01", 22.00, 22.50, 22.80, 80, "Điểm thi THPT hoặc Học bạ"),
        ("HAU", "ART-DES", "D01", 23.00, 23.40, 23.80, 120, "Mỹ thuật đồ họa"),

        # MTCN - Mỹ thuật Công nghiệp
        ("MTCN", "ART-FASH", "D01", 21.50, 22.00, 22.50, 100, "Năng khiếu vẽ thẩm mỹ"),
        ("MTCN", "ART-DES", "D01", 22.50, 23.00, 23.50, 150, "Thiết kế đồ họa"),

        # HANU - ĐH Hà Nội
        ("HANU", "SOC-ENG", "D01", 34.50, 35.00, 35.50, 300, "Tiếng Anh nhân hệ số 2"),
        ("HANU", "SOC-CHINESE", "D01", 35.00, 35.50, 36.00, 250, "Ngoại ngữ nhân hệ số 2"),
        ("HANU", "SOC-KOREAN", "D01", 34.80, 35.20, 35.70, 200, "Tiếng Hàn nhân hệ số 2"),
        ("HANU", "SOC-JAPANESE", "D01", 34.20, 34.70, 35.20, 200, "Tiếng Nhật nhân hệ số 2"),
        ("HANU", "TOUR-HOSP", "D01", 25.50, 25.80, 26.10, 150, "Tiếng Anh >= 7.5"),

        # AJC - Báo chí & Tuyên truyền
        ("AJC", "SOC-JOUR", "C00", 27.50, 27.80, 28.25, 120, "Ngữ văn >= 8.5"),
        ("AJC", "SOC-PR", "D01", 26.80, 27.10, 27.40, 150, "Tiếng Anh >= 8.0"),
        ("AJC", "SOC-PR", "C00", 27.20, 27.50, 27.90, 100, "Văn >= 8.2"),

        # HaUI - Công nghiệp Hà Nội
        ("HaUI", "ENG-AUTO", "A00", 23.50, 23.80, 24.20, 300, "Toán >= 7.5"),
        ("HaUI", "ENG-EE", "A00", 23.00, 23.40, 23.80, 250, "Điện - Điện tử"),
        ("HaUI", "IT-CS", "A00", 24.50, 24.80, 25.20, 250, "Khoa học máy tính"),
        ("HaUI", "ACC-AUD", "A00", 23.20, 23.60, 24.00, 200, "Kế toán"),
        ("HaUI", "TOUR-HOSP", "D01", 23.00, 23.40, 23.70, 250, "Tiếng Anh >= 7.0"),
        ("HaUI", "ECO-ECOM", "A00", 24.20, 24.50, 24.80, 200, "Toán >= 7.8"),

        # UTC - Giao thông Vận tải
        ("UTC", "ENG-AUTO", "A00", 24.80, 25.10, 25.40, 250, "Toán >= 8.0"),
        ("UTC", "ECO-LOG", "A00", 25.50, 25.80, 26.10, 220, "Toán >= 8.2"),
        ("UTC", "ENG-CIVIL", "A00", 21.50, 22.00, 22.50, 250, "Kỹ thuật cầu đường"),
        ("UTC", "ENG-EE", "A00", 23.80, 24.20, 24.60, 200, "Kỹ thuật điện tự động hóa"),

        # HPMU - Y Dược Hải Phòng
        ("HPMU", "MED-DOC", "B00", 25.80, 26.20, 26.50, 300, "Y đa khoa, Sinh học >= 8.2"),
        ("HPMU", "MED-DENT", "B00", 26.00, 26.40, 26.70, 60, "Răng - Hàm - Mặt"),
        ("HPMU", "MED-PHARM", "A00", 24.50, 24.90, 25.20, 150, "Dược học"),

        # KMA - Kỹ thuật Mật mã
        ("KMA", "IT-CYBER", "A00", 25.20, 25.60, 25.85, 300, "An toàn thông tin hàng đầu"),
        ("KMA", "IT-SE", "A00", 25.00, 25.40, 25.65, 250, "Kỹ thuật phần mềm"),
        ("KMA", "ENG-EE", "A01", 24.40, 24.80, 25.10, 150, "Kỹ thuật điện tử viễn thông"),

        # HOU - Mở Hà Nội
        ("HOU", "LAW-CIVIL", "C00", 24.50, 25.00, 25.40, 200, "Luật học"),
        ("HOU", "IT-SE", "A00", 22.50, 22.90, 23.20, 250, "CNTT"),
        ("HOU", "ECO-ECOM", "D01", 23.00, 23.50, 23.80, 180, "Thương mại điện tử"),
        ("HOU", "ART-DES", "D01", 22.00, 22.50, 22.80, 120, "Thiết kế đồ họa"),

        # VNUA - Nông nghiệp VN
        ("VNUA", "AGRI-VET", "B00", 22.50, 23.00, 23.50, 250, "Sinh học >= 7.5"),
        ("VNUA", "BIO-TECH", "B00", 20.50, 21.00, 21.50, 150, "Sinh học >= 7.0"),

        # TMU - Đại học Thương mại
        ("TMU", "ECO-MKT", "D01", 26.20, 26.40, 26.50, 250, "Tiếng Anh >= 7.8"),
        ("TMU", "ECO-LOG", "A01", 26.00, 26.25, 26.35, 200, "Toán >= 8.0"),
        ("TMU", "ECO-ECOM", "D01", 26.50, 26.80, 27.00, 200, "Toán >= 8.0"),

        # HNUE - Sư phạm Hà Nội
        ("HNUE", "EDU-MATH", "A00", 26.50, 27.00, 27.40, 120, "Sư phạm Toán, Miễn HP"),
        ("HNUE", "EDU-LIT", "C00", 27.20, 27.60, 28.00, 100, "Sư phạm Ngữ văn, Miễn HP"),
        ("HNUE", "SOC-ENG", "D01", 26.40, 26.65, 26.80, 120, "Tiếng Anh >= 8.5"),
        ("HNUE", "PSYCH-APP", "D01", 25.00, 25.40, 25.80, 100, "Tâm lý học giáo dục"),

        # FPT
        ("FPT", "IT-SE", "A00", 21.00, 21.00, 21.00, 1200, "Top 40 SchoolRank hoặc Phỏng vấn"),
        ("FPT", "ART-DES", "D01", 21.00, 21.00, 21.00, 500, "Điểm thi tốt nghiệp >= 21.0"),
        ("FPT", "ART-FASH", "D01", 21.00, 21.00, 21.00, 200, "Portfolio hoặc Điểm thi >= 21.0"),


        # === MIỀN TRUNG ===
        # DUT - Bách khoa Đà Nẵng
        ("DUT", "IT-SE", "A00", 25.20, 25.40, 25.60, 200, "Toán >= 7.8"),
        ("DUT", "ENG-ROBOT", "A00", 24.50, 24.70, 24.90, 150, "Toán >= 7.5"),
        ("DUT", "ENG-AUTO", "A00", 24.80, 25.10, 25.30, 180, "Toán >= 7.6"),
        ("DUT", "ENG-ARCH", "A00", 22.50, 22.80, 23.00, 120, "Kiến trúc công trình"),

        # DUE - Kinh tế Đà Nẵng
        ("DUE", "ECO-IB", "A01", 25.00, 25.25, 25.40, 180, "Tiếng Anh >= 7.5"),
        ("DUE", "ECO-MKT", "D01", 24.80, 25.10, 25.30, 200, "Toán >= 7.2"),
        ("DUE", "TOUR-HOSP", "D01", 23.80, 24.20, 24.50, 150, "Khách sạn biển Đà Nẵng"),
        ("DUE", "ECO-ECOM", "D01", 24.50, 24.80, 25.10, 140, "Thương mại số"),

        # HMED - Y Dược Huế
        ("HMED", "MED-DOC", "B00", 26.50, 26.75, 27.00, 300, "Sinh học >= 8.0, TTNV <= 3"),
        ("HMED", "MED-DENT", "B00", 26.40, 26.80, 27.10, 60, "Răng Hàm Mặt miền Trung"),
        ("HMED", "MED-PHARM", "A00", 24.50, 24.80, 25.10, 150, "Hóa học >= 7.8"),

        # UTE_DN - Sư phạm Kỹ thuật Đà Nẵng
        ("UTE_DN", "ENG-AUTO", "A00", 22.50, 22.90, 23.30, 150, "Kỹ thuật Ô tô"),
        ("UTE_DN", "ENG-ROBOT", "A00", 21.80, 22.20, 22.50, 120, "Cơ điện tử"),

        # HUL - Ngoại ngữ Huế
        ("HUL", "SOC-LANG-EAST", "D01", 22.50, 23.00, 23.50, 180, "Tiếng Trung/Hàn/Nhật"),
        ("HUL", "SOC-ENG", "D01", 23.00, 23.50, 23.80, 200, "Tiếng Anh hệ số 2"),

        # HUAF - Nông Lâm Huế
        ("HUAF", "AGRI-VET", "B00", 19.50, 20.00, 20.50, 120, "Bác sĩ thú y"),
        ("HUAF", "BIO-TECH", "B00", 18.00, 18.50, 19.00, 100, "Công nghệ sinh học"),

        # NTU - Nha Trang
        ("NTU", "TOUR-HOSP", "D01", 21.00, 21.50, 22.00, 250, "Du lịch & Khách sạn Nha Trang"),
        ("NTU", "ECO-LOG", "A01", 20.50, 21.00, 21.50, 120, "Logistics hàng hải"),

        # QNU - Quy Nhơn
        ("QNU", "EDU-PED", "C00", 24.50, 25.00, 25.50, 120, "Sư phạm Văn, miễn học phí"),
        ("QNU", "IT-SE", "A00", 20.00, 20.50, 21.00, 150, "Toán >= 6.5"),

        # VINH - ĐH Vinh
        ("VINH", "EDU-PED", "D01", 24.00, 24.50, 25.00, 180, "Sư phạm tiểu học/Toán"),
        ("VINH", "AGRI-VET", "B00", 20.00, 20.50, 21.00, 100, "Thú y miền Trung"),

        # TDU - Tây Nguyên
        ("TDU", "MED-DOC", "B00", 24.80, 25.20, 25.60, 150, "Y đa khoa Tây Nguyên"),
        ("TDU", "AGRI-VET", "B00", 18.50, 19.00, 19.50, 120, "Thú y động vật"),

        # DTU - Đại học Duy Tân (ĐẦY ĐỦ CÁC NGÀNH)
        ("DTU", "MED-DOC", "B00", 22.00, 22.50, 23.00, 150, "Bác sĩ Y đa khoa"),
        ("DTU", "MED-DENT", "B00", 22.50, 23.00, 23.50, 80, "Răng - Hàm - Mặt"),
        ("DTU", "MED-PHARM", "A00", 21.00, 21.50, 22.00, 120, "Dược học"),
        ("DTU", "IT-SE", "A00", 19.00, 19.50, 20.00, 300, "Kỹ thuật phần mềm"),
        ("DTU", "TOUR-HOSP", "D01", 18.00, 18.50, 19.00, 250, "Quản trị du lịch & Khách sạn"),


        # === MIỀN NAM ===
        # HCMUT - Bách Khoa TP.HCM
        ("HCMUT", "IT-CS", "A00", 28.00, 28.20, 28.30, 250, "ĐGNL + Điểm thi THPT kết hợp"),
        ("HCMUT", "ENG-ROBOT", "A00", 26.40, 26.60, 26.75, 200, "Toán >= 8.2"),
        ("HCMUT", "ENG-SEMI", "A00", 26.80, 27.20, 27.60, 120, "Toán >= 8.4"),
        ("HCMUT", "ENG-AUTO", "A00", 26.50, 26.80, 27.10, 180, "Toán >= 8.2"),
        ("HCMUT", "ENG-EE", "A00", 26.50, 26.90, 27.20, 250, "Kỹ thuật Điện - Điện tử"),
        ("HCMUT", "ENG-CIVIL", "A00", 23.00, 23.50, 23.80, 180, "Kỹ thuật Xây dựng"),
        ("HCMUT", "FOOD-CHEM", "A00", 25.50, 25.80, 26.10, 200, "Hóa học"),

        # UIT - CNTT TP.HCM
        ("UIT", "IT-CS", "A00", 27.80, 28.00, 28.15, 200, "Toán >= 8.6"),
        ("UIT", "IT-SE", "A00", 27.60, 27.80, 27.95, 250, "Toán >= 8.4"),
        ("UIT", "IT-CYBER", "A01", 27.10, 27.30, 27.45, 160, "Tiếng Anh >= 7.8"),
        ("UIT", "IT-DS", "A01", 27.30, 27.50, 27.65, 140, "Toán >= 8.4"),
        ("UIT", "ECO-ECOM", "A01", 26.80, 27.10, 27.35, 120, "Thương mại điện tử công nghệ"),

        # UEH - Kinh tế TP.HCM
        ("UEH", "ECO-IB", "A01", 27.20, 27.45, 27.60, 300, "Tiếng Anh >= 8.0"),
        ("UEH", "ECO-FIN", "D01", 26.50, 26.75, 26.90, 350, "Toán >= 7.8"),
        ("UEH", "ACC-AUD", "A00", 26.40, 26.70, 26.90, 300, "Kế toán - Kiểm toán"),
        ("UEH", "BUS-ADMIN", "D01", 26.30, 26.60, 26.80, 350, "Quản trị kinh doanh"),
        ("UEH", "ECO-MKT", "D01", 27.00, 27.20, 27.35, 280, "Tiếng Anh >= 8.0"),
        ("UEH", "ECO-LOG", "A00", 26.80, 27.00, 27.15, 200, "Toán >= 8.0"),
        ("UEH", "IT-MIS", "A00", 26.20, 26.50, 26.75, 180, "Hệ thống thông tin"),
        ("UEH", "TOUR-HOSP", "D01", 25.80, 26.20, 26.50, 220, "Quản trị du lịch"),
        ("UEH", "ECO-ECOM", "D01", 26.80, 27.10, 27.30, 200, "Toán >= 7.8"),

        # UMP - Y Dược TP.HCM
        ("UMP", "MED-DOC", "B00", 27.90, 28.05, 28.25, 420, "Toán >= 8.6, Sinh >= 8.6"),
        ("UMP", "MED-DENT", "B00", 27.65, 27.85, 28.10, 100, "Răng - Hàm - Mặt phương Nam"),
        ("UMP", "MED-PHARM", "A00", 26.50, 26.70, 26.85, 220, "Hóa học >= 8.4"),
        ("UMP", "MED-NURS", "B00", 23.80, 24.20, 24.50, 200, "Điều dưỡng lâm sàng"),

        # PNTU - Phạm Ngọc Thạch
        ("PNTU", "MED-DOC", "B00", 26.80, 27.15, 27.50, 350, "Y đa khoa TP.HCM"),
        ("PNTU", "MED-DENT", "B00", 26.90, 27.30, 27.60, 60, "Răng - Hàm - Mặt"),
        ("PNTU", "MED-PHARM", "A00", 25.50, 25.80, 26.10, 150, "Dược học lâm sàng"),

        # HUB - Đại học Ngân hàng TP.HCM
        ("HUB", "ECO-FIN", "A01", 25.20, 25.60, 25.80, 400, "Toán >= 8.0"),
        ("HUB", "ECO-FIN", "D01", 25.40, 25.80, 26.00, 350, "Tiếng Anh >= 7.8"),
        ("HUB", "ECO-INT", "D01", 25.80, 26.20, 26.40, 250, "Tiếng Anh >= 8.2"),
        ("HUB", "BUS-ADMIN", "D01", 25.00, 25.40, 25.60, 300, "Toán >= 7.8"),
        ("HUB", "ECO-ECOM", "A01", 25.30, 25.70, 25.90, 180, "Thương mại điện tử"),

        # UFM - Tài chính Marketing TP.HCM
        ("UFM", "ECO-MKT", "D01", 25.20, 25.60, 25.90, 450, "Marketing số, Tiếng Anh >= 7.8"),
        ("UFM", "ECO-IB", "D01", 24.80, 25.20, 25.50, 350, "Tiếng Anh >= 7.6"),
        ("UFM", "BUS-ADMIN", "D01", 24.20, 24.60, 24.90, 400, "Quản trị kinh doanh"),
        ("UFM", "ACC-AUD", "A00", 24.00, 24.40, 24.70, 300, "Kế toán tài chính"),

        # HCMUE - Sư phạm TP.HCM
        ("HCMUE", "EDU-MATH", "A00", 26.20, 26.60, 27.00, 120, "Sư phạm Toán, miễn học phí"),
        ("HCMUE", "EDU-LIT", "C00", 26.80, 27.20, 27.60, 100, "Sư phạm Ngữ văn, miễn học phí"),
        ("HCMUE", "SOC-ENG", "D01", 26.50, 26.90, 27.20, 150, "Sư phạm Tiếng Anh, Tiếng Anh >= 8.5"),
        ("HCMUE", "PSYCH-APP", "D01", 25.50, 25.90, 26.20, 120, "Tâm lý học ứng dụng"),

        # CTUMP - Y Dược Cần Thơ
        ("CTUMP", "MED-DOC", "B00", 25.50, 25.80, 26.10, 350, "Y đa khoa ĐBSCL, Toán >= 8.2"),
        ("CTUMP", "MED-DENT", "B00", 25.80, 26.10, 26.40, 80, "Răng - Hàm - Mặt"),
        ("CTUMP", "MED-PHARM", "A00", 24.20, 24.60, 24.90, 180, "Dược học"),
        ("CTUMP", "MED-NURS", "B00", 21.50, 22.00, 22.40, 150, "Điều dưỡng"),

        # HCMUS - Khoa học Tự nhiên TP.HCM (ĐẦY ĐỦ CÁC NGÀNH)
        ("HCMUS", "IT-CS", "A00", 27.80, 28.20, 28.40, 200, "Toán >= 8.8"),
        ("HCMUS", "IT-CS", "A01", 27.50, 27.90, 28.15, 150, "Tiếng Anh >= 8.4"),
        ("HCMUS", "IT-DS", "A00", 26.40, 26.80, 27.10, 120, "Toán >= 8.4"),
        ("HCMUS", "ENG-SEMI", "A00", 25.50, 26.20, 26.80, 100, "Công nghệ bán dẫn, Toán >= 8.2"),
        ("HCMUS", "BIO-TECH", "B00", 24.20, 24.60, 24.90, 180, "Sinh học >= 8.0"),
        ("HCMUS", "FOOD-CHEM", "A00", 24.00, 24.40, 24.70, 150, "Hóa học >= 8.0"),

        # TDTU - Tôn Đức Thắng (ĐẦY ĐỦ CÁC NGÀNH)
        ("TDTU", "IT-SE", "A00", 24.80, 25.20, 25.50, 250, "Toán >= 7.8"),
        ("TDTU", "ECO-MKT", "D01", 25.50, 25.90, 26.10, 200, "Tiếng Anh >= 7.8"),
        ("TDTU", "BUS-ADMIN", "D01", 24.80, 25.20, 25.40, 300, "Toán >= 7.5"),
        ("TDTU", "MED-PHARM", "A00", 25.20, 25.50, 25.75, 120, "Dược học chuẩn quốc tế"),
        ("TDTU", "ART-DES", "D01", 24.50, 24.80, 25.10, 150, "Thiết kế đồ họa"),
        ("TDTU", "SOC-ENG", "D01", 25.00, 25.40, 25.70, 220, "Tiếng Anh hệ số 2"),

        # UAH - Kiến trúc TP.HCM
        ("UAH", "ENG-ARCH", "A00", 24.50, 24.80, 25.20, 200, "Toán >= 7.8, Năng khiếu"),
        ("UAH", "ART-FASH", "D01", 23.50, 23.90, 24.30, 80, "Thiết kế thời trang Nam"),
        ("UAH", "ART-DES", "D01", 24.00, 24.40, 24.80, 120, "Thiết kế đồ họa"),

        # HCMUTE - Sư phạm Kỹ thuật TP.HCM
        ("HCMUTE", "ENG-AUTO", "A00", 25.80, 26.20, 26.60, 300, "Toán >= 8.0"),
        ("HCMUTE", "ENG-ROBOT", "A00", 25.50, 25.90, 26.30, 200, "Cơ điện tử"),
        ("HCMUTE", "ENG-EE", "A00", 25.20, 25.60, 26.00, 250, "Điện - Điện tử"),
        ("HCMUTE", "ART-FASH", "D01", 22.80, 23.20, 23.60, 120, "Công nghệ may & Thời trang"),

        # NLU - Nông Lâm TP.HCM
        ("NLU", "AGRI-VET", "B00", 23.80, 24.20, 24.60, 250, "Bác sĩ thú y TP.HCM"),
        ("NLU", "BIO-TECH", "B00", 21.50, 22.00, 22.50, 180, "Công nghệ sinh học"),

        # USSH_HCM
        ("USSH_HCM", "SOC-JOUR", "C00", 26.80, 27.10, 27.35, 150, "Ngữ văn >= 8.2"),
        ("USSH_HCM", "SOC-ENG", "D01", 26.30, 26.50, 26.65, 200, "Tiếng Anh hệ số 2"),
        ("USSH_HCM", "PSYCH-APP", "D01", 25.80, 26.20, 26.60, 140, "Tâm lý học ứng dụng"),
        ("USSH_HCM", "SOC-LANG-EAST", "D01", 26.00, 26.40, 26.70, 220, "Hàn Quốc học / Nhật Bản học"),

        # CTU - Cần Thơ
        ("CTU", "IT-SE", "A00", 24.00, 24.30, 24.60, 250, "Toán >= 7.5"),
        ("CTU", "AGRI-VET", "B00", 22.00, 22.50, 23.00, 200, "Bác sĩ thú y ĐBSCL"),
        ("CTU", "EDU-PED", "D01", 25.00, 25.40, 25.80, 180, "Sư phạm Toán/Anh"),

        # RMIT
        ("RMIT", "ART-DES", "D01", 20.00, 20.00, 20.00, 200, "IELTS >= 6.5 và GPA 12 >= 7.0"),
        ("RMIT", "ART-FASH", "D01", 20.00, 20.00, 20.00, 150, "IELTS >= 6.5 và Portfolio"),
        ("RMIT", "ECO-IB", "D01", 20.00, 20.00, 20.00, 350, "IELTS >= 6.5 và GPA 12 >= 7.0"),

        # --- ĐIỂM CHUẨN CÁC TRƯỜNG VỪA SỨC 18 - 23 ĐIỂM ---
        # TLU - Thủy lợi
        ("TLU", "IT-SE", "A00", 22.00, 22.30, 22.50, 250, "Toán >= 7.2"),
        ("TLU", "IT-SE", "A01", 21.80, 22.10, 22.30, 150, "Tiếng Anh >= 7.0"),
        ("TLU", "IT-CS", "A00", 22.80, 23.00, 23.20, 200, "Toán >= 7.5"),
        ("TLU", "ENG-AUTO", "A00", 21.20, 21.50, 21.80, 180, "Toán >= 7.0"),
        ("TLU", "ECO-LOG", "A00", 21.50, 21.80, 22.00, 150, "Toán >= 7.0"),
        ("TLU", "ECO-IB", "D01", 22.00, 22.30, 22.50, 160, "Tiếng Anh >= 7.2"),

        # EPU - Điện lực
        ("EPU", "IT-SE", "A00", 21.50, 21.80, 22.00, 220, "Toán >= 7.0"),
        ("EPU", "IT-SE", "A01", 21.30, 21.60, 21.80, 140, "Tiếng Anh >= 6.8"),
        ("EPU", "ENG-ROBOT", "A00", 20.80, 21.00, 21.20, 150, "Tự động hóa"),
        ("EPU", "ENG-AUTO", "A00", 20.50, 20.80, 21.00, 160, "Kỹ thuật ô tô"),

        # HUMG - Mỏ Địa chất
        ("HUMG", "IT-SE", "A00", 20.50, 20.80, 21.00, 200, "Toán >= 6.8"),
        ("HUMG", "IT-SE", "A01", 20.30, 20.60, 20.80, 120, "Tiếng Anh >= 6.5"),
        ("HUMG", "IT-DS", "A00", 20.00, 20.30, 20.50, 100, "Toán >= 6.5"),
        ("HUMG", "ENG-AUTO", "A00", 19.50, 19.80, 20.00, 150, "Kỹ thuật ô tô"),
        ("HUMG", "ENG-ROBOT", "A00", 19.80, 20.00, 20.20, 120, "Điều khiển & Tự động hóa"),

        # HUIT - Công Thương TP.HCM
        ("HUIT", "IT-SE", "A00", 21.00, 21.30, 21.50, 250, "Toán >= 7.0"),
        ("HUIT", "IT-SE", "A01", 20.80, 21.00, 21.20, 150, "Tiếng Anh >= 6.8"),
        ("HUIT", "ENG-AUTO", "A00", 20.50, 20.80, 21.00, 200, "Kỹ thuật ô tô"),
        ("HUIT", "ECO-MKT", "D01", 21.20, 21.50, 21.80, 180, "Marketing số"),
        ("HUIT", "ECO-ECOM", "D01", 21.00, 21.30, 21.50, 160, "Thương mại điện tử"),

        # UTH - Giao thông Vận tải TP.HCM
        ("UTH", "ECO-LOG", "A00", 22.30, 22.60, 22.80, 250, "Logistics cảng biển"),
        ("UTH", "ECO-LOG", "A01", 22.40, 22.70, 22.90, 180, "Tiếng Anh >= 7.0"),
        ("UTH", "IT-SE", "A00", 21.80, 22.00, 22.20, 200, "Toán >= 7.0"),
        ("UTH", "ENG-AUTO", "A00", 21.30, 21.60, 21.80, 180, "Kỹ thuật ô tô"),

        # SGU - Sài Gòn
        ("SGU", "IT-CS", "A00", 23.00, 23.30, 23.50, 200, "Khoa học máy tính"),
        ("SGU", "IT-SE", "A00", 22.50, 22.80, 23.00, 180, "Kỹ thuật phần mềm"),
        ("SGU", "EDU-PED", "D01", 24.00, 24.30, 24.50, 120, "Sư phạm Toán/Văn")
    ]

    benchmarks_to_insert = []
    for uni_c, maj_c, combo, s23, s24, s25, quota, sub in benchmarks_data:
        if uni_c in uni_map and maj_c in major_map:
            benchmarks_to_insert.append((
                uni_map[uni_c], major_map[maj_c], combo, s23, s24, s25, quota, sub
            ))

    cursor.executemany("""
    INSERT INTO admission_benchmarks (university_id, major_id, combination_code, score_2023, score_2024, score_2025, quota, sub_criteria)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, benchmarks_to_insert)

    # 4. Dữ liệu Đề án & Quy chế tuyển sinh chi tiết
    prospectus_data = [
        ("BKHN", 2025, 
         json.dumps({
             "IELTS 5.0": 8.0,
             "IELTS 5.5": 8.5,
             "IELTS 6.0": 9.0,
             "IELTS 6.5": 9.5,
             "IELTS 7.0": 10.0,
             "IELTS 7.5+": 10.0
         }, ensure_ascii=False),
         "Cộng 1.0 đến 2.0 điểm cho giải Học sinh giỏi Tỉnh/Quốc gia môn Toán, Lý, Hóa, Tin. Điểm ưu tiên khu vực KV1 +0.75, KV2-NT +0.5, KV2 +0.25.",
         """ĐỀ ÁN TUYỂN SINH ĐẠI HỌC BÁCH KHOA HÀ NỘI NĂM 2025:
Phương thức 1: Xét tuyển tài năng (XTTN - khoảng 20% chỉ tiêu).
Phương thức 2: Xét tuyển theo kết quả Kỳ thi Đánh giá tư duy (ĐGTD - khoảng 30% chỉ tiêu).
Phương thức 3: Xét tuyển theo điểm thi tốt nghiệp THPT (khoảng 50% chỉ tiêu).
Quy chế quy đổi chứng chỉ Ngoại ngữ: Thí sinh có chứng chỉ IELTS Academic từ 5.0 trở lên được quy đổi thành điểm môn Tiếng Anh khi xét tuyển tổ hợp A01, D01, D07. Thang điểm: 5.0 quy đổi 8.0; 5.5 quy đổi 8.5; 6.0 quy đổi 9.0; 6.5 quy đổi 9.5; 7.0 trở lên quy đổi 10.0.
Tiêu chí phụ: Khi thí sinh cuối danh sách có cùng điểm xét tuyển, ưu tiên thí sinh có điểm môn Toán cao hơn và thứ tự nguyện vọng cao hơn.""",
         "Không tuyển thí sinh cận thị nặng quá 5 độ cho các ngành kỹ thuật đặc thù quân sự."),

        ("FTU", 2025,
         json.dumps({
             "IELTS 6.5": 8.5,
             "IELTS 7.0": 9.0,
             "IELTS 7.5": 9.5,
             "IELTS 8.0+": 10.0
         }, ensure_ascii=False),
         "Cộng tối đa 2.0 điểm giải Nhất/Nhì/Ba HSG Quốc gia. Thí sinh trường Chuyên toàn quốc có điểm khuyến khích từ 0.5 đến 1.5 điểm tùy thành tích.",
         """ĐỀ ÁN TUYỂN SINH TRƯỜNG ĐẠI HỌC NGOẠI THƯƠNG:
Phương thức 1: Xét tuyển kết hợp chứng chỉ ngoại ngữ quốc tế và kết quả học tập THPT (Học bạ 3 năm). Yêu cầu IELTS tối thiểu 6.5, tổng điểm 2 môn còn lại trong tổ hợp từ 16.0 điểm trở lên.
Phương thức 2: Xét tuyển dựa trên kết quả thi Đánh giá năng lực của ĐHQG Hà Nội hoặc ĐHQG TP.HCM.
Phương thức 3: Xét tuyển theo kết quả thi tốt nghiệp THPT năm 2025.
Bảng quy đổi IELTS: 6.5 tương đương 8.5 điểm; 7.0 tương đương 9.0 điểm; 7.5 tương đương 9.5 điểm; 8.0 trở lên tương đương 10.0 điểm.
Điều kiện phụ: Thứ tự nguyện vọng 1 được ưu tiên tuyệt đối nếu bằng điểm chuẩn cắt ngưỡng.""",
         "Hạnh kiểm cả 3 năm THPT đạt loại Tốt."),

        ("NEU", 2025,
         json.dumps({
             "IELTS 5.5": 8.0,
             "IELTS 6.0": 8.5,
             "IELTS 6.5": 9.0,
             "IELTS 7.0": 9.5,
             "IELTS 7.5+": 10.0
         }, ensure_ascii=False),
         "Cộng điểm thưởng 0.5 - 1.5 điểm cho thí sinh đạt giải học sinh giỏi cấp tỉnh môn Toán, Văn, Anh.",
         """ĐỀ ÁN TUYỂN SINH TRƯỜNG ĐẠI HỌC KINH TẾ QUỐC DÂN:
Chỉ tiêu xét tuyển theo điểm thi tốt nghiệp THPT chiếm 18% tổng chỉ tiêu.
Xét tuyển kết hợp chứng chỉ tiếng Anh quốc tế (IELTS từ 5.5 trở lên) với điểm thi ĐGNL (HSA/APT) hoặc 2 môn thi tốt nghiệp THPT (Toán + 1 môn bất kỳ trừ Tiếng Anh).
Bảng quy đổi điểm chứng chỉ tiếng Anh: IELTS 5.5 = 8.0; IELTS 6.0 = 8.5; IELTS 6.5 = 9.0; IELTS 7.0 = 9.5; IELTS 7.5 trở lên = 10.0 điểm.
Tiêu chí phụ: Ưu tiên điểm môn Toán trong mọi tổ hợp xét tuyển.""",
         "Điểm thi tốt nghiệp môn Toán phải đạt từ 6.0 trở lên."),

        ("AOF", 2025,
         json.dumps({
             "IELTS 5.5": 8.5,
             "IELTS 6.0": 9.0,
             "IELTS 6.5": 9.5,
             "IELTS 7.0+": 10.0
         }, ensure_ascii=False),
         "Cộng 1.0 đến 2.0 điểm giải HSG Quốc gia, giải Nhất/Nhì tỉnh môn Toán, Anh.",
         """ĐỀ ÁN TUYỂN SINH HỌC VIỆN TÀI CHÍNH:
Phương thức: 1. Xét tuyển thẳng và ưu tiên xét tuyển; 2. Xét tuyển học sinh giỏi THPT; 3. Xét tuyển kết hợp chứng chỉ tiếng Anh quốc tế với điểm thi tốt nghiệp THPT; 4. Xét tuyển dựa vào kết quả thi tốt nghiệp THPT; 5. Xét tuyển dựa vào kết quả kỳ thi ĐGNL ĐHQGHN và ĐGTD ĐHBKHN.
Quy đổi IELTS: IELTS 5.5 = 8.5; IELTS 6.0 = 9.0; IELTS 6.5 = 9.5; IELTS 7.0+ = 10.0 điểm.""",
         "Có hạnh kiểm Khá trở lên trong cả 3 năm THPT."),

        ("DAV", 2025,
         json.dumps({
             "IELTS 6.0": 8.5,
             "IELTS 6.5": 9.0,
             "IELTS 7.0": 9.5,
             "IELTS 7.5+": 10.0
         }, ensure_ascii=False),
         "Ưu tiên thí sinh trường THPT chuyên và giải HSG cấp quốc gia môn Văn, Sử, Địa, Ngoại ngữ.",
         """ĐỀ ÁN TUYỂN SINH HỌC VIỆN NGOẠI GIAO:
Phương thức 1: Tuyển thẳng và ưu tiên xét tuyển theo quy chế Bộ GD&ĐT (5%).
Phương thức 2: Xét tuyển kết hợp Chứng chỉ quốc tế và Kết quả học tập THPT (70%). Yêu cầu IELTS >= 6.5.
Phương thức 3: Xét tuyển dựa trên kết quả Phỏng vấn kết hợp học bạ (5%).
Phương thức 4: Xét tuyển dựa trên kết quả thi tốt nghiệp THPT năm 2025 (20%).
Quy đổi IELTS: 6.0 = 8.5; 6.5 = 9.0; 7.0 = 9.5; 7.5+ = 10.0 điểm.""",
         "Điểm trung bình học tập từng năm lớp 10, 11 và học kỳ 1 lớp 12 đạt từ 8.0 trở lên."),

        ("HLU", 2025,
         json.dumps({
             "IELTS 6.0": 8.5,
             "IELTS 6.5": 9.0,
             "IELTS 7.0": 9.5,
             "IELTS 7.5+": 10.0
         }, ensure_ascii=False),
         "Cộng điểm khuyến khích cho học sinh trường THPT chuyên và giải HSG cấp tỉnh môn Ngữ văn, Lịch sử, Toán.",
         """ĐỀ ÁN TUYỂN SINH TRƯỜNG ĐẠI HỌC LUẬT HÀ NỘI:
Phương thức: Xét tuyển thẳng (theo quy chế của Bộ); Xét tuyển thí sinh tham dự Vòng thi tháng cuộc thi Đường lên đỉnh Olympia; Xét tuyển dựa trên kết quả học tập THPT (Học bạ); Xét tuyển dựa trên kết quả Kỳ thi tốt nghiệp THPT 2025; Xét tuyển kết hợp chứng chỉ ngoại ngữ quốc tế.""",
         "Không có môn nào trong tổ hợp xét tuyển có điểm thi tốt nghiệp THPT dưới 3.0 điểm."),

        ("UIT", 2025,
         json.dumps({
             "IELTS 5.0": 8.0,
             "IELTS 5.5": 8.5,
             "IELTS 6.0": 9.0,
             "IELTS 6.5": 9.5,
             "IELTS 7.0+": 10.0
         }, ensure_ascii=False),
         "Ưu tiên xét tuyển thẳng thí sinh trường chuyên, năng khiếu và giải tin học trẻ.",
         """ĐỀ ÁN TUYỂN SINH TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN - ĐHQG-HCM:
Phương thức: 1. Tuyển thẳng theo quy chế Bộ GD&ĐT; 2. Ưu tiên xét tuyển theo quy định ĐHQG-HCM; 3. Xét tuyển dựa trên điểm thi ĐGNL ĐHQG-HCM; 4. Xét tuyển dựa trên kết quả thi tốt nghiệp THPT.
Quy đổi IELTS sang thang điểm 10 thay cho môn Tiếng Anh: 5.0 -> 8.0; 5.5 -> 8.5; 6.0 -> 9.0; 6.5 -> 9.5; 7.0+ -> 10.0.
Tiêu chí phụ: Ưu tiên môn Toán và thứ tự nguyện vọng.""",
         "Có sức khỏe tốt để đáp ứng học tập ngành công nghệ."),

        ("DUT", 2025,
         json.dumps({
             "IELTS 5.5": 8.0,
             "IELTS 6.0": 8.5,
             "IELTS 6.5": 9.0,
             "IELTS 7.0+": 10.0
         }, ensure_ascii=False),
         "Cộng điểm ưu tiên cho thí sinh đạt giải HSG cấp Tỉnh/Thành phố môn Toán, Lý, Hóa, Tin.",
         """ĐỀ ÁN TUYỂN SINH TRƯỜNG ĐẠI HỌC BÁCH KHOA - ĐẠI HỌC ĐÀ NẴNG (DUT):
Phương thức 1: Tuyển thẳng theo quy định của Bộ GD&ĐT.
Phương thức 2: Xét tuyển theo phương thức riêng của trường (Xét tuyển thí sinh đạt giải HSG, học sinh chuyên).
Phương thức 3: Xét kết quả thi Đánh giá năng lực của ĐHQG TP.HCM hoặc ĐHQG Hà Nội.
Phương thức 4: Xét tuyển theo kết quả kỳ thi tốt nghiệp THPT năm 2025.
Quy chế quy đổi điểm chứng chỉ tiếng Anh (IELTS): IELTS 5.5 = 8.0; IELTS 6.0 = 8.5; IELTS 6.5 = 9.0; IELTS 7.0 trở lên = 10.0 điểm.
Tiêu chí phụ: Ưu tiên điểm môn Toán đối với tất cả các ngành kỹ thuật công nghệ.""",
         "Đáp ứng ngưỡng đảm bảo chất lượng đầu vào theo thông báo của ĐH Đà Nẵng."),

        ("HCMUT", 2025,
         json.dumps({
             "IELTS 6.0": 8.5,
             "IELTS 6.5": 9.0,
             "IELTS 7.0": 9.5,
             "IELTS 7.5+": 10.0
         }, ensure_ascii=False),
         "Ưu tiên xét tuyển học sinh các trường THPT chuyên, năng khiếu và thành viên đội tuyển quốc tế.",
         """ĐỀ ÁN TUYỂN SINH TRƯỜNG ĐẠI HỌC BÁCH KHOA - ĐHQG-HCM:
Phương thức chủ đạo: Xét tuyển tổng hợp bao gồm Tiêu chí học lực (kết hợp kỳ thi Đánh giá năng lực ĐHQG-HCM 75%, kỳ thi tốt nghiệp THPT 20%, học bạ THPT 5%) cùng các hoạt động xã hội và năng lực cá nhân.
Quy đổi chứng chỉ IELTS: IELTS 6.0 = 8.5 điểm; IELTS 6.5 = 9.0 điểm; IELTS 7.0 = 9.5 điểm; IELTS 7.5 trở lên = 10.0 điểm.
Tiêu chí phụ: Điểm thành phần môn Toán và thứ tự nguyện vọng đăng ký.""",
         "Có sức khỏe đảm bảo để theo học các chương trình đào tạo kỹ sư.")
    ]

    prospectus_to_insert = []
    for uni_c, yr, ielts_c, bonus, raw_txt, spec in prospectus_data:
        if uni_c in uni_map:
            prospectus_to_insert.append((
                uni_map[uni_c], yr, ielts_c, bonus, raw_txt, spec
            ))

    cursor.executemany("""
    INSERT INTO prospectus_rules (university_id, year, ielts_conversion_rules, bonus_points_policy, raw_prospectus_text, special_conditions)
    VALUES (?, ?, ?, ?, ?, ?)
    """, prospectus_to_insert)

    conn.commit()
    conn.close()
    print(f"Database seeded successfully with {len(universities)} universities, {len(majors)} majors, and {len(benchmarks_to_insert)} benchmarks!")

if __name__ == "__main__":
    seed_database(force_refresh=True)
