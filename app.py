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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'Segoe UI', sans-serif !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
}

/* Container */
.block-container {
    max-width: 1400px !important;
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}

/* Hero Box - Blue Glassmorphism */
.hero-box {
    text-align: center;
    padding: 3rem 2rem;
    margin-bottom: 3rem;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 2px solid rgba(59, 130, 246, 0.2);
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.5);
    animation: fadeInUp 0.8s ease-out;
}

.hero-subtitle {
    font-size: 1.3rem !important;
    color: var(--text-secondary) !important;
    margin-top: 1rem !important;
    font-weight: 500;
    line-height: 1.6 !important;
}

/* Premium Blue Buttons */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%) !important;
    color: var(--text-primary) !important;
    border: 2px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 16px !important;
    padding: 2rem 1.5rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15), 0 0 0 1px rgba(59, 130, 246, 0.05) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: -0.3px !important;
}

div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--success-gradient);
    opacity: 0;
    transition: opacity 0.3s ease;
    border-radius: 16px;
    z-index: -1;
}

div.stButton > button:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 8px 30px rgba(59, 130, 246, 0.3), 0 0 0 1px rgba(59, 130, 246, 0.2) !important;
    transform: translateY(-4px) scale(1.02) !important;
    color: var(--accent-dark) !important;
}

div.stButton > button:hover::before {
    opacity: 0.1;
}

div.stButton > button:active {
    transform: translateY(-2px) scale(1.01) !important;
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
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2);
    border-color: rgba(59, 130, 246, 0.4);
}

.info-card h4 {
    text-align: left !important;
    color: var(--accent) !important;
    font-size: 1.1rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

.info-card p,
.info-card strong,
.info-card span,
.info-card div {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
}

.metric-value {
    font-size: 3rem;
    font-weight: 800;
    background: var(--success-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.5rem 0;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

.metric-label {
    color: var(--text-secondary) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
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

/* Expander - Blue Premium Button */
.streamlit-expanderHeader {
    background: var(--success-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 1.3rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3) !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.3px !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

.streamlit-expanderHeader:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 30px rgba(59, 130, 246, 0.4) !important;
}

.streamlit-expanderHeader svg {
    fill: white !important;
}

/* Expander text - ensure SF Pro */
.streamlit-expanderHeader,
.streamlit-expanderHeader p,
.streamlit-expanderHeader span,
.streamlit-expanderHeader div {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

/* Protect Material Icons from font override */
.streamlit-expanderHeader svg text {
    font-family: 'Material Icons' !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', sans-serif !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] span,
[data-testid="stMetricValue"] p {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] div,
[data-testid="stMetricLabel"] span,
[data-testid="stMetricLabel"] p {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

/* Button text - force SF Pro */
div.stButton > button,
div.stButton > button span,
div.stButton > button p {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
}

/* Caption text under buttons */
.stCaption, .stCaption p {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
    color: var(--text-secondary) !important;
}

/* Info card content */
.info-card p,
.info-card strong,
.info-card span {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
}

/* Download buttons - special styling */
div.stDownloadButton > button,
div.stDownloadButton > button span,
div.stDownloadButton > button p {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
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
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
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
def render_selection_screen():
    render_hero()
    
    # Selection Grid
    if st.session_state.data_mode is None:
        # Use columns with explicit padding/gap
        col_space_l, col1, col2, col_space_r = st.columns([1, 2, 2, 1], gap="large")
        
        with col1:
             if st.button(t("browse_open_data"), key="btn_open_data", width="stretch"):
                st.session_state.data_mode = 'open_data'
                st.rerun()
             st.caption(t("open_data_desc"))

        with col2:
             if st.button(t("upload_your_own"), key="btn_upload", width="stretch"):
                st.session_state.data_mode = 'upload'
                st.rerun()
             st.caption(t("upload_desc"))

    # --- Mode: Open Data ---
    elif st.session_state.data_mode == 'open_data':
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button(t("back"), key="back_btn"):
                st.session_state.data_mode = None
                st.rerun()
        
        st.markdown(f"<h3>{t('select_dataset')}</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_opts, col_detais = st.columns([1.2, 0.8], gap="large")
        
        with col_opts:
            source = st.selectbox(t("choose_source"), [
                "UCI Household (2M+ records)",
                "EPIAS Turkey (Real-time)",
                "World Bank - Energy & Carbon",
                "IEA - Global Energy Data",
                "US EIA - Electricity Stats",
                "Eurostat - EU Energy"
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


    # --- Mode: Upload ---
    elif st.session_state.data_mode == 'upload':
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button(t("back"), key="back_btn_up"):
                st.session_state.data_mode = None
                st.rerun()
            
        st.markdown(f"<h3>{t('upload_data')}</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
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
    # Top Bar: Logo Left, Language Center, New Analysis Right
    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        st.image("assets/octogreen-logo.png", width=120)
    with c2:
        # Language selector in center
        col_lang1, col_lang2, col_lang3 = st.columns([2, 1, 2])
        with col_lang2:
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
    with c3:
        if st.button(t("new_analysis")):
            reset_app()
    
    st.divider()
    
    df = st.session_state.df
    
    # Feature Cards Row using CSS Grid inside Markdown or Columns
    st.markdown(f"### {t('dataset_overview')}")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(t("total_records"), f"{len(df):,}")
    with m2:
        if 'timestamp' in df.columns:
            st.metric(t("timeline"), t("time_series_data"))
        else:
            st.metric(t("structure"), t("tabular"))
    with m3:
        if 'device_id' in df.columns:
            st.metric(t("sources"), f"{df['device_id'].nunique()}")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Main Content Area
    col_main, col_side = st.columns([2, 1], gap="large")
    
    with col_main:
        # AI Analysis Section
        st.markdown(f"""
            <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;'>
                <i class='fa-solid fa-brain' style='color: #8b5cf6;'></i> {t("ai_analysis")}
            </h3>
        """, unsafe_allow_html=True)
        
        analysis = st.session_state.get('analysis')
        if analysis is None:
            with st.spinner(t("processing_analytics")):
                analysis = ai_analysis.analyze(df)
            st.session_state.analysis = analysis
            
        # Display AI summary in a collapsible expander
        with st.expander(t("view_detailed_analysis"), expanded=False):
            st.markdown(f"""
            <div style="background:white; padding:1.5rem; border-radius:12px; border:2px solid rgba(16, 185, 129, 0.2); margin-bottom:1rem;">
                <p style="color:#0f172a; font-size:1.05rem; line-height:1.6;">{analysis['summary']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualization Header with custom styling to match other headers
        st.markdown(f"""
            <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; 
                       border-left: 4px solid #6366f1; padding-left: 1rem; margin-top: 2rem;'>
                <i class='fa-solid fa-chart-column' style='color: #6366f1;'></i> {t('visualization')}
            </h3>
        """, unsafe_allow_html=True)
        report_tools.visualize(df, analysis)


    with col_side:
        st.markdown(f"""
            <h3 style='color: #1d1d1f; font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;'>
                <i class='fa-solid fa-lightbulb' style='color: #f59e0b;'></i> {t("key_findings")}
            </h3>
        """, unsafe_allow_html=True)
        
        # Display recommendations as styled list
        for i, rec in enumerate(analysis['recommendations'], 1):
            st.markdown(f"""
                <div style='background: #eff6ff; border-left: 3px solid #3b82f6; 
                            padding: 0.8rem 1rem; margin-bottom: 0.8rem; border-radius: 6px;'>
                    <p style='color: #1e3a8a; margin: 0; font-size: 0.95rem; line-height: 1.5;'>
                        <strong>{i}.</strong> {rec}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <h3 style='color: #1d1d1f; font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;'>
                <i class='fa-solid fa-download' style='color: #10b981;'></i> {t("export")}
            </h3>
        """, unsafe_allow_html=True)
        report_tools.download_buttons(df, analysis)


# --- MAIN ROUTER ---
if 'df' not in st.session_state:
    render_selection_screen()
else:
    render_dashboard()
