import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "c:", "chọn ngành nghề", "web")))
# or simply
sys.path.insert(0, r"c:\chọn ngành nghề\web")

from app.slm.school_evaluator import SchoolEvaluator

def run_eval_test():
    scores = {"Toán": 8.0, "Ngữ văn": 8.5, "Tiếng Anh": 9.0, "Vật lý": 8.0, "Hóa học": 8.0, "Sinh học": 8.5}
    
    for school in ["HANU", "AOF", "HMU", "ULIS", "BKHN", "NEU"]:
        res = SchoolEvaluator.evaluate_school_admission(school, scores, priority_area="KV1")
        print(f"\n==================== Trường: {school} ({res['school_info']['name']}) ====================")
        all_majors = res["tiers"]["safe"] + res["tiers"]["competitive"] + res["tiers"]["risky"]
        for m in all_majors[:4]: # show up to 4 majors
            print(f"- {m['major_name']} ({m['major_code']})")
            print(f"  Thang: {m['target_scale']} | Điểm của bạn: {m['student_score']} | Điểm chuẩn: {m['benchmark_2025']} | Diff: {m['score_difference']:+0.2f}")
            print(f"  Quy tắc: {m['rule_name']} | Công thức: {m['formula_desc']}")

if __name__ == "__main__":
    run_eval_test()
