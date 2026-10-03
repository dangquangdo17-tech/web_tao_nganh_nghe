// Global State & Chart Instances
let chartCombos = null;
let chartHolland = null;
let chartHistorical = null;
let currentConsultResult = null;
let userHollandScores = {};
let currentDreamMatches = [];

const ALL_SUBJECTS = ["toan", "van", "anh", "ly", "hoa", "sinh", "su", "dia"];
const SUBJECT_INFO = {
    toan: { name: "Toán", inputId: "score-toan" },
    van: { name: "Ngữ văn", inputId: "score-van" },
    anh: { name: "Tiếng Anh", inputId: "score-anh" },
    ly: { name: "Vật lý", inputId: "score-ly" },
    hoa: { name: "Hóa học", inputId: "score-hoa" },
    sinh: { name: "Sinh học", inputId: "score-sinh" },
    su: { name: "Lịch sử", inputId: "score-su" },
    dia: { name: "Địa lý", inputId: "score-dia" }
};

// Presets data for quick testing
const PRESETS = {
    cs_medium: {
        khoi: "A01",
        subjects: ["toan", "van", "anh", "ly"],
        toan: 7.2, van: 7.0, anh: 7.8, ly: 7.5, hoa: 6.5, sinh: 6.0, su: 6.5, dia: 6.8,
        gpa: 7.8, ielts: 6.5, priority: "KV3", ethnicity: "kinh", region: "Tất cả", category: "Tất cả", tuition: "Tất cả",
        interest: "Em thích làm việc với máy tính nhưng điểm toán chỉ dự đoán khoảng 7"
    },
    ai_top: {
        khoi: "A00",
        subjects: ["toan", "van", "ly", "hoa"],
        toan: 9.2, van: 7.5, anh: 8.5, ly: 9.0, hoa: 8.8, sinh: 7.0, su: 6.5, dia: 6.5,
        gpa: 9.1, ielts: 7.5, priority: "KV2", ethnicity: "kinh", region: "Bắc", category: "Tất cả", tuition: "Tất cả",
        interest: "Em đam mê giải thuật AI, machine learning, nghiên cứu mô hình tính toán lớn và muốn vào trường top 1 công nghệ."
    },
    med_student: {
        khoi: "B00",
        subjects: ["toan", "van", "hoa", "sinh"],
        toan: 8.8, van: 7.2, anh: 7.5, ly: 7.0, hoa: 9.0, sinh: 9.2, su: 6.0, dia: 6.0,
        gpa: 8.9, ielts: "", priority: "KV1", ethnicity: "minority", region: "Tất cả", category: "Tất cả", tuition: "Tất cả",
        interest: "Em là người dân tộc thiểu số, mong muốn trở thành bác sĩ đa khoa chữa bệnh cứu người, không ngại áp lực trực đêm và học tập dài hạn."
    },
    economic_social: {
        khoi: "A01",
        subjects: ["toan", "van", "anh", "ly"],
        toan: 8.0, van: 8.2, anh: 8.5, ly: 7.0, hoa: 6.5, sinh: 6.0, su: 7.5, dia: 7.5,
        gpa: 8.6, ielts: 6.5, priority: "KV2-NT", ethnicity: "kinh", region: "Tất cả", category: "Tất cả", tuition: "Tất cả",
        interest: "Em thích làm việc trong môi trường đa quốc gia, đàm phán thương mại, logistics xuất nhập khẩu và giao tiếp tiếng Anh linh hoạt."
    },
    fashion_design: {
        khoi: "D14",
        subjects: ["toan", "van", "anh", "su"],
        toan: 7.0, van: 7.5, anh: 7.8, ly: 6.5, hoa: 6.0, sinh: 6.0, su: 7.0, dia: 7.0,
        gpa: 7.6, ielts: 6.0, priority: "KV3", ethnicity: "kinh", region: "Tất cả", category: "Tất cả", tuition: "Tất cả",
        interest: "Em thích làm việc ngành thiết kế thời trang nhưng điểm toán dự đoán 7"
    }
};

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
    // Load default school target & preset on startup
    onSelectSchoolTarget("BKHN");
    loadHollandQuestions();
    loadProspectusSample("BKHN");
    updatePriorityPreview();
    updateWishlistBadge();
    setupAlignmentSliders();
    populateAllUniversitiesForTuitionCalculator();
    loadReverseCareerRoles();
    loadRealityCheckProfiles();

    // Lắng nghe phím Enter trên ô nhập sở thích để tự động đánh giá lại ngay
    const interestEl = document.getElementById("user-interest");
    if (interestEl) {
        interestEl.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                triggerMultiAgentConsultation();
            }
        });

        // Khi người dùng gõ câu hỏi mới, xóa trạng thái trắc nghiệm cũ để AI tâm lý suy luận tươi mới
        interestEl.addEventListener("input", () => {
            if (userHollandScores && Object.keys(userHollandScores).length > 0) {
                userHollandScores = {};
            }
            // Giải phóng khóa danh mục nếu đang bị giữ bởi dropdown cũ
            const catSelect = document.getElementById("target-category");
            if (catSelect && catSelect.value !== "Tất cả") {
                catSelect.value = "Tất cả";
            }
        });
    }
});

// Cấu hình các khối thi chuẩn 4 môn (theo yêu cầu tuyển sinh & chương trình mới)
const KHOI_CONFIGS = {
    A01: {
        name: "Khối A01",
        subs: ["toan", "van", "anh", "ly"],
        core: ["toan", "van", "anh"],
        elective: ["ly"],
        desc: "<strong>Khối A01:</strong> Gồm 4 môn thi: <strong>3 môn chính</strong> (Toán, Ngữ văn, Tiếng Anh) + <strong>1 môn chọn của khối</strong> (Vật lý)."
    },
    A00: {
        name: "Khối A00",
        subs: ["toan", "van", "ly", "hoa"],
        core: ["toan", "van"],
        elective: ["ly", "hoa"],
        desc: "<strong>Khối A00:</strong> Gồm 4 môn thi: <strong>2 môn chính</strong> (Toán, Ngữ văn) + <strong>2 môn chọn của khối</strong> (Vật lý, Hóa học)."
    },
    D01: {
        name: "Khối D01",
        subs: ["toan", "van", "anh", "su"],
        core: ["toan", "van", "anh"],
        elective: ["su"],
        desc: "<strong>Khối D01:</strong> Gồm 4 môn thi: <strong>3 môn chính</strong> (Toán, Ngữ văn, Tiếng Anh) + <strong>1 môn tự chọn</strong> (Lịch sử)."
    },
    D07: {
        name: "Khối D07",
        subs: ["toan", "van", "anh", "hoa"],
        core: ["toan", "van", "anh"],
        elective: ["hoa"],
        desc: "<strong>Khối D07:</strong> Gồm 4 môn thi: <strong>3 môn chính</strong> (Toán, Ngữ văn, Tiếng Anh) + <strong>1 môn chọn của khối</strong> (Hóa học)."
    },
    B00: {
        name: "Khối B00",
        subs: ["toan", "van", "hoa", "sinh"],
        core: ["toan", "van"],
        elective: ["hoa", "sinh"],
        desc: "<strong>Khối B00:</strong> Gồm 4 môn thi: <strong>2 môn chính</strong> (Toán, Ngữ văn) + <strong>2 môn chọn của khối</strong> (Hóa học, Sinh học)."
    },
    C00: {
        name: "Khối C00",
        subs: ["toan", "van", "su", "dia"],
        core: ["toan", "van"],
        elective: ["su", "dia"],
        desc: "<strong>Khối C00:</strong> Gồm 4 môn thi: <strong>2 môn chính</strong> (Toán, Ngữ văn) + <strong>2 môn chọn của khối</strong> (Lịch sử, Địa lý)."
    },
    D14: {
        name: "Khối D14",
        subs: ["toan", "van", "anh", "su"],
        core: ["toan", "van", "anh"],
        elective: ["su"],
        desc: "<strong>Khối D14:</strong> Gồm 4 môn thi: <strong>3 môn chính</strong> (Toán, Ngữ văn, Tiếng Anh) + <strong>1 môn chọn của khối</strong> (Lịch sử)."
    },
    D15: {
        name: "Khối D15",
        subs: ["toan", "van", "anh", "dia"],
        core: ["toan", "van", "anh"],
        elective: ["dia"],
        desc: "<strong>Khối D15:</strong> Gồm 4 môn thi: <strong>3 môn chính</strong> (Toán, Ngữ văn, Tiếng Anh) + <strong>1 môn chọn của khối</strong> (Địa lý)."
    }
};

let currentSelectedKhoi = "A01";

// Chọn khối thi mục tiêu và tự động hiển thị đúng 4 môn tương ứng
function selectKhoiTarget(khoiCode) {
    if (!KHOI_CONFIGS[khoiCode]) return;
    currentSelectedKhoi = khoiCode;
    const cfg = KHOI_CONFIGS[khoiCode];

    // Highlight button pill
    document.querySelectorAll(".btn-khoi-pill").forEach(btn => {
        btn.classList.remove("active");
    });
    const activeBtn = document.getElementById(`btn-khoi-${khoiCode}`);
    if (activeBtn) activeBtn.classList.add("active");

    // Cập nhật tên khối hiển thị
    const selectedKhoiName = document.getElementById("selected-khoi-name");
    if (selectedKhoiName) selectedKhoiName.textContent = cfg.name;

    // Cập nhật banner mô tả cấu trúc 4 môn
    const bannerText = document.getElementById("khoi-structure-text");
    if (bannerText) bannerText.innerHTML = cfg.desc;

    // Bật/tắt 4 môn của khối và cập nhật tag vai trò
    ALL_SUBJECTS.forEach(s => {
        const isSelected = cfg.subs.includes(s);
        const chk = document.getElementById(`chk-${s}`);
        const chip = document.getElementById(`chip-${s}`);
        const wrap = document.getElementById(`wrap-score-${s}`);
        const tag = document.getElementById(`tag-role-${s}`);

        if (chk) chk.checked = isSelected;
        if (chip) {
            if (isSelected) chip.classList.add("checked");
            else chip.classList.remove("checked");
        }
        if (wrap) {
            if (isSelected) {
                wrap.classList.remove("hidden");
                wrap.style.display = "flex";
            } else {
                wrap.classList.add("hidden");
                wrap.style.display = "none";
            }
        }

        if (tag) {
            if (cfg.core.includes(s)) {
                tag.className = "sub-role-tag role-core";
                tag.textContent = "Môn chính";
            } else if (cfg.elective.includes(s)) {
                tag.className = "sub-role-tag role-elective";
                tag.textContent = `Môn chọn ${khoiCode}`;
            } else {
                tag.className = "sub-role-tag role-elective";
                tag.textContent = "Môn chọn";
            }
        }
    });

    updateSelectedSubjectsCount();
}

// Bật/tắt ngăn kéo tùy chỉnh môn thi
function toggleCustomSubsDrawer() {
    const drawer = document.getElementById("custom-subs-drawer");
    if (!drawer) return;
    drawer.classList.toggle("hidden");
}

// Bật/tắt thủ công từng môn trong ngăn kéo tùy chỉnh
function toggleSubject(subKey) {
    const chk = document.getElementById(`chk-${subKey}`);
    const chip = document.getElementById(`chip-${subKey}`);
    const wrap = document.getElementById(`wrap-score-${subKey}`);
    if (!chk || !wrap) return;

    if (chk.checked) {
        if (chip) chip.classList.add("checked");
        wrap.classList.remove("hidden");
        wrap.style.display = "flex";
    } else {
        if (chip) chip.classList.remove("checked");
        wrap.classList.add("hidden");
        wrap.style.display = "none";
    }
    updateSelectedSubjectsCount();
}

function updateSelectedSubjectsCount() {
    let count = 0;
    ALL_SUBJECTS.forEach(s => {
        const chk = document.getElementById(`chk-${s}`);
        if (chk && chk.checked) count++;
    });
    const countEl = document.getElementById("selected-subjects-count");
    if (countEl) countEl.textContent = count;
}

// Priority preview update
function updatePriorityPreview() {
    const areaSelect = document.getElementById("priority-area");
    const ethSelect = document.getElementById("priority-ethnicity");
    if (!areaSelect || !ethSelect) return;

    const areaVal = areaSelect.value;
    const ethVal = ethSelect.value;

    const areaMap = { "KV1": 0.75, "KV2-NT": 0.5, "KV2": 0.25, "KV3": 0.0 };
    const areaPts = areaMap[areaVal] || 0.0;
    const ethPts = (ethVal === "minority") ? 1.0 : 0.0;
    const totalBase = areaPts + ethPts;

    const elTotal = document.getElementById("preview-priority-total");
    const elArea = document.getElementById("preview-priority-area");
    const elEth = document.getElementById("preview-priority-ethnicity");

    if (elTotal) elTotal.textContent = `+${totalBase.toFixed(2)} điểm`;
    if (elArea) elArea.textContent = `${areaPts.toFixed(2)}đ`;
    if (elEth) elEth.textContent = `${ethPts.toFixed(2)}đ`;
}

function loadPreset(key) {
    if (!key || !PRESETS[key]) return;
    const p = PRESETS[key];

    // Cập nhật khối thi mục tiêu tương ứng với preset (chỉ hiện 4 môn của khối)
    const khoi = p.khoi || "A01";
    selectKhoiTarget(khoi);

    // Điền điểm số
    document.getElementById("score-toan").value = p.toan;
    document.getElementById("score-van").value = p.van;
    document.getElementById("score-anh").value = p.anh;
    document.getElementById("score-ly").value = p.ly;
    document.getElementById("score-hoa").value = p.hoa;
    document.getElementById("score-sinh").value = p.sinh;
    document.getElementById("score-su").value = p.su;
    document.getElementById("score-dia").value = p.dia;
    document.getElementById("transcript-gpa").value = p.gpa;
    document.getElementById("ielts-score").value = p.ielts;
    document.getElementById("priority-area").value = p.priority;
    if (document.getElementById("priority-ethnicity")) {
        document.getElementById("priority-ethnicity").value = p.ethnicity || "kinh";
    }
    document.getElementById("target-region").value = p.region;
    document.getElementById("target-category").value = p.category;
    if (document.getElementById("target-tuition")) {
        document.getElementById("target-tuition").value = p.tuition || "Tất cả";
    }
    document.getElementById("user-interest").value = p.interest;

    updatePriorityPreview();

    // Đồng bộ vào ô followup
    const followupEl = document.getElementById("followup-query");
    if (followupEl) followupEl.value = p.interest;

    // Reset What-If and update baseline scores for preset
    if (typeof resetWhatIf === "function") {
        resetWhatIf();
    }
    baselineOriginalScores = {
        "Toán": p.toan,
        "Tiếng Anh": p.anh,
        "ielts": p.ielts || ""
    };
}

// HyDE Quick Test
async function testHyDEQuickly() {
    const query = document.getElementById("user-interest").value.trim();
    if (!query) {
        alert("Vui lòng nhập một câu mô tả sở thích hoặc nguyện vọng trước!");
        return;
    }

    try {
        const res = await fetch("/api/hyde-search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query, top_k: 3 })
        });
        const json = await res.json();
        if (json.status === "success") {
            document.getElementById("hyde-text").textContent = json.data.hypothetical_document;
            document.getElementById("hyde-result-box").classList.remove("hidden");
        }
    } catch (err) {
        console.error("HyDE error:", err);
    }
}

function closeHyDEBox() {
    document.getElementById("hyde-result-box").classList.add("hidden");
}

// Multi-Agent LangGraph Consultation Pipeline
async function triggerMultiAgentConsultation() {
    const btn = document.getElementById("btn-consult");
    const loading = document.getElementById("loading-state");
    const agentsSection = document.getElementById("agents-results-section");
    const dashboardSection = document.getElementById("dashboard-section");

    // Gather Inputs: CHỈ LẤY CÁC MÔN ĐÃ ĐƯỢC CHỌN
    const examScores = {};
    ALL_SUBJECTS.forEach(s => {
        const chk = document.getElementById(`chk-${s}`);
        if (chk && chk.checked) {
            const info = SUBJECT_INFO[s];
            const val = parseFloat(document.getElementById(info.inputId).value);
            examScores[info.name] = !isNaN(val) ? val : 0;
        }
    });

    if (Object.keys(examScores).length === 0) {
        alert("Vui lòng chọn ít nhất 1 môn thi tốt nghiệp!");
        return;
    }

    const gpa = parseFloat(document.getElementById("transcript-gpa").value) || 7.5;
    const transcriptScores = {
        "Toán": gpa, "Ngữ văn": gpa, "Tiếng Anh": gpa, "Vật lý": gpa, "Hóa học": gpa
    };

    const ieltsVal = document.getElementById("ielts-score").value.trim();
    const ieltsScore = ieltsVal ? parseFloat(ieltsVal) : null;
    const priorityArea = document.getElementById("priority-area").value;
    const priorityEthnicity = document.getElementById("priority-ethnicity") ? document.getElementById("priority-ethnicity").value : "kinh";
    const targetRegion = document.getElementById("target-region").value;
    const targetCategory = document.getElementById("target-category").value;
    const targetTuition = document.getElementById("target-tuition") ? document.getElementById("target-tuition").value : "Tất cả";
    const userInterest = document.getElementById("user-interest").value.trim();

    const payload = {
        exam_scores: examScores,
        transcript_scores: transcriptScores,
        user_interest: userInterest,
        holland_answers: userHollandScores,
        ielts_score: ieltsScore,
        priority_area: priorityArea,
        ethnicity: priorityEthnicity,
        target_region: targetRegion,
        target_category: targetCategory,
        target_tuition: targetTuition
    };

    // UI Loading state
    btn.disabled = true;
    loading.classList.remove("hidden");
    agentsSection.classList.add("hidden");
    dashboardSection.classList.add("hidden");

    // Hiển thị câu hỏi đang được thẩm định
    const loadingAgentText = document.getElementById("loading-agent-text");
    if (loadingAgentText) {
        loadingAgentText.textContent = userInterest 
            ? `Hội đồng Agent đang thẩm định câu hỏi: "${userInterest.length > 50 ? userInterest.substring(0, 48) + '...' : userInterest}"` 
            : "Hội đồng Agent đang phối hợp phân tích...";
    }

    try {
        const response = await fetch("/api/consult", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.status !== "success") {
            throw new Error(result.detail || "Có lỗi xảy ra khi thực thi tư vấn.");
        }

        const data = result.data;
        currentConsultResult = data;

        // Populate sections
        populateAgentResults(data);
        populateDashboard(data);

        // Hiển thị thanh trạng thái thời gian đánh giá mới nhất
        const statusBar = document.getElementById("eval-status-bar");
        const timeBadge = document.getElementById("eval-timestamp-badge");
        if (statusBar && timeBadge) {
            const now = new Date().toLocaleTimeString('vi-VN');
            const qDisp = userInterest ? `"${userInterest.length > 60 ? userInterest.substring(0, 57) + '...' : userInterest}"` : "Hồ sơ điểm";
            timeBadge.innerHTML = `<span style="color: #059669; font-weight: bold;">[${now}]</span> cho câu hỏi: <em>${qDisp}</em>`;
            statusBar.classList.remove("hidden");
        }

        // Đồng bộ câu hỏi vào ô followup
        const followupEl = document.getElementById("followup-query");
        if (followupEl) {
            followupEl.value = userInterest;
        }

        // Show sections
        loading.classList.add("hidden");
        agentsSection.classList.remove("hidden");
        dashboardSection.classList.remove("hidden");

        // Scroll to results
        agentsSection.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
        loading.classList.add("hidden");
        alert("Lỗi khi kết nối với Hội đồng Agent: " + err.message);
        console.error(err);
    } finally {
        btn.disabled = false;
    }
}

// Multi-Dimensional Interest Tags Toggle
function toggleInterestTag(tagText) {
    const input = document.getElementById("user-interest");
    if (!input) return;

    let currentVal = input.value.trim();
    
    // Tìm button vừa click để toggle class active
    const buttons = document.querySelectorAll("#interest-tags-grid .tag-chip");
    let clickedBtn = null;
    buttons.forEach(btn => {
        if (btn.getAttribute("onclick") && btn.getAttribute("onclick").includes(tagText)) {
            clickedBtn = btn;
        }
    });

    if (currentVal.includes(tagText)) {
        // Đã có -> gỡ bỏ
        currentVal = currentVal.replace(new RegExp(`,?\\s*${tagText}`, "g"), "").trim();
        currentVal = currentVal.replace(/^,\s*/, "").replace(/,\s*$/, "");
        input.value = currentVal;
        if (clickedBtn) clickedBtn.classList.remove("active");
    } else {
        // Chưa có -> bổ sung
        if (currentVal === "" || currentVal.startsWith("Em thích làm việc với máy tính nhưng điểm toán chỉ dự đoán khoảng 7")) {
            input.value = "Em " + tagText;
        } else {
            input.value = currentVal + ", " + tagText;
        }
        if (clickedBtn) clickedBtn.classList.add("active");
    }

    // Đánh thức sự kiện input để reset bộ nhớ đệm
    input.dispatchEvent(new Event("input"));
}

// Render "Hệ Thống Hiểu Bạn Thế Nào?" (AI Empathy Summary)
function renderAiEmpathySummary(empathy) {
    const card = document.getElementById("ai-empathy-card");
    if (!card) return;

    if (!empathy || !empathy.narrative) {
        card.classList.add("hidden");
        return;
    }

    const strengths = (empathy.identified_strengths || []).map(s => `
        <span class="empathy-tag empathy-tag-positive"><i class="fa-solid fa-circle-check"></i> ${s}</span>
    `).join("");

    const excluded = (empathy.excluded_constraints || []).map(e => `
        <span class="empathy-tag empathy-tag-excluded"><i class="fa-solid fa-ban"></i> Đã loại trừ: ${e}</span>
    `).join("");

    card.innerHTML = `
        <div class="empathy-header">
            <div class="empathy-title-wrap">
                <div class="empathy-icon"><i class="fa-solid fa-heart-circle-check"></i></div>
                <div>
                    <h3 class="empathy-title">Hệ Thống Hiểu Bạn Thế Nào?</h3>
                    <p class="empathy-subtitle">Góc nhìn thấu cảm & phân tích đa chiều từ lời chia sẻ tự nhiên của bạn</p>
                </div>
            </div>
            <span class="empathy-riasec-badge"><i class="fa-solid fa-brain"></i> ${empathy.dominant_type || 'Đa dạng'} (${empathy.primary_code || 'RIASEC'})</span>
        </div>
        <div class="empathy-body">
            <div class="empathy-narrative">
                <i class="fa-solid fa-quote-left quote-icon"></i>
                <div>${formatMarkdown(empathy.narrative)}</div>
            </div>
            <div class="empathy-badges-row">
                <div class="empathy-group">
                    <span class="empathy-group-label"><i class="fa-solid fa-thumbs-up text-success"></i> Điểm cộng & Thế mạnh nhận diện:</span>
                    <div class="empathy-tags-wrap">${strengths || '<span class="empathy-tag empathy-tag-positive">Tư duy linh hoạt</span>'}</div>
                </div>
                ${excluded ? `
                    <div class="empathy-group">
                        <span class="empathy-group-label"><i class="fa-solid fa-shield-halved text-danger"></i> Ràng buộc đã chủ động loại trừ (Bạn tránh):</span>
                        <div class="empathy-tags-wrap">${excluded}</div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    card.classList.remove("hidden");

    // Also populate the Section 4 roadmap empathy banner directly above the 10 recommendations
    const banner = document.getElementById("roadmap-empathy-banner");
    if (banner) {
        const excludedText = (empathy.excluded_constraints || []).length > 0
            ? `<div class="empathy-excluded-inline"><i class="fa-solid fa-ban text-danger"></i> Đã loại trừ khỏi đề xuất: <strong>${empathy.excluded_constraints.join(", ")}</strong></div>`
            : '';
        banner.innerHTML = `
            <div class="roadmap-empathy-inner">
                <i class="fa-solid fa-heart-circle-check"></i>
                <div class="roadmap-empathy-content">
                    <div><strong>AI Thấu Hiểu Nguyện Vọng:</strong> ${empathy.narrative}</div>
                    ${excludedText}
                </div>
            </div>
        `;
        banner.classList.remove("hidden");
    }
}

// Render Agent Results
function populateAgentResults(data) {
    const academic = data.academic_analysis;
    const psychology = data.psychology_analysis;
    const admission = data.admission_analysis;
    const finalReport = data.final_report;

    // 0. AI Empathy Summary
    renderAiEmpathySummary(finalReport?.empathy_summary || psychology?.empathy_summary);

    // 0b. Tích hợp Đánh giá & Phỏng vấn Trường mục tiêu nếu có
    renderIntegratedSchoolConsultationCard();

    // 1. Academic Agent
    document.getElementById("academic-commentary").innerHTML = formatMarkdown(academic.commentary);
    document.getElementById("metric-top-combo").textContent = academic.top_combination;
    document.getElementById("metric-top-score").textContent = academic.top_score.toFixed(2) + " điểm";
    document.getElementById("metric-std").textContent = "±" + academic.std_deviation.toFixed(2);
    renderCombosChart(academic.ranked_combinations);

    // 2. Psychology Agent
    document.getElementById("psychology-commentary").innerHTML = formatMarkdown(psychology.commentary);
    document.getElementById("metric-holland-code").textContent = psychology.primary_code;
    document.getElementById("metric-dominant-group").textContent = psychology.dominant_type;
    renderHollandRadarChart(psychology.holland_scores);

    // 3. Admission Agent
    document.getElementById("admission-commentary").innerHTML = formatMarkdown(admission.commentary);
    
    // IELTS Advantage Tags
    const ieltsBox = document.getElementById("ielts-advantage-box");
    ieltsBox.innerHTML = "";
    if (admission.ielts_advantages && admission.ielts_advantages.length > 0) {
        admission.ielts_advantages.slice(0, 3).forEach(adv => {
            const tag = document.createElement("div");
            tag.className = "ielts-pill";
            tag.innerHTML = `<strong>${adv.university_code}:</strong> IELTS ${adv.ielts_band} ➔ ${adv.converted_english_score}đ (+${adv.score_gain}đ)`;
            ieltsBox.appendChild(tag);
        });
    }

    // Sub-criteria Alerts
    const alertBox = document.getElementById("sub-criteria-alert-box");
    alertBox.innerHTML = "";
    if (admission.sub_criteria_alerts && admission.sub_criteria_alerts.length > 0) {
        admission.sub_criteria_alerts.forEach(al => {
            const p = document.createElement("p");
            p.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-warning"></i> ${al}`;
            alertBox.appendChild(p);
        });
    }

    // Synthesis Summary
    document.getElementById("synthesis-summary-text").innerHTML = formatMarkdown(finalReport.summary);
}

// // Render Roadmap cards
function renderRoadmap(topRecs) {
    const roadmapContainer = document.getElementById("roadmap-items");
    if (!roadmapContainer) return;
    roadmapContainer.innerHTML = "";

    if (!topRecs || topRecs.length === 0) {
        roadmapContainer.innerHTML = `<div class="placeholder-text">Không tìm thấy tổ hợp phù hợp với bộ lọc hiện tại. Hãy mở rộng khu vực, khối thi hoặc học phí.</div>`;
        return;
    }

    topRecs.forEach((item, idx) => {
        let roleClass = "role-target";
        let badgeClass = "prob-target";
        if (item.pass_probability >= 90) {
            roleClass = "role-safety";
            badgeClass = "prob-safety";
        } else if (item.pass_probability < 60) {
            roleClass = "role-reach";
            badgeClass = "prob-reach";
        }

        const cg = item.career_guidance || {};
        const sb = cg.skill_sandbox || {};
        const aiImp = cg.ai_impact || {};
        const workDist = cg.work_distribution || {};
        const caseStudy = cg.mini_case_study || null;
        const isFav = isInWishlist(item.university_code, item.major_name);

        // Highlight banner if simulated
        let highlightBannerHtml = "";
        if (item.score_diff_from_baseline && item.score_diff_from_baseline > 0) {
            highlightBannerHtml = `
                <div class="whatif-card-highlight">
                    <i class="fa-solid fa-wand-magic-sparkles" style="color: #16a34a;"></i>
                    <span><strong>Mô phỏng nâng điểm:</strong> Điểm tăng +${item.score_diff_from_baseline}đ (${item.old_candidate_score}đ ➔ <strong>${item.candidate_score}đ</strong>), tỷ lệ đỗ: ${item.old_pass_probability}% ➔ <strong>${item.pass_probability}%</strong> (${item.strategy_role})</span>
                </div>
            `;
        }

        // 1. Work Distribution Bar HTML (handles array [{task, percent}] or object {task: percent})
        let workDistHtml = "";
        let workDistItems = [];
        if (Array.isArray(cg.work_distribution)) {
            workDistItems = cg.work_distribution;
        } else if (typeof cg.work_distribution === "object" && cg.work_distribution !== null) {
            workDistItems = Object.keys(cg.work_distribution).map(k => ({ task: k, percent: cg.work_distribution[k] }));
        }

        if (workDistItems.length > 0) {
            const segBars = workDistItems.map((item, i) => 
                `<div class="work-dist-seg seg-${i % 4}" style="width: ${item.percent}%;" title="${item.task}: ${item.percent}%"></div>`
            ).join('');
            const legendItems = workDistItems.map((item, i) => `
                <div class="legend-item">
                    <span class="legend-color-dot seg-${i % 4}"></span>
                    <span>${item.task} (<strong>${item.percent}%</strong>)</span>
                </div>
            `).join('');
            workDistHtml = `
                <div class="work-dist-bar-wrap">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #334155; margin-bottom: 0.2rem;">
                        <i class="fa-solid fa-pie-chart" style="color: #3b82f6;"></i> Phân rã thời gian làm việc thực tế:
                    </div>
                    <div class="work-dist-bar">${segBars}</div>
                    <div class="work-dist-legend">${legendItems}</div>
                </div>
            `;
        }

        // 2. AI Impact Badge
        let aiImpactHtml = "";
        const aiRisk = aiImp.automation_risk_pct !== undefined ? aiImp.automation_risk_pct : aiImp.automation_risk_percent;
        if (aiRisk !== undefined) {
            const riskClass = aiRisk < 25 ? 'ai-risk-low' : (aiRisk < 50 ? 'ai-risk-med' : 'ai-risk-high');
            aiImpactHtml = `
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-top: 0.4rem;">
                    <span class="ai-impact-badge ${riskClass}">
                        <i class="fa-solid fa-robot"></i> Rủi ro AI tự động hóa: ${aiRisk}% (${aiImp.risk_level || 'Thấp'})
                    </span>
                    ${(aiImp.national_priority || aiImp.national_strategic_priority) ? `
                        <span class="ai-impact-badge" style="background: #fdf2f8; color: #9d174d; border: 1px solid #fbcfe8;">
                            <i class="fa-solid fa-star"></i> Ngành Trọng điểm Quốc gia
                        </span>
                    ` : ''}
                    ${(aiImp.ai_augmented_skills || []).length > 0 ? `
                        <div style="font-size: 0.75rem; color: #475569; width: 100%; margin-top: 0.2rem;">
                            <strong>Kỹ năng cộng hưởng AI:</strong> ${aiImp.ai_augmented_skills.join(' • ')}
                        </div>
                    ` : ''}
                </div>
            `;
        }

        // 3. Pressure & Challenges HTML
        let pressureHtml = "";
        const rawPressure = cg.pressure_challenges;
        let pressureList = [];
        if (Array.isArray(rawPressure)) {
            pressureList = rawPressure;
        } else if (typeof rawPressure === "string" && rawPressure.trim().length > 0) {
            pressureList = [rawPressure];
        }
        if (pressureList.length > 0) {
            pressureHtml = `
                <div class="reality-pressure-box mt-3">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #b45309; margin-bottom: 0.3rem;">
                        <i class="fa-solid fa-triangle-exclamation text-warning"></i> Mặt trái & Áp lực đặc thù của nghề:
                    </div>
                    <ul class="pressure-list">
                        ${pressureList.map(c => `<li><i class="fa-solid fa-circle-exclamation text-danger" style="font-size: 0.7rem; margin-right: 0.3rem;"></i> ${c}</li>`).join("")}
                    </ul>
                </div>
            `;
        }

        // 4. Mini Case Study HTML
        let caseStudyHtml = "";
        if (caseStudy && caseStudy.scenario) {
            const firstQ = (caseStudy.questions && caseStudy.questions.length > 0) ? caseStudy.questions[0] : null;
            const qText = firstQ ? firstQ.q : "Hành động đầu tiên bạn sẽ xử lý là gì?";
            const options = firstQ ? (firstQ.options || []) : (caseStudy.options || []);
            if (options.length > 0) {
                const optBtns = options.map((opt, optIdx) => {
                    const optText = typeof opt === "string" ? opt : (opt.text || opt.title || JSON.stringify(opt));
                    return `
                        <button type="button" class="case-study-btn" id="cs-opt-${idx}-${optIdx}" onclick="selectCaseStudyOption(${idx}, ${optIdx})">
                            <span class="opt-label">${String.fromCharCode(65 + optIdx)}.</span> ${optText}
                        </button>
                    `;
                }).join('');
                caseStudyHtml = `
                    <div class="case-study-box">
                        <div style="font-size: 0.85rem; font-weight: 700; color: #15803d; display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.4rem;">
                            <i class="fa-solid fa-lightbulb"></i> Mini Case-Study: Tình Huống Xử Lý Thực Tế
                        </div>
                        <div class="case-study-scenario">${caseStudy.scenario}</div>
                        <div class="case-study-question" style="font-size: 0.82rem; font-weight: 600; color: #1e293b; margin: 0.5rem 0 0.35rem 0;">
                            <strong>Câu hỏi tình huống:</strong> ${qText}
                        </div>
                        <div class="case-study-options">${optBtns}</div>
                        <div id="cs-feedback-${idx}" class="case-study-feedback" style="display: none;"></div>
                    </div>
                `;
            }
        }

        const el = document.createElement("div");
        el.className = `roadmap-item ${roleClass}`;
        el.innerHTML = `
            ${highlightBannerHtml}
            <div class="roadmap-main-row">
                <div class="roadmap-left">
                    <div class="roadmap-rank-badge">#${idx + 1}</div>
                    <div class="roadmap-title-area">
                        <div class="roadmap-tags-row">
                            <span class="roadmap-role-tag">${item.strategy_role || 'Phù hợp'}</span>
                            <span class="roadmap-tuition-tag"><i class="fa-solid fa-layer-group"></i> ${item.major_category}</span>
                            ${aiImp.automation_risk_pct !== undefined ? `
                                <span class="ai-impact-badge ${aiImp.automation_risk_pct < 25 ? 'ai-risk-low' : (aiImp.automation_risk_pct < 50 ? 'ai-risk-med' : 'ai-risk-high')}">
                                    <i class="fa-solid fa-robot"></i> AI Risk: ${aiImp.automation_risk_pct}%
                                </span>
                            ` : ''}
                        </div>
                        <div class="roadmap-major-row">
                            <span class="roadmap-major">${item.major_name} (${item.combination_code})</span>
                            <span class="program-type-badge ${item.program_type && (item.program_type.includes('CLC') || item.program_type.includes('Chất lượng')) ? 'badge-clc' : (item.program_type && item.program_type.includes('Quốc tế')) ? 'badge-intl' : 'badge-standard'}">
                                <i class="fa-solid fa-graduation-cap"></i> ${item.program_type || 'Hệ Chuẩn (Đại trà)'}
                            </span>
                        </div>
                        <div class="roadmap-uni-row">
                            <span class="roadmap-uni"><i class="fa-solid fa-building-columns"></i> <strong>${item.university_name} (${item.university_code})</strong> • ${item.university_region}</span>
                            <span class="uni-tuition-pill ${item.is_tuition_alert ? 'tuition-alert' : 'tuition-normal'}">
                                <i class="fa-solid fa-coins"></i> Học phí: <strong>~${item.tuition_range || 'Chưa công bố'} tr/năm</strong>
                            </span>
                            ${item.is_tuition_alert ? `
                                <span class="tuition-alert-badge" title="${item.tuition_alert_msg}">
                                    <i class="fa-solid fa-triangle-exclamation"></i> ${item.tuition_alert_msg}
                                </span>
                            ` : ''}
                        </div>
                    </div>
                </div>
                <div class="roadmap-right">
                    <div>
                        <div style="font-size: 0.8rem; color: #64748b;">Điểm chuẩn 2025: <strong>${item.score_2025}đ</strong></div>
                        <div style="font-size: 0.8rem;">Điểm bạn: <strong>${item.candidate_score}đ</strong> (${item.score_delta >= 0 ? '+' : ''}${item.score_delta}đ)</div>
                    </div>
                    <span class="prob-badge ${badgeClass}"><i class="fa-solid fa-chart-pie"></i> ${item.pass_probability}% Đỗ</span>
                    <div style="display: flex; gap: 0.35rem; align-items: center; flex-wrap: wrap;">
                        <button type="button" class="btn-toggle-wishlist ${isFav ? 'active' : ''}" id="btn-wishlist-${idx}" onclick="toggleWishlistItemFromCard(${idx})">
                            <i class="fa-${isFav ? 'solid' : 'regular'} fa-bookmark"></i> <span>${isFav ? 'Đã lưu' : 'Lưu NV'}</span>
                        </button>
                        <button type="button" class="btn-secondary" style="font-size: 0.75rem; padding: 0.28rem 0.5rem;" onclick="openRoiForMajor('${item.university_code}', '${encodeURIComponent(item.major_name)}')">
                            <i class="fa-solid fa-calculator text-success"></i> ROI
                        </button>
                        <button type="button" class="btn-toggle-details" onclick="toggleRoadmapDetails(${idx})">
                            <i class="fa-solid fa-circle-info"></i> <span id="toggle-text-${idx}">Chi tiết</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Collapsible Detailed Analysis & Career Guidance -->
            <div id="roadmap-details-${idx}" class="roadmap-details" style="display: none;">
                <div class="ai-explanation-box">
                    <i class="fa-solid fa-brain"></i> <strong>Lý do Hội đồng AI đề xuất:</strong> ${item.ai_explanation || 'Phù hợp với năng lực và tổ hợp xét tuyển của bạn.'}
                </div>

                ${cg.entry_roles ? `
                    <div class="career-guidance-card">
                        <!-- Left col: Roles, Daily work & Reality check -->
                        <div class="career-roles-section">
                            <span class="career-section-label"><i class="fa-solid fa-briefcase"></i> Vị trí việc làm tiêu biểu:</span>
                            <div class="career-role-chips">
                                ${(cg.entry_roles || []).map(r => `<span class="career-role-chip">${r}</span>`).join('')}
                            </div>
                            <p style="font-size: 0.8rem; color: #475569; margin-top: 0.35rem;">
                                <strong>Công việc hàng ngày:</strong> ${cg.daily_work || ''}
                            </p>

                            <!-- Reality Check: Work Distribution -->
                            ${workDistHtml}

                            <!-- Reality Check: Pressure & Challenges -->
                            ${pressureHtml}
                        </div>

                        <!-- Right col: Salary, AI Impact, Shortcuts -->
                        <div class="career-roles-section">
                            <span class="career-section-label"><i class="fa-solid fa-chart-line"></i> Mức thu nhập & Thị trường:</span>
                            <div class="salary-box">
                                <span>Mới ra trường (Fresher):</span>
                                <span class="salary-val">${cg.starting_salary || '8 - 12 tr/tháng'}</span>
                            </div>
                            <div class="salary-box" style="margin-top: 0.35rem;">
                                <span>3 - 5 năm kinh nghiệm:</span>
                                <span class="salary-val">${cg.mid_salary || '15 - 25 tr/tháng'}</span>
                            </div>
                            <p style="font-size: 0.78rem; color: #64748b; margin-top: 0.35rem;">
                                <i class="fa-solid fa-globe"></i> ${cg.labor_market_outlook || ''}
                            </p>

                            <!-- AI Automation Impact -->
                            ${aiImpactHtml}

                            <!-- Quick Action Buttons -->
                            <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem; flex-wrap: wrap;">
                                <button type="button" class="btn-secondary" style="font-size: 0.78rem; padding: 0.4rem 0.65rem;" onclick="openRoiForMajor('${item.university_code}', '${encodeURIComponent(item.major_name)}')">
                                    <i class="fa-solid fa-calculator" style="color: #10b981;"></i> Tính ROI trường này
                                </button>
                                <button type="button" class="btn-secondary" style="font-size: 0.78rem; padding: 0.4rem 0.65rem;" onclick="openCompareWithMajor('${encodeURIComponent(item.major_name)}')">
                                    <i class="fa-solid fa-code-compare" style="color: #6366f1;"></i> So sánh đối đầu
                                </button>
                            </div>
                        </div>

                        <!-- Skill Sandbox Box -->
                        <div class="skill-sandbox-box">
                            <div class="skill-sandbox-title">
                                <i class="fa-solid fa-flask-vial"></i> Skill Sandbox: Thử Thách Trải Nghiệm Năng Lực
                            </div>
                            <div class="sandbox-task">
                                <strong><i class="fa-solid fa-stopwatch"></i> Nhiệm vụ thử nghiệm (30 - 45 phút):</strong> ${sb.tryout_task || 'Tìm hiểu dự án thực tế về ngành.'}
                            </div>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #1e293b; margin: 0.5rem 0 0.35rem 0;">
                                <i class="fa-solid fa-circle-check" style="color: #10b981;"></i> Dấu hiệu bạn thực sự phù hợp với ngành (Tự suy xét):
                            </div>
                            <ul class="sandbox-criteria-list">
                                ${(sb.self_assessment_criteria || []).map(c => `<li>${c}</li>`).join('')}
                            </ul>
                            ${sb.self_assessment ? `
                                <div style="font-size: 0.78rem; color: #3730a3; background: #eef2ff; border-left: 3px solid #6366f1; border-radius: 4px; padding: 0.45rem 0.65rem; margin-top: 0.45rem;">
                                    <i class="fa-solid fa-lightbulb" style="color: #f59e0b;"></i> ${sb.self_assessment}
                                </div>
                            ` : ''}
                            ${sb.course_name ? `
                                <div style="font-size: 0.78rem; color: #2563eb; margin-top: 0.45rem; font-weight: 500;">
                                    <i class="fa-solid fa-graduation-cap"></i> Khóa học/Tài liệu nhập môn gợi ý: <strong>${sb.course_name}</strong>
                                </div>
                            ` : ''}
                            ${sb.link ? `
                                <a href="${sb.link}" target="_blank" class="sandbox-course-link">
                                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Truy cập khóa học: ${sb.intro_course_name || sb.course_name} (${sb.provider || 'Online'})
                                </a>
                            ` : ''}
                        </div>

                        <!-- Mini Case Study Box -->
                        ${caseStudyHtml ? `<div style="grid-column: 1 / -1;">${caseStudyHtml}</div>` : ''}
                    </div>
                ` : ''}
            </div>
        `;
        roadmapContainer.appendChild(el);
    });
}

// Render Dashboard & 3-Tier Categorization
function populateDashboard(data) {
    const safety = data.safety_majors || [];
    const target = data.target_majors || [];
    const reach = data.reach_majors || [];
    const finalReport = data.final_report;

    // Record baseline original scores for what-if
    baselineOriginalScores = {
        "Toán": parseFloat(document.getElementById("score-toan")?.value) || 0,
        "Tiếng Anh": parseFloat(document.getElementById("score-anh")?.value) || 0,
        "ielts": document.getElementById("ielts-score")?.value || ""
    };

    // Counters
    document.getElementById("count-safety").textContent = `${safety.length} ngành`;
    document.getElementById("count-target").textContent = `${target.length} ngành`;
    document.getElementById("count-reach").textContent = `${reach.length} ngành`;

    document.getElementById("tab-count-safety").textContent = safety.length;
    document.getElementById("tab-count-target").textContent = target.length;
    document.getElementById("tab-count-reach").textContent = reach.length;

    // Top 10 Roadmap (Tỷ Lệ Vàng)
    const topRecs = finalReport.top_recommendations || [];
    renderRoadmap(topRecs);

    // Render default tab: safety
    switchTierTab("safety");

    // Render Historical Benchmarks Comparison Chart
    renderHistoricalChart(topRecs);
}

// Toggle Roadmap Details
function toggleRoadmapDetails(idx) {
    const el = document.getElementById(`roadmap-details-${idx}`);
    const btnText = document.getElementById(`toggle-text-${idx}`);
    if (!el) return;
    if (el.style.display === "none" || el.style.display === "") {
        el.style.display = "flex";
        if (btnText) btnText.textContent = "Thu gọn chi tiết";
    } else {
        el.style.display = "none";
        if (btnText) btnText.textContent = "Chi tiết nghề & Sandbox";
    }
}

// Export Strategy to PDF (A4)
function exportStrategyPDF() {
    if (!currentConsultResult) {
        alert("Vui lòng thực hiện tư vấn để có lộ trình trước khi xuất báo cáo PDF!");
        return;
    }
    // Mở rộng tất cả chi tiết nghề nghiệp và sandbox để in trọn vẹn
    const details = document.querySelectorAll(".roadmap-details");
    details.forEach(d => {
        d.style.display = "flex";
    });
    window.print();
}

// Switch between Tier tabs (Safety, Target, Reach)
function switchTierTab(tier) {
    const tabBtns = document.querySelectorAll(".tier-tab-btn");
    tabBtns.forEach(btn => btn.classList.remove("active"));
    const container = document.getElementById("tier-table-container");
    if (!currentConsultResult) return;

    let items = [];
    if (tier === "safety") {
        if (tabBtns[0]) tabBtns[0].classList.add("active");
        items = currentConsultResult.safety_majors || [];
    } else if (tier === "target") {
        if (tabBtns[1]) tabBtns[1].classList.add("active");
        items = currentConsultResult.target_majors || [];
    } else {
        if (tabBtns[2]) tabBtns[2].classList.add("active");
        items = currentConsultResult.reach_majors || [];
    }

    if (items.length === 0) {
        container.innerHTML = `<p style="padding: 1.5rem; text-align: center; color: #64748b;">Không có ngành nào trong nhóm này với điểm số hiện tại.</p>`;
        return;
    }

    let html = `
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Trường Đại Học</th>
                        <th>Ngành Đào Tạo</th>
                        <th>Khối</th>
                        <th>Điểm Bạn Có</th>
                        <th>Điểm Chuẩn 2025</th>
                        <th>Độ Lệch (Δ)</th>
                        <th>Tỷ Lệ Đỗ Dự Đoán</th>
                        <th>Tiêu Chí Phụ / Ghi Chú</th>
                    </tr>
                </thead>
                <tbody>
    `;

    items.slice(0, 15).forEach(m => {
        const deltaColor = m.score_delta >= 0 ? "color: #10b981;" : "color: #ef4444;";
        const deltaSign = m.score_delta >= 0 ? `+${m.score_delta}` : `${m.score_delta}`;
        html += `
            <tr>
                <td><strong>${m.university_name}</strong><br><small style="color: #64748b;">${m.university_code} - ${m.university_region}</small></td>
                <td><strong>${m.major_name}</strong><br><small style="color: #64748b;">${m.major_category}</small></td>
                <td><span class="score-badge" style="background: #e0e7ff; color: #4338ca;">${m.combination_code}</span></td>
                <td><strong style="color: #4f46e5;">${m.candidate_score}</strong></td>
                <td>${m.score_2025}</td>
                <td><strong style="${deltaColor}">${deltaSign}</strong></td>
                <td><span class="score-badge" style="background: #f1f5f9;">${m.pass_probability}%</span></td>
                <td><small>${m.sub_criteria || "Xét điểm từ cao xuống thấp"}</small></td>
            </tr>
        `;
    });

    html += `</tbody></table></div>`;
    container.innerHTML = html;
}

// Chart 1: Subject Combinations Bar Chart
function renderCombosChart(combos) {
    const ctx = document.getElementById("chart-combos").getContext("2d");
    if (chartCombos) chartCombos.destroy();

    const labels = combos.map(c => c.combination);
    const scores = combos.map(c => c.total_score);

    chartCombos = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tổng Điểm Tổ Hợp',
                data: scores,
                backgroundColor: '#3b82f6',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { min: 15, max: 30, ticks: { stepSize: 3 } }
            }
        }
    });
}

// Chart 2: Holland RIASEC Radar Chart
function renderHollandRadarChart(hollandScores) {
    const ctx = document.getElementById("chart-holland").getContext("2d");
    if (chartHolland) chartHolland.destroy();

    const labels = [
        "R (Thực tế)", "I (Nghiên cứu)", "A (Sáng tạo)", 
        "S (Xã hội)", "E (Quản trị)", "C (Nghiệp vụ)"
    ];
    const dataVals = [
        hollandScores["R"] || 10,
        hollandScores["I"] || 10,
        hollandScores["A"] || 10,
        hollandScores["S"] || 10,
        hollandScores["E"] || 10,
        hollandScores["C"] || 10
    ];

    chartHolland = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Hồ Sơ Tố Chất Holland',
                data: dataVals,
                backgroundColor: 'rgba(219, 39, 119, 0.25)',
                borderColor: '#db2777',
                pointBackgroundColor: '#db2777',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                r: { min: 0, max: 30, ticks: { display: false } }
            }
        }
    });
}

