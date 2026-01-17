import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from modules import ai_analysis, report_tools, open_data, ui_utils

st.set_page_config(
    page_title="OctoGreen Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(ui_utils.CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(f"<h1>{ui_utils.get_icon('energy')} OctoGreen: Smart Energy Analysis Platform</h1>", unsafe_allow_html=True)

st.sidebar.markdown(f"<h3>{ui_utils.get_icon('database')} Data Source</h3>", unsafe_allow_html=True)
data_source = st.sidebar.radio("How to load data?", ["Upload CSV", "Open Data Sources"])

if data_source == "Open Data Sources":
    st.sidebar.markdown(f"<h4>{ui_utils.get_icon('world')} Select Data Source</h4>", unsafe_allow_html=True)
    source = st.sidebar.selectbox("Source", [
        f"{ui_utils.get_icon('chart')} UCI Household (2M+ records)",
        f"{ui_utils.get_icon('energy')} EPIAS Turkey (Real-time)",
        f"{ui_utils.get_icon('bank')} World Bank - Energy & Carbon",
        f"{ui_utils.get_icon('chart_line')} OECD Energy Statistics",
        f"{ui_utils.get_icon('world')} EU Open Data Portal",
        f"{ui_utils.get_icon('home')} London Smart Meter Data",
        f"{ui_utils.get_icon('database')} Sample Datasets"
    ])
    
    if "UCI Household" in source:
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Download Data", key="uci_btn"):
            with st.spinner("Downloading UCI dataset..."):
                df = open_data.fetch_kaggle_household()
                st.success(f"{ui_utils.get_icon('check')} {len(df)} records loaded!")
        else:
            st.info(f"{ui_utils.get_icon('click')} Click 'Download Data' button")
            st.stop()
    
    elif "EPIAS Turkey" in source:
        start = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=7))
        end = st.sidebar.date_input("End Date", datetime.now())
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Fetch Data"):
            with st.spinner("Fetching data from EPIAS..."):
                df = open_data.fetch_epias_data(start, end)
                if df is not None:
                    st.success(f"{ui_utils.get_icon('check')} Turkey electricity consumption data loaded!")
                else:
                    st.error(f"{ui_utils.get_icon('error')} Failed to fetch data. Check API access.")
                    st.stop()
        else:
            st.info(f"{ui_utils.get_icon('click')} Select dates and click 'Fetch Data' button")
            st.stop()
    
    elif "World Bank" in source:
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Fetch World Bank Data"):
            with st.spinner("Fetching World Bank data..."):
                energy_df = open_data.fetch_world_bank_energy()
                if energy_df is not None:
                    st.success(f"{ui_utils.get_icon('check')} World Bank data loaded! {len(energy_df)} records")
                    st.dataframe(energy_df.head())
                    df = energy_df.copy()
                    df["timestamp"] = pd.to_datetime(df["year"], format="%Y")
                    df["device_id"] = df["country"]
                    df["consumption_kWh"] = df["consumption_kwh_per_capita"]
                    df = df[["timestamp", "device_id", "consumption_kWh"]].dropna()
                else:
                    st.error(f"{ui_utils.get_icon('error')} Failed to fetch World Bank data.")
                    st.stop()
        else:
            st.info(f"{ui_utils.get_icon('click')} Click 'Fetch World Bank Data' button")
            st.stop()
    
    elif "OECD" in source:
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Fetch OECD Data"):
            with st.spinner("Fetching OECD data..."):
                oecd_data = open_data.fetch_oecd_energy()
                if oecd_data:
                    st.success(f"{ui_utils.get_icon('check')} OECD energy statistics loaded!")
                    st.json(oecd_data)
                    st.info("Data structure: OECD energy statistics for OECD countries (2015-2023)")
                    df = pd.DataFrame({"timestamp": [datetime.now()], "device_id": ["OECD"], "consumption_kWh": [0]})
                else:
                    st.error(f"{ui_utils.get_icon('error')} Failed to fetch OECD data.")
                    st.stop()
        else:
            st.info(f"{ui_utils.get_icon('click')} Click 'Fetch OECD Data' button")
            st.stop()
    
    elif "EU" in source:
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Fetch EU Data"):
            with st.spinner("Fetching EU Open Data..."):
                eu_data = open_data.fetch_eu_open_data()
                if eu_data:
                    st.success(f"{ui_utils.get_icon('check')} EU Open Data loaded!")
                    st.json(eu_data)
                    st.info("Available datasets from EU Open Data Portal")
                    df = pd.DataFrame({"timestamp": [datetime.now()], "device_id": ["EU"], "consumption_kWh": [0]})
                else:
                    st.error(f"{ui_utils.get_icon('error')} Failed to fetch EU data.")
                    st.stop()
        else:
            st.info(f"{ui_utils.get_icon('click')} Click 'Fetch EU Data' button")
            st.stop()
    
    elif "London" in source:
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Fetch London Data"):
            with st.spinner("Fetching London smart meter data..."):
                london_data = open_data.fetch_london_smart_meter()
                if london_data:
                    st.success(f"{ui_utils.get_icon('check')} London smart meter datasets found!")
                    st.json(london_data)
                    st.info("Smart meter energy use data from London Data Store")
                    df = pd.DataFrame({"timestamp": [datetime.now()], "device_id": ["London"], "consumption_kWh": [0]})
                else:
                    st.error(f"{ui_utils.get_icon('error')} Failed to fetch London data.")
                    st.stop()
        else:
            st.info(f"{ui_utils.get_icon('click')} Click 'Fetch London Data' button")
            st.stop()
    
    else:  # Sample Datasets
        if st.sidebar.button(f"{ui_utils.get_icon('download')} Download Sample Data"):
            with st.spinner("Downloading sample datasets..."):
                datasets = open_data.download_sample_datasets()
                if datasets:
                    df = pd.concat(datasets.values(), ignore_index=True)
                    st.success(f"{ui_utils.get_icon('check')} {len(datasets)} datasets merged!")
                else:
                    st.error(f"{ui_utils.get_icon('error')} Failed to download data.")
                    st.stop()
        else:
            st.info(f"{ui_utils.get_icon('click')} Click 'Download Sample Data' button")
            st.stop()

