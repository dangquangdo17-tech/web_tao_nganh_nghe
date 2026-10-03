from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class CounselorState(BaseModel):
    # Dữ liệu đầu vào từ học sinh
    exam_scores: Dict[str, float] = Field(default_factory=dict) # {"Toán": 7.0, "Văn": 7.5, "Anh": 8.0, "Lý": 7.5, ...}
    transcript_scores: Dict[str, float] = Field(default_factory=dict) # Điểm học bạ THPT
    user_interest: str = "" # Sở thích ngôn ngữ tự nhiên: "Em thích làm việc với máy tính nhưng toán khoảng 7"
    holland_answers: Dict[str, int] = Field(default_factory=dict) # Điểm 6 nhóm R, I, A, S, E, C (thang 1-5 hoặc đếm)
    ielts_score: Optional[float] = None
    priority_area: str = "KV3" # KV1 (+0.75), KV2-NT (+0.5), KV2 (+0.25), KV3 (0)
    ethnicity: str = "kinh" # "kinh" (0đ), "minority" (+1.0đ)
    target_region: str = "Tất cả" # "Bắc", "Trung", "Nam", "Tất cả"
    target_category: str = "Tất cả" # Lĩnh vực mong muốn
    target_tuition: str = "Tất cả" # "Tất cả", "under_20", "20_40", "over_40"

    # Kết quả phân tích từ Agent Học thuật (Academic Agent)
    academic_analysis: Dict[str, Any] = Field(default_factory=dict)

    # Kết quả phân tích từ Agent Tâm lý (Psychology Agent)
    psychology_analysis: Dict[str, Any] = Field(default_factory=dict)

    # Kết quả phân tích từ Agent Tuyển sinh (Admission Agent)
    admission_analysis: Dict[str, Any] = Field(default_factory=dict)

    # Danh sách gợi ý phân nhóm 3 mức độ (Data Dashboard)
    safety_majors: List[Dict[str, Any]] = Field(default_factory=list)      # An toàn: Đỗ > 90%
    target_majors: List[Dict[str, Any]] = Field(default_factory=list)      # Phù hợp: Đỗ 60 - 80%
    reach_majors: List[Dict[str, Any]] = Field(default_factory=list)       # Thử thách: Đỗ < 50%

    # Báo cáo tư vấn tổng hợp cuối cùng
    final_report: Dict[str, Any] = Field(default_factory=dict)