// Chart 3: Historical Benchmarks vs Student Score
function renderHistoricalChart(topRecs) {
    const ctx = document.getElementById("chart-historical-benchmarks").getContext("2d");
    if (chartHistorical) chartHistorical.destroy();

    if (!topRecs || topRecs.length === 0) return;

    const displayItems = topRecs.slice(0, 5);
    const labels = displayItems.map(i => `${i.major_name.substring(0, 15)}... (${i.university_code})`);

    const s2023 = displayItems.map(i => i.score_2023);
    const s2024 = displayItems.map(i => i.score_2024);
    const s2025 = displayItems.map(i => i.score_2025);
    const myScore = displayItems.map(i => i.candidate_score);

    chartHistorical = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Điểm Cắt 2023',
                    data: s2023,
                    backgroundColor: '#cbd5e1',
                    borderRadius: 4
                },
                {
                    label: 'Điểm Cắt 2024',
                    data: s2024,
                    backgroundColor: '#94a3b8',
                    borderRadius: 4
                },
                {
                    label: 'Điểm Cắt 2025',
                    data: s2025,
                    backgroundColor: '#64748b',
                    borderRadius: 4
                },
                {
                    type: 'line',
                    label: 'Điểm Dự Kiến Của Bạn',
                    data: myScore,
                    borderColor: '#4f46e5',
                    backgroundColor: '#4f46e5',
                    borderWidth: 3,
                    pointRadius: 6,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: { min: 18, max: 30, title: { display: true, text: 'Điểm chuẩn xét tuyển' } }
            }
        }
    });
}

// Holland Modal logic
async function openHollandModal() {
    document.getElementById("holland-modal").classList.remove("hidden");
}

function closeHollandModal() {
    document.getElementById("holland-modal").classList.add("hidden");
}

async function loadHollandQuestions() {
    try {
        const res = await fetch("/api/holland-questions");
        const json = await res.json();
        if (json.status === "success") {
            const container = document.getElementById("holland-quiz-container");
            container.innerHTML = "";
            json.data.forEach((q, idx) => {
                const box = document.createElement("div");
                box.className = "quiz-question-box";
                box.innerHTML = `
                    <div class="quiz-q-title">Câu ${idx+1}: ${q.title}</div>
                    <div class="quiz-q-scenario">${q.scenario}</div>
                    <div class="quiz-options">
                        <label class="quiz-opt-label">
                            <input type="radio" name="${q.id}" value="${q.options[0].points}" data-trait="${q.trait}" checked>
                            ${q.options[0].text}
                        </label>
                        <label class="quiz-opt-label">
                            <input type="radio" name="${q.id}" value="${q.options[1].points}" data-trait="${q.trait}">
                            ${q.options[1].text}
                        </label>
                    </div>
                `;
                container.appendChild(box);
            });
        }
    } catch (err) {
        console.error("Failed to load Holland questions:", err);
    }
}

let modalRadarChartInstance = null;

function renderModalHollandRadar(scores) {
    const wrapper = document.getElementById("holland-radar-wrapper");
    if (!wrapper) return;
    wrapper.style.display = "block";

    const ctx = document.getElementById("hollandRadarChart");
    if (!ctx) return;

    const labels = [
        "R - Kỹ thuật", "I - Nghiên cứu", "A - Nghệ thuật", 
        "S - Xã hội", "E - Quản trị", "C - Nghiệp vụ"
    ];
    const dataVals = [
        scores["R"] || 0,
        scores["I"] || 0,
        scores["A"] || 0,
        scores["S"] || 0,
        scores["E"] || 0,
        scores["C"] || 0
    ];

    if (modalRadarChartInstance) modalRadarChartInstance.destroy();

    modalRadarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Điểm tố chất RIASEC',
                data: dataVals,
                backgroundColor: 'rgba(99, 102, 241, 0.25)',
                borderColor: '#4f46e5',
                pointBackgroundColor: '#4f46e5',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: { min: 0, max: 10, ticks: { stepSize: 2, display: false } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function submitHollandQuiz() {
    const radios = document.querySelectorAll("#holland-quiz-container input[type='radio']:checked");
    userHollandScores = { "R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0 };
    radios.forEach(r => {
        const trait = r.getAttribute("data-trait");
        const val = parseInt(r.value, 10);
        if (trait) {
            userHollandScores[trait] = (userHollandScores[trait] || 0) + val;
        }
    });

    renderModalHollandRadar(userHollandScores);
    setTimeout(() => {
        closeHollandModal();
        alert("Đã lưu kết quả bài test Holland và vẽ biểu đồ Radar RIASEC! Khi bạn bấm 'Nhận Tư Vấn', Agent Tâm lý sẽ sử dụng dữ liệu này.");
    }, 600);
}

// SLM Prospectus Analyzer Section
async function loadProspectusSample(uniCode) {
    try {
        const res = await fetch(`/api/prospectus/${uniCode}`);
        const json = await res.json();
        if (json.status === "success") {
            document.getElementById("slm-input-text").value = json.data.raw_prospectus_text;
        }
    } catch (err) {
        console.error(err);
    }
}

async function runSLMProspectusAnalysis() {
    const text = document.getElementById("slm-input-text").value.trim();
    const uniCode = document.getElementById("slm-sample-selector").value;
    const outputBox = document.getElementById("slm-results");

    if (!text) {
        alert("Vui lòng nhập văn bản đề án cần phân tích!");
        return;
    }

    outputBox.innerHTML = "<p>Đang phân tích cấu trúc quy chế bằng SLM cục bộ...</p>";

    try {
        const res = await fetch("/api/prospectus/parse", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, university_code: uniCode })
        });
        const json = await res.json();
        if (json.status === "success") {
            const data = json.data;
            let html = `
                <div class="slm-card-item">
                    <h5><i class="fa-solid fa-list-check"></i> Các Phương Thức Xét Tuyển:</h5>
                    <ul style="padding-left: 1.25rem;">
                        ${data.admission_methods.map(m => `<li>${m.raw_text}</li>`).join('')}
                    </ul>
                </div>

                <div class="slm-card-item">
                    <h5><i class="fa-solid fa-certificate"></i> Bảng Quy Đổi Điểm Chứng Chỉ Tiếng Anh (IELTS sang thang 10):</h5>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.35rem;">
                        ${Object.entries(data.ielts_conversion).map(([k, v]) => `
                            <span style="background: #334155; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: bold; color: #38bdf8;">${k} ➔ ${v}đ</span>
                        `).join('')}
                    </div>
                </div>

                <div class="slm-card-item">
                    <h5><i class="fa-solid fa-scale-balanced"></i> Tiêu Chí Phụ (Ngưỡng hòa điểm):</h5>
                    <ul style="padding-left: 1.25rem;">
                        ${data.sub_criteria.map(sc => `<li>${sc}</li>`).join('')}
                    </ul>
                </div>

                <div class="slm-card-item">
                    <h5><i class="fa-solid fa-gift"></i> Chính Sách Điểm Thưởng & Ưu Tiên:</h5>
                    <ul style="padding-left: 1.25rem;">
                        ${data.bonus_rules.map(b => `<li>${b}</li>`).join('')}
                    </ul>
                </div>
            `;
            outputBox.innerHTML = html;
        }
    } catch (err) {
        outputBox.innerHTML = `<p style="color: #ef4444;">Lỗi phân tích SLM: ${err.message}</p>`;
    }
}

