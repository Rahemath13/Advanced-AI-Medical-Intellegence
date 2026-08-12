import streamlit as st


def load_css() -> None:
    st.markdown(
        """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(37, 99, 235, 0.12), transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.08), transparent 40%),
                #070c1e !important;
    color: #f8fafc;
}

.block-container {
    max-width: 1600px !important;
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #090f23 !important;
    border-right: 1px solid rgba(56, 189, 248, 0.12) !important;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 8px 20px 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 15px;
}

.sidebar-brand-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 15px rgba(37, 99, 235, 0.4);
}

.sidebar-brand-title {
    font-size: 14px;
    font-weight: 700;
    line-height: 1.2;
    color: #f8fafc;
}

.sidebar-status-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 14px;
    padding: 14px;
    margin-top: 25px;
    font-size: 12px;
}

.sidebar-status-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 4px;
}

.status-dot-green {
    width: 8px;
    height: 8px;
    background-color: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 8px #22c55e;
}

/* TOP HEADER */
.top-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.header-title-box h1 {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    color: #f8fafc;
}

.header-title-box p {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 2px;
    margin-bottom: 0;
}

.user-profile-card {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #0d1630;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 14px 6px 6px;
    border-radius: 999px;
}

.user-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #3b82f6;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

.user-info-name {
    font-size: 12px;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.1;
}

.user-info-role {
    font-size: 10px;
    color: #64748b;
}

/* METRIC CARDS */
.kpi-card {
    background: linear-gradient(145deg, #0d1630, #090f23);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 16px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
    margin-bottom: 15px;
}

.kpi-icon-box {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.kpi-icon-blue { background: rgba(37, 99, 235, 0.18); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); }
.kpi-icon-pink { background: rgba(244, 63, 94, 0.18); color: #fb7185; border: 1px solid rgba(251, 113, 133, 0.3); }
.kpi-icon-green { background: rgba(34, 197, 94, 0.18); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); }
.kpi-icon-amber { background: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }

.kpi-title { font-size: 12px; color: #94a3b8; font-weight: 500; }
.kpi-value-row { display: flex; align-items: baseline; gap: 8px; margin-top: 2px; }
.kpi-value { font-size: 24px; font-weight: 800; color: #f8fafc; }
.kpi-badge { font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 999px; }
.kpi-badge-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.kpi-subtext { font-size: 10px; color: #64748b; }

/* UI CARD CONTAINERS */
.ui-card-box {
    background: linear-gradient(145deg, #0d1630, #090f23);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    margin-bottom: 16px;
}

.ui-card-title {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}

.badge-confidence-high {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.3);
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
}

/* X-RAY FILE BAR */
.xray-file-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #070d1e;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 14px;
    margin-top: 12px;
}

.xray-filename { font-size: 12px; font-weight: 600; color: #f8fafc; }
.xray-meta { font-size: 10px; color: #64748b; }

/* PREDICTION RESULT BOX */
.prediction-result-box {
    background: rgba(244, 63, 94, 0.08);
    border: 1px solid rgba(244, 63, 94, 0.2);
    border-radius: 14px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
}

.prediction-result-box.normal {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.2);
}

.prediction-circle-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(244, 63, 94, 0.2);
    color: #fb7185;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
}

.prediction-circle-icon.normal {
    background: rgba(34, 197, 94, 0.2);
    color: #4ade80;
}

.prediction-text-title { font-size: 20px; font-weight: 800; color: #fb7185; line-height: 1.1; }
.prediction-text-title.normal { color: #4ade80; }
.prediction-text-sub { font-size: 11px; color: #94a3b8; margin-top: 2px; }
.prediction-score-big { font-size: 24px; font-weight: 800; color: #f8fafc; }

.progress-track-custom {
    width: 100%;
    height: 8px;
    border-radius: 999px;
    background: #070d1e;
    overflow: hidden;
    margin-top: 6px;
}

.progress-fill-custom {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ef4444, #fb7185);
}

.progress-fill-custom.normal {
    background: linear-gradient(90deg, #16a34a, #4ade80);
}

.progress-labels-row {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #64748b;
    margin-top: 4px;
    margin-bottom: 14px;
}

.prob-section-box {
    background: #070d1e;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 14px;
}

.prob-row { display: flex; align-items: center; gap: 10px; margin-top: 8px; }
.prob-label { width: 75px; font-size: 12px; font-weight: 600; color: #cbd5e1; }
.prob-bar-container { flex: 1; height: 8px; border-radius: 999px; background: #0f172a; overflow: hidden; }
.prob-bar-fill-pneumonia { height: 100%; border-radius: 999px; background: #fb7185; }
.prob-bar-fill-normal { height: 100%; border-radius: 999px; background: #4ade80; }
.prob-percent { width: 40px; text-align: right; font-size: 12px; font-weight: 700; color: #f8fafc; }

.patient-meta-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.patient-meta-item { background: #070d1e; border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 8px; font-size: 10px; }
.patient-meta-label { color: #64748b; }
.patient-meta-val { font-size: 12px; font-weight: 700; color: #f8fafc; margin-top: 2px; }

/* GRAD-CAM COLORBAR */
.gradcam-wrapper { display: flex; gap: 12px; align-items: center; }
.gradcam-colorbar-legend { width: 30px; height: 210px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; font-size: 9px; color: #94a3b8; }
.colorbar-gradient-bar { width: 8px; flex: 1; margin: 4px 0; border-radius: 999px; background: linear-gradient(180deg, #ef4444 0%, #fbbf24 40%, #3b82f6 100%); }

/* REPORT */
.report-narrative {
    font-size: 12px;
    line-height: 1.6;
    color: #cbd5e1;
    background: #070d1e;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.report-section-title { font-size: 12px; font-weight: 700; color: #f8fafc; margin-bottom: 8px; }
.report-item-row { display: flex; align-items: center; gap: 8px; font-size: 11px; color: #cbd5e1; margin-bottom: 6px; }
.icon-check-green { color: #4ade80; font-weight: 800; }
.icon-doctor-blue { color: #38bdf8; }

.report-disclaimer-banner {
    font-size: 10px;
    color: #64748b;
    background: rgba(15, 23, 42, 0.8);
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.04);
    margin-top: 14px;
}

/* RECENT LIST */
.recent-item-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #070d1e;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 11px;
}

.recent-item-left { display: flex; align-items: center; gap: 10px; }
.recent-thumb-icon { width: 32px; height: 32px; border-radius: 8px; background: #1e293b; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.recent-patient-id { font-weight: 700; color: #f8fafc; }
.recent-date-sub { font-size: 9px; color: #64748b; margin-top: 1px; }

.badge-recent-pneumonia { background: rgba(244, 63, 94, 0.15); color: #fb7185; padding: 3px 6px; border-radius: 999px; font-weight: 700; font-size: 10px; }
.badge-recent-normal { background: rgba(34, 197, 94, 0.15); color: #4ade80; padding: 3px 6px; border-radius: 999px; font-weight: 700; font-size: 10px; }

/* UPLOAD BANNER & CARD OVERLAY */
.card-upload-overlay-wrapper {
    position: relative;
    margin-top: 15px;
    margin-bottom: 20px;
    cursor: pointer;
}

.upload-banner-container {
    background: linear-gradient(145deg, #0d1630, #090f23);
    border: 2px dashed rgba(56, 189, 248, 0.3);
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.2s ease;
}

.card-upload-overlay-wrapper:hover .upload-banner-container {
    border-color: #38bdf8;
    background: linear-gradient(145deg, #0f1e42, #0c1633);
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
}

.upload-banner-left { display: flex; align-items: center; gap: 16px; }
.upload-cloud-icon-box { width: 48px; height: 48px; border-radius: 14px; background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #38bdf8; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.upload-banner-title { font-size: 15px; font-weight: 700; color: #f8fafc; }
.upload-banner-sub { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.upload-banner-types { font-size: 10px; color: #64748b; margin-top: 2px; }

.card-upload-overlay-wrapper div[data-testid="stFileUploader"] {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
    cursor: pointer !important;
    z-index: 10 !important;
}

.card-upload-overlay-wrapper div[data-testid="stFileUploader"] section {
    width: 100% !important;
    height: 100% !important;
    min-height: 90px !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
    cursor: pointer !important;
}

/* CUSTOM VIEW BUTTONS */
div.stButton > button {
    width: 100%;
    border-radius: 10px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 6px 12px !important;
    background: #070d1e !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #94a3b8 !important;
    box-shadow: none !important;
}

div.stButton > button:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
}

div.stButton > button[data-testid="baseButton-secondaryActive"],
div.stButton > button:focus {
    background: rgba(37, 99, 235, 0.25) !important;
    border-color: #3b82f6 !important;
    color: #38bdf8 !important;
}

# HIDE HEADER/FOOTER CLEANUP
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>""",
        unsafe_allow_html=True,
    )


def apply_custom_styles() -> None:
    """Alias for load_css."""
    load_css()