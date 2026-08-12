from __future__ import annotations

import textwrap
from typing import Any

import streamlit as st

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

from streamlit_app.api_client import APIClient


def generate_pdf_report(
    summary: str,
    findings: list[str],
    recommendations: list[str],
) -> bytes:
    """Generate professional PDF report bytes using FPDF."""
    if FPDF is None:
        text_content = (
            "ADVANCED AI MEDICAL INTELLIGENCE PLATFORM\n"
            "AI-ASSISTED CHEST X-RAY DECISION SUPPORT REPORT\n\n"
            f"CLINICAL SUMMARY:\n{summary}\n\n"
            "KEY FINDINGS:\n" + "\n".join(f"- {f}" for f in findings) + "\n\n"
            "RECOMMENDATIONS:\n" + "\n".join(f"- {r}" for r in recommendations) + "\n\n"
            "Disclaimer: This AI-generated report is for decision support only and should not replace professional medical diagnosis."
        )
        return text_content.encode("utf-8")

    pdf = FPDF()
    pdf.add_page()

    # Title Header
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "ADVANCED AI MEDICAL INTELLIGENCE PLATFORM", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 8, "AI-ASSISTED CHEST X-RAY DECISION SUPPORT REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Clinical Summary Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "CLINICAL SUMMARY:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, summary)
    pdf.ln(5)

    # Key Findings Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "KEY FINDINGS:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    for f in findings:
        pdf.cell(0, 6, f"- {f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Recommendations Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "RECOMMENDATIONS:", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    for r in recommendations:
        pdf.cell(0, 6, f"- {r}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Disclaimer Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(
        0,
        5,
        "Disclaimer: This AI-generated report is for decision support only and should not replace professional medical diagnosis.",
    )

    return bytes(pdf.output())


def render_sidebar() -> str:
    """Render sidebar navigation menu, brand logo, platform status card, and logout button."""
    with st.sidebar:
        st.markdown(
            textwrap.dedent(
                """<div class="sidebar-brand">
<div class="sidebar-brand-icon">🫁</div>
<div>
<div class="sidebar-brand-title">AI Medical Intelligence<br>Platform</div>
</div>
</div>"""
            ),
            unsafe_allow_html=True,
        )

        default_index = 0
        if "nav_page" in st.session_state:
            options = [
                "Dashboard",
                "New Analysis",
                "History",
                "Patients",
                "Analytics",
                "Model Performance",
                "Settings",
                "API Docs",
                "About",
            ]
            if st.session_state["nav_page"] in options:
                default_index = options.index(st.session_state["nav_page"])

        selected_page = st.radio(
            "Navigation",
            options=[
                "Dashboard",
                "New Analysis",
                "History",
                "Patients",
                "Analytics",
                "Model Performance",
                "Settings",
                "API Docs",
                "About",
            ],
            index=default_index,
            key="sidebar_nav_radio",
            label_visibility="collapsed",
        )

        st.session_state["nav_page"] = selected_page

        st.markdown(
            textwrap.dedent(
                """<div class="sidebar-status-card">
<div class="sidebar-status-header">
<span class="status-dot-green"></span>
<span>Platform Status</span>
</div>
<div style="color: #4ade80; font-size: 11px; margin-bottom: 10px;">All systems operational</div>
<div style="color: #94a3b8; font-size: 11px; font-weight: 600;">Model v1.0.0</div>
<div style="color: #64748b; font-size: 10px; margin-top: 2px;">Last updated: May 24, 2025</div>
</div>

<div style="display: flex; align-items: center; gap: 10px; color: #94a3b8; padding: 12px 0; margin-top: 15px; font-size: 13px; cursor: pointer;">
<span>↪</span>
<span>Logout</span>
</div>"""
            ),
            unsafe_allow_html=True,
        )

        return selected_page


def render_top_bar(
    title: str = "Chest X-Ray Analysis",
    subtitle: str = "AI Powered Pneumonia Detection with Explainable AI & Medical Report Generation",
) -> None:
    """Render top bar header with page title, + New Analysis button, and user profile card."""
    col_left, col_right = st.columns([0.65, 0.35])

    with col_left:
        st.markdown(
            textwrap.dedent(
                f"""<div class="header-title-box">
<h1>{title}</h1>
<p>{subtitle}</p>
</div>"""
            ),
            unsafe_allow_html=True,
        )

    with col_right:
        c1, c2 = st.columns([0.5, 0.5])
        with c1:
            if st.button("+ New Analysis", key="btn_top_new_analysis"):
                st.session_state["nav_page"] = "New Analysis"
                st.rerun()

        with c2:
            st.markdown(
                textwrap.dedent(
                    """<div class="user-profile-card">
<div class="user-avatar">👨‍⚕️</div>
<div>
<div class="user-info-name">Dr. Alex Morgan</div>
<div class="user-info-role">Radiologist</div>
</div>
</div>"""
                ),
                unsafe_allow_html=True,
            )


def render_kpi_metrics(
    total_analyses: int = 248,
    pneumonia_cases: int = 112,
    model_accuracy: str = "94.6%",
    avg_response: str = "2.3s",
) -> None:
    """Render top 4 KPI metric cards matching the mockup."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            textwrap.dedent(
                f"""<div class="kpi-card">
<div class="kpi-icon-box kpi-icon-blue">📄</div>
<div>
<div class="kpi-title">Total Analyses</div>
<div class="kpi-value-row">
<div class="kpi-value">{total_analyses}</div>
<span class="kpi-badge kpi-badge-green">↑ 18.3%</span>
</div>
<div class="kpi-subtext">vs last month</div>
</div>
</div>"""
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            textwrap.dedent(
                f"""<div class="kpi-card">
<div class="kpi-icon-box kpi-icon-pink">🫁</div>
<div>
<div class="kpi-title">Pneumonia Cases</div>
<div class="kpi-value-row">
<div class="kpi-value">{pneumonia_cases}</div>
<span class="kpi-badge kpi-badge-green">↑ 14.2%</span>
</div>
<div class="kpi-subtext">vs last month</div>
</div>
</div>"""
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            textwrap.dedent(
                f"""<div class="kpi-card">
<div class="kpi-icon-box kpi-icon-green">🛡️</div>
<div>
<div class="kpi-title">Model Accuracy</div>
<div class="kpi-value-row">
<div class="kpi-value">{model_accuracy}</div>
<span class="kpi-badge kpi-badge-green">↑ 2.1%</span>
</div>
<div class="kpi-subtext">vs last month</div>
</div>
</div>"""
            ),
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            textwrap.dedent(
                f"""<div class="kpi-card">
<div class="kpi-icon-box kpi-icon-amber">⏱️</div>
<div>
<div class="kpi-title">Avg. Response Time</div>
<div class="kpi-value-row">
<div class="kpi-value">{avg_response}</div>
<span class="kpi-badge kpi-badge-green">↓ -0.6s</span>
</div>
<div class="kpi-subtext">vs last month</div>
</div>
</div>"""
            ),
            unsafe_allow_html=True,
        )


def render_uploaded_xray(
    image_file_path: str,
    filename: str = "patient_20250524_001.png",
    meta_info: str = "May 24, 2025 • 10:24 AM • 1024x1024",
) -> None:
    """Render Card 1: Uploaded X-Ray image display with filename tag bar."""
    st.markdown(
        textwrap.dedent(
            """<div class="ui-card-box">
<div class="ui-card-title">1. Uploaded X-Ray</div></div>"""
        ),
        unsafe_allow_html=True,
    )

    st.image(image_file_path, use_container_width=True)

    st.markdown(
        textwrap.dedent(
            f"""<div class="xray-file-bar">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 16px;">📄</span>
<div>
<div class="xray-filename">{filename}</div>
<div class="xray-meta">{meta_info}</div>
</div>
</div>
<div style="color: #ef4444; cursor: pointer;" title="Remove Image">🗑️</div>
</div>"""
        ),
        unsafe_allow_html=True,
    )


def render_prediction_card(result: dict[str, Any]) -> None:
    """Render Card 2: AI Prediction with probabilities, confidence score, and patient info grid."""
    prediction = str(result.get("prediction", "PNEUMONIA")).upper()
    confidence = float(result.get("confidence", 0.927))
    normal_prob = float(result.get("normal_probability", 0.073))
    pneumonia_prob = float(result.get("pneumonia_probability", 0.927))

    is_pneumonia = prediction == "PNEUMONIA"
    prediction_title = "Pneumonia Detected" if is_pneumonia else "Normal - No Pneumonia"
    status_class = "" if is_pneumonia else "normal"
    circle_icon = "🫁" if is_pneumonia else "✓"

    conf_percent = f"{confidence * 100:.1f}%"
    pne_percent = f"{pneumonia_prob * 100:.1f}%"
    norm_percent = f"{normal_prob * 100:.1f}%"

    patient_id = result.get("patient_id", "PT-2025-001")
    age = result.get("age", "45 Years")
    gender = result.get("gender", "Male")

    st.markdown(
        textwrap.dedent(
            f"""<div class="ui-card-box">
<div class="ui-card-title">
<span>2. AI Prediction</span>
<span class="badge-confidence-high">High Confidence</span>
</div>

<div class="prediction-result-box {status_class}">
<div class="prediction-circle-icon {status_class}">{circle_icon}</div>
<div>
<div class="prediction-text-title {status_class}">{prediction_title}</div>
<div class="prediction-text-sub">Confidence Score</div>
<div class="prediction-score-big">{conf_percent}</div>
</div>
</div>

<div class="progress-track-custom">
<div class="progress-fill-custom {status_class}" style="width: {conf_percent};"></div>
</div>
<div class="progress-labels-row">
<span>0%</span>
<span>50%</span>
<span>100%</span>
</div>

<div class="prob-section-box">
<div style="font-size: 11px; font-weight: 700; color: #cbd5e1; margin-bottom: 4px;">Prediction Probabilities</div>
<div class="prob-row">
<div class="prob-label">Pneumonia</div>
<div class="prob-bar-container"><div class="prob-bar-fill-pneumonia" style="width: {pne_percent};"></div></div>
<div class="prob-percent">{pne_percent}</div>
</div>
<div class="prob-row">
<div class="prob-label">Normal</div>
<div class="prob-bar-container"><div class="prob-bar-fill-normal" style="width: {norm_percent};"></div></div>
<div class="prob-percent">{norm_percent}</div>
</div>
</div>

<div class="patient-meta-grid">
<div class="patient-meta-item"><div class="patient-meta-label">Patient ID</div><div class="patient-meta-val">{patient_id}</div></div>
<div class="patient-meta-item"><div class="patient-meta-label">Age</div><div class="patient-meta-val">{age}</div></div>
<div class="patient-meta-item"><div class="patient-meta-label">Gender</div><div class="patient-meta-val">{gender}</div></div>
</div>
</div>"""
        ),
        unsafe_allow_html=True,
    )


def render_gradcam_card(
    xai_image_path: str,
    original_image_path: str = "",
) -> None:
    """Render Card 3: Grad-CAM Explanation with colorbar legend and CLICKABLE view buttons."""
    st.markdown(
        textwrap.dedent(
            """<div class="ui-card-box">
<div class="ui-card-title"><span>3. Grad-CAM Explanation</span></div></div>"""
        ),
        unsafe_allow_html=True,
    )

    current_mode = st.session_state.get("gradcam_view_mode", "Heatmap")

    display_img = xai_image_path
    if current_mode == "Original" and original_image_path:
        display_img = original_image_path

    col_img, col_bar = st.columns([0.88, 0.12])
    with col_img:
        st.image(display_img, use_container_width=True)

    with col_bar:
        st.markdown(
            textwrap.dedent(
                """<div class="gradcam-colorbar-legend">
<span>High Importance</span>
<div class="colorbar-gradient-bar"></div>
<span>Low Importance</span>
</div>"""
            ),
            unsafe_allow_html=True,
        )

    # CLICKABLE Interactive View Mode Buttons
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Heatmap", key="btn_heatmap"):
            st.session_state["gradcam_view_mode"] = "Heatmap"
            st.rerun()

    with b2:
        if st.button("Overlay", key="btn_overlay"):
            st.session_state["gradcam_view_mode"] = "Overlay"
            st.rerun()

    with b3:
        if st.button("Original", key="btn_original"):
            st.session_state["gradcam_view_mode"] = "Original"
            st.rerun()


def render_report_card(
    report: dict[str, Any] | str | None,
    client: APIClient | None = None,
) -> None:
    """Render AI-Assisted Medical Report with narrative, findings checkmarks, recommendations, disclaimer, and DOWNLOAD PDF button."""
    if report is None:
        report = {}

    if isinstance(report, str):
        summary = report
        findings = [
            "Opacities in lower lung zones",
            "Possible inflammatory infiltrates",
            "Right lower lobe involvement",
            "Recommend clinical correlation",
        ]
        recommendations = [
            "Clinical correlation",
            "Further examination",
            "Follow-up imaging",
            "Consult pulmonologist",
        ]
    else:
        summary = report.get(
            "summary",
            "The chest X-ray indicates findings consistent with pneumonia. There are prominent opacities observed in the lower lung zones, especially in the right lower lobe, which may represent inflammatory infiltrates. Clinical correlation is recommended along with further examination.",
        )
        findings = report.get("findings", []) or [
            "Opacities in lower lung zones",
            "Possible inflammatory infiltrates",
            "Right lower lobe involvement",
            "Recommend clinical correlation",
        ]
        recommendations = report.get("recommendations", []) or [
            "Clinical correlation",
            "Further examination",
            "Follow-up imaging",
            "Consult pulmonologist",
        ]

    findings_html = "".join(
        f'<div class="report-item-row"><span class="icon-check-green">✓</span><span>{item}</span></div>'
        for item in findings
    )

    recommendations_html = "".join(
        f'<div class="report-item-row"><span class="icon-doctor-blue">👤</span><span>{item}</span></div>'
        for item in recommendations
    )

    st.markdown(
        textwrap.dedent(
            f"""<div class="ui-card-box">
<div class="ui-card-title"><span>✦ AI-Assisted Medical Report</span></div>
<div class="report-narrative">{summary}</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
<div>
<div class="report-section-title">Key Findings</div>
{findings_html}
</div>
<div>
<div class="report-section-title">Recommendations</div>
{recommendations_html}
</div>
</div>
<div class="report-disclaimer-banner">
<strong>Disclaimer:</strong> This AI-generated report is for decision support only and should not replace professional medical diagnosis.
</div>
</div>"""
        ),
        unsafe_allow_html=True,
    )

    # DOWNLOADABLE REPORT BUTTON IN PDF FORMAT
    pdf_bytes = generate_pdf_report(summary, findings, recommendations)
    st.download_button(
        label="📥 Download Medical Report (.pdf)",
        data=pdf_bytes,
        file_name="Medical_Report_PT-2025-001.pdf",
        mime="application/pdf",
        key="btn_download_pdf_report_file",
    )


def render_recent_analyses(history: list[dict[str, Any]] | None) -> None:
    """Render Recent Analyses list card with CLICKABLE 'View All' button."""
    col_t1, col_t2 = st.columns([0.7, 0.3])
    with col_t1:
        st.markdown(
            textwrap.dedent(
                """<div class="ui-card-box" style="margin-bottom: 0;">
<div class="ui-card-title" style="margin-bottom: 0;">
<span>Recent Analyses</span>
</div></div>"""
            ),
            unsafe_allow_html=True,
        )
    with col_t2:
        if st.button("View All", key="btn_view_all_recent"):
            st.session_state["nav_page"] = "History"
            st.rerun()

    st.markdown('<div class="ui-card-box" style="margin-top: 10px;">', unsafe_allow_html=True)

    if not history:
        demo_items = [
            {"patient_id": "PT-2025-001", "date": "May 24, 2025 • 10:24 AM", "prediction": "Pneumonia", "conf": "92.7%"},
            {"patient_id": "PT-2025-002", "date": "May 24, 2025 • 09:15 AM", "prediction": "Normal", "conf": "8.3%"},
            {"patient_id": "PT-2025-003", "date": "May 23, 2025 • 04:22 PM", "prediction": "Pneumonia", "conf": "88.1%"},
        ]
        for item in demo_items:
            badge_cls = "badge-recent-pneumonia" if item["prediction"] == "Pneumonia" else "badge-recent-normal"
            st.markdown(
                textwrap.dedent(
                    f"""<div class="recent-item-card">
<div class="recent-item-left">
<div class="recent-thumb-icon">🫁</div>
<div>
<div class="recent-patient-id">{item['patient_id']}</div>
<div class="recent-date-sub">{item['date']}</div>
</div>
</div>
<div style="display: flex; align-items: center; gap: 6px;">
<span class="{badge_cls}">{item['prediction']}</span>
<span style="font-weight: 700; color: #f8fafc;">{item['conf']}</span>
<span style="color: #64748b;">›</span>
</div>
</div>"""
                ),
                unsafe_allow_html=True,
            )
    else:
        for item in history[:5]:
            pred = str(item.get("predicted_class", "UNKNOWN")).upper()
            is_pne = pred == "PNEUMONIA"
            badge_cls = "badge-recent-pneumonia" if is_pne else "badge-recent-normal"
            label = "Pneumonia" if is_pne else "Normal"
            conf_val = float(item.get("confidence", 0.0)) * 100

            st.markdown(
                textwrap.dedent(
                    f"""<div class="recent-item-card">
<div class="recent-item-left">
<div class="recent-thumb-icon">🫁</div>
<div>
<div class="recent-patient-id">{item.get('image_filename', 'PT-2025-001')}</div>
<div class="recent-date-sub">{str(item.get('created_at', ''))[:16]}</div>
</div>
</div>
<div style="display: flex; align-items: center; gap: 6px;">
<span class="{badge_cls}">{label}</span>
<span style="font-weight: 700; color: #f8fafc;">{conf_val:.1f}%</span>
<span style="color: #64748b;">›</span>
</div>
</div>"""
                ),
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def render_bottom_upload_banner() -> None:
    """Render bottom cloud banner matching the original UI design mockup."""
    st.markdown(
        textwrap.dedent(
            """<div class="upload-banner-container">
<div class="upload-banner-left">
<div class="upload-cloud-icon-box">☁️</div>
<div>
<div class="upload-banner-title">Upload New Chest X-Ray</div>
<div class="upload-banner-sub">Drag and drop an image here, or click to browse</div>
<div class="upload-banner-types">Supports: JPG, PNG, WEBP • Max size: 10MB</div>
</div>
</div>
</div>"""
        ),
        unsafe_allow_html=True,
    )


def render_header(title: str = "Chest X-Ray Analysis", subtitle: str = "AI Powered Pneumonia Detection") -> None:
    render_top_bar(title=title, subtitle=subtitle)


def render_metric(title: str, value: Any, delta: str = "", icon: str = "▣") -> None:
    pass


def render_prediction(result: dict[str, Any]) -> None:
    render_prediction_card(result)


def render_report(report: dict[str, Any] | str | None) -> None:
    render_report_card(report)


def render_upload_section() -> None:
    render_bottom_upload_banner()


def render_history(history: list[dict[str, Any]] | None) -> None:
    render_recent_analyses(history)