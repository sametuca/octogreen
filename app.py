import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from modules import ai_analysis, report_tools, open_data, ui_utils, translations

# Page Config
st.set_page_config(
    page_title="OctoGreen",
    layout="wide",
    page_icon="assets/logo.png",
    initial_sidebar_state="collapsed"
)

# Apply CSS - Wrapped in hidden div to prevent display
st.markdown(f"""
<div style="display: none;">
{ui_utils.CUSTOM_CSS}
</div>
""", unsafe_allow_html=True)

# Also inject directly for backup
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-gradient: linear-gradient(135deg, #eff6ff 0%, #dbeafe 50%, #bfdbfe 100%);
    --text-primary: #1e3a8a;
    --text-secondary: #1e40af;
    --accent: #3b82f6;
    --accent-dark: #2563eb;
    --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    --success-gradient: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    --card-bg: rgba(255, 255, 255, 0.95);
}

/* Force Light Theme with Blue Tones */
html, body, .stApp {
    background: var(--bg-gradient) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Segoe UI', 'Helvetica Neue', 'Segoe UI', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

/* Typography - SF Pro Style */
h1, h2, h3 {
    text-align: center !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 2rem !important;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

p {
    font-size: 1.05rem !important;
    line-height: 1.6 !important;
    color: var(--text-secondary) !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* Container */
.block-container {
    max-width: 1400px !important;
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}


/* Hero Box - Modern Minimalist */
.hero-box {
    text-align: center;
    padding: 2.5rem 1.5rem 3rem;
    margin: 2rem auto 3rem;
    max-width: 800px;
    position: relative;
}

.hero-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 120px;
    height: 4px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
    border-radius: 2px;
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.hero-subtitle {
    font-size: 1.4rem !important;
    background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 1.5rem !important;
    font-weight: 600 !important;
    line-height: 1.5 !important;
    letter-spacing: -0.02em;
}



/* Premium Modern Buttons */
div.stButton > button {
    width: 100%;
    background: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 2.5rem 2rem !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: visible !important;
    letter-spacing: -0.02em !important;
}

/* Gradient accent bar on top of button */
div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    border-radius: 0 0 2px 2px;
    opacity: 0;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    border-color: #3b82f6 !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15) !important;
    transform: translateY(-2px);
}

div.stButton > button:hover::before {
    opacity: 1;
    width: 100px;
}

div.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1) !important;
}


/* Info Cards - Blue Glassmorphism */
.info-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(15px);
    border: 2px solid rgba(59, 130, 246, 0.2);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
    transition: all 0.3s ease;
}

.info-card:hover {
    box-shadow: 0 10px 35px rgba(59, 130, 246, 0.18);
    border-color: rgba(59, 130, 246, 0.4);
}

.info-card h4 {
    text-align: left !important;
    color: var(--accent) !important;
    font-size: 1.1rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.info-card p,
.info-card strong,
.info-card span,
.info-card div {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.metric-value {
    font-size: 3rem;
    font-weight: 800;
    background: var(--success-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.5rem 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.metric-label {
    color: var(--text-secondary) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Inputs - Blue Theme */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"],
input {
    background-color: white !important;
    color: var(--text-primary) !important;
    border: 2px solid rgba(59, 130, 246, 0.25) !important;
    border-radius: 14px !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08) !important;
    transition: all 0.3s ease !important;
    padding: 0.75rem 1rem !important;
}

/* Selectbox - Clean & Professional */
div[data-baseweb="select"] > div:first-child {
    background-color: white !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    border-radius: 12px !important;
    padding: 6px 12px !important;
    box-shadow: 0 2px 6px rgba(59, 130, 246, 0.05) !important;
    transition: all 0.2s ease;
}

div[data-baseweb="select"] > div:first-child:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1) !important;
}

/* Fix text color inside selectbox - generic catch-all */
div[data-baseweb="select"] span, 
div[data-baseweb="select"] div,
[data-baseweb="menu"] div,
[data-baseweb="menu"] span {
    color: #1e3a8a !important; 
    font-size: 1rem !important;
    font-weight: 500 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Dropdown Menu (Popover) */
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background-color: white !important;
    border: 1px solid rgba(59, 130, 246, 0.2) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
}

div[data-baseweb="option"] {
    background-color: transparent !important;
}

div[data-baseweb="option"]:hover,
div[data-baseweb="option"][aria-selected="true"] {
    background-color: #eff6ff !important;
    font-weight: 600 !important;
}

/* Adjust label styling */
.stSelectbox label p {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.5rem !important;
}

/* Remove default streamlit borders if they appear on wrapper */
.stSelectbox > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Date inputs */
.stDateInput > div > div {
    background-color: white !important;
    border: 2px solid rgba(59, 130, 246, 0.25) !important;
    border-radius: 12px !important;
    padding: 0.5rem 0.75rem !important;
}

/* Text inputs */
.stTextInput > div > div {
    background-color: white !important;
    border: 2px solid rgba(59, 130, 246, 0.25) !important;
    border-radius: 12px !important;
    padding: 0.5rem 0.75rem !important;
}

/* Expander - Premium Button Style */
.streamlit-expanderHeader,
[data-testid="stExpander"] > div:first-child,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.25) !important;
    transition: all 0.3s ease !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-testid="stExpander"] summary {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    cursor: pointer !important;
}

[data-testid="stExpander"] summary:hover {
    box-shadow: 0 6px 25px rgba(59, 130, 246, 0.35) !important;
}

[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p,
.streamlit-expanderHeader span,
.streamlit-expanderHeader p {
    color: white !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-testid="stExpander"] svg,
.streamlit-expanderHeader svg {
    fill: white !important;
    color: white !important;
}

/* Hide material icon text artifacts */
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p:empty,
.streamlit-expanderHeader svg text {
    display: none !important;
}


/* DataFrames - Blue Theme */
[data-testid="stDataFrame"] {
    background-color: white !important;
    color: var(--text-primary) !important;
    border: 2px solid rgba(59, 130, 246, 0.2);
    border-radius: 12px;
}

[data-testid="stDataFrame"] div[role="grid"],
[data-testid="stDataFrame"] div[role="columnheader"] {
    color: var(--text-primary) !important;
    background-color: #eff6ff !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Plotly Charts */
.js-plotly-plot .plotly .modebar {
    background-color: transparent !important;
}
.js-plotly-plot .plotly .modebar-btn {
    background-color: transparent !important;
}
.js-plotly-plot .plotly .modebar-btn path {
    fill: #1e40af !important;
}
.js-plotly-plot .plotly .modebar-btn:hover path {
    fill: #3b82f6 !important;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeScale {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

div.stButton > button {
    animation: fadeScale 0.6s ease-out forwards;
    animation-delay: 0.2s;
    opacity: 0;
}

.info-card {
    animation: fadeInUp 0.7s ease-out forwards;
    opacity: 0;
    animation-delay: 0.3s;
}

div[data-testid="stImage"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    animation: fadeScale 0.8s ease-out;
}

/* Status widgets */
div[data-testid="stStatusWidget"] {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid rgba(59, 130, 246, 0.2) !important;
    border-radius: 12px !important;
}

/* Success/Info boxes */
.stSuccess {
    background-color: #dbeafe !important;
    color: var(--text-primary) !important;
    border-left: 4px solid var(--accent) !important;
}

/* ===== METRICS - FORCE SF PRO FONT ===== */
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stMetricDelta"],
.stMetric,
[data-testid="stMetric"],
[data-testid="stMetric"] *,
[data-testid="stMetricValue"] *,
[data-testid="stMetricLabel"] *,
[data-testid="stMetricDelta"] * {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Segoe UI', sans-serif !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] span,
[data-testid="stMetricValue"] p {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] div,
[data-testid="stMetricLabel"] span,
[data-testid="stMetricLabel"] p {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Button text - force SF Pro */
div.stButton > button,
div.stButton > button span,
div.stButton > button p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Checkbox - Premium Style like Performance Insights heading */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] label span,
[data-testid="stCheckbox"] label p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #0071e3 !important;
    letter-spacing: -0.01em !important;
}

[data-testid="stCheckbox"] > label {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    padding: 0.75rem 1rem !important;
    background: rgba(59, 130, 246, 0.05) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(59, 130, 246, 0.15) !important;
    cursor: pointer !important;
}

[data-testid="stCheckbox"] > label:hover {
    background: rgba(59, 130, 246, 0.1) !important;
    border-color: rgba(59, 130, 246, 0.3) !important;
}

/* Caption text under buttons */
.stCaption, .stCaption p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    color: var(--text-secondary) !important;
}

/* Info card content */
.info-card p,
.info-card strong,
.info-card span {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Download buttons - special styling */
div.stDownloadButton > button,
div.stDownloadButton > button span,
div.stDownloadButton > button p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-weight: 600 !important;
}

/* All button text - comprehensive coverage */
button,
button span,
button p,
button div,
[role="button"],
[role="button"] span,
[role="button"] p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}


</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)
# Session State Initialization
if 'data_mode' not in st.session_state:
    st.session_state.data_mode = None  # 'open_data' or 'upload'
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default language

def reset_app():
    for key in ['df', 'analysis', 'data_mode']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def t(key):
    """Translation helper function"""
    return translations.get_text(key, st.session_state.language)

# --- HEADER / HERO SECTION ---
def render_hero():
    # Language selector at top right
    col_lang1, col_lang2, col_lang3 = st.columns([4, 1, 1])
    with col_lang3:
        available_langs = translations.get_available_languages()
        selected_lang = st.selectbox(
            "Language",
            options=list(available_langs.keys()),
            format_func=lambda x: available_langs[x],
            index=list(available_langs.keys()).index(st.session_state.language),
            key="language_selector",
            label_visibility="collapsed"
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
    
    # Logo'yu tam ortaya almak için daha geniş orta kolon
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.image("assets/octogreen-logo.png", width=400)
        except:
            st.markdown(f"<h1 style='text-align: center;'>{t('app_title')}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="hero-box">
            <p class="hero-subtitle">{t('hero_subtitle')}<br><span style="font-size: 0.95rem; color: #64748b;">{t('hero_description')}</span></p>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN SELECTION SCREEN ---
# --- MAIN SELECTION SCREEN ---
def render_selection_screen():
    # Page Transition Animations
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main-menu-container {
        animation: fadeIn 0.5s ease-out forwards;
    }
    .sub-page-container {
        animation: fadeIn 0.4s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 1. MAIN MENU STATE (No selection yet)
    if st.session_state.data_mode is None:
        st.markdown('<div class="main-menu-container">', unsafe_allow_html=True)
        render_hero()
        
        # Centered Navigation Grid
        col_space_l, col1, col2, col_space_r = st.columns([1, 2, 2, 1], gap="large")
        
        with col1:
             if st.button(t("browse_open_data"), key="btn_open_data", use_container_width=True):
                st.session_state.data_mode = 'open_data'
                st.rerun()
             st.caption(t("open_data_desc"))

        with col2:
             if st.button(t("upload_your_own"), key="btn_upload", use_container_width=True):
                st.session_state.data_mode = 'upload'
                st.rerun()
             st.caption(t("upload_desc"))
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. OPEN DATA PAGE
    elif st.session_state.data_mode == 'open_data':
        st.markdown('<div class="sub-page-container">', unsafe_allow_html=True)
        
        # Header with Back Button
        c_back, c_title = st.columns([0.5, 4])
        with c_back:
            if st.button("←", key="back_btn_open", help="Back to Menu"):
                st.session_state.data_mode = None
                st.rerun()
        with c_title:
             st.markdown(f"<h2 style='margin:0; padding-top:5px;'>{t('select_dataset')}</h2>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin-top:0.5rem; margin-bottom:2rem; opacity:0.3;'>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_opts, col_detais = st.columns([1.2, 0.8], gap="large")
        
        with col_opts:
            source = st.selectbox(t("choose_source"), [
                "UCI Household (2M+ records)",
                "EPIAS Turkey (Real-time)",
                "World Bank - Energy & Carbon",
                "IEA - Global Energy Data",
                "US EIA - Electricity Stats",
                "Eurostat - EU Energy",
                "UK National Grid - Carbon Intensity",
                "WRI - Global Power Plants"
            ], index=0)
            

            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action Area
            if "UCI Household" in source:
                if st.button(t("download_analyze"), key="dl_uci", width="stretch"):
                    with st.status(t("processing_data"), expanded=True) as status:
                        st.write(t("connecting"))
                        time.sleep(0.5)
                        st.write(t("downloading"))
                        st.session_state.df = open_data.fetch_kaggle_household()
                        st.write(t("running_analysis"))
                        time.sleep(0.5)
                        status.update(label=t("ready"), state="complete", expanded=False)
                    st.rerun()

            elif "EPIAS Turkey" in source:
                c1, c2 = st.columns(2)
                with c1:
                    start = st.date_input(t("start_date"), datetime.now() - timedelta(days=7))
                with c2:
                    end = st.date_input(t("end_date"), datetime.now())
                
                if st.button(t("fetch_live_data"), key="dl_epias", width="stretch"):
                    with st.spinner(t("fetching_live")):
                        df = open_data.fetch_epias_data(start, end)
                        if df is not None:
                            st.session_state.df = df
                            st.rerun()
                        else:
                            st.error(t("failed_epias"))
            
            elif "World Bank" in source:
                 if st.button(t("fetch_world_bank"), key="dl_wb", width="stretch"):
                    with st.spinner(t("accessing_wb")):
                        energy_df = open_data.fetch_world_bank_energy()
                        if energy_df is not None:
                            df = energy_df.copy()
                            df["timestamp"] = pd.to_datetime(df["year"], format="%Y")
                            df["device_id"] = df["country"]
                            df["consumption_kWh"] = df["consumption_kwh_per_capita"]
                            st.session_state.df = df[["timestamp", "device_id", "consumption_kWh"]].dropna()
                            st.rerun()
            
            elif "IEA" in source:
                if st.button(t("fetch_iea"), key="dl_iea", width="stretch"):
                    with st.spinner(t("accessing_iea")):
                        df = open_data.fetch_iea_global_energy()
                        if df is not None:
                            st.session_state.df = df
                            st.rerun()
                        else:
                            st.error(t("failed_iea"))
            
            elif "US EIA" in source:
                if st.button(t("fetch_us_data"), key="dl_eia", width="stretch"):
                    with st.spinner(t("accessing_eia")):
                        df = open_data.fetch_us_eia_electricity()
                        if df is not None:
                            st.session_state.df = df
                            st.rerun()
                        else:
                            st.error(t("failed_eia"))
            
            elif "Eurostat" in source:
                if st.button(t("fetch_eu_data"), key="dl_eurostat", width="stretch"):
                    with st.spinner(t("accessing_eurostat")):
                        df = open_data.fetch_eurostat_energy()
                        if df is not None:
                            st.session_state.df = df
                            st.rerun()
                        else:
                            st.error(t("failed_eurostat"))
                            
            elif "UK National Grid" in source:
                if st.button(t("fetch_uk_carbon"), key="dl_uk", width="stretch"):
                    with st.spinner("Fetching UK Carbon Data..."):
                       df = open_data.fetch_uk_carbon_intensity()
                       if df is not None:
                           st.session_state.df = df
                           st.rerun()
                       else:
                           st.error("Failed to fetch UK data")

            elif "WRI" in source:
                if st.button(t("fetch_power_plants"), key="dl_wri", width="stretch"):
                     with st.spinner("Fetching Global Power Plants..."):
                        df = open_data.fetch_global_power_plants()
                        if df is not None:
                            st.session_state.df = df
                            st.rerun()
                        else:
                            st.error("Failed to fetch Power Plant data")

        with col_detais:
            if "UCI Household" in source:
                st.markdown(f"""
                <div class="info-card">
                    <h4>{t('dataset_snapshot')}</h4>
                    <div class="metric-value">2M+</div>
                    <p>{t('individual_records')}</p>
                    <div style="margin-top:1rem; border-top:2px solid rgba(59, 130, 246, 0.2); padding-top:1rem;">
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('contains')}</strong><br>{t('uci_contains')}</p>
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('best_for')}</strong><br>{t('uci_best')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif "EPIAS Turkey" in source:
                 st.markdown(f"""
                <div class="info-card">
                    <h4>{t('real_time_feed')}</h4>
                    <div class="metric-value">Live</div>
                    <p>Energy Exchange Istanbul</p>
                    <div style="margin-top:1rem; border-top:2px solid rgba(59, 130, 246, 0.2); padding-top:1rem;">
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('contains')}</strong><br>{t('epias_contains')}</p>
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('best_for')}</strong><br>{t('epias_best')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif "World Bank" in source:
                 st.markdown(f"""
                <div class="info-card">
                    <h4>{t('global_indicators')}</h4>
                    <div class="metric-value">190+</div>
                    <p>{t('countries_regions')}</p>
                    <div style="margin-top:1rem; border-top:2px solid rgba(59, 130, 246, 0.2); padding-top:1rem;">
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('contains')}</strong><br>{t('wb_contains')}</p>
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('best_for')}</strong><br>{t('wb_best')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif "IEA" in source:
                st.markdown(f"""
                <div class="info-card">
                    <h4>{t('iea_database')}</h4>
                    <div class="metric-value">5000+</div>
                    <p>{t('global_records')}</p>
                    <div style="margin-top:1rem; border-top:2px solid rgba(59, 130, 246, 0.2); padding-top:1rem;">
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('contains')}</strong><br>{t('iea_contains')}</p>
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('best_for')}</strong><br>{t('iea_best')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif "US EIA" in source:
                st.markdown(f"""
                <div class="info-card">
                    <h4>{t('us_energy_authority')}</h4>
                    <div class="metric-value">1000+</div>
                    <p>{t('production_records')}</p>
                    <div style="margin-top:1rem; border-top:2px solid rgba(59, 130, 246, 0.2); padding-top:1rem;">
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('contains')}</strong><br>{t('eia_contains')}</p>
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('best_for')}</strong><br>{t('eia_best')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif "Eurostat" in source:
                st.markdown(f"""
                <div class="info-card">
                    <h4>{t('eu_stats')}</h4>
                    <div class="metric-value">27</div>
                    <p>{t('eu_members')}</p>
                    <div style="margin-top:1rem; border-top:2px solid rgba(59, 130, 246, 0.2); padding-top:1rem;">
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('contains')}</strong><br>{t('eurostat_contains')}</p>
                        <p style="font-size:0.9rem; color:#64748b;"><strong>{t('best_for')}</strong><br>{t('eurostat_best')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)


    # 3. UPLOAD PAGE
    elif st.session_state.data_mode == 'upload':
        st.markdown('<div class="sub-page-container">', unsafe_allow_html=True)
        
        # Header with Back Button
        c_back, c_title = st.columns([0.5, 4])
        with c_back:
            if st.button("←", key="back_btn_up", help="Back to Menu"):
                st.session_state.data_mode = None
                st.rerun()
        with c_title:
             st.markdown(f"<h2 style='margin:0; padding-top:5px;'>{t('upload_data')}</h2>", unsafe_allow_html=True)
             
        st.markdown("<hr style='margin-top:0.5rem; margin-bottom:2rem; opacity:0.3;'>", unsafe_allow_html=True)
        
        uploaded = st.file_uploader("", type=["csv"])
        
        if uploaded:
            st.session_state.df = pd.read_csv(uploaded)
            st.success(t("file_uploaded"))
            time.sleep(1)
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            t("download_template"),
            "timestamp,device_id,consumption_kWh\n2026-01-01 00:00:00,Device_1,0.45\n",
            file_name="template.csv",
        )

# --- DASHBOARD (DATA LOADED) ---
def render_dashboard():
    df = st.session_state.df 
    
    # Custom CSS for Navbar alignment and Styling
    st.markdown("""
        <style>
        /* Top Bar Container Style */
        div[data-testid="stHorizontalBlock"]:first-of-type {
            align-items: center;
            padding-bottom: 1rem;
        }
        
        /* Selectbox Styling */
        div[data-testid="stSelectbox"] > div > div {
            min-height: 40px !important;
            height: 40px !important;
            border-radius: 8px !important;
            border-color: #e2e8f0 !important;
            background-color: #ffffff !important;
        }
        
        /* GENERAL BUTTON STYLING */
        div[data-testid="column"] button {
            height: 40px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            padding: 0px 16px !important;
            font-size: 0.9rem !important;
            border-radius: 8px !important;
            border-color: #e2e8f0 !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            white-space: nowrap !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
        }

        /* RESET CONTENT STYLES INSIDE BUTTON */
        div[data-testid="column"] button p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            font-weight: 500 !important;
        }

        div[data-testid="column"] button div {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        
        /* Remove default margins from button containers */
        div.stButton {
            margin: 0 !important;
            padding: 0 !important;
            height: 40px !important;
            width: 100% !important;
        }
        
        div.stDownloadButton button {
            font-weight: 500 !important;
        }
        
        /* Logo Alignment */
        div[data-testid="column"]:first-child img {
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navbar Layout: Logo | Spacer | Language | Mini-Spacer | New Analysis
    # Added explicit spacing between language and button
    c_logo, c_space, c_lang, c_gap, c_reset = st.columns([1.5, 4.9, 1.2, 0.3, 1.6], gap="small")
    
    with c_logo:
        st.image("assets/octogreen-logo.png", width=130)
        
    with c_space:
        pass # Big Spacer
        
    with c_lang:
        available_langs = translations.get_available_languages()
        selected_lang = st.selectbox(
            "Language",
            options=list(available_langs.keys()),
            format_func=lambda x: available_langs[x],
            index=list(available_langs.keys()).index(st.session_state.language),
            key="dashboard_language_selector",
            label_visibility="collapsed"
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
            
    with c_gap:
        pass # Small Spacer between lang and button
            
    with c_reset:
        if st.button(f"↻  {t('new_analysis')}", key="btn_new_analysis"):
            reset_app()
    
    st.divider()
    
    # Calculate analysis
    analysis = st.session_state.get('analysis')
    if analysis is None:
        with st.spinner(t("processing_analytics")):
            analysis = ai_analysis.analyze(df)
        st.session_state.analysis = analysis

    # Modern Dataset Overview
    st.markdown(f"""
    <div style='text-align: center; margin-top: 2rem; margin-bottom: 2rem;'>
        <h3 style='font-size: 1.4rem; font-weight: 600; color: #1e293b; letter-spacing: -0.01em;'>{t('dataset_overview')}</h3>
        <div style='height: 3px; width: 60px; background: linear-gradient(90deg, #3b82f6, #06b6d4); margin: 0.5rem auto 0; border-radius: 2px;'></div>
    </div>
    
    <style>
    .overview-card {{
        background: white;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        padding: 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }}
    .overview-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #e2e8f0;
    }}
    .overview-icon {{
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        flex-shrink: 0;
    }}
    .overview-label {{
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .overview-value {{
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3, gap="medium")
    
    with m1:
        st.markdown(f"""
        <div class='overview-card'>
            <div class='overview-icon' style='background: #eff6ff; color: #3b82f6;'>
                <i class="fa-solid fa-server"></i>
            </div>
            <div>
                <div class='overview-label'>{t("total_records")}</div>
                <div class='overview-value'>{len(df):,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        timeline_val = t("time_series_data") if 'timestamp' in df.columns else t("tabular")
        timeline_icon = "fa-clock" if 'timestamp' in df.columns else "fa-table"
        st.markdown(f"""
        <div class='overview-card'>
            <div class='overview-icon' style='background: #f5f3ff; color: #8b5cf6;'>
                <i class="fa-solid {timeline_icon}"></i>
            </div>
            <div>
                <div class='overview-label'>{t("timeline")}</div>
                <div class='overview-value' style='font-size: 1.1rem;'>{timeline_val}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        source_count = df['device_id'].nunique() if 'device_id' in df.columns else 1
        st.markdown(f"""
        <div class='overview-card'>
            <div class='overview-icon' style='background: #ecfeff; color: #06b6d4;'>
                <i class="fa-solid fa-bolt"></i>
            </div>
            <div>
                <div class='overview-label'>{t("sources")}</div>
                <div class='overview-value'>{source_count}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Main Content Area - Single Column Layout
    
    # AI Analysis Section
    st.markdown(f"""
        <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;
                   border-left: 4px solid #8b5cf6; padding-left: 1rem;
                   font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;'>
            <i class='fa-solid fa-brain' style='color: #8b5cf6;'></i> {t("ai_analysis")}
        </h3>
    """, unsafe_allow_html=True)
    
    # Custom HTML Expander with FontAwesome icon
    st.markdown(f"""
    <details style="
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;">
        <summary style="
            cursor: pointer;
            font-weight: 600;
            color: #475569;
            list-style: none;
            display: flex;
            align-items: center;
            gap: 10px;
            outline: none;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="fa-solid fa-magnifying-glass-chart" style="color: #6366f1;"></i>
                {t('view_detailed_analysis')}
            </div>
            <span style="margin-left: auto; color: #cbd5e1; font-size: 0.8em;">▼</span>
        </summary>
        <div style="
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #f1f5f9;
            color: #1e293b;
            line-height: 1.7;
            animation: fadeIn 0.3s ease-in;">
            {analysis['summary']}
        </div>
    </details>
    <style>
    details > summary::marker {{
        display: none;
    }}
    details[open] summary ~ * {{
        animation: keyframes-fadeIn 0.3s ease-in-out;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    
    report_tools.visualize(df, analysis)


# --- MAIN ROUTER ---
if 'df' not in st.session_state:
    render_selection_screen()
else:
    render_dashboard()