// Markdown helper for formatting text
function formatMarkdown(text) {
    if (!text) return "";
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function escapeHtml(text) {
    if (!text) return "";
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Quick Question Asker (Re-evaluate immediately on click or enter)
function askQuickQuestion(questionText) {
    const interestEl = document.getElementById("user-interest");
    const followupEl = document.getElementById("followup-query");
    if (interestEl) interestEl.value = questionText;
    if (followupEl) followupEl.value = questionText;

    // Clear old Holland answers so the AI infers personality fresh for the new question
    userHollandScores = {};

    // Reset category dropdown so no stale filter blocks the search
    const catSelect = document.getElementById("target-category");
    if (catSelect) catSelect.value = "Tất cả";

    triggerMultiAgentConsultation();
}

function handleFollowupKeydown(e) {
    if (e.key === "Enter") {
        e.preventDefault();
        submitFollowupQuestion();
    }
}

function submitFollowupQuestion() {
    const followupEl = document.getElementById("followup-query");
    if (!followupEl) return;
    const q = followupEl.value.trim();
    if (!q) {
        alert("Vui lòng nhập câu hỏi hoặc nguyện vọng mới của bạn!");
        followupEl.focus();
        return;
    }
    askQuickQuestion(q);
}

// =========================================================================
// Khung Tra Cứu & Đánh Giá Trường Đại Học Mơ Ước (Dream University Target)
// =========================================================================

function handleDreamKeydown(e) {
    if (e.key === "Enter") {
        e.preventDefault();
        searchDreamUniversity();
    }
}

function quickSearchDream(keyword) {
    const input = document.getElementById("dream-search-input");
    if (input) {
        input.value = keyword;
        searchDreamUniversity();
    }
}

async function searchDreamUniversity() {
    const input = document.getElementById("dream-search-input");
    const container = document.getElementById("dream-results-container");
    if (!input || !container) return;

    const keyword = input.value.trim();
    const userInterest = document.getElementById("user-interest") ? document.getElementById("user-interest").value.trim() : "";

    if (!keyword && !userInterest) {
        alert("Vui lòng nhập tên trường hoặc mô tả sở thích nghề nghiệp ở Bước 2 để tra cứu!");
        input.focus();
        return;
    }

    // Thu thập điểm thi hiện tại
    const examScores = {};
    ALL_SUBJECTS.forEach(s => {
        const chk = document.getElementById(`chk-${s}`);
        if (chk && chk.checked) {
            const info = SUBJECT_INFO[s];
            const val = parseFloat(document.getElementById(info.inputId).value);
            examScores[info.name] = !isNaN(val) ? val : 0;
        }
    });

    const gpa = parseFloat(document.getElementById("transcript-gpa").value) || 7.5;
    const transcriptScores = { "Toán": gpa, "Ngữ văn": gpa, "Tiếng Anh": gpa, "Vật lý": gpa, "Hóa học": gpa };
    const ieltsVal = document.getElementById("ielts-score").value.trim();
    const ieltsScore = ieltsVal ? parseFloat(ieltsVal) : null;
    const priorityArea = document.getElementById("priority-area").value;
    const priorityEthnicity = document.getElementById("priority-ethnicity") ? document.getElementById("priority-ethnicity").value : "kinh";

    container.classList.remove("hidden");
    const searchingText = keyword ? `trường mơ ước "${keyword}"` : `các trường phù hợp với sở thích "${userInterest}"`;
    container.innerHTML = `
        <div style="padding: 1.5rem; text-align: center; color: #0284c7;">
            <i class="fa-solid fa-spinner fa-spin" style="font-size: 1.8rem;"></i>
            <p style="margin-top: 0.5rem; font-weight: 600;">Hội đồng AI đang đối chiếu dữ liệu điểm và phân tích ${searchingText}...</p>
        </div>
    `;

    try {
        const res = await fetch("/api/evaluate-dream-major", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                keyword: keyword,
                user_interest: userInterest,
                exam_scores: examScores,
                transcript_scores: transcriptScores,
                ielts_score: ieltsScore,
                priority_area: priorityArea,
                ethnicity: priorityEthnicity
            })
        });

        const json = await res.json();
        if (json.status !== "success") {
            throw new Error(json.detail || "Không thể đánh giá trường mơ ước.");
        }

        const matches = json.data.matches || [];
        currentDreamMatches = matches;
        if (matches.length === 0) {
            container.innerHTML = `
                <div style="padding: 1.25rem; background: #ffffff; border-radius: 10px; border: 1px dashed #cbd5e1; text-align: center; color: #64748b;">
                    <i class="fa-solid fa-circle-question text-warning" style="font-size: 1.5rem; margin-bottom: 0.5rem;"></i>
                    <p>Không tìm thấy trường hoặc ngành đào tạo phù hợp với từ khóa <strong>"${keyword || userInterest}"</strong>.</p>
                    <p style="font-size: 0.82rem; margin-top: 0.25rem;">Gợi ý: Thử tìm theo mã trường viết tắt (<strong>BKHN, NEU, UIT, FTU, HCMUT</strong>...) hoặc tên ngành tổng quát (<strong>Kỹ thuật phần mềm, Y Đa khoa, Logistics</strong>...).</p>
                </div>
            `;
            return;
        }

        let html = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <span style="font-size: 0.9rem; font-weight: 700; color: #0369a1;">
                    <i class="fa-solid fa-list-check"></i> Tìm thấy ${matches.length} kết quả phù hợp cho "${keyword || userInterest}":
                </span>
                <button type="button" class="btn-toggle-details" onclick="document.getElementById('dream-results-container').classList.add('hidden')" style="font-size: 0.78rem;">
                    <i class="fa-solid fa-xmark"></i> Thu gọn
                </button>
            </div>
            ${userInterest ? `
                <div class="dream-interest-hint mb-3">
                    <i class="fa-solid fa-wand-magic-sparkles text-primary"></i> Đã ưu tiên xếp các ngành khớp với sở thích nghề nghiệp bạn mô tả: "<strong>${userInterest}</strong>" lên đầu tiên.
                </div>
            ` : ''}
        `;

        matches.forEach((item, idx) => {
            let roleClass = "role-target";
            let badgeClass = "prob-target";
            if (item.pass_probability >= 90) {
                roleClass = "role-safety";
                badgeClass = "prob-safety";
            } else if (item.pass_probability < 60) {
                roleClass = "role-reach";
                badgeClass = "prob-reach";
            }

            const cg = item.career_guidance || {};
            const sb = cg.skill_sandbox || {};
            const isFav = isInWishlist(item.university_code, item.major_name);

            html += `
                <div class="dream-result-card ${item.is_interest_match ? 'dream-matched-border' : ''}">
                    <div class="roadmap-main-row">
                        <div class="roadmap-left">
                            <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                                <span class="dream-card-badge"><i class="fa-solid fa-star text-warning"></i> TRƯỜNG MƠ ƯỚC #${idx + 1}</span>
                                ${item.is_interest_match ? `<span class="dream-matched-badge"><i class="fa-solid fa-sparkles"></i> Ưu tiên theo sở thích của bạn</span>` : ''}
                            </div>
                            <div class="roadmap-title-area" style="margin-top: 0.25rem;">
                                <div class="roadmap-tags-row">
                                    <span class="roadmap-role-tag ${roleClass}">${item.strategy_role}</span>
                                    <span class="roadmap-tuition-tag"><i class="fa-solid fa-layer-group"></i> ${item.major_category}</span>
                                </div>
                                <div class="roadmap-major-row">
                                    <span class="roadmap-major">${item.major_name} (${item.combination_code})</span>
                                    <span class="program-type-badge ${item.program_type && (item.program_type.includes('CLC') || item.program_type.includes('Chất lượng')) ? 'badge-clc' : (item.program_type && item.program_type.includes('Quốc tế')) ? 'badge-intl' : 'badge-standard'}">
                                        <i class="fa-solid fa-graduation-cap"></i> ${item.program_type || 'Hệ Chuẩn (Đại trà)'}
                                    </span>
                                </div>
                                <div class="roadmap-uni-row">
                                    <span class="roadmap-uni"><i class="fa-solid fa-building-columns"></i> <strong>${item.university_name} (${item.university_code})</strong> • ${item.region} • ${item.province || ''}</span>
                                    <span class="uni-tuition-pill ${item.is_tuition_alert ? 'tuition-alert' : 'tuition-normal'}">
                                        <i class="fa-solid fa-coins"></i> Học phí: <strong>~${item.tuition_range || 'Chưa công bố'} tr/năm</strong>
                                    </span>
                                    ${item.is_tuition_alert ? `
                                        <span class="tuition-alert-badge" title="${item.tuition_alert_msg}">
                                            <i class="fa-solid fa-triangle-exclamation"></i> ${item.tuition_alert_msg}
                                        </span>
                                    ` : ''}
                                </div>
                            </div>
                        </div>
                        <div class="roadmap-right">
                            <div>
                                <div style="font-size: 0.8rem; color: #64748b;">Điểm chuẩn 2025: <strong>${item.score_2025}đ</strong> (2024: ${item.score_2024}đ | 2023: ${item.score_2023}đ)</div>
                                <div style="font-size: 0.8rem;">Điểm bạn: <strong style="color: var(--primary);">${item.candidate_score}đ</strong> (${item.score_delta >= 0 ? '+' : ''}${item.score_delta}đ)</div>
                            </div>
                            <span class="prob-badge ${badgeClass}"><i class="fa-solid fa-chart-pie"></i> ${item.pass_probability}% Đỗ</span>
                            <div style="display: flex; gap: 0.4rem; align-items: center;">
                                <button type="button" class="btn-toggle-wishlist ${isFav ? 'active' : ''}" id="btn-dream-wishlist-${idx}" onclick="toggleWishlistItemFromDream(${idx})">
                                    <i class="fa-${isFav ? 'solid' : 'regular'} fa-bookmark"></i> <span>${isFav ? 'Đã lưu' : 'Lưu NV'}</span>
                                </button>
                                <button type="button" class="btn-toggle-details" onclick="toggleDreamDetails(${idx})">
                                    <i class="fa-solid fa-circle-info"></i> <span id="toggle-dream-text-${idx}">Chi tiết & Sandbox</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Lời khuyên chiến lược từ AI -->
                    <div class="dream-strategic-advice">
                        <i class="fa-solid fa-lightbulb text-warning"></i> <strong>Lời khuyên chiến lược từ AI:</strong> ${item.strategic_advice}
                    </div>

                    <!-- Chi tiết nghề nghiệp & Skill Sandbox -->
                    <div id="dream-details-${idx}" class="roadmap-details" style="display: none;">
                        <!-- Nút Thao Tác Nhanh (Tính ROI & So Sánh) -->
                        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap;">
                            <button type="button" class="btn-secondary" style="font-size: 0.78rem; padding: 0.4rem 0.65rem;" onclick="openRoiForMajor('${item.university_code}', '${encodeURIComponent(item.major_name)}')">
                                <i class="fa-solid fa-calculator" style="color: #10b981;"></i> Tính ROI trường này
                            </button>
                            <button type="button" class="btn-secondary" style="font-size: 0.78rem; padding: 0.4rem 0.65rem;" onclick="openCompareWithMajor('${encodeURIComponent(item.major_name)}')">
                                <i class="fa-solid fa-code-compare" style="color: #6366f1;"></i> So sánh đối đầu
                            </button>
                        </div>
                        ${cg.entry_roles ? `
                            <div class="career-guidance-card">
                                <div class="career-roles-section">
                                    <span class="career-section-label"><i class="fa-solid fa-briefcase"></i> Vị trí việc làm tiêu biểu:</span>
                                    <div class="career-role-chips">
                                        ${(cg.entry_roles || []).map(r => `<span class="career-role-chip">${r}</span>`).join('')}
                                    </div>
                                    <p style="font-size: 0.8rem; color: #475569; margin-top: 0.35rem;">
                                        <strong>Công việc hàng ngày:</strong> ${cg.daily_work || ''}
                                    </p>
                                </div>

                                <div class="career-roles-section">
                                    <span class="career-section-label"><i class="fa-solid fa-chart-line"></i> Mức thu nhập thị trường:</span>
                                    <div class="salary-box">
                                        <span>Mới ra trường (Fresher):</span>
                                        <span class="salary-val">${cg.starting_salary || '8 - 12 tr/tháng'}</span>
                                    </div>
                                    <div class="salary-box" style="margin-top: 0.35rem;">
                                        <span>3 - 5 năm kinh nghiệm:</span>
                                        <span class="salary-val">${cg.mid_salary || '15 - 25 tr/tháng'}</span>
                                    </div>
                                    <p style="font-size: 0.78rem; color: #64748b; margin-top: 0.35rem;">
                                        <i class="fa-solid fa-globe"></i> ${cg.labor_market_outlook || ''}
                                    </p>
                                </div>

                                <div class="skill-sandbox-box">
                                    <div class="skill-sandbox-title">
                                        <i class="fa-solid fa-flask-vial"></i> Skill Sandbox: Thử Thách Trải Nghiệm Năng Lực
                                    </div>
                                    <div class="sandbox-task">
                                        <strong><i class="fa-solid fa-stopwatch"></i> Nhiệm vụ thử nghiệm (30 - 45 phút):</strong> ${sb.tryout_task || 'Tìm hiểu dự án thực tế về ngành.'}
                                    </div>
                                    <div style="font-size: 0.8rem; font-weight: 700; color: #1e293b; margin: 0.5rem 0 0.35rem 0;">
                                        <i class="fa-solid fa-circle-check" style="color: #10b981;"></i> Dấu hiệu bạn thực sự phù hợp với ngành (Tự suy xét):
                                    </div>
                                    <ul class="sandbox-criteria-list">
                                        ${(sb.self_assessment_criteria || []).map(c => `<li>${c}</li>`).join('')}
                                    </ul>
                                    ${sb.self_assessment ? `
                                        <div style="font-size: 0.78rem; color: #3730a3; background: #eef2ff; border-left: 3px solid #6366f1; border-radius: 4px; padding: 0.45rem 0.65rem; margin-top: 0.45rem;">
                                            <i class="fa-solid fa-lightbulb" style="color: #f59e0b;"></i> ${sb.self_assessment}
                                        </div>
                                    ` : ''}
                                    ${sb.course_name ? `
                                        <div style="font-size: 0.78rem; color: #2563eb; margin-top: 0.45rem; font-weight: 500;">
                                            <i class="fa-solid fa-graduation-cap"></i> Khóa học/Tài liệu nhập môn gợi ý: <strong>${sb.course_name}</strong>
                                        </div>
                                    ` : ''}
                                    ${sb.link ? `
                                        <a href="${sb.link}" target="_blank" class="sandbox-course-link">
                                            <i class="fa-solid fa-arrow-up-right-from-square"></i> Truy cập khóa học: ${sb.intro_course_name || sb.course_name} (${sb.provider || 'Online'})
                                        </a>
                                    ` : ''}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;

    } catch (err) {
        container.innerHTML = `
            <div style="padding: 1rem; color: #ef4444; background: #fef2f2; border-radius: 8px;">
                <i class="fa-solid fa-triangle-exclamation"></i> Lỗi tra cứu trường mơ ước: ${err.message}
            </div>
        `;
    }
}

function toggleDreamDetails(idx) {
    const el = document.getElementById(`dream-details-${idx}`);
    const btnText = document.getElementById(`toggle-dream-text-${idx}`);
    if (!el) return;
    if (el.style.display === "none" || el.style.display === "") {
        el.style.display = "flex";
        if (btnText) btnText.textContent = "Thu gọn chi tiết";
    } else {
        el.style.display = "none";
        if (btnText) btnText.textContent = "Chi tiết nghề & Sandbox";
    }
}

// ==========================================================================
// WHAT-IF ANALYSIS SIMULATOR LOGIC
// ==========================================================================
let currentWhatIfDeltas = { "Toán": 0, "Tiếng Anh": 0 };
let currentWhatIfIelts = null;
let baselineOriginalScores = {};

function adjustSubjectDelta(subject, delta) {
    if (!currentConsultResult || !currentConsultResult.final_report) {
        alert("Vui lòng bấm 'Nhận Tư Vấn Chiến Lược Nguyện Vọng Ngay' trước để có danh sách nguyện vọng gốc!");
        return;
    }

    // Initialize baseline if not set
    if (baselineOriginalScores["Toán"] === undefined) {
        baselineOriginalScores["Toán"] = parseFloat(document.getElementById("score-toan")?.value) || 0;
    }
    if (baselineOriginalScores["Tiếng Anh"] === undefined) {
        baselineOriginalScores["Tiếng Anh"] = parseFloat(document.getElementById("score-anh")?.value) || 0;
    }
    if (baselineOriginalScores["ielts"] === undefined) {
        baselineOriginalScores["ielts"] = document.getElementById("ielts-score")?.value || "";
    }

    const key = subject;
    // Toggle if already selected
    if (currentWhatIfDeltas[key] === delta) {
        currentWhatIfDeltas[key] = 0;
    } else {
        currentWhatIfDeltas[key] = delta;
    }

    // Update active UI classes for buttons
    const subjSlug = subject === "Toán" ? "toan" : "anh";
    ["05", "10", "15"].forEach(val => {
        const btn = document.getElementById(`btn-step-${subjSlug}-${val}`);
        if (btn) btn.classList.remove("active");
    });

    const activeVal = currentWhatIfDeltas[key];
    if (activeVal === 0.5) document.getElementById(`btn-step-${subjSlug}-05`)?.classList.add("active");
    if (activeVal === 1.0) document.getElementById(`btn-step-${subjSlug}-10`)?.classList.add("active");
    if (activeVal === 1.5) document.getElementById(`btn-step-${subjSlug}-15`)?.classList.add("active");

    // Sync into main score inputs
    if (subject === "Toán") {
        const input = document.getElementById("score-toan");
        if (input) {
            const newScore = Math.min(10.0, baselineOriginalScores["Toán"] + currentWhatIfDeltas["Toán"]);
            input.value = newScore.toFixed(1);
        }
    } else if (subject === "Tiếng Anh") {
        const input = document.getElementById("score-anh");
        if (input) {
            const newScore = Math.min(10.0, baselineOriginalScores["Tiếng Anh"] + currentWhatIfDeltas["Tiếng Anh"]);
            input.value = newScore.toFixed(1);
        }
    }

    applyWhatIfSimulation();
}

function adjustIeltsWhatIf(val) {
    if (!currentConsultResult || !currentConsultResult.final_report) {
        alert("Vui lòng bấm 'Nhận Tư Vấn Chiến Lược Nguyện Vọng Ngay' trước để có danh sách nguyện vọng gốc!");
        const el = document.getElementById("whatif-ielts");
        if (el) el.value = "";
        return;
    }

    if (baselineOriginalScores["ielts"] === undefined) {
        baselineOriginalScores["ielts"] = document.getElementById("ielts-score")?.value || "";
    }

    currentWhatIfIelts = val ? parseFloat(val) : null;

    // Sync into main IELTS input
    const ieltsInput = document.getElementById("ielts-score");
    if (ieltsInput) {
        if (val) {
            ieltsInput.value = val;
        } else {
            ieltsInput.value = baselineOriginalScores["ielts"] || "";
        }
    }

    applyWhatIfSimulation();
}

function resetWhatIf() {
    currentWhatIfDeltas = { "Toán": 0, "Tiếng Anh": 0 };
    currentWhatIfIelts = null;

    ["toan", "anh"].forEach(subjSlug => {
        ["05", "10", "15"].forEach(val => {
            const btn = document.getElementById(`btn-step-${subjSlug}-${val}`);
            if (btn) btn.classList.remove("active");
        });
    });

    const ieltsSel = document.getElementById("whatif-ielts");
    if (ieltsSel) ieltsSel.value = "";

    const banner = document.getElementById("whatif-live-banner");
    if (banner) banner.style.display = "none";

    const breakdownBox = document.getElementById("whatif-impact-breakdown");
    if (breakdownBox) breakdownBox.style.display = "none";

    // Restore original scores to main inputs
    if (baselineOriginalScores["Toán"] !== undefined) {
        const toanInput = document.getElementById("score-toan");
        if (toanInput) toanInput.value = baselineOriginalScores["Toán"].toFixed(1);
    }
    if (baselineOriginalScores["Tiếng Anh"] !== undefined) {
        const anhInput = document.getElementById("score-anh");
        if (anhInput) anhInput.value = baselineOriginalScores["Tiếng Anh"].toFixed(1);
    }
    if (baselineOriginalScores["ielts"] !== undefined) {
        const ieltsInput = document.getElementById("ielts-score");
        if (ieltsInput) ieltsInput.value = baselineOriginalScores["ielts"];
    }

    if (currentConsultResult && currentConsultResult.final_report) {
        // Restore original roadmap
        renderRoadmap(currentConsultResult.final_report.top_recommendations || []);
        document.getElementById("count-safety").textContent = `${(currentConsultResult.safety_majors || []).length} ngành`;
        document.getElementById("count-target").textContent = `${(currentConsultResult.target_majors || []).length} ngành`;
        document.getElementById("count-reach").textContent = `${(currentConsultResult.reach_majors || []).length} ngành`;
    }
}

async function applyWhatIfSimulation() {
    if (!currentConsultResult || !currentConsultResult.final_report) return;

    const hasAnyDelta = Object.values(currentWhatIfDeltas).some(d => d > 0) || currentWhatIfIelts !== null;
    if (!hasAnyDelta) {
        resetWhatIf();
        return;
    }

    // Build baseScores using baseline original scores for Toán and Tiếng Anh to avoid double-counting
    const baseScores = {};
    ALL_SUBJECTS.forEach(s => {
        const chk = document.getElementById(`chk-${s}`);
        if (chk && chk.checked) {
            const info = SUBJECT_INFO[s];
            let val;
            if (info.name === "Toán" && baselineOriginalScores["Toán"] !== undefined) {
                val = baselineOriginalScores["Toán"];
            } else if (info.name === "Tiếng Anh" && baselineOriginalScores["Tiếng Anh"] !== undefined) {
                val = baselineOriginalScores["Tiếng Anh"];
            } else {
                val = parseFloat(document.getElementById(info.inputId).value);
            }
            baseScores[info.name] = !isNaN(val) ? val : 0;
        }
    });

    const origRecs = currentConsultResult.final_report.top_recommendations || [];
    const banner = document.getElementById("whatif-live-banner");
    const bannerText = document.getElementById("whatif-banner-text");

    try {
        const payload = {
            baseline_scores: baseScores,
            delta_scores: currentWhatIfDeltas,
            ielts_score: currentWhatIfIelts,
            priority_area: document.getElementById("priority-area")?.value || "KV3",
            ethnicity: document.getElementById("priority-ethnicity")?.value || "kinh",
            current_recommendations: origRecs
        };

        const res = await fetch("/api/simulate-what-if", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const json = await res.json();
        if (json.status === "success") {
            const data = json.data;
            // Update Roadmap cards
            renderRoadmap(data.simulated_recommendations);

            // Update Counter badges
            document.getElementById("count-safety").textContent = `${data.summary_after.safety} ngành`;
            document.getElementById("count-target").textContent = `${data.summary_after.target} ngành`;
            document.getElementById("count-reach").textContent = `${data.summary_after.reach} ngành`;

            // Display banner
            if (banner && bannerText) {
                const changes = [];
                if (currentWhatIfDeltas["Toán"] > 0) changes.push(`Toán +${currentWhatIfDeltas["Toán"]}đ`);
                if (currentWhatIfDeltas["Tiếng Anh"] > 0) changes.push(`Tiếng Anh +${currentWhatIfDeltas["Tiếng Anh"]}đ`);
                if (currentWhatIfIelts) changes.push(`IELTS ${currentWhatIfIelts}`);

                bannerText.innerHTML = `Giả định <strong>[${changes.join(", ")}]</strong>: Có <strong>${data.promoted_count}</strong> nguyện vọng nâng hạng! (An toàn: ${data.summary_after.safety}, Vừa sức: ${data.summary_after.target}, Thử thách: ${data.summary_after.reach})`;
                banner.style.display = "flex";
            }

            // Render detailed impact breakdown list
            const breakdownBox = document.getElementById("whatif-impact-breakdown");
            const breakdownList = document.getElementById("whatif-breakdown-list");
            if (breakdownBox && breakdownList) {
                breakdownList.innerHTML = "";
                (data.simulated_recommendations || []).forEach((item, idx) => {
                    const isPromoted = item.status_change && item.status_change !== "unchanged";
                    const itemCard = document.createElement("div");
                    itemCard.className = `whatif-item-card ${isPromoted ? 'promoted' : ''}`;

                    const diffSign = item.score_diff_from_baseline > 0 ? `+${item.score_diff_from_baseline}` : `${item.score_diff_from_baseline}`;
                    const probDiff = (item.pass_probability - item.old_pass_probability).toFixed(1);
                    const probDiffSign = probDiff >= 0 ? `+${probDiff}` : `${probDiff}`;

                    itemCard.innerHTML = `
                        <div class="whatif-item-header">
                            <span class="whatif-nv-tag">NV #${idx + 1}</span>
                            <strong>${escapeHtml(item.major_name)}</strong> - <span>${escapeHtml(item.university_name)} (${escapeHtml(item.university_code)})</span>
                            <span class="score-badge" style="background: #e0e7ff; color: #4338ca; font-size: 0.75rem;">${escapeHtml(item.combination_code)}</span>
                        </div>
                        <div class="whatif-item-metrics">
                            <span class="whatif-metric-badge">
                                Điểm xét tuyển: <strong>${item.old_candidate_score}đ</strong> ➔ <strong style="color: #15803d;">${item.candidate_score}đ</strong>
                                <span class="whatif-gain-tag">${diffSign}đ</span>
                            </span>
                            <span class="whatif-metric-badge">
                                Điểm chuẩn 2025: <strong>${item.score_2025}đ</strong>
                                (Độ lệch: ${item.old_score_delta >= 0 ? '+' : ''}${item.old_score_delta}đ ➔ <strong style="color: #15803d;">${item.score_delta >= 0 ? '+' : ''}${item.score_delta}đ</strong>)
                            </span>
                            <span class="whatif-metric-badge">
                                Xác suất đỗ: <strong>${item.old_pass_probability}%</strong> ➔ <strong style="color: #15803d;">${item.pass_probability}%</strong>
                                <span class="whatif-gain-tag">${probDiffSign}%</span>
                            </span>
                            <span class="whatif-metric-badge">
                                Phân loại: <em>${escapeHtml(item.old_strategy_role)}</em> ➔ <strong style="color: #1d4ed8;">${escapeHtml(item.strategy_role)}</strong>
                            </span>
                        </div>
                        <p class="whatif-item-desc">${formatMarkdown(item.change_description || '')}</p>
                    `;
                    breakdownList.appendChild(itemCard);
                });
                breakdownBox.style.display = "block";
            }
        }
    } catch (err) {
        console.error("What-if error:", err);
    }
}

// ==========================================================================
// FOLLOW-UP AI CHATBOT LOGIC
// ==========================================================================
function toggleChatbot() {
    const win = document.getElementById("chatbot-window");
    if (!win) return;
    win.classList.toggle("hidden");
    if (!win.classList.contains("hidden")) {
        document.getElementById("chatbot-input")?.focus();
    }
}

function handleChatKeydown(e) {
    if (e.key === "Enter") {
        e.preventDefault();
        sendChatMessage();
    }
}

function askFollowupQuestion(text) {
    const input = document.getElementById("chatbot-input");
    if (input) {
        input.value = text;
        sendChatMessage();
    }
}

function buildChatContext() {
    const examScores = {};
    ALL_SUBJECTS.forEach(s => {
        const chk = document.getElementById(`chk-${s}`);
        if (chk && chk.checked) {
            const info = SUBJECT_INFO[s];
            const val = parseFloat(document.getElementById(info.inputId).value);
            examScores[info.name] = !isNaN(val) ? val : 0;
        }
    });

    const profile = {
        scores: examScores,
        holland_code: document.getElementById("metric-holland-code")?.textContent || "RIA",
        interest: document.getElementById("user-interest")?.value || "",
        priority_area: document.getElementById("priority-area")?.value || "KV3",
        ethnicity: document.getElementById("priority-ethnicity")?.value || "kinh",
        ielts_score: parseFloat(document.getElementById("ielts-score")?.value) || null
    };

    const recs = currentConsultResult && currentConsultResult.final_report 
        ? (currentConsultResult.final_report.top_recommendations || [])
        : [];

    return {
        candidate_profile: profile,
        recommendations: recs
    };
}

async function sendChatMessage() {
    const input = document.getElementById("chatbot-input");
    const text = input ? input.value.trim() : "";
    if (!text) return;

    input.value = "";
    const msgContainer = document.getElementById("chatbot-messages");
    if (!msgContainer) return;

    // 1. Render User message
    const userMsgEl = document.createElement("div");
    userMsgEl.className = "chat-msg user-msg";
    userMsgEl.innerHTML = `<div class="msg-bubble">${escapeHtml(text)}</div>`;
    msgContainer.appendChild(userMsgEl);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    // 2. Render Loading indicator
    const loadingEl = document.createElement("div");
    loadingEl.className = "chat-msg bot-msg";
    loadingEl.id = "chat-loading-msg";
    loadingEl.innerHTML = `<div class="msg-bubble"><i class="fa-solid fa-spinner fa-spin"></i> Cố vấn AI đang phân tích dữ liệu...</div>`;
    msgContainer.appendChild(loadingEl);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    try {
        const context = buildChatContext();
        const res = await fetch("/api/chat-followup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, consultation_context: context })
        });

        const json = await res.json();
        loadingEl.remove();

        if (json.status === "success") {
            const botMsgEl = document.createElement("div");
            botMsgEl.className = "chat-msg bot-msg";
            botMsgEl.innerHTML = `<div class="msg-bubble">${formatMarkdown(json.data.reply)}</div>`;
            msgContainer.appendChild(botMsgEl);
        } else {
            const errEl = document.createElement("div");
            errEl.className = "chat-msg bot-msg";
            errEl.innerHTML = `<div class="msg-bubble" style="color: #ef4444;">Xin lỗi, đã xảy ra sự cố khi xử lý câu hỏi. Vui lòng thử lại!</div>`;
            msgContainer.appendChild(errEl);
        }
        msgContainer.scrollTop = msgContainer.scrollHeight;
    } catch (err) {
        if (loadingEl) loadingEl.remove();
        console.error("Chat error:", err);
        const errEl = document.createElement("div");
        errEl.className = "chat-msg bot-msg";
        errEl.innerHTML = `<div class="msg-bubble" style="color: #ef4444;">Không thể kết nối đến máy chủ AI. Vui lòng kiểm tra kết nối mạng!</div>`;
        msgContainer.appendChild(errEl);
        msgContainer.scrollTop = msgContainer.scrollHeight;
    }
}

// ==========================================================================
// 6 ADVANCED CAREER ORIENTATION MODULES
// ==========================================================================

// --- Common Modal Management ---
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add("hidden");
    }
}

// --- MODULE 1: MINI CASE STUDY INTERACTION ---
function selectCaseStudyOption(cardIdx, optIdx) {
    if (!currentConsultResult || !currentConsultResult.final_report) return;
    const topRecs = currentConsultResult.final_report.top_recommendations || [];
    const item = topRecs[cardIdx];
    if (!item) return;

    const caseStudy = (item.career_guidance || {}).mini_case_study;
    if (!caseStudy) return;

    const firstQ = (caseStudy.questions && caseStudy.questions.length > 0) ? caseStudy.questions[0] : null;
    let analysis = "Tư duy nhạy bén và phản ứng linh hoạt là tố chất tuyệt vời để giải quyết tình huống nghề nghiệp này!";
    if (firstQ && firstQ.mindset_analysis) {
        analysis = firstQ.mindset_analysis;
    } else if (caseStudy.options && caseStudy.options[optIdx] && caseStudy.options[optIdx].analysis) {
        analysis = caseStudy.options[optIdx].analysis;
    }

    // Highlight selected button
    const container = document.getElementById(`roadmap-details-${cardIdx}`);
    if (container) {
        const btns = container.querySelectorAll(".case-study-btn");
        btns.forEach((b, i) => {
            if (i === optIdx) b.classList.add("selected");
            else b.classList.remove("selected");
        });
    }

    // Show feedback
    const feedbackEl = document.getElementById(`cs-feedback-${cardIdx}`);
    if (feedbackEl) {
        feedbackEl.innerHTML = `
            <div style="font-weight: 700; color: #065f46; margin-bottom: 0.25rem;"><i class="fa-solid fa-brain" style="color: #10b981;"></i> Phân tích tư duy xử lý của bạn:</div>
            <div style="color: #047857; font-size: 0.85rem; line-height: 1.45;">${analysis}</div>
        `;
        feedbackEl.style.display = "block";
    }
}

// ==========================================================================
// MODULE 0: PHÁ BỎ ẢO TƯỞNG NGHỀ NGHIỆP (REALITY CHECK & MỘT NGÀY LÀM NGHỀ)
// ==========================================================================
let cachedRealityProfiles = [];

async function loadRealityCheckProfiles() {
    if (cachedRealityProfiles.length === 0) {
        try {
            const res = await fetch("/api/reality-check-profiles");
            const json = await res.json();
            if (json.status === "success" && json.data) {
                cachedRealityProfiles = json.data;
            }
        } catch (e) {
            console.error("Error fetching reality check profiles:", e);
        }
    }
    const selectEl = document.getElementById("reality-check-select");
    if (selectEl && cachedRealityProfiles.length > 0) {
        selectEl.innerHTML = cachedRealityProfiles.map(p => `
            <option value="${p.code}">${p.title} (${p.code})</option>
        `).join("");
    }
}

async function openRealityCheckModal(prefCode = null) {
    const modal = document.getElementById("modal-reality-check");
    if (!modal) return;
    modal.classList.remove("hidden");

    if (cachedRealityProfiles.length === 0) {
        await loadRealityCheckProfiles();
    }

    const selectEl = document.getElementById("reality-check-select");
    if (selectEl && cachedRealityProfiles.length > 0) {
        const codeToSelect = prefCode || selectEl.value || cachedRealityProfiles[0].code;
        selectEl.value = codeToSelect;
        onRealityCheckChange(codeToSelect);
    }
}

function onRealityCheckChange(code) {
    const container = document.getElementById("reality-check-content");
    if (!container) return;

    const p = cachedRealityProfiles.find(item => item.code === code);
    if (!p) {
        container.innerHTML = `<div class="alert alert-warning">Không tìm thấy dữ liệu cho ngành này.</div>`;
        return;
    }

    // 1. Work distribution
    const workDistItems = Array.isArray(p.work_distribution) ? p.work_distribution : [];
    let workDistHtml = "";
    if (workDistItems.length > 0) {
        const segBars = workDistItems.map((item, i) => 
            `<div class="work-dist-seg seg-${i % 4}" style="width: ${item.percent}%;" title="${item.task}: ${item.percent}%"></div>`
        ).join("");
        const legendItems = workDistItems.map((item, i) => `
            <div class="legend-item">
                <span class="legend-color-dot seg-${i % 4}"></span>
                <span>${item.task} (<strong>${item.percent}%</strong>)</span>
            </div>
        `).join("");
        workDistHtml = `
            <div class="work-dist-bar-wrap mb-3">
                <div style="font-size: 0.9rem; font-weight: 700; color: #1e293b; margin-bottom: 0.4rem;">
                    <i class="fa-solid fa-chart-pie text-primary"></i> Phân rã thời gian làm việc thực tế:
                </div>
                <div class="work-dist-bar">${segBars}</div>
                <div class="work-dist-legend">${legendItems}</div>
            </div>
        `;
    }

    // 2. Pressure & challenges
    const challenges = Array.isArray(p.pressure_challenges) ? p.pressure_challenges : [];
    let pressureHtml = "";
    if (challenges.length > 0) {
        pressureHtml = `
            <div class="reality-pressure-box mb-3">
                <div style="font-size: 0.9rem; font-weight: 700; color: #b45309; margin-bottom: 0.4rem;">
                    <i class="fa-solid fa-triangle-exclamation text-warning"></i> Mặt trái & Thách thức áp lực đặc thù của nghề:
                </div>
                <ul class="pressure-list">
                    ${challenges.map(c => `<li><i class="fa-solid fa-circle-exclamation text-danger" style="margin-right: 0.35rem;"></i> ${c}</li>`).join("")}
                </ul>
            </div>
        `;
    }

    // 3. Mini Case Study
    const cs = p.mini_case_study || {};
    let caseStudyHtml = "";
    if (cs.scenario) {
        const firstQ = (cs.questions && cs.questions.length > 0) ? cs.questions[0] : null;
        const qText = firstQ ? firstQ.q : "Hành động đầu tiên bạn sẽ xử lý là gì?";
        const options = firstQ ? (firstQ.options || []) : [];
        const optBtns = options.map((opt, optIdx) => {
            const optText = typeof opt === "string" ? opt : (opt.text || JSON.stringify(opt));
            return `
                <button type="button" class="case-study-btn" id="standalone-cs-opt-${optIdx}" onclick="selectStandaloneCaseStudyOption(${optIdx})">
                    <span class="opt-label">${String.fromCharCode(65 + optIdx)}.</span> ${optText}
                </button>
            `;
        }).join("");

        caseStudyHtml = `
            <div class="case-study-box mb-3">
                <div style="font-size: 0.95rem; font-weight: 700; color: #15803d; display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.4rem;">
                    <i class="fa-solid fa-lightbulb text-warning"></i> Mini Case-Study: Tình Huống Công Việc Thực Tế
                </div>
                <div class="case-study-scenario">${cs.scenario}</div>
                <div class="case-study-question" style="font-size: 0.88rem; font-weight: 700; color: #1e293b; margin: 0.6rem 0 0.4rem 0;">
                    <strong>Câu hỏi tình huống:</strong> ${qText}
                </div>
                <div class="case-study-options">${optBtns}</div>
                <div id="standalone-cs-feedback" class="case-study-feedback" style="display: none;"></div>
            </div>
        `;
    }

    // 4. AI Impact
    const ai = p.ai_impact || {};
    const aiRisk = ai.automation_risk_percent !== undefined ? ai.automation_risk_percent : 20;
    const riskClass = aiRisk < 25 ? 'ai-risk-low' : (aiRisk < 50 ? 'ai-risk-med' : 'ai-risk-high');

    container.innerHTML = `
        <div class="reality-check-card">
            <!-- Header Banner -->
            <div class="reality-banner">
                <div class="reality-title-wrap">
                    <span class="badge-tag"><i class="fa-solid fa-masks-theater"></i> THỰC TẾ NGHỀ NGHIỆP</span>
                    <h3 class="reality-title">${p.title}</h3>
                    <p class="reality-daily"><strong>Một ngày làm việc thực tế:</strong> ${p.daily_work || ''}</p>
                </div>
                <div class="reality-metrics-row">
                    <div class="metric-pill">
                        <span class="lbl"><i class="fa-solid fa-coins text-warning"></i> Lương Fresher</span>
                        <strong class="val text-success">${p.starting_salary || '10 - 15 tr/tháng'}</strong>
                    </div>
                    <div class="metric-pill">
                        <span class="lbl"><i class="fa-solid fa-chart-line text-primary"></i> Sau 3–5 Năm</span>
                        <strong class="val text-indigo">${p.mid_salary || '22 - 40 tr/tháng'}</strong>
                    </div>
                    <div class="metric-pill">
                        <span class="lbl"><i class="fa-solid fa-robot text-danger"></i> Rủi Ro Tự Động Hóa AI</span>
                        <strong class="val ${riskClass}">${aiRisk}% (${ai.risk_level || 'Thấp'})</strong>
                    </div>
                </div>
            </div>

            <!-- 2-col content: Distribution & Challenges -->
            <div class="reality-grid-2col">
                <div class="reality-col-left">
                    ${workDistHtml}
                    ${pressureHtml}
                </div>
                <div class="reality-col-right">
                    ${caseStudyHtml}

                    <!-- AI & National Priority Box -->
                    <div class="ai-priority-card">
                        <div style="font-size: 0.85rem; font-weight: 700; color: #1e293b; margin-bottom: 0.35rem;">
                            <i class="fa-solid fa-brain text-primary"></i> Kỹ Năng Tương Hỗ AI & Quy Hoạch Quốc Gia:
                        </div>
                        ${ai.national_priority ? `
                            <div class="national-priority-badge mb-2">
                                <i class="fa-solid fa-medal text-warning"></i> <strong>Định hướng Quốc gia:</strong> ${ai.national_priority}
                            </div>
                        ` : ''}
                        ${(ai.ai_augmented_skills || []).length > 0 ? `
                            <ul class="ai-skills-list">
                                ${ai.ai_augmented_skills.map(s => `<li><i class="fa-solid fa-check text-success"></i> ${s}</li>`).join('')}
                            </ul>
                        ` : ''}
                    </div>
                </div>
            </div>

            <!-- Footer Action Buttons -->
            <div class="reality-footer-actions">
                <button type="button" class="btn-primary" onclick="closeModal('modal-reality-check'); openReverseCareerModal();">
                    <i class="fa-solid fa-sitemap"></i> Xem Cây Kỹ Năng 4 Năm Của Nghề Này
                </button>
                <button type="button" class="btn-secondary" onclick="closeModal('modal-reality-check'); openRoiCalculatorModal();">
                    <i class="fa-solid fa-calculator text-success"></i> Tính Học Phí & Hoàn Vốn (ROI)
                </button>
            </div>
        </div>
    `;
}

function selectStandaloneCaseStudyOption(optIdx) {
    const sel = document.getElementById("reality-check-select");
    if (!sel || !sel.value) return;
    const p = cachedRealityProfiles.find(item => item.code === sel.value);
    if (!p || !p.mini_case_study) return;

    const cs = p.mini_case_study;
    const firstQ = (cs.questions && cs.questions.length > 0) ? cs.questions[0] : null;
    const analysis = firstQ && firstQ.mindset_analysis ? firstQ.mindset_analysis : "Tư duy nhạy bén và bản lĩnh dám đối diện thách thức là nền tảng cốt lõi của ngành nghề này!";

    const container = document.getElementById("reality-check-content");
    if (container) {
        const btns = container.querySelectorAll(".case-study-btn");
        btns.forEach((b, i) => {
            if (i === optIdx) b.classList.add("selected");
            else b.classList.remove("selected");
        });
    }

    const feedbackEl = document.getElementById("standalone-cs-feedback");
    if (feedbackEl) {
        feedbackEl.innerHTML = `
            <div style="font-weight: 700; color: #065f46; margin-bottom: 0.25rem;">
                <i class="fa-solid fa-brain text-success"></i> Phân tích xu hướng tư duy của bạn:
            </div>
            <div style="color: #047857; font-size: 0.88rem; line-height: 1.45;">${analysis}</div>
        `;
        feedbackEl.style.display = "block";
    }
}

// ==========================================================================
// MODULE AI IMPACT & QUY HOẠCH LAO ĐỘNG QUỐC GIA 5-10 NĂM TỚI
// ==========================================================================
async function openAiImpactModal(prefCode = null) {
    const modal = document.getElementById("modal-ai-impact");
    if (!modal) return;
    modal.classList.remove("hidden");

    if (cachedRealityProfiles.length === 0) {
        await loadRealityCheckProfiles();
    }

    const sel = document.getElementById("ai-impact-select");
    if (sel && cachedRealityProfiles.length > 0) {
        sel.innerHTML = cachedRealityProfiles.map(p => `
            <option value="${p.code}">${p.title} (${p.code})</option>
        `).join("");

        const codeToSelect = prefCode || sel.value || cachedRealityProfiles[0].code;
        sel.value = codeToSelect;
        onAiImpactChange(codeToSelect);
    }
}

function onAiImpactChange(code) {
    const container = document.getElementById("ai-impact-content");
    if (!container) return;

    const p = cachedRealityProfiles.find(item => item.code === code);
    if (!p) return;

    const ai = p.ai_impact || {};
    const aiRisk = ai.automation_risk_percent !== undefined ? ai.automation_risk_percent : 20;
    const riskClass = aiRisk < 25 ? 'ai-risk-low' : (aiRisk < 50 ? 'ai-risk-med' : 'ai-risk-high');

    container.innerHTML = `
        <div class="ai-impact-overview">
            <div class="ai-risk-hero-card">
                <div class="ai-risk-header">
                    <div>
                        <span class="ai-risk-tag"><i class="fa-solid fa-robot"></i> ĐÁNH GIÁ TỰ ĐỘNG HÓA AI</span>
                        <h3>${p.title}</h3>
                    </div>
                    <div class="ai-risk-meter ${riskClass}">
                        <span class="risk-num">${aiRisk}%</span>
                        <span class="risk-lbl">${ai.risk_level || 'Thấp'}</span>
                    </div>
                </div>
                <p class="ai-risk-desc">
                    Mức độ các đầu việc lặp lại có thể bị AI/tự động hóa thay thế: <strong>${aiRisk}%</strong>.
                    ${aiRisk < 25 
                        ? 'Đây là ngành đòi hỏi tư duy trừu tượng, giải quyết vấn đề phức tạp và sáng tạo cao — AI đóng vai trò là trợ lý đắc lực nhân bội năng suất thay vì thay thế con người.' 
                        : (aiRisk < 50 
                            ? 'Các tác vụ nhập liệu, tổng hợp cơ bản đang được AI hóa nhanh chóng. Nhân sự cần trang bị thêm kỹ năng phân tích sâu và tương hỗ công nghệ để giữ vị thế cạnh tranh.' 
                            : 'Nguy cơ tự động hóa cao đối với các công việc lặp đi lặp lại. Bắt buộc người học phải làm chủ công nghệ và chuyển dịch lên các khâu chiến lược.')}
                </p>
            </div>

            <div class="ai-impact-grid mt-3">
                <div class="ai-skills-card">
                    <h5><i class="fa-solid fa-wand-magic-sparkles text-primary"></i> Kỹ Năng Tương Hỗ AI Cần Trang Bị (AI-Augmented Skills):</h5>
                    <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 0.5rem;">Để phối hợp hiệu quả với công nghệ và không bị đào thải trong 5–10 năm tới:</p>
                    <ul class="ai-skills-checklist">
                        ${(ai.ai_augmented_skills || []).map(s => `
                            <li><i class="fa-solid fa-circle-check text-success"></i> <span>${s}</span></li>
                        `).join('')}
                    </ul>
                </div>

                <div class="national-priority-card">
                    <h5><i class="fa-solid fa-flag-checkered text-warning"></i> Nhu Cầu Nhân Lực Theo Quy Hoạch Quốc Gia:</h5>
                    <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 0.5rem;">Cơ hội việc làm và các chính sách học bổng, ưu đãi đầu tư trọng điểm:</p>
                    <div class="priority-policy-box">
                        <i class="fa-solid fa-landmark text-primary"></i>
                        <strong>${ai.national_priority || 'Nằm trong quy hoạch phát triển nguồn nhân lực chất lượng cao quốc gia.'}</strong>
                    </div>
                    <div class="market-outlook-box mt-2">
                        <i class="fa-solid fa-briefcase text-info"></i>
                        <span>${p.labor_market_outlook || 'Nhu cầu nhân lực ổn định và tăng trưởng tích cực.'}</span>
                    </div>
                </div>
            </div>

            <div class="text-center mt-3">
                <button type="button" class="btn-primary" onclick="closeModal('modal-ai-impact'); openReverseCareerModal();">
                    <i class="fa-solid fa-sitemap"></i> Xem Cây Kỹ Năng & Lộ Trình 4 Năm Đại Học
                </button>
            </div>
        </div>
    `;
}

// --- MODULE 2: REVERSE CAREER MAPPING & SKILL TREE ---
let cachedTargetRoles = [];

async function loadReverseCareerRoles() {
    if (cachedTargetRoles.length === 0) {
        try {
            const res = await fetch("/api/target-roles");
            const json = await res.json();
            if (json.status === "success" && json.data) {
                cachedTargetRoles = json.data;
            }
        } catch (e) {
            console.error("Error fetching target roles:", e);
        }
    }
    const selectEl = document.getElementById("reverse-role-select");
    if (selectEl && cachedTargetRoles.length > 0) {
        selectEl.innerHTML = cachedTargetRoles.map(r => `
            <option value="${r.code}">${r.target_role || r.title} [Lương khởi điểm: ${r.starting_salary || r.salary_range}]</option>
        `).join("");
    }
}

async function openReverseCareerModal() {
    const modal = document.getElementById("modal-reverse-career");
    if (!modal) return;
    modal.classList.remove("hidden");

    const sel = document.getElementById("reverse-role-select");
    if (!sel) return;

    if (cachedTargetRoles.length === 0) {
        sel.innerHTML = `<option value="">-- Đang tải danh mục nghề nghiệp mục tiêu... --</option>`;
        await loadReverseCareerRoles();
    }

    if (cachedTargetRoles.length > 0) {
        if (!sel.value || sel.value === "") {
            sel.innerHTML = cachedTargetRoles.map(r => `
                <option value="${r.code}">${r.target_role || r.title} [Lương khởi điểm: ${r.starting_salary || r.salary_range}]</option>
            `).join("");
        }
        const currentCode = sel.value || cachedTargetRoles[0].code;
        onReverseRoleChange(currentCode);
    } else {
        sel.innerHTML = `<option value="">Không tải được danh mục nghề. Vui lòng thử lại.</option>`;
    }
}

async function onReverseRoleChange(roleCode) {
    const container = document.getElementById("reverse-role-details");
    if (!container || !roleCode) return;

    container.innerHTML = `
        <div style="padding: 2rem; text-align: center; color: #4338ca;">
            <i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem;"></i>
            <p style="margin-top: 0.6rem; font-weight: 600;">Hội đồng Chuyên gia đang lập sơ đồ cây kỹ năng & lộ trình 4 năm...</p>
        </div>
    `;

    try {
        let role = cachedTargetRoles.find(r => r.code === roleCode);
        if (!role || !role.skill_tree) {
            const res = await fetch(`/api/target-roles/${roleCode}`);
            const json = await res.json();
            if (json.status === "success") {
                role = json.data;
            }
        }

        if (!role) {
            container.innerHTML = `<div class="alert alert-warning">Không tìm thấy thông tin chi tiết nghề.</div>`;
            return;
        }

        const rcm = role.reverse_career_map || role;
        const skillTree = rcm.skill_tree || {};
        const unis = rcm.top_specialized_unis || [];
        const aiImpact = role.ai_impact || {};

        // Sơ đồ cây kỹ năng 3 giai đoạn (Năm 1-2, Năm 3, Năm 4)
        const y12Text = skillTree.year_1_2 || "Nền tảng Toán/Tin/Ngoại ngữ, Tư duy phản biện, Làm việc nhóm.";
        const y3Text = skillTree.year_3 || "Kiến thức chuyên ngành sâu, Chứng chỉ chuyên môn quốc tế, Dự án thực tế.";
        const y4Text = skillTree.year_4 || "Thực tập doanh nghiệp, Khóa luận tốt nghiệp, Chuyển đổi chính thức.";

        let unisHtml = "";
        if (unis.length > 0) {
            unisHtml = unis.map((u, i) => `
                <div class="specialized-uni-card">
                    <div class="specialized-uni-header">
                        <div class="specialized-uni-rank">#${i + 1}</div>
                        <div class="specialized-uni-title">
                            <strong>${u.name}</strong>
                            <span class="uni-code-tag">${u.code}</span>
                        </div>
                    </div>
                    <div class="specialized-uni-body">
                        <div class="uni-feature-item">
                            <span class="feature-label"><i class="fa-solid fa-flask-vial text-primary"></i> Khoa & Lab mũi nhọn:</span>
                            <span class="feature-val">${u.lab_strength || u.strength || 'Khoa đào tạo mũi nhọn với hệ thống phòng lab hiện đại.'}</span>
                        </div>
                        <div class="uni-feature-item">
                            <span class="feature-label"><i class="fa-solid fa-handshake text-success"></i> Mạng lưới doanh nghiệp:</span>
                            <span class="feature-val">${u.corporate_network || 'Liên kết sâu rộng với các tập đoàn công nghệ & doanh nghiệp đầu ngành.'}</span>
                        </div>
                    </div>
                    <div class="specialized-uni-footer">
                        <button type="button" class="btn-uni-action" onclick="closeModal('modal-reverse-career'); quickSearchDream('${u.code}');">
                            <i class="fa-solid fa-star text-warning"></i> Tra cứu trường này
                        </button>
                        <button type="button" class="btn-uni-action" onclick="openRoiForMajor('${u.code}', '${encodeURIComponent(rcm.target_role || role.title)}')">
                            <i class="fa-solid fa-calculator text-primary"></i> Tính học phí & ROI
                        </button>
                    </div>
                </div>
            `).join("");
        }

        container.innerHTML = `
            <div class="reverse-role-card">
                <!-- Chức danh mục tiêu Overview Banner -->
                <div class="reverse-overview-banner">
                    <div class="reverse-title-wrap">
                        <div class="reverse-role-badge"><i class="fa-solid fa-crosshairs"></i> VỊ TRÍ MỤC TIÊU</div>
                        <h3 class="reverse-role-name">${rcm.target_role || role.title}</h3>
                        <p class="reverse-role-desc">${role.daily_work || 'Đảm nhiệm các công tác chuyên môn cao, giải quyết các bài toán chiến lược của tổ chức.'}</p>
                    </div>
                    <div class="reverse-metrics-grid">
                        <div class="reverse-metric-box">
                            <span class="metric-lbl"><i class="fa-solid fa-coins text-warning"></i> Lương Khởi Điểm</span>
                            <strong class="metric-num text-success">${role.starting_salary || '10 - 15 tr/tháng'}</strong>
                        </div>
                        <div class="reverse-metric-box">
                            <span class="metric-lbl"><i class="fa-solid fa-chart-line text-primary"></i> Sau 3–5 Năm</span>
                            <strong class="metric-num text-indigo">${role.mid_salary || '25 - 45 tr/tháng'}</strong>
                        </div>
                        <div class="reverse-metric-box">
                            <span class="metric-lbl"><i class="fa-solid fa-briefcase text-info"></i> Tỷ Lệ Việc Làm</span>
                            <strong class="metric-num text-dark">${role.employment_rate || 98.0}%</strong>
                        </div>
                        <div class="reverse-metric-box">
                            <span class="metric-lbl"><i class="fa-solid fa-shield-virus text-danger"></i> Rủi Ro Tự Động Hóa AI</span>
                            <strong class="metric-num text-warning">${aiImpact.automation_risk_percent || 20}% (${aiImpact.risk_level || 'Thấp'})</strong>
                        </div>
                    </div>
                </div>

                <!-- Sơ đồ cây kỹ năng (Skill Tree) & Lộ trình 4 năm -->
                <div class="skill-tree-section">
                    <div class="section-title-wrap">
                        <h4><i class="fa-solid fa-sitemap text-primary"></i> Sơ Đồ Cây Kỹ Năng (Skill Tree) & Lộ Trình 4 Năm Đại Học</h4>
                        <p class="section-sub">Bản đồ hướng dẫn chính xác từng năm sinh viên cần tích lũy những kiến thức, kỹ năng mềm và chứng chỉ quốc tế gì:</p>
                    </div>

                    <div class="skill-tree-grid">
                        <!-- Stage 1: Năm 1 - 2 -->
                        <div class="skill-stage-card stage-year-1-2">
                            <div class="skill-stage-header">
                                <span class="stage-tag">GIAI ĐOẠN 1</span>
                                <h5>Năm 1 – 2: Xây Chắc Nền Tảng</h5>
                            </div>
                            <div class="skill-stage-body">
                                <div class="skill-group-title">
                                    <i class="fa-solid fa-square-root-variable text-primary"></i> Nền tảng Toán / Tin / Ngoại ngữ:
                                </div>
                                <div class="skill-text-content">${y12Text}</div>
                                
                                <div class="skill-group-title mt-3">
                                    <i class="fa-solid fa-people-group text-success"></i> Kỹ năng mềm cần tích lũy:
                                </div>
                                <ul class="skill-check-list">
                                    <li>Tư duy phản biện (Critical Thinking) & giải quyết vấn đề</li>
                                    <li>Kỹ năng tự học & đọc hiểu tài liệu chuyên ngành tiếng Anh</li>
                                    <li>Làm việc nhóm (Teamwork) theo phương pháp Agile/Scrum</li>
                                    <li>Quản lý thời gian và thiết lập mục tiêu cá nhân (OKRs)</li>
                                </ul>
                            </div>
                        </div>

                        <!-- Stage 2: Năm 3 -->
                        <div class="skill-stage-card stage-year-3">
                            <div class="skill-stage-header">
                                <span class="stage-tag stage-tag-warning">GIAI ĐOẠN 2</span>
                                <h5>Năm 3: Bứt Phá & Chứng Chỉ Quốc Tế</h5>
                            </div>
                            <div class="skill-stage-body">
                                <div class="skill-group-title">
                                    <i class="fa-solid fa-certificate text-warning"></i> Chứng chỉ chuyên môn quốc tế nên có:
                                </div>
                                <div class="skill-text-content">${y3Text}</div>

                                <div class="skill-group-title mt-3">
                                    <i class="fa-solid fa-laptop-code text-indigo"></i> Dự án thực chiến & Cuộc thi:
                                </div>
                                <ul class="skill-check-list">
                                    <li>Tham gia nghiên cứu khoa học cấp khoa / trường</li>
                                    <li>Xây dựng ít nhất 2 dự án thực tế đưa lên GitHub / Portfolio</li>
                                    <li>Thi đấu tại các cuộc thi chuyên môn (Hackathon, Olympic, Case Study)</li>
                                    <li>Đạt chuẩn ngoại ngữ đầu ra (IELTS 6.0 - 6.5+ hoặc tương đương)</li>
                                </ul>
                            </div>
                        </div>

                        <!-- Stage 3: Năm 4 -->
                        <div class="skill-stage-card stage-year-4">
                            <div class="skill-stage-header">
                                <span class="stage-tag stage-tag-success">GIAI ĐOẠN 3</span>
                                <h5>Năm 4: Đồ Án & Thực Tập Doanh Nghiệp</h5>
                            </div>
                            <div class="skill-stage-body">
                                <div class="skill-group-title">
                                    <i class="fa-solid fa-graduation-cap text-success"></i> Hướng đề tài tốt nghiệp & Tuyển dụng:
                                </div>
                                <div class="skill-text-content">${y4Text}</div>

                                <div class="skill-group-title mt-3">
                                    <i class="fa-solid fa-building text-info"></i> Lộ trình chuyển đổi Fresher:
                                </div>
                                <ul class="skill-check-list">
                                    <li>Thực tập sinh toàn thời gian (Internship) tại các đối tác lớn</li>
                                    <li>Chuyển tiếp lên vị trí Nhân viên chính thức (Fresher) trước khi nhận bằng</li>
                                    <li>Mở rộng mạng lưới quan hệ với các chuyên gia trong ngành (Networking)</li>
                                    <li>Đồ án tốt nghiệp giải quyết bài toán thực tiễn của doanh nghiệp</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Xếp Hạng Trường Đại Học Theo Thế Mạnh Chuyên Sâu -->
                <div class="specialized-unis-section mt-4">
                    <div class="section-title-wrap">
                        <h4><i class="fa-solid fa-ranking-star text-warning"></i> Xếp Hạng Trường Theo Thế Mạnh Chuyên Sâu</h4>
                        <p class="section-sub">
                            Gợi ý các trường đại học hàng đầu có mạng lưới doanh nghiệp và khoa/lab đào tạo mũi nhọn về vị trí <strong>${rcm.target_role || role.title}</strong> thay vì chỉ nhìn vào danh tiếng chung:
                        </p>
                    </div>

                    <div class="specialized-unis-grid">
                        ${unisHtml}
                    </div>
                </div>
            </div>
        `;
    } catch (err) {
        container.innerHTML = `<div class="alert alert-danger">Lỗi tải dữ liệu: ${err.message}</div>`;
    }
}

// =========================================================================
// MODULE 2: BỘ TÍNH HỌC PHÍ & HOÀN VỐN (EDUCATION ROI CALCULATOR)
// =========================================================================
const ALL_UNIVERSITIES_DATA = [
    { code: "BKHN", name: "Đại học Bách Khoa Hà Nội", region: "Miền Bắc", base_tuition: 30 },
    { code: "NEU", name: "Trường Đại học Kinh tế Quốc dân", region: "Miền Bắc", base_tuition: 26 },
    { code: "FTU", name: "Trường Đại học Ngoại thương", region: "Miền Bắc", base_tuition: 28 },
    { code: "UET", name: "Trường ĐH Công nghệ - ĐHQGHN", region: "Miền Bắc", base_tuition: 28.5 },
    { code: "HMU", name: "Trường Đại học Y Hà Nội", region: "Miền Bắc", base_tuition: 45 },
    { code: "PTIT", name: "Học viện Công nghệ Bưu chính Viễn thông", region: "Miền Bắc", base_tuition: 27 },
    { code: "DAV", name: "Học viện Ngoại giao", region: "Miền Bắc", base_tuition: 25 },
    { code: "AOF", name: "Học viện Tài chính", region: "Miền Bắc", base_tuition: 25 },
    { code: "TMU", name: "Trường Đại học Thương mại", region: "Miền Bắc", base_tuition: 26 },
    { code: "HNUE", name: "Trường Đại học Sư phạm Hà Nội", region: "Miền Bắc", base_tuition: 0 },
    { code: "HAU", name: "Trường Đại học Kiến trúc Hà Nội", region: "Miền Bắc", base_tuition: 24 },
    { code: "MTCN", name: "Trường ĐH Mỹ thuật Công nghiệp", region: "Miền Bắc", base_tuition: 20 },
    { code: "HANU", name: "Trường Đại học Hà Nội", region: "Miền Bắc", base_tuition: 26 },
    { code: "AJC", name: "Học viện Báo chí & Tuyên truyền", region: "Miền Bắc", base_tuition: 22 },
    { code: "HaUI", name: "Trường Đại học Công nghiệp Hà Nội", region: "Miền Bắc", base_tuition: 24 },
    { code: "UTC", name: "Trường Đại học Giao thông Vận tải", region: "Miền Bắc", base_tuition: 22 },
    { code: "DUT", name: "Trường ĐH Bách khoa - ĐH Đà Nẵng", region: "Miền Trung", base_tuition: 26 },
    { code: "DUE", name: "Trường ĐH Kinh tế - ĐH Đà Nẵng", region: "Miền Trung", base_tuition: 24 },
    { code: "HMED", name: "Trường Đại học Y Dược - ĐH Huế", region: "Miền Trung", base_tuition: 40 },
    { code: "UTE_DN", name: "Trường ĐH Sư phạm Kỹ thuật - ĐH Đà Nẵng", region: "Miền Trung", base_tuition: 22 },
    { code: "HCMUT", name: "Trường ĐH Bách khoa - ĐHQG-HCM", region: "Miền Nam", base_tuition: 35 },
    { code: "UIT", name: "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", region: "Miền Nam", base_tuition: 35 },
    { code: "UEH", name: "Đại học Kinh tế TP. Hồ Chí Minh", region: "Miền Nam", base_tuition: 32 },
    { code: "UMP", name: "Đại học Y Dược TP. Hồ Chí Minh", region: "Miền Nam", base_tuition: 55 },
    { code: "USSH_HCM", name: "Trường ĐH KHXH&NV - ĐHQG-HCM", region: "Miền Nam", base_tuition: 24 },
    { code: "HCMUS", name: "Trường ĐH Khoa học Tự nhiên - ĐHQG-HCM", region: "Miền Nam", base_tuition: 30 },
    { code: "UAH", name: "Trường Đại học Kiến trúc TP. Hồ Chí Minh", region: "Miền Nam", base_tuition: 28 },
    { code: "HCMUTE", name: "Trường ĐH Sư phạm Kỹ thuật TP.HCM", region: "Miền Nam", base_tuition: 28 },
    { code: "CTU", name: "Trường Đại học Cần Thơ", region: "Miền Nam", base_tuition: 20 },
    { code: "PNTU", name: "Trường ĐH Y khoa Phạm Ngọc Thạch", region: "Miền Nam", base_tuition: 45 },
    { code: "TDTU", name: "Trường Đại học Tôn Đức Thắng", region: "Miền Nam", base_tuition: 32 },
    { code: "FPT", name: "Đại học FPT", region: "Toàn quốc", base_tuition: 75 },
    { code: "RMIT", name: "Đại học RMIT Việt Nam", region: "Toàn quốc", base_tuition: 320 }
];

function populateAllUniversitiesForTuitionCalculator() {
    const sel = document.getElementById("roi-uni-select");
    if (!sel || sel.options.length > 2) return;
    sel.innerHTML = ALL_UNIVERSITIES_DATA.map(u => `
        <option value="${u.code}">${u.name} (${u.code} - ${u.region}) [~${u.base_tuition} tr/năm]</option>
    `).join("");
}

function openRoiCalculatorModal() {
    const modal = document.getElementById("modal-roi-calculator");
    if (!modal) return;
    populateAllUniversitiesForTuitionCalculator();
    modal.classList.remove("hidden");
    recalculateEducationROI();
}

function openRoiForMajor(uniCode, encodedMajorName) {
    const modal = document.getElementById("modal-roi-calculator");
    if (!modal) return;
    populateAllUniversitiesForTuitionCalculator();
    modal.classList.remove("hidden");

    const sel = document.getElementById("roi-uni-select");
    if (sel && uniCode) {
        sel.value = uniCode;
    }
    recalculateEducationROI();
}

async function recalculateEducationROI() {
    const uniCode = document.getElementById("roi-uni-select")?.value || "BKHN";
    const programType = document.getElementById("roi-program-type")?.value || "standard";
    const city = document.getElementById("roi-living-city")?.value || "Hà Nội";
    const studyYears = parseFloat(document.getElementById("roi-study-years")?.value) || 4.0;

    const payload = {
        university_code: uniCode,
        major_name: "Công nghệ thông tin",
        program_type: programType,
        city: city,
        study_years: studyYears
    };

    try {
        const res = await fetch("/api/education-roi/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (json.status === "success") {
            renderRoiResults(json.data);
        }
    } catch (err) {
        console.error("ROI calculation error:", err);
    }
}

function renderRoiResults(data) {
    const container = document.getElementById("roi-results-card") || document.getElementById("roi-results-container");
    if (!container) return;

    container.innerHTML = `
        <div style="font-size: 1.05rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <span><i class="fa-solid fa-chart-pie" style="color: #3b82f6;"></i> Báo Cáo Đầu Tư Học Tập: <strong>${data.university_name}</strong></span>
            <span class="badge-count" style="background: #10b981; color: white; padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.8rem;">Hệ: ${data.program_type.toUpperCase()}</span>
        </div>

        <div class="roi-metrics-grid">
            <div class="roi-metric-item">
                <span class="roi-metric-label">Tổng học phí ${data.study_years || 4} năm</span>
                <span class="roi-metric-val">${(data.total_tuition || data.total_tuition_4y || 0).toLocaleString()} tr</span>
            </div>
            <div class="roi-metric-item">
                <span class="roi-metric-label">Tổng sinh hoạt phí</span>
                <span class="roi-metric-val">${(data.total_living_cost || data.total_living_cost_4y || 0).toLocaleString()} tr</span>
            </div>
            <div class="roi-metric-item">
                <span class="roi-metric-label">Tổng mức đầu tư</span>
                <span class="roi-metric-val" style="color: #ef4444;">${(data.grand_total_investment || data.total_cost || 0).toLocaleString()} tr</span>
            </div>
            <div class="roi-metric-item">
                <span class="roi-metric-label">Thời gian hoàn vốn</span>
                <span class="roi-metric-val highlight" style="color: #10b981;"><i class="fa-solid fa-bolt"></i> ${data.payback_period_years} năm (${data.payback_period_months} tháng)</span>
            </div>
        </div>

        <table class="roi-breakdown-table mt-3" style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
            <thead>
                <tr style="background: #f1f5f9; text-align: left;">
                    <th style="padding: 0.6rem;">Hạng Mục Chi Phí & Doanh Thu</th>
                    <th style="padding: 0.6rem;">Giá Trị Ước Tính</th>
                    <th style="padding: 0.6rem;">Ghi Chú</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 0.6rem;">Học phí bình quân / năm</td>
                    <td style="padding: 0.6rem;"><strong>${data.annual_tuition} triệu VNĐ</strong></td>
                    <td style="padding: 0.6rem; color: #64748b;">Đã tính hệ ${data.program_type}</td>
                </tr>
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 0.6rem;">Sinh hoạt phí / tháng (${data.city})</td>
                    <td style="padding: 0.6rem;"><strong>${data.monthly_living_cost} triệu VNĐ</strong></td>
                    <td style="padding: 0.6rem; color: #64748b;">Trọ, ăn uống, đi lại tại ${data.city}</td>
                </tr>
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 0.6rem;">Mức lương khởi điểm kỳ vọng</td>
                    <td style="padding: 0.6rem;"><strong style="color: #059669;">${data.estimated_starting_salary} triệu VNĐ / tháng</strong></td>
                    <td style="padding: 0.6rem; color: #64748b;">Khảo sát sinh viên mới tốt nghiệp</td>
                </tr>
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 0.6rem;">Số tiền tích lũy trả vốn / tháng</td>
                    <td style="padding: 0.6rem;"><strong>${data.estimated_monthly_savings} triệu VNĐ</strong></td>
                    <td style="padding: 0.6rem; color: #64748b;">Giả định trích 40% lương để bù đắp chi phí học</td>
                </tr>
            </tbody>
        </table>

        <div class="scholarship-alert-box mt-3" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 0.85rem; font-size: 0.85rem; color: #166534;">
            <i class="fa-solid fa-hand-holding-dollar"></i> <strong>Học bổng & Gói hỗ trợ tài chính:</strong>
            <div>${data.scholarship_advice}</div>
            <div style="margin-top: 0.35rem; font-size: 0.78rem; opacity: 0.9;">
                <i class="fa-solid fa-info-circle"></i> ${data.student_loan_note}
            </div>
        </div>
    `;
}

// =========================================================================
// MODULE 3: CẦU NỐI ĐỒNG THUẬN GIA ĐÌNH (PARENT & STUDENT ALIGNMENT)
// =========================================================================
function openParentAlignmentModal() {
    const modal = document.getElementById("modal-parent-alignment");
    if (modal) modal.classList.remove("hidden");
}

async function runParentStudentAlignment() {
    const student = {
        stability: parseFloat(document.getElementById("align-s-stab")?.value) || 3,
        location: parseFloat(document.getElementById("align-s-loc")?.value) || 3,
        brand: parseFloat(document.getElementById("align-s-brand")?.value) || 3,
        cost: parseFloat(document.getElementById("align-s-cost")?.value) || 3
    };

    const parent = {
        stability: parseFloat(document.getElementById("align-p-stab")?.value) || 2,
        location: parseFloat(document.getElementById("align-p-loc")?.value) || 2,
        brand: parseFloat(document.getElementById("align-p-brand")?.value) || 2,
        cost: parseFloat(document.getElementById("align-p-cost")?.value) || 2
    };

    const studentMajor = document.getElementById("user-interest")?.value || "Công nghệ Thông tin / Kỹ thuật Số";

    const payload = {
        student_scores: student,
        parent_scores: parent,
        student_target_major: studentMajor
    };

    const container = document.getElementById("alignment-results-box");
    if (container) {
        container.classList.remove("hidden");
        container.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: #4338ca;">
                <i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem;"></i>
                <p style="margin-top: 0.6rem; font-weight: 600;">Hội đồng Cố vấn đang phân tích 4 trục đồng thuận và lập Báo cáo Phụ huynh...</p>
            </div>
        `;
    }

    try {
        const res = await fetch("/api/parent-student-alignment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (json.status === "success") {
            renderParentAlignmentResult(json.data);
        }
    } catch (err) {
        console.error("Alignment error:", err);
        if (container) {
            container.innerHTML = `<div class="alert alert-danger">Lỗi phân tích: ${err.message}</div>`;
        }
    }
}