else:
    uploaded = st.sidebar.file_uploader(f"{ui_utils.get_icon('upload')} Upload CSV file", type=["csv"])
    st.sidebar.download_button(
        f"{ui_utils.get_icon('download')} Download sample CSV template",
        "timestamp,device_id,consumption_kWh\n2026-01-01 00:00:00,Device_1,0.45\n2026-01-01 01:00:00,Device_1,0.51\n2026-01-01 00:00:00,Device_2,0.38\n",
        file_name="sample_template.csv"
    )
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"{ui_utils.get_icon('check')} CSV data loaded.")
    else:
        st.warning(f"{ui_utils.get_icon('warning')} Please upload a CSV file.")
        st.stop()

st.markdown(f"<h2>{ui_utils.get_icon('chart')} Data Preview</h2>", unsafe_allow_html=True)
st.dataframe(df.head())

analysis = ai_analysis.analyze(df)
st.markdown(f"<h2>{ui_utils.get_icon('chart_line')} AI Analysis Results and Recommendations</h2>", unsafe_allow_html=True)
st.write(analysis["summary"])
st.write(analysis["recommendations"])

st.markdown(f"<h2>{ui_utils.get_icon('report')} Download Report</h2>", unsafe_allow_html=True)
report_tools.download_buttons(df, analysis)

st.markdown(f"<h2>{ui_utils.get_icon('chart')} Consumption Charts and Carbon Footprint</h2>", unsafe_allow_html=True)
report_tools.visualize(df, analysis)
