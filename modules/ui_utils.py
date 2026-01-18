"""Styling utilities for OctoGreen"""

# Modern Energy-Themed CSS
CUSTOM_CSS = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ===== BASE SETTINGS ===== */
:root {
    --primary: #10b981;
    --primary-dark: #059669;
    --primary-light: #d1fae5;
    --accent: #f59e0b;
    --dark-bg: #0f172a;
    --light-bg: #f8fafc;
    --card-bg: #ffffff;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --border: #e2e8f0;
}

/* Force Sora font on EVERYTHING */
* {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

html, body, div, span, p, a, button, input, select, textarea, label, h1, h2, h3, h4, h5, h6 {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stApp {
    background: linear-gradient(180deg, #f0fdf4 0%, #f8fafc 50%, #f0f9ff 100%) !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stApp * {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

p {
    color: var(--text-secondary) !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

span {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Container */
.block-container {
    max-width: 1300px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 5rem !important;
}

/* ===== HERO SECTION ===== */
.hero-box {
    text-align: center;
    padding: 4rem 2.5rem;
    margin-bottom: 3.5rem;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(245, 158, 11, 0.05) 100%);
    backdrop-filter: blur(20px);
    border-radius: 28px;
    border: 2px solid rgba(16, 185, 129, 0.2);
    box-shadow: 0 20px 60px rgba(16, 185, 129, 0.1);
}

.hero-box * {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.hero-subtitle {
    font-size: 1.25rem !important;
    color: var(--text-secondary) !important;
    margin-top: 1.5rem !important;
    font-weight: 500 !important;
    line-height: 1.7 !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* ===== BUTTONS ===== */
div.stButton > button {
    width: 100%;
    background: white !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--primary) !important;
    border-radius: 12px !important;
    padding: 1.8rem 1.5rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2) !important;
    transition: all 0.2s ease !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

div.stButton > button:hover {
    border-color: var(--primary-dark) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
    transform: translateY(-2px) !important;
    background: rgba(16, 185, 129, 0.05) !important;
}

div.stButton > button:active {
    transform: translateY(0) !important;
}

/* ===== SELECTBOX - COMPLETE NEW IMPLEMENTATION ===== */

/* Container */
.stSelectbox {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stSelectbox * {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Label */
.stSelectbox label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Main select wrapper */
.stSelectbox [data-baseweb="select"] {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stSelectbox [data-baseweb="select"] * {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Select control (the box) */
.stSelectbox [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    min-height: 48px !important;
    padding: 0 12px !important;
}

/* Select control hover */
.stSelectbox [data-baseweb="select"] > div:hover {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
}

/* The clickable button area */
.stSelectbox [data-baseweb="select"] [role="button"] {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 8px 0 !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Selected value container */
.stSelectbox [data-baseweb="select"] [role="button"] > div {
    color: var(--text-primary) !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Selected value text - ALL NESTED ELEMENTS */
.stSelectbox [data-baseweb="select"] [role="button"] > div > div,
.stSelectbox [data-baseweb="select"] [role="button"] > div > div > div,
.stSelectbox [data-baseweb="select"] [role="button"] span,
.stSelectbox [data-baseweb="select"] [role="button"] p {
    color: var(--text-primary) !important;
    font-size: 1rem !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Dropdown arrow */
.stSelectbox [data-baseweb="select"] svg {
    fill: var(--text-primary) !important;
    width: 20px !important;
    height: 20px !important;
}

/* Dropdown menu container */
[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
    margin-top: 4px !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-baseweb="popover"] * {
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Options list */
[role="listbox"] {
    background-color: #ffffff !important;
    padding: 6px !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Individual option */
[role="option"] {
    background-color: #ffffff !important;
    color: var(--text-primary) !important;
    padding: 12px 14px !important;
    border-radius: 6px !important;
    margin: 2px 0 !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    font-family: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Option hover */
[role="option"]:hover {
    background-color: var(--primary-light) !important;
    color: var(--primary-dark) !important;
}

/* Selected option */
[role="option"][aria-selected="true"] {
    background-color: var(--primary) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ===== OTHER INPUTS ===== */

/* Text Input */
.stTextInput input {
    background-color: #ffffff !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

/* Date Input */
.stDateInput input {
    background-color: #ffffff !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 1.3rem 1.8rem !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.streamlit-expanderHeader p {
    color: white !important;
    margin: 0 !important;
    padding: 0 !important;
}

.streamlit-expanderHeader:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 35px rgba(16, 185, 129, 0.4) !important;
}

.streamlit-expanderHeader svg {
    fill: white !important;
    flex-shrink: 0 !important;
}

details[open] > .streamlit-expanderHeader {
    border-radius: 14px 14px 0 0 !important;
}

details > div {
    border: 2px solid var(--primary-light) !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    background: white !important;
    padding: 2rem !important;
}

/* ===== INFO CARDS ===== */
.info-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 253, 244, 0.5) 100%);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(16, 185, 129, 0.2);
    border-radius: 18px;
    padding: 2.2rem;
    box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
    transition: all 0.4s ease;
}

.info-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 50px rgba(16, 185, 129, 0.2);
    border-color: rgba(16, 185, 129, 0.4);
}

.info-card h4 {
    color: var(--primary) !important;
    font-size: 1.15rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 800 !important;
}

.metric-value {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.8rem 0;
    font-family: 'Space Mono', monospace;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    background-color: white !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stDataFrame"] div[role="columnheader"] {
    background: linear-gradient(135deg, #f0fdf4 0%, #f0f9ff 100%) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--primary) !important;
}

/* ===== METRICS ===== */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(240, 253, 244, 0.5) 100%) !important;
    border: 2px solid rgba(16, 185, 129, 0.15) !important;
    border-radius: 16px !important;
    padding: 1.8rem !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.08) !important;
    transition: all 0.3s ease !important;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 35px rgba(16, 185, 129, 0.15) !important;
}

/* ===== DIVIDER ===== */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, var(--primary), transparent) !important;
    margin: 2rem 0 !important;
}

/* ===== ANIMATIONS ===== */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

.hero-box {
    animation: slideInUp 0.6s ease-out;
}

div.stButton > button {
    animation: fadeIn 0.4s ease-out;
    animation-delay: 0.1s;
    animation-fill-mode: both;
}

.info-card {
    animation: slideInUp 0.5s ease-out;
    animation-delay: 0.2s;
    animation-fill-mode: both;
}

/* Image Container */
div[data-testid="stImage"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    animation: fadeIn 0.6s ease-out;
}

div[data-testid="stImage"] > img {
    display: block !important;
    margin: 0 auto !important;
}

/* ===== MESSAGES ===== */
.stSuccess {
    background-color: rgba(16, 185, 129, 0.1) !important;
    border: 2px solid var(--primary) !important;
    border-radius: 12px !important;
    color: var(--primary-dark) !important;
}

.stError {
    background-color: rgba(239, 68, 68, 0.1) !important;
    border: 2px solid #ef4444 !important;
    border-radius: 12px !important;
    color: #dc2626 !important;
}

.stInfo {
    background-color: rgba(59, 130, 246, 0.1) !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 12px !important;
    color: #1e40af !important;
}
</style>
'''

def show_loading_progress(message, steps=None):
    """Show minimal loading progress"""
    import streamlit as st
    import time
    
    if steps:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, step in enumerate(steps):
            status_text.markdown(f"<p style='text-align:center; color:#64748b; font-size:0.9rem;'>{step}</p>", unsafe_allow_html=True)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.15)
        
        status_text.markdown(f"<p style='text-align:center; color:#10b981; font-weight:600;'>✓ {message}</p>", unsafe_allow_html=True)
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
    else:
        with st.spinner(f"{message}"):
            time.sleep(0.3)