function renderParentAlignmentResult(data) {
    const container = document.getElementById("alignment-results-box");
    if (!container) return;

    container.classList.remove("hidden");
    const report = data.parent_summary_report || {};
    const axisList = data.axis_comparisons || [];
    const risks = report.risk_analysis || [];
    const roadmap = report.four_year_roadmap || [];
    const questions = report.family_dialogue_guide || [];

    // Tạo bảng so sánh 4 trục
    const tableRowsHtml = axisList.map(a => `
        <tr>
            <td class="axis-name-col">
                <strong>${a.axis_name}</strong>
            </td>
            <td class="student-val-col">
                <div class="score-pill score-student">${a.student_score}/5</div>
                <div class="label-text">${a.student_text}</div>
            </td>
            <td class="parent-val-col">
                <div class="score-pill score-parent">${a.parent_score}/5</div>
                <div class="label-text">${a.parent_text}</div>
            </td>
            <td class="gap-eval-col">
                <span class="status-badge ${a.status_class}">${a.status}</span>
                <div class="advice-subtext">${a.advice}</div>
            </td>
        </tr>
    `).join("");

    container.innerHTML = `
        <div class="alignment-result-wrapper">
            <!-- Header & Gauge -->
            <div class="alignment-header-banner">
                <div class="gauge-display-box">
                    <div class="gauge-circle-wrap">
                        <div class="gauge-pct-value">${data.overall_alignment_pct || data.alignment_percent}%</div>
                        <div class="gauge-lbl">Đồng thuận</div>
                    </div>
                </div>
                <div class="gauge-desc-box">
                    <div class="alignment-status-title">
                        Mức độ Đồng Thuận Gia Đình: <span class="text-success">${data.alignment_level}</span>
                    </div>
                    <p class="alignment-status-desc">
                        Chỉ số phản ánh sự thấu hiểu và ăn khớp về kỳ vọng giữa học sinh và cha mẹ trên 4 trục: <strong>Ổn định việc làm, Vị trí địa lý, Danh tiếng trường</strong> và <strong>Học phí tài chính</strong>.
                    </p>
                </div>
            </div>

            <!-- BẢNG SO SÁNH SỰ ĐỒNG THUẬN GIA ĐÌNH (4 TRỤC) -->
            <div class="alignment-table-card mt-4">
                <div class="card-header-clean">
                    <h5><i class="fa-solid fa-scale-balanced text-primary"></i> Bảng So Sánh Đối Chiếu Sự Đồng Thuận Gia Đình (4 Trục Kỳ Vọng)</h5>
                    <p class="section-sub">Đối chiếu trực quan giữa góc nhìn của Con và mong muốn của Bố Mẹ để nhận diện điểm chung và khoảng cách:</p>
                </div>
                <div class="table-responsive">
                    <table class="alignment-comparison-table">
                        <thead>
                            <tr>
                                <th style="width: 25%;">Trục Khảo Sát</th>
                                <th style="width: 25%;"><i class="fa-solid fa-graduation-cap"></i> Quan Điểm Của Con</th>
                                <th style="width: 25%;"><i class="fa-solid fa-hands-holding-child"></i> Kỳ Vọng Của Bố Mẹ</th>
                                <th style="width: 25%;"><i class="fa-solid fa-comments"></i> Đánh Giá & Lời Khuyên Đối Thoại</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${tableRowsHtml}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- BẢN TÓM TẮT DÀNH RIÊNG CHO PHỤ HUYNH (PARENT SUMMARY REPORT) -->
            <div class="parent-summary-report-card mt-4" id="printable-parent-report">
                <div class="report-top-bar">
                    <div>
                        <div class="report-badge-top"><i class="fa-solid fa-envelope-open-text"></i> DÀNH RIÊNG CHO PHỤ HUYNH</div>
                        <h4 class="report-main-title">${report.title || 'Bản Tóm Tắt Định Hướng Dành Cho Phụ Huynh'}</h4>
                        <div class="report-meta-info">
                            <span><i class="fa-solid fa-calendar-day"></i> Ngày lập: ${new Date().toLocaleDateString('vi-VN')}</span> • 
                            <span><i class="fa-solid fa-brain"></i> Hệ thống Cố vấn EduCompass AI</span> • 
                            <span><i class="fa-solid fa-bullseye"></i> Ngành mục tiêu: <strong>${report.target_major || 'Công nghệ'}</strong></span>
                        </div>
                    </div>
                    <button type="button" class="btn-print-report" onclick="window.print()">
                        <i class="fa-solid fa-print"></i> In / Xuất PDF Báo Cáo
                    </button>
                </div>

                <div class="report-letter-body">
                    <div class="report-greeting">
                        <strong>Kính gửi Quý Phụ huynh,</strong>
                        <p style="margin-top: 0.35rem;">${report.reassurance_message || ''}</p>
                    </div>

                    <!-- Phần 1: Giải mã ngành nghề mới -->
                    <div class="report-section-block">
                        <div class="block-title">
                            <i class="fa-solid fa-lightbulb text-warning"></i> 1. Giải Mã Tiềm Năng Ngành "${report.target_major || 'Công nghệ'}" Bằng Ngôn Ngữ Rõ Ràng:
                        </div>
                        <div class="block-content">
                            <p>${report.plain_explanation || 'Ngành nghề đào tạo ứng dụng thực tiễn cao, phát triển kỹ năng tư duy và cơ hội việc làm vững chắc.'}</p>
                            <div class="salary-highlight-box mt-2">
                                <i class="fa-solid fa-coins text-warning"></i> <strong>Thu nhập thị trường thực tế:</strong> ${report.market_demand_salary || '12 - 18 tr/tháng (Fresher), 25 - 45 tr/tháng sau 3-5 năm.'}
                            </div>
                        </div>
                    </div>

                    <!-- Phần 2: Phân tích rủi ro & Cách khắc phục -->
                    <div class="report-section-block mt-3">
                        <div class="block-title">
                            <i class="fa-solid fa-shield-halved text-success"></i> 2. Bảng Phân Tích Rủi Ro Thực Tế & Cách Khắc Phục Để Phụ Huynh An Tâm:
                        </div>
                        <div class="risk-solution-grid mt-2">
                            ${risks.map(r => `
                                <div class="risk-item-row">
                                    <div class="risk-col">
                                        <i class="fa-solid fa-triangle-exclamation text-danger"></i> <strong>Băn khoăn:</strong> ${r.risk}
                                    </div>
                                    <div class="solution-col">
                                        <i class="fa-solid fa-circle-check text-success"></i> <strong>Giải pháp an tâm:</strong> ${r.solution}
                                    </div>
                                </div>
                            `).join("")}
                        </div>
                    </div>

                    <!-- Phần 3: Lộ trình 4 năm đại học minh bạch -->
                    <div class="report-section-block mt-3">
                        <div class="block-title">
                            <i class="fa-solid fa-route text-indigo"></i> 3. Lộ Trình 4 Năm Đại Học Cụ Thể (Con sẽ học và làm gì?):
                        </div>
                        <div class="report-roadmap-list mt-2">
                            ${roadmap.map(rm => `
                                <div class="report-roadmap-item">
                                    <span class="roadmap-stage-name">${rm.stage}:</span>
                                    <span class="roadmap-stage-desc">${rm.content}</span>
                                </div>
                            `).join("")}
                        </div>
                    </div>

                    <!-- Phần 4: Khung 4 câu hỏi đối thoại cởi mở -->
                    <div class="report-section-block mt-3">
                        <div class="block-title">
                            <i class="fa-solid fa-heart text-danger"></i> 4. Khung 4 Câu Hỏi Gợi Mở Để Cha Mẹ Trò Chuyện Cởi Mở Cùng Con:
                        </div>
                        <ul class="dialogue-questions-list mt-2">
                            ${questions.map((q, idx) => `
                                <li>
                                    <span class="q-num">Câu ${idx + 1}:</span>
                                    <span class="q-text">"${q}"</span>
                                </li>
                            `).join("")}
                        </ul>
                    </div>

                    <div class="report-footer-note mt-3">
                        <i class="fa-solid fa-circle-info text-primary"></i> <strong>Lời kết từ Hội đồng Cố vấn:</strong> Cha mẹ là điểm tựa tinh thần lớn nhất của con. Hãy dành cho con sự tin tưởng và một không gian đối thoại cởi mở để cùng nhau chọn ra ngôi trường phù hợp nhất!
                    </div>
                </div>
            </div>
        </div>
    `;
}

// =========================================================================
// MODULE 4: TỦ NGUYỆN VỌNG & SO SÁNH ĐỐI ĐẦU
// =========================================================================
const WISHLIST_STORAGE_KEY = "educompass_smart_wishlist_v2";

function getSavedWishlist() {
    try {
        const raw = localStorage.getItem(WISHLIST_STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        return [];
    }
}

function saveWishlistToStorage(list) {
    try {
        localStorage.setItem(WISHLIST_STORAGE_KEY, JSON.stringify(list));
    } catch (e) {}
    updateWishlistBadge();
}

function updateWishlistBadge() {
    const list = getSavedWishlist();
    const badge = document.getElementById("wishlist-badge-count") || document.getElementById("wishlist-count-badge");
    const drawerBadge = document.getElementById("wishlist-drawer-count") || document.getElementById("wishlist-drawer-badge");
    const navBadge = document.getElementById("nav-wishlist-count");
    if (badge) badge.textContent = list.length;
    if (drawerBadge) drawerBadge.textContent = list.length;
    if (navBadge) navBadge.textContent = list.length;
}

function isInWishlist(uniCode, majorName) {
    const list = getSavedWishlist();
    return list.some(item => item.university_code === uniCode && item.major_name === majorName);
}

function toggleWishlistItemFromDream(idx) {
    if (!currentDreamMatches || !currentDreamMatches[idx]) return;
    const item = currentDreamMatches[idx];
    let list = getSavedWishlist();
    const existingIdx = list.findIndex(w => w.university_code === item.university_code && w.major_name === item.major_name);

    if (existingIdx >= 0) {
        list.splice(existingIdx, 1);
    } else {
        if (list.length >= 15) {
            alert("Tủ nguyện vọng chỉ lưu tối đa 15 nguyện vọng ưu tiên!");
            return;
        }
        list.push({
            university_name: item.university_name,
            university_code: item.university_code,
            university_region: item.region || item.university_region || "Toàn quốc",
            major_name: item.major_name,
            major_category: item.major_category || "Đại học",
            combination_code: item.combination_code || "A00",
            candidate_score: item.candidate_score,
            score_2025: item.score_2025,
            pass_probability: item.pass_probability,
            tuition_range: item.tuition_range || "25 - 35 tr/năm",
            strategy_role: item.strategy_role || "Mơ ước",
            added_at: new Date().toISOString()
        });
    }

    saveWishlistToStorage(list);

    // Update UI button on dream card
    const btn = document.getElementById(`btn-dream-wishlist-${idx}`);
    const isNowFav = isInWishlist(item.university_code, item.major_name);
    if (btn) {
        btn.className = `btn-toggle-wishlist ${isNowFav ? 'active' : ''}`;
        btn.innerHTML = `<i class="fa-${isNowFav ? 'solid' : 'regular'} fa-bookmark"></i> <span>${isNowFav ? 'Đã lưu' : 'Lưu NV'}</span>`;
    }

    renderWishlistDrawer();
    populateCompareSelects();
}

function toggleWishlistItemFromCard(cardIdx) {
    if (!currentConsultResult || !currentConsultResult.final_report) return;
    const topRecs = currentConsultResult.final_report.top_recommendations || [];
    const item = topRecs[cardIdx];
    if (!item) return;

    let list = getSavedWishlist();
    const existingIdx = list.findIndex(w => w.university_code === item.university_code && w.major_name === item.major_name);

    if (existingIdx >= 0) {
        list.splice(existingIdx, 1);
    } else {
        if (list.length >= 15) {
            alert("Tủ nguyện vọng chỉ lưu tối đa 15 nguyện vọng ưu tiên!");
            return;
        }
        list.push({
            university_name: item.university_name,
            university_code: item.university_code,
            university_region: item.university_region,
            major_name: item.major_name,
            major_category: item.major_category,
            combination_code: item.combination_code,
            candidate_score: item.candidate_score,
            score_2025: item.score_2025,
            pass_probability: item.pass_probability,
            tuition_range: item.tuition_range,
            strategy_role: item.strategy_role,
            added_at: new Date().toISOString()
        });
    }

    saveWishlistToStorage(list);

    const btn = document.getElementById(`btn-wishlist-${cardIdx}`);
    const isNowFav = isInWishlist(item.university_code, item.major_name);
    if (btn) {
        btn.className = `btn-toggle-wishlist ${isNowFav ? 'active' : ''}`;
        btn.innerHTML = `<i class="fa-${isNowFav ? 'solid' : 'regular'} fa-bookmark"></i> <span>${isNowFav ? 'Đã lưu' : 'Lưu NV'}</span>`;
    }

    renderWishlistDrawer();
    populateCompareSelects();
}

function openWishlistDrawer() {
    const drawer = document.getElementById("wishlist-drawer");
    if (!drawer) return;
    renderWishlistDrawer();
    drawer.classList.remove("hidden");
}

function closeWishlistDrawer() {
    const drawer = document.getElementById("wishlist-drawer");
    if (drawer) drawer.classList.add("hidden");
}

function removeWishlistItem(idx) {
    let list = getSavedWishlist();
    if (idx >= 0 && idx < list.length) {
        list.splice(idx, 1);
        saveWishlistToStorage(list);
        renderWishlistDrawer();
        populateCompareSelects();
        if (currentConsultResult && currentConsultResult.final_report) {
            renderRoadmap(currentConsultResult.final_report.top_recommendations || []);
        }
    }
}

function clearWishlist() {
    if (confirm("Bạn có chắc chắn muốn xóa toàn bộ danh sách nguyện vọng đã lưu?")) {
        saveWishlistToStorage([]);
        renderWishlistDrawer();
        populateCompareSelects();
        if (currentConsultResult && currentConsultResult.final_report) {
            renderRoadmap(currentConsultResult.final_report.top_recommendations || []);
        }
    }
}

function renderWishlistDrawer() {
    const container = document.getElementById("wishlist-items-list") || document.getElementById("wishlist-items-container");
    if (!container) return;

    const list = getSavedWishlist();
    updateWishlistBadge();

    if (list.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 2.5rem 1rem; color: #94a3b8;">
                <i class="fa-regular fa-folder-open" style="font-size: 2.8rem; margin-bottom: 0.75rem; color: #cbd5e1;"></i>
                <p style="font-size: 0.95rem; font-weight: 700; color: #475569;">Tủ nguyện vọng đang trống</p>
                <p style="font-size: 0.82rem; margin-top: 0.35rem; color: #64748b; line-height: 1.5;">
                    Hãy bấm <strong>"Lưu NV"</strong> trên các thẻ gợi ý hoặc kết quả <strong>"Tra Cứu Trường Mơ Ước"</strong> để lưu lại các ngành/trường bạn quan tâm và mang sang so sánh đối đầu!
                </p>
            </div>
        `;
        return;
    }

    container.innerHTML = list.map((item, idx) => `
        <div class="wishlist-item-card">
            <div class="wishlist-item-top">
                <div>
                    <div class="wishlist-major-name">NV${idx + 1}: ${item.major_name}</div>
                    <div class="wishlist-uni-name"><i class="fa-solid fa-building-columns"></i> ${item.university_name} (${item.university_code}) • ${item.university_region || ''}</div>
                </div>
                <button type="button" class="btn-remove-wishlist" onclick="removeWishlistItem(${idx})" title="Xóa khỏi tủ">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div class="wishlist-meta-row">
                <span class="wishlist-meta-badge" style="background: #e0e7ff; color: #4338ca; font-weight: 700;">${item.combination_code}</span>
                <span class="wishlist-meta-badge">Điểm chuẩn '25: <strong>${item.score_2025}đ</strong></span>
                <span class="wishlist-meta-badge" style="color: #059669; font-weight: 700;">Đỗ: ${item.pass_probability}%</span>
                <span class="wishlist-meta-badge">${item.strategy_role || 'Mơ ước'}</span>
            </div>
            <div class="wishlist-actions-row" style="display: flex; gap: 0.4rem; margin-top: 0.6rem;">
                <button type="button" class="btn-secondary" style="font-size: 0.75rem; padding: 0.3rem 0.6rem; flex: 1;" onclick="openCompareWithMajor('${encodeURIComponent(item.major_name)}')">
                    <i class="fa-solid fa-scale-balanced text-indigo"></i> So Sánh
                </button>
                <button type="button" class="btn-secondary" style="font-size: 0.75rem; padding: 0.3rem 0.6rem; flex: 1;" onclick="openRoiForMajor('${item.university_code}', '${encodeURIComponent(item.major_name)}')">
                    <i class="fa-solid fa-calculator text-success"></i> Tính ROI
                </button>
            </div>
        </div>
    `).join("");
}

// Head-to-Head Compare Modal
function populateCompareSelects() {
    const selA = document.getElementById("compare-select-a") || document.getElementById("compare-major-a");
    const selB = document.getElementById("compare-select-b") || document.getElementById("compare-major-b");
    if (!selA || !selB) return;

    const map = new Map();
    if (currentConsultResult && currentConsultResult.final_report) {
        (currentConsultResult.final_report.top_recommendations || []).forEach(r => {
            map.set(r.major_name, r.major_name);
        });
    }
    getSavedWishlist().forEach(w => {
        map.set(w.major_name, w.major_name);
    });

    const fallbackMajors = [
        "Công nghệ thông tin", "Kỹ thuật phần mềm", "Trí tuệ nhân tạo", "Khoa học máy tính",
        "Khoa học dữ liệu", "Quản trị kinh doanh", "Kinh doanh quốc tế", "Marketing",
        "Tài chính ngân hàng", "Logistics và Quản lý chuỗi cung ứng", "Thương mại điện tử",
        "Y đa khoa", "Dược học", "Thiết kế đồ họa", "Truyền thông đa phương tiện"
    ];
    fallbackMajors.forEach(m => map.set(m, m));

    const opts = Array.from(map.values()).map(m => `<option value="${m}">${m}</option>`).join("");
    selA.innerHTML = opts;
    selB.innerHTML = opts;

    if (selB.options.length > 1) {
        selB.selectedIndex = 1;
    }
}

function openCompareModal() {
    const modal = document.getElementById("modal-compare");
    if (!modal) return;
    populateCompareSelects();
    modal.classList.remove("hidden");
    triggerHeadToHeadComparison();
}

function openCompareWithMajor(encodedMajorName) {
    const majorName = decodeURIComponent(encodedMajorName);
    const modal = document.getElementById("modal-compare");
    if (!modal) return;
    populateCompareSelects();
    modal.classList.remove("hidden");

    const selA = document.getElementById("compare-select-a") || document.getElementById("compare-major-a");
    if (selA) selA.value = majorName;
    triggerHeadToHeadComparison();
}

function openCompareModalFromWishlist() {
    closeWishlistDrawer();
    openCompareModal();
}

async function triggerHeadToHeadComparison() {
    const selA = document.getElementById("compare-select-a") || document.getElementById("compare-major-a");
    const selB = document.getElementById("compare-select-b") || document.getElementById("compare-major-b");
    const majorA = selA?.value || "Công nghệ thông tin";
    const majorB = selB?.value || "Kỹ thuật phần mềm";

    const payload = {
        major_a_name: majorA,
        major_b_name: majorB,
        candidate_score: parseFloat(document.getElementById("score-toan")?.value) || 24.5
    };

    try {
        const res = await fetch("/api/compare-majors", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (json.status === "success") {
            renderCompareTable(json.data);
        }
    } catch (err) {
        console.error("Comparison error:", err);
    }
}

function renderCompareTable(data) {
    const container = document.getElementById("compare-table-container") || document.getElementById("compare-results-container");
    if (!container) return;

    const a = data.major_a || {};
    const b = data.major_b || {};
    const comp = data.comparison || {};

    const tableRows = [
        { label: "Nhóm ngành đào tạo", valA: a.major_category, valB: b.major_category, winner: null },
        { label: "Điểm chuẩn 2025 (Tham chiếu)", valA: `${a.benchmark_2025}đ`, valB: `${b.benchmark_2025}đ`, winner: a.benchmark_2025 <= b.benchmark_2025 ? 'a' : 'b' },
        { label: "Điểm chuẩn 2024", valA: `${a.benchmark_2024}đ`, valB: `${b.benchmark_2024}đ`, winner: null },
        { label: "Điểm chuẩn 2023", valA: `${a.benchmark_2023}đ`, valB: `${b.benchmark_2023}đ`, winner: null },
        { label: "Học phí toàn khóa 4 năm", valA: `${a.tuition_total_4y} triệu VNĐ`, valB: `${b.tuition_total_4y} triệu VNĐ`, winner: a.tuition_total_4y <= b.tuition_total_4y ? 'a' : 'b' },
        { label: "Mức lương khởi điểm TB", valA: `<strong style="color: #059669;">${a.average_starting_salary} tr/tháng</strong>`, valB: `<strong style="color: #059669;">${b.average_starting_salary} tr/tháng</strong>`, winner: a.average_starting_salary >= b.average_starting_salary ? 'a' : 'b' },
        { label: "Tỷ lệ việc làm sau 1 năm", valA: `<strong>${a.employment_rate}%</strong>`, valB: `<strong>${b.employment_rate}%</strong>`, winner: a.employment_rate >= b.employment_rate ? 'a' : 'b' },
        { label: "Chuẩn đầu ra ngoại ngữ", valA: a.english_exit_req, valB: b.english_exit_req, winner: null },
        { label: "Rủi ro AI & Tự động hóa", valA: `<span class="ai-impact-badge ${a.ai_risk_pct < 25 ? 'ai-risk-low' : (a.ai_risk_pct < 50 ? 'ai-risk-med' : 'ai-risk-high')}">${a.ai_risk_pct}% (${a.ai_risk_level})</span>`, valB: `<span class="ai-impact-badge ${b.ai_risk_pct < 25 ? 'ai-risk-low' : (b.ai_risk_pct < 50 ? 'ai-risk-med' : 'ai-risk-high')}">${b.ai_risk_pct}% (${b.ai_risk_level})</span>`, winner: a.ai_risk_pct <= b.ai_risk_pct ? 'a' : 'b' },
        { label: "Thời gian hoàn vốn (ROI)", valA: `<strong>${a.payback_period_years} năm</strong>`, valB: `<strong>${b.payback_period_years} năm</strong>`, winner: a.payback_period_years <= b.payback_period_years ? 'a' : 'b' }
    ];

    const rowsHtml = tableRows.map(r => {
        const classA = r.winner === 'a' ? 'compare-winner' : '';
        const classB = r.winner === 'b' ? 'compare-winner' : '';
        return `
            <tr>
                <td class="metric-name">${r.label}</td>
                <td class="col-a ${classA}">${r.valA} ${r.winner === 'a' ? '<i class="fa-solid fa-crown" style="color: #f59e0b; margin-left: 0.35rem;"></i>' : ''}</td>
                <td class="col-b ${classB}">${r.valB} ${r.winner === 'b' ? '<i class="fa-solid fa-crown" style="color: #f59e0b; margin-left: 0.35rem;"></i>' : ''}</td>
            </tr>
        `;
    }).join("");

    container.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
            <div class="compare-table-container">
                <table class="compare-table">
                    <thead>
                        <tr>
                            <th class="metric-name">Chỉ Số Đặt Lên Bàn Cân</th>
                            <th class="col-a" style="color: #4f46e5; font-size: 1rem;"><i class="fa-solid fa-graduation-cap"></i> ${a.major_name}</th>
                            <th class="col-b" style="color: #059669; font-size: 1rem;"><i class="fa-solid fa-graduation-cap"></i> ${b.major_name}</th>
                        </tr>
                    </thead>
                    <tbody>${rowsHtml}</tbody>
                </table>
            </div>

            <div style="background: #eef2ff; border-left: 4px solid #4f46e5; padding: 1rem; border-radius: 0 8px 8px 0; font-size: 0.85rem; color: #1e1b4b; line-height: 1.6;">
                <div style="font-weight: 700; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                    <i class="fa-solid fa-scale-balanced" style="color: #4f46e5;"></i> Đánh giá tổng quan từ Hội đồng AI:
                </div>
                <div>${comp.overview_summary || 'Cả hai ngành đều có thế mạnh riêng biệt.'}</div>
                <div style="margin-top: 0.5rem; font-weight: 600; color: #3730a3;">
                    <i class="fa-solid fa-lightbulb" style="color: #f59e0b;"></i> Lời khuyên lựa chọn: ${comp.recommended_choice_advice || ''}
                </div>
            </div>
        </div>
    `;
}

// Đóng / mở từng khung trợ giúp (What-If, Trường Mơ Ước, 6 Công Cụ)
function toggleHelperBox(boxId) {
    const box = document.getElementById(boxId);
    if (!box) return;
    const isNowCollapsed = box.classList.toggle("is-collapsed");

    // Cập nhật nút đóng/mở trong khung
    const btn = box.querySelector(".btn-collapse-toggle");
    if (btn) {
        btn.innerHTML = isNowCollapsed 
            ? '<i class="fa-solid fa-chevron-down"></i> <span>Mở rộng</span>' 
            : '<i class="fa-solid fa-chevron-up"></i> <span>Thu gọn</span>';
        btn.title = isNowCollapsed ? "Bấm để mở rộng khung này" : "Bấm để thu gọn khung này";
    }

    updateMasterCollapseBtnState();
}

// Thu gọn hoặc mở rộng đồng loạt cả 3 khung trợ giúp
function toggleAllHelperBoxes() {
    const boxIds = ["what-if-card", "dream-search-card", "feature-hub"];
    // Kiểm tra xem có ít nhất 1 khung đang mở hay không
    const anyOpen = boxIds.some(id => {
        const el = document.getElementById(id);
        return el && !el.classList.contains("is-collapsed");
    });

    const shouldCollapse = anyOpen; // nếu có khung đang mở -> thu gọn tất cả; ngược lại mở tất cả

    boxIds.forEach(id => {
        const box = document.getElementById(id);
        if (!box) return;
        if (shouldCollapse) {
            box.classList.add("is-collapsed");
        } else {
            box.classList.remove("is-collapsed");
        }
        const btn = box.querySelector(".btn-collapse-toggle");
        if (btn) {
            btn.innerHTML = shouldCollapse
                ? '<i class="fa-solid fa-chevron-down"></i> <span>Mở rộng</span>'
                : '<i class="fa-solid fa-chevron-up"></i> <span>Thu gọn</span>';
            btn.title = shouldCollapse ? "Bấm để mở rộng khung này" : "Bấm để thu gọn khung này";
        }
    });

    updateMasterCollapseBtnState();
}

// Cập nhật trạng thái nút tổng trên thanh tiêu đề
function updateMasterCollapseBtnState() {
    const masterBtn = document.getElementById("btn-toggle-all-boxes");
    if (!masterBtn) return;
    const boxIds = ["what-if-card", "dream-search-card", "feature-hub"];
    const allCollapsed = boxIds.every(id => {
        const el = document.getElementById(id);
        return !el || el.classList.contains("is-collapsed");
    });

    if (allCollapsed) {
        masterBtn.innerHTML = '<i class="fa-solid fa-expand"></i> <span>Mở rộng 3 khung</span>';
        masterBtn.classList.add("all-collapsed");
    } else {
        masterBtn.innerHTML = '<i class="fa-solid fa-compress"></i> <span>Thu gọn 3 khung</span>';
        masterBtn.classList.remove("all-collapsed");
    }
}

// Cuộn mượt đến Bộ 6 công cụ đột phá ở khu vực tư vấn
function scrollToCareerTools(event) {
    if (event) event.preventDefault();
    const dashboard = document.getElementById("dashboard-section");
    if (dashboard && dashboard.classList.contains("hidden")) {
        // Mở khóa bảng kết quả/công cụ nếu chưa thực hiện tư vấn
        dashboard.classList.remove("hidden");
    }
    const tools = document.getElementById("feature-hub");
    if (tools) {
        // Nếu khung đang bị đóng, tự động mở rộng để hiển thị các công cụ
        if (tools.classList.contains("is-collapsed")) {
            toggleHelperBox("feature-hub");
        }
        tools.scrollIntoView({ behavior: "smooth", block: "center" });
        tools.classList.add("highlight-pulse");
        setTimeout(() => tools.classList.remove("highlight-pulse"), 2000);
    }
}

// =========================================================================
// THẨM ĐỊNH & PHỎNG VẤN CHUYÊN SÂU THEO TRƯỜNG ĐẠI HỌC MƠ ƯỚC
// =========================================================================
let currentSelectedSchool = "BKHN";
let currentSchoolCheckResult = null;
let currentSchoolCheckFilter = "all";
let currentInterviewSession = null;

const SCHOOL_METADATA = {
    BKHN: {
        code: "BKHN", name: "Đại học Bách khoa Hà Nội", logo: "🏛️", region: "Hà Nội (Miền Bắc)", type: "Công lập",
        tuition: "25 - 45 tr/năm", website: "https://hust.edu.vn",
        desc: "Top 1 Kỹ thuật & Công nghệ miền Bắc, đào tạo chuyên sâu và áp lực học tập cao.",
        methods: "THPT + ĐGTD (TSA) + IELTS",
        focusInputs: ["tsa", "ielts"],
        defaultKhoi: "A01"
    },
    HCMUT: {
        code: "HCMUT", name: "Trường Đại học Bách khoa - ĐHQG-HCM", logo: "⚙️", region: "TP. Hồ Chí Minh (Miền Nam)", type: "Công lập",
        tuition: "30 - 50 tr/năm", website: "https://hcmut.edu.vn",
        desc: "Đại học kỹ thuật danh tiếng bậc nhất miền Nam, đào tạo kỹ sư chất lượng cao và năng động.",
        methods: "ĐGNL (APT 75%) + THPT (20%) + Học bạ (5%)",
        focusInputs: ["apt", "gpa"],
        defaultKhoi: "A00"
    },
    UET: {
        code: "UET", name: "Trường Đại học Công nghệ - ĐHQGHN", logo: "🔬", region: "Hà Nội (Miền Bắc)", type: "Công lập",
        tuition: "20 - 35 tr/năm", website: "https://uet.vnu.edu.vn",
        desc: "Trường công nghệ mũi nhọn thuộc ĐHQGHN, thế mạnh CNTT, AI và Công nghệ Bán dẫn.",
        methods: "THPT + ĐGNL ĐHQGHN (HSA) + IELTS",
        focusInputs: ["hsa", "ielts"],
        defaultKhoi: "A01"
    },
    UIT: {
        code: "UIT", name: "Trường ĐH Công nghệ Thông tin - ĐHQG-HCM", logo: "💻", region: "TP. Hồ Chí Minh (Miền Nam)", type: "Công lập",
        tuition: "32 - 45 tr/năm", website: "https://uit.edu.vn",
        desc: "Chuyên sâu hoàn toàn về Khoa học máy tính, AI, Kỹ thuật dữ liệu và An toàn thông tin.",
        methods: "ĐGNL ĐHQG-HCM (APT) + THPT + IELTS",
        focusInputs: ["apt", "ielts"],
        defaultKhoi: "A01"
    },
    NEU: {
        code: "NEU", name: "Trường Đại học Kinh tế Quốc dân", logo: "📈", region: "Hà Nội (Miền Bắc)", type: "Công lập",
        tuition: "22 - 38 tr/năm", website: "https://neu.edu.vn",
        desc: "Trường đầu ngành kinh tế, tài chính và quản trị tại miền Bắc, bản lĩnh và thực tiễn.",
        methods: "Xét tuyển kết hợp IELTS + THPT/ĐGNL (HSA)",
        focusInputs: ["ielts", "hsa"],
        defaultKhoi: "D01"
    },
    FTU: {
        code: "FTU", name: "Trường Đại học Ngoại thương (Cơ sở Hà Nội)", logo: "🚢", region: "Hà Nội (Miền Bắc)", type: "Công lập",
        tuition: "25 - 45 tr/năm", website: "https://ftu.edu.vn",
        desc: "Thương hiệu hàng đầu về Kinh tế đối ngoại, năng động, chuẩn quốc tế.",
        methods: "IELTS (≥ 6.5) + Học bạ Giỏi + THPT",
        focusInputs: ["ielts", "gpa"],
        defaultKhoi: "A01"
    },
    UEH: {
        code: "UEH", name: "Đại học Kinh tế TP. Hồ Chí Minh", logo: "📊", region: "TP. Hồ Chí Minh (Miền Nam)", type: "Công lập",
        tuition: "28 - 48 tr/năm", website: "https://ueh.edu.vn",
        desc: "Đại học đa ngành về Kinh tế, Quản lý công và Đổi mới sáng tạo hàng đầu phía Nam.",
        methods: "ĐGNL ĐHQG-HCM (APT) + THPT + IELTS",
        focusInputs: ["apt", "ielts"],
        defaultKhoi: "A01"
    },
    HMU: {
        code: "HMU", name: "Trường Đại học Y Hà Nội", logo: "🩺", region: "Hà Nội (Miền Bắc)", type: "Công lập",
        tuition: "27 - 55 tr/năm", website: "https://hmu.edu.vn",
        desc: "Cơ sở đào tạo y khoa danh giá bậc nhất Việt Nam, điểm chuẩn luôn ở mức đỉnh.",
        methods: "Điểm thi THPT khối B00 + IELTS kết hợp",
        focusInputs: ["ielts"],
        defaultKhoi: "B00"
    },
    UMP: {
        code: "UMP", name: "Đại học Y Dược TP. Hồ Chí Minh", logo: "💊", region: "TP. Hồ Chí Minh (Miền Nam)", type: "Công lập",
        tuition: "35 - 70 tr/năm", website: "https://ump.edu.vn",
        desc: "Biểu tượng y khoa phương Nam, chất lượng đào tạo bác sĩ và dược sĩ đầu ngành.",
        methods: "Điểm thi THPT khối B00/A00 + Sơ tuyển",
        focusInputs: ["ielts"],
        defaultKhoi: "B00"
    },
    PTIT: {
        code: "PTIT", name: "Học viện Công nghệ Bưu chính Viễn thông", logo: "📡", region: "Hà Nội (Miền Bắc)", type: "Công lập",
        tuition: "24 - 32 tr/năm", website: "https://ptit.edu.vn",
        desc: "Thế mạnh lớn về Viễn thông, CNTT, Đa phương tiện và An toàn thông tin.",
        methods: "THPT + ĐGNL (HSA/APT) + IELTS",
        focusInputs: ["hsa", "ielts"],
        defaultKhoi: "A01"
    },
    DUT: {
        code: "DUT", name: "Trường Đại học Bách khoa - ĐH Đà Nẵng", logo: "🏗️", region: "Đà Nẵng (Miền Trung)", type: "Công lập",
        tuition: "22 - 32 tr/năm", website: "https://dut.udn.vn",
        desc: "Trung tâm đào tạo kỹ thuật công nghệ lớn nhất miền Trung.",
        methods: "THPT + ĐGNL + Học bạ THPT",
        focusInputs: ["apt", "gpa"],
        defaultKhoi: "A00"
    },
    DUE: {
        code: "DUE", name: "Trường Đại học Kinh tế - ĐH Đà Nẵng", logo: "📉", region: "Đà Nẵng (Miền Trung)", type: "Công lập",
        tuition: "20 - 30 tr/năm", website: "https://due.udn.vn",
        desc: "Trường kinh tế hàng đầu khu vực miền Trung và Tây Nguyên.",
        methods: "THPT + Học bạ + IELTS",
        focusInputs: ["ielts", "gpa"],
        defaultKhoi: "D01"
    }
};

// 1. Khi người dùng chọn một trường đại học mục tiêu
function onSelectSchoolTarget(schoolCode) {
    if (!schoolCode) schoolCode = "BKHN";
    currentSelectedSchool = schoolCode;

    // Cập nhật giá trị trên dropdown nếu chưa đồng bộ
    const selectEl = document.getElementById("school-target-select");
    if (selectEl && selectEl.value !== schoolCode) {
        selectEl.value = schoolCode;
    }

    const meta = SCHOOL_METADATA[schoolCode] || {
        code: schoolCode, name: `Trường ĐH ${schoolCode}`, logo: "🎓", region: "Toàn quốc", type: "Đại học",
        tuition: "20 - 35 tr/năm", website: "#", desc: "Trường đào tạo đại học uy tín theo quy chế Bộ GD&ĐT.",
        methods: "Điểm thi THPT + Xét tuyển kết hợp", focusInputs: [], defaultKhoi: "A01"
    };

    // Cập nhật Thẻ Nhận diện thương hiệu trường
    const logoBadge = document.getElementById("school-logo-badge");
    const nameEl = document.getElementById("school-display-name");
    const codeEl = document.getElementById("school-display-code");
    const typeEl = document.getElementById("school-display-type");
    const regionEl = document.getElementById("school-display-region");
    const descEl = document.getElementById("school-display-desc");
    const tuitionEl = document.getElementById("school-display-tuition");
    const websiteEl = document.getElementById("school-display-website");
    const methodBadge = document.getElementById("school-method-badge");

    if (logoBadge) logoBadge.textContent = meta.logo;
    if (nameEl) nameEl.textContent = meta.name;
    if (codeEl) codeEl.textContent = meta.code;
    if (typeEl) typeEl.textContent = meta.type;
    if (regionEl) regionEl.innerHTML = `<i class="fa-solid fa-location-dot"></i> ${meta.region}`;
    if (descEl) descEl.textContent = meta.desc;
    if (tuitionEl) tuitionEl.textContent = meta.tuition;
    if (websiteEl) {
        websiteEl.href = meta.website;
        websiteEl.innerHTML = `Website trường <i class="fa-solid fa-arrow-up-right-from-square"></i>`;
    }
    if (methodBadge) {
        methodBadge.innerHTML = `<i class="fa-solid fa-sliders text-success"></i> Phương thức chính: <strong>${meta.methods}</strong>`;
    }

    // Dynamic Form Highlight: Làm nổi bật các ô điểm theo phương thức trường đó dùng
    const focusInputs = meta.focusInputs || [];
    const allWrappers = ["wrap-score-tsa", "wrap-score-apt", "wrap-score-hsa", "wrap-ielts-score", "wrap-transcript-gpa"];
    allWrappers.forEach(wId => {
        const el = document.getElementById(wId);
        if (el) el.classList.remove("highlight-school-input");
    });

    if (focusInputs.includes("tsa")) {
        const el = document.getElementById("wrap-score-tsa");
        if (el) el.classList.add("highlight-school-input");
    }
    if (focusInputs.includes("apt")) {
        const el = document.getElementById("wrap-score-apt");
        if (el) el.classList.add("highlight-school-input");
    }
    if (focusInputs.includes("hsa")) {
        const el = document.getElementById("wrap-score-hsa");
        if (el) el.classList.add("highlight-school-input");
    }
    if (focusInputs.includes("ielts")) {
        const el = document.getElementById("wrap-ielts-score");
        if (el) el.classList.add("highlight-school-input");
    }
    if (focusInputs.includes("gpa")) {
        const el = document.getElementById("wrap-transcript-gpa");
        if (el) el.classList.add("highlight-school-input");
    }

    // Tự động chuyển Khối xét tuyển mặc định phù hợp nhất với trường này
    if (meta.defaultKhoi && typeof selectKhoiTarget === "function") {
        selectKhoiTarget(meta.defaultKhoi);
    }
}

// 2. Tự động điền điểm thi mẫu của trường được chọn
async function applySampleScoreForSelectedSchool() {
    try {
        const res = await fetch(`/api/school-sample-score/${currentSelectedSchool}`);
        const json = await res.json();
        if (json.status === "success" && json.sample_scores) {
            const p = json.sample_scores;
            if (p.toan !== undefined) document.getElementById("score-toan").value = p.toan;
            if (p.van !== undefined) document.getElementById("score-van").value = p.van;
            if (p.anh !== undefined) document.getElementById("score-anh").value = p.anh;
            if (p.ly !== undefined) document.getElementById("score-ly").value = p.ly;
            if (p.hoa !== undefined) document.getElementById("score-hoa").value = p.hoa;
            if (p.sinh !== undefined) document.getElementById("score-sinh").value = p.sinh;
            if (p.su !== undefined) document.getElementById("score-su").value = p.su;
            if (p.dia !== undefined) document.getElementById("score-dia").value = p.dia;
            if (p.gpa !== undefined) document.getElementById("transcript-gpa").value = p.gpa;
            if (p.ielts !== undefined) document.getElementById("ielts-score").value = p.ielts;
            if (p.tsa !== undefined) document.getElementById("score-tsa").value = p.tsa;
            if (p.apt !== undefined) document.getElementById("score-apt").value = p.apt;
            if (p.hsa !== undefined) document.getElementById("score-hsa").value = p.hsa;
            if (p.priority) document.getElementById("priority-area").value = p.priority;

            updatePriorityPreview();

            // Hiệu ứng thông báo nhẹ
            const card = document.getElementById("school-branding-card");
            if (card) {
                card.classList.add("highlight-pulse");
                setTimeout(() => card.classList.remove("highlight-pulse"), 1200);
            }
        }
    } catch (e) {
        console.error("Error applying sample score:", e);
    }
}

// 3. Kích hoạt thẩm định cơ hội xét tuyển trường này
async function triggerSchoolAdmissionCheck() {
    // Thu thập điểm các môn
    const examScores = {};
    ALL_SUBJECTS.forEach(s => {
        const info = SUBJECT_INFO[s];
        const val = parseFloat(document.getElementById(info.inputId).value);
        examScores[info.name] = !isNaN(val) ? val : 0;
    });

    const gpa = parseFloat(document.getElementById("transcript-gpa").value) || 7.5;
    const ieltsVal = document.getElementById("ielts-score").value.trim();
    const ieltsScore = ieltsVal ? parseFloat(ieltsVal) : null;
    const tsaVal = document.getElementById("score-tsa").value.trim();
    const tsaScore = tsaVal ? parseFloat(tsaVal) : null;
    const aptVal = document.getElementById("score-apt").value.trim();
    const aptScore = aptVal ? parseFloat(aptVal) : null;
    const hsaVal = document.getElementById("score-hsa").value.trim();
    const hsaScore = hsaVal ? parseFloat(hsaVal) : null;
    const priorityArea = document.getElementById("priority-area").value;
    const priorityEth = document.getElementById("priority-ethnicity") ? document.getElementById("priority-ethnicity").value : "kinh";

    const payload = {
        school_code: currentSelectedSchool,
        exam_scores: examScores,
        transcript_gpa: gpa,
        ielts_score: ieltsScore,
        tsa_score: tsaScore,
        apt_score: aptScore,
        hsa_score: hsaScore,
        priority_area: priorityArea,
        ethnicity: priorityEth
    };

    try {
        const btn = document.querySelector(".btn-school-check");
        if (btn) {
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Đang tính toán...`;
            btn.disabled = true;
        }

        const res = await fetch("/api/school-check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (btn) {
            btn.innerHTML = `<i class="fa-solid fa-bolt-lightning text-warning"></i> <strong>Thẩm Định Cửa Đỗ Trường Này</strong>`;
            btn.disabled = false;
        }

        if (data.status === "success") {
            currentSchoolCheckResult = data;
            renderSchoolCheckModal(data);
        } else {
            alert(data.message || "Không thể thực hiện thẩm định trường.");
        }
    } catch (e) {
        console.error("Lỗi thẩm định trường:", e);
        alert("Có lỗi khi kết nối máy chủ để thẩm định trường.");
        const btn = document.querySelector(".btn-school-check");
        if (btn) {
            btn.innerHTML = `<i class="fa-solid fa-bolt-lightning text-warning"></i> <strong>Thẩm Định Cửa Đỗ Trường Này</strong>`;
            btn.disabled = false;
        }
    }
}

// Render dữ liệu lên Modal Thẩm Định Cửa Đỗ
function renderSchoolCheckModal(data) {
    window.lastSchoolCheckData = data;
    syncSchoolCheckToOnPage(data);

    const schoolInfo = data.school_info || {};
    const persona = data.persona || {};
    const counts = data.counts || {};
    const alerts = data.criteria_alerts || [];

    // Header info
    const logoEl = document.getElementById("modal-check-logo");
    const titleEl = document.getElementById("modal-check-title");
    const subEl = document.getElementById("modal-check-subtitle");
    if (logoEl) logoEl.textContent = persona.avatar || "🏛️";
    if (titleEl) titleEl.textContent = `Thẩm Định Cửa Đỗ & Dự Báo Trúng Tuyển: ${schoolInfo.name}`;
    if (subEl) subEl.textContent = `So sánh trực tiếp điểm xét tuyển của bạn với ${counts.total} ngành đào tạo của ${schoolInfo.code}. Học phí dự kiến: ${schoolInfo.tuition_range || "25 - 45"} tr/năm.`;

    // Stats
    document.getElementById("stat-count-safe").textContent = counts.safe || 0;
    document.getElementById("stat-count-competitive").textContent = counts.competitive || 0;
    document.getElementById("stat-count-risky").textContent = counts.risky || 0;

    document.getElementById("tab-count-all").textContent = counts.total || 0;
    document.getElementById("tab-count-safe").textContent = counts.safe || 0;
    document.getElementById("tab-count-competitive").textContent = counts.competitive || 0;
    document.getElementById("tab-count-risky").textContent = counts.risky || 0;

    // Criteria Alerts Box
    const alertsBox = document.getElementById("school-check-criteria-alerts");
    if (alertsBox) {
        if (alerts.length > 0) {
            alertsBox.innerHTML = alerts.map(a => `
                <div class="criteria-alert-item ${a.type === 'warning' ? 'criteria-alert-warning' : 'criteria-alert-info'}">
                    <i class="fa-solid ${a.type === 'warning' ? 'fa-triangle-exclamation' : 'fa-circle-info'}"></i>
                    <div>
                        <strong>${a.title}:</strong> ${a.detail}
                    </div>
                </div>
            `).join("");
            alertsBox.style.display = "flex";
        } else {
            alertsBox.style.display = "none";
        }
    }

    // Render danh sách ngành
    currentSchoolCheckFilter = "all";
    document.querySelectorAll(".btn-tier-tab").forEach(b => b.classList.remove("active"));
    const activeTab = document.getElementById("tab-tier-all");
    if (activeTab) activeTab.classList.add("active");

    renderTierMajorCards();

    // Mở modal
    const modal = document.getElementById("modal-school-check");
    if (modal) modal.classList.remove("hidden");
}

function filterSchoolCheckTier(tier) {
    currentSchoolCheckFilter = tier;
    document.querySelectorAll(".btn-tier-tab").forEach(b => b.classList.remove("active"));
    const tabEl = document.getElementById(`tab-tier-${tier}`);
    if (tabEl) tabEl.classList.add("active");
    renderTierMajorCards();
}

function renderTierMajorCards() {
    if (!currentSchoolCheckResult) return;
    const container = document.getElementById("school-check-majors-list");
    if (!container) return;

    const tiers = currentSchoolCheckResult.tiers || {};
    let listToRender = [];

    if (currentSchoolCheckFilter === "safe") {
        listToRender = tiers.safe || [];
    } else if (currentSchoolCheckFilter === "competitive") {
        listToRender = tiers.competitive || [];
    } else if (currentSchoolCheckFilter === "risky") {
        listToRender = tiers.risky || [];
    } else {
        listToRender = [...(tiers.safe || []), ...(tiers.competitive || []), ...(tiers.risky || [])];
    }

    if (listToRender.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #64748b;">
                <i class="fa-solid fa-folder-open" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                <p>Không có ngành nào trong phân tầng này.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = listToRender.map(m => {
        const isSafe = m.tier === "safe";
        const isComp = m.tier === "competitive";
        const diffText = m.score_difference >= 0 ? `+${m.score_difference.toFixed(2)}đ` : `${m.score_difference.toFixed(2)}đ`;
        const diffClass = isSafe ? "diff-positive" : (isComp ? "diff-neutral" : "diff-negative");
        const tierName = isSafe ? "🟢 Cửa đỗ cao (An toàn)" : (isComp ? "🟡 Cạnh tranh sát nút" : "🔴 Nguy cơ thử thách");

        return `
            <div class="tier-major-card card-${m.tier}">
                <div class="card-header-row">
                    <div>
                        <h5>${m.major_name}</h5>
                        <small style="color: #64748b; font-weight: 600;">Mã ngành: ${m.major_code} | Tổ hợp: <strong>${m.combination}</strong></small>
                    </div>
                    <span class="diff-badge ${diffClass}">${diffText}</span>
                </div>
                <div class="score-compare-bar">
                    <div>Điểm của bạn: <strong style="color: #1e1b4b;">${m.student_score.toFixed(2)}</strong></div>
                    <div>Điểm chuẩn 2025: <strong style="color: #4338ca;">${m.benchmark_2025.toFixed(2)}</strong></div>
                    <div>Xác suất: <strong style="color: #059669;">${m.admission_probability}%</strong></div>
                </div>
                <div style="font-size: 0.78rem; color: #475569; line-height: 1.35;">
                    <i class="fa-solid fa-circle-check text-primary"></i> ${tierName}
                </div>
                <div class="card-action-row">
                    <small style="color: #0284c7; font-weight: 600;"><i class="fa-solid fa-briefcase"></i> ${m.expected_salary}</small>
                    <button type="button" class="btn-card-interview" onclick="launchInterviewFromCheckModal('${m.major_code}')" title="Phỏng vấn thử với Đại diện tuyển sinh ngành này">
                        <i class="fa-solid fa-comments"></i> Phỏng Vấn Thử Ngành Này
                    </button>
                </div>
            </div>
        `;
    }).join("");
}

// 4. Khởi động buổi Phỏng Vấn Thử (AI Mock Interview)
function launchInterviewFromCheckModal(majorCode) {
    closeModal("modal-school-check");
    startSchoolInterview(currentSelectedSchool, majorCode);
}

async function startSchoolInterview(schoolCode, majorCode) {
    if (!schoolCode) schoolCode = currentSelectedSchool;

    try {
        const payload = {
            school_code: schoolCode,
            target_major_code: majorCode || null,
            student_data: {
                scores: currentSchoolCheckResult ? currentSchoolCheckResult.counts : {}
            }
        };

        const res = await fetch("/api/school-interview/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (json.status === "success") {
            currentInterviewSession = json.data;
            openInterviewModal(currentInterviewSession);
        }
    } catch (e) {
        console.error("Lỗi khởi tạo phỏng vấn:", e);
        alert("Không thể khởi tạo phòng phỏng vấn trực tuyến.");
    }
}

function openInterviewModal(session) {
    const persona = session.persona || {};

    // Header persona
    document.getElementById("interview-persona-avatar").textContent = persona.avatar || "🎓";
    document.getElementById("interview-persona-name").textContent = persona.name || "Thầy Đại diện Tuyển sinh";
    document.getElementById("interview-persona-school").textContent = persona.school || session.school_code;
    document.getElementById("interview-persona-role").textContent = persona.role || "Ban Tuyển sinh";
    document.getElementById("interview-persona-motto").textContent = `"${persona.motto || ''}"`;

    // Clear chat log
    const chatLog = document.getElementById("interview-chat-log");
    chatLog.innerHTML = "";

    // Reset Evaluation Report
    const reportBox = document.getElementById("interview-evaluation-report");
    if (reportBox) {
        reportBox.innerHTML = "";
        reportBox.classList.add("hidden");
    }

    // In câu chào và Câu hỏi 1
    appendChatMessage("bot", session.bot_message);

    // In Quick Replies
    renderQuickReplies(session.quick_replies || []);

    // Hiển thị modal
    const modal = document.getElementById("modal-school-interview");
    if (modal) modal.classList.remove("hidden");
}

function appendChatMessage(sender, text) {
    const chatLog = document.getElementById("interview-chat-log");
    if (!chatLog) return;

    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${sender === 'bot' ? 'chat-bubble-bot' : 'chat-bubble-user'}`;
    bubble.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    chatLog.appendChild(bubble);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function renderQuickReplies(replies) {
    const wrap = document.getElementById("interview-quick-replies-wrap");
    if (!wrap) return;

    if (!replies || replies.length === 0) {
        wrap.innerHTML = "";
        wrap.style.display = "none";
        return;
    }

    wrap.style.display = "flex";
    wrap.innerHTML = replies.map((r) => {
        const safeR = r.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        return `<button type="button" class="btn-quick-reply" onclick="sendInterviewAnswer('${safeR}')"><i class="fa-solid fa-reply"></i> ${r}</button>`;
    }).join("");
}

function handleInterviewKeydown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendInterviewAnswerFromInput();
    }
}

function sendInterviewAnswerFromInput() {
    const input = document.getElementById("interview-user-input");
    if (!input) return;
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendInterviewAnswer(text);
}

async function sendInterviewAnswer(answerText) {
    if (!currentInterviewSession) return;

    // 1. In tin nhắn của học sinh lên chat log
    appendChatMessage("user", answerText);

    // Ẩn quick replies tạm thời
    renderQuickReplies([]);

    // 2. Hiện typing indicator
    const typing = document.getElementById("interview-typing-indicator");
    if (typing) typing.classList.remove("hidden");

    try {
        const payload = {
            session_id: currentInterviewSession.session_id,
            school_code: currentInterviewSession.school_code,
            turn_index: currentInterviewSession.turn_index,
            user_answer: answerText,
            target_major_name: currentInterviewSession.target_major_name || "Ngành mục tiêu"
        };

        const res = await fetch("/api/school-interview/turn", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        const data = json.data;

        // Giả lập độ trễ đánh máy tự nhiên của Thầy/Cô (800ms)
        setTimeout(() => {
            if (typing) typing.classList.add("hidden");

            // In câu trả lời / câu hỏi tiếp theo của Thầy/Cô
            appendChatMessage("bot", data.bot_message);

            if (!data.is_finished) {
                // Cập nhật lượt
                currentInterviewSession.turn_index = data.turn_index;
                renderQuickReplies(data.quick_replies || []);
            } else {
                // Buổi phỏng vấn kết thúc -> Hiện Báo Cáo Đánh Giá Chung Cuộc
                renderEvaluationReport(data.evaluation_report);
            }
        }, 800);

    } catch (e) {
        console.error("Lỗi gửi câu trả lời phỏng vấn:", e);
        if (typing) typing.classList.add("hidden");
    }
}

// Render Bản Báo Cáo Đánh Giá Chung Cuộc (Fit Score & Tactical Recommendation)
function renderEvaluationReport(report) {
    const reportBox = document.getElementById("interview-evaluation-report");
    if (!reportBox || !report) return;

    window.lastInterviewReport = report;
    syncInterviewReportToOnPage(report);

    const tactical = report.tactical_recommendation || {};
    const strengths = report.strengths_observed || [];

    reportBox.innerHTML = `
        <div class="report-header-row">
            <div>
                <h4 style="color: #1e1b4b; font-weight: 800; margin: 0;">
                    <i class="fa-solid fa-award text-warning"></i> Bản Báo Cáo Nhận Xét Tuyển Sinh & Độ Phù Hợp
                </h4>
                <small style="color: #64748b;">Được xác nhận bởi Hội đồng Ban Tuyển sinh ${currentInterviewSession.persona?.school || ''}</small>
            </div>
            <div class="fit-score-box">
                <div style="text-align: right;">
                    <span style="font-size: 0.75rem; color: #047857; font-weight: 700;">ĐỘ PHÙ HỢP (FIT SCORE)</span>
                </div>
                <div class="fit-score-badge">${report.fit_score}%</div>
            </div>
        </div>

        <div style="font-size: 0.88rem; color: #1e293b; line-height: 1.55; margin-bottom: 0.85rem;">
            <strong>Nhận xét hồ sơ & phỏng vấn:</strong> ${report.candidate_evaluation}
        </div>

        <div style="margin-bottom: 0.85rem;">
            <strong style="font-size: 0.82rem; color: #4338ca;"><i class="fa-solid fa-star text-warning"></i> Điểm mạnh ghi nhận qua phỏng vấn:</strong>
            <ul style="margin: 0.35rem 0 0 1.25rem; font-size: 0.82rem; color: #334155;">
                ${strengths.map(s => `<li>${s}</li>`).join("")}
            </ul>
        </div>

        <div class="tactical-card">
            <div style="font-weight: 800; color: #15803d; margin-bottom: 0.35rem;">
                <i class="fa-solid fa-compass"></i> Chiến Thuật Đặt Nguyện Vọng Đề Xuất Chuẩn Bộ GD&ĐT:
            </div>
            <div style="margin-bottom: 0.35rem;">🎯 ${tactical.nv1_advice || ''}</div>
            <div>🛡️ ${tactical.nv2_backup || ''}</div>
        </div>

        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap;">
            <button type="button" class="btn-export-interview-web" onclick="exportInterviewReportToWeb()">
                <i class="fa-solid fa-arrow-down-to-bracket"></i> Xuất Báo Cáo Ra Web & Xem Chi Tiết
            </button>
            <button type="button" class="btn-primary" style="padding: 0.6rem 1.25rem; font-size: 0.85rem;" onclick="closeModal('modal-school-interview')">
                <i class="fa-solid fa-check"></i> Hoàn Tất & Đóng Chat
            </button>
        </div>
    `;

    reportBox.classList.remove("hidden");
    reportBox.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ==========================================================================
// CÁC HÀM XUẤT KẾT QUẢ THẨM ĐỊNH & PHỎNG VẤN RA GIAO DIỆN WEB (ON-PAGE)
// ==========================================================================

function syncSchoolCheckToOnPage(data) {
    if (!data) return;
    const card = document.getElementById("school-onpage-result-card");
    if (!card) return;

    const schoolInfo = data.school_info || {};
    const persona = data.persona || {};
    const counts = data.counts || {};
    const alerts = data.criteria_alerts || [];
    const allMajors = [
        ...(data.tiers?.safe || []),
        ...(data.tiers?.competitive || []),
        ...(data.tiers?.risky || [])
    ];

    // Header info
    const iconEl = document.getElementById("onpage-school-icon");
    const titleEl = document.getElementById("onpage-school-title");
    const codeBadgeEl = document.getElementById("onpage-school-code-badge");
    const subEl = document.getElementById("onpage-school-subtitle");

    if (iconEl) iconEl.textContent = persona.avatar || "🏛️";
    if (titleEl) titleEl.textContent = `Bản Thẩm Định Cửa Đỗ: ${schoolInfo.name || currentSelectedSchool}`;
    if (codeBadgeEl) codeBadgeEl.textContent = schoolInfo.code || currentSelectedSchool;
    if (subEl) subEl.textContent = `Tổng hợp ${counts.total || 0} ngành đào tạo • Học phí: ${schoolInfo.tuition_range || "Tiêu chuẩn"} • Đối chiếu điểm chuẩn 2025`;

    // Tier pills
    const pillsRow = document.getElementById("onpage-tier-pills");
    if (pillsRow) {
        pillsRow.innerHTML = `
            <div class="onpage-tier-pill pill-safe" onclick="openSchoolCheckModalWithFilter('safe')">
                <div>🟢 Cửa đỗ cao</div>
                <strong style="font-size: 1rem;">${counts.safe || 0} ngành</strong>
            </div>
            <div class="onpage-tier-pill pill-competitive" onclick="openSchoolCheckModalWithFilter('competitive')">
                <div>🟡 Cạnh tranh</div>
                <strong style="font-size: 1rem;">${counts.competitive || 0} ngành</strong>
            </div>
            <div class="onpage-tier-pill pill-risky" onclick="openSchoolCheckModalWithFilter('risky')">
                <div>🔴 Thử thách</div>
                <strong style="font-size: 1rem;">${counts.risky || 0} ngành</strong>
            </div>
        `;
    }

    // Criteria alert
    const alertBox = document.getElementById("onpage-criteria-alert");
    if (alertBox) {
        if (alerts.length > 0) {
            alertBox.innerHTML = `<strong><i class="fa-solid fa-triangle-exclamation"></i> Tiêu chí phụ/sàn:</strong> ${alerts.map(a => `${a.title} (${a.detail})`).join(" • ")}`;
            alertBox.classList.remove("hidden");
            alertBox.style.display = "block";
        } else {
            alertBox.innerHTML = `<strong><i class="fa-solid fa-circle-check text-success"></i> Tiêu chí xét tuyển:</strong> Bạn đáp ứng đầy đủ điều kiện nhận hồ sơ cơ bản của trường.`;
            alertBox.classList.remove("hidden");
            alertBox.style.display = "block";
        }
    }

    // Preview top 4 majors
    const majorsPreview = document.getElementById("onpage-majors-preview");
    if (majorsPreview) {
        const topDisplay = allMajors.slice(0, 5);
        majorsPreview.innerHTML = topDisplay.map(m => {
            const isSafe = m.tier === "safe";
            const isComp = m.tier === "competitive";
            const tagClass = isSafe ? "score-safe-tag" : (isComp ? "score-comp-tag" : "score-risk-tag");
            const tagText = isSafe ? `🟢 Đỗ cao (+${m.score_difference >= 0 ? m.score_difference.toFixed(1) : m.score_difference}đ)` : (isComp ? `🟡 Sát nút (${m.score_difference.toFixed(1)}đ)` : `🔴 Nguy cơ (${m.score_difference.toFixed(1)}đ)`);
            return `
                <div class="onpage-major-item">
                    <div>
                        <div class="onpage-major-title">${m.major_name}</div>
                        <small style="color: #64748b;">${m.combination} • Chuẩn '25: ${m.benchmark_2025.toFixed(1)}đ (Bạn: ${m.student_score.toFixed(1)}đ)</small>
                    </div>
                    <span class="onpage-major-score ${tagClass}">${tagText}</span>
                </div>
            `;
        }).join("");
    }

    card.classList.remove("hidden");
}

function syncInterviewReportToOnPage(report) {
    if (!report) return;
    const card = document.getElementById("school-onpage-result-card");
    if (card) card.classList.remove("hidden");

    const container = document.getElementById("onpage-interview-content");
    if (!container) return;

    const persona = currentInterviewSession?.persona || {};
    const tactical = report.tactical_recommendation || {};
    const strengths = report.strengths_observed || [];

    container.innerHTML = `
        <div class="onpage-interview-card">
            <div class="onpage-persona-row">
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                    <div class="onpage-persona-avatar">${persona.avatar || "👨‍🏫"}</div>
                    <div>
                        <strong style="color: #1e1b4b; font-size: 0.9rem;">${persona.name || "Đại diện Tuyển sinh"}</strong>
                        <div style="font-size: 0.75rem; color: #64748b;">${persona.role || "Ban Tuyển sinh"} • ${persona.school || currentSelectedSchool}</div>
                    </div>
                </div>
                <div class="fit-score-box">
                    <span style="font-size: 0.72rem; color: #047857; font-weight: 700;">FIT SCORE</span>
                    <div class="fit-score-badge" style="font-size: 1.1rem; padding: 0.2rem 0.6rem;">${report.fit_score}%</div>
                </div>
            </div>

            <div style="font-size: 0.82rem; color: #334155; line-height: 1.45;">
                ${report.candidate_evaluation}
            </div>

            <div style="font-size: 0.78rem; color: #4338ca;">
                <strong><i class="fa-solid fa-star text-warning"></i> Điểm mạnh:</strong> ${strengths.join(" • ")}
            </div>

            <div class="tactical-card" style="margin-top: 0.45rem; padding: 0.65rem; font-size: 0.8rem;">
                <div style="font-weight: 800; color: #15803d; margin-bottom: 0.25rem;">
                    <i class="fa-solid fa-compass"></i> Đề xuất chiến thuật đặt nguyện vọng:
                </div>
                <div>🎯 ${tactical.nv1_advice || ''}</div>
                <div style="margin-top: 0.2rem;">🛡️ ${tactical.nv2_backup || ''}</div>
            </div>

            <div style="margin-top: 0.45rem; display: flex; gap: 0.5rem;">
                <button type="button" class="btn-secondary btn-sm" style="flex: 1;" onclick="launchInterviewFromCheckModal()">
                    <i class="fa-solid fa-comments"></i> Phỏng vấn lại
                </button>
            </div>
        </div>
    `;
}

function exportSchoolCheckToWeb() {
    closeModal("modal-school-check");
    if (window.lastSchoolCheckData) {
        syncSchoolCheckToOnPage(window.lastSchoolCheckData);
    }
    const card = document.getElementById("school-onpage-result-card");
    if (card) {
        card.classList.remove("hidden");
        card.classList.remove("highlight-flash");
        void card.offsetWidth;
        card.classList.add("highlight-flash");
        card.scrollIntoView({ behavior: "smooth", block: "center" });
    }
}

function exportInterviewReportToWeb() {
    closeModal("modal-school-interview");
    if (window.lastInterviewReport) {
        syncInterviewReportToOnPage(window.lastInterviewReport);
    }
    const card = document.getElementById("school-onpage-result-card");
    if (card) {
        card.classList.remove("hidden");
        card.classList.remove("highlight-flash");
        void card.offsetWidth;
        card.classList.add("highlight-flash");
        card.scrollIntoView({ behavior: "smooth", block: "center" });
    }
}

function openSchoolCheckModalWithFilter(tier) {
    if (window.lastSchoolCheckData) {
        renderSchoolCheckModal(window.lastSchoolCheckData);
        filterSchoolCheckTier(tier);
        const modal = document.getElementById("modal-school-check");
        if (modal) modal.classList.remove("hidden");
    } else {
        triggerSchoolAdmissionCheck();
    }
}

function renderIntegratedSchoolConsultationCard() {
    const card = document.getElementById("school-integrated-consultation-card");
    if (!card) return;

    if (!window.lastSchoolCheckData && !window.lastInterviewReport && !currentSelectedSchool) {
        card.classList.add("hidden");
        return;
    }

    const schoolCode = currentSelectedSchool || window.lastSchoolCheckData?.school_info?.code || "BKHN";
    const schoolMeta = SCHOOL_METADATA[schoolCode] || {};
    const checkData = window.lastSchoolCheckData;
    const interview = window.lastInterviewReport;
    const counts = checkData?.counts || {};
    const fitScore = interview?.fit_score ? `${interview.fit_score}%` : "Chưa phỏng vấn";

    card.innerHTML = `
        <div class="school-integrated-header">
            <h4>
                <span>${schoolMeta.logo || '🏛️'}</span>
                <span>Thẩm Định Trường Mục Tiêu: ${schoolMeta.name || schoolCode} (${schoolCode})</span>
            </h4>
            <div style="display: flex; align-items: center; gap: 0.65rem;">
                <span class="badge-item" style="background: #ffffff; padding: 0.25rem 0.65rem; border-radius: 6px; font-weight: 700; color: #047857; font-size: 0.8rem;">
                    Culture Fit: <strong>${fitScore}</strong>
                </span>
                <button type="button" class="btn-secondary btn-sm" onclick="scrollToSchoolOnPage()">
                    <i class="fa-solid fa-eye"></i> Xem Chi Tiết Thẩm Định
                </button>
            </div>
        </div>
        <div style="font-size: 0.88rem; color: #1e293b; line-height: 1.55;">
            <strong>Khuyến nghị từ Hội đồng Cố vấn:</strong> Đối chiếu với kết quả học tập và năng lực thực tế, trường <strong>${schoolMeta.name || schoolCode}</strong> có <strong>${counts.safe || 0} ngành An Toàn</strong> và <strong>${counts.competitive || 0} ngành Cạnh Tranh</strong>.
            ${interview?.tactical_recommendation?.nv1_advice ? ` ${interview.tactical_recommendation.nv1_advice}` : ` Bạn nên ưu tiên xếp ngành thế mạnh của ${schoolCode} vào NV1 hoặc NV2.`}
        </div>
    `;
    card.classList.remove("hidden");
}

function scrollToSchoolOnPage() {
    const card = document.getElementById("school-onpage-result-card");
    if (card) {
        card.classList.remove("hidden");
        card.scrollIntoView({ behavior: "smooth", block: "center" });
        card.classList.add("highlight-flash");
    }
}


