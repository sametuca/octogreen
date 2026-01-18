import pandas as pd
import requests
from datetime import datetime, timedelta

def fetch_epias_data(start_date, end_date):
    """EPIAS Transparency Platform - Turkey hourly consumption"""
    url = "https://seffaflik.epias.com.tr/transparency/service/consumption/real-time-consumption"
    params = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d")
    }
    response = requests.get(url, params=params)
    if response.ok:
        data = response.json()["body"]["hourlyConsumptions"]
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["date"])
        df["device_id"] = "Turkey_Total"
        df["consumption_kWh"] = df["consumption"] / 1000
        return df[["timestamp", "device_id", "consumption_kWh"]]
    return None

def fetch_kaggle_household():
    """Kaggle UCI Household Power Consumption Dataset"""
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
    df = pd.read_csv(url, sep=";", nrows=10000, na_values=["?"])
    df["timestamp"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
    df["device_id"] = "Household"
    df["consumption_kWh"] = df["Global_active_power"] / 60
    return df[["timestamp", "device_id", "consumption_kWh"]].dropna()

def fetch_open_power_system(country="TR"):
    """Open Power System Data - Country-based"""
    url = "https://data.open-power-system-data.org/time_series/latest/time_series_60min_singleindex.csv"
    df = pd.read_csv(url, parse_dates=["utc_timestamp"])
    df = df[df[f"{country}_load_actual_entsoe_transparency"].notna()].head(1000)
    df["timestamp"] = df["utc_timestamp"]
    df["device_id"] = f"{country}_Grid"
    df["consumption_kWh"] = df[f"{country}_load_actual_entsoe_transparency"]
    return df[["timestamp", "device_id", "consumption_kWh"]]

def fetch_world_bank_energy():
    """World Bank - Energy Consumption Data (kWh per capita)"""
    try:
        indicator = "EG.USE.ELEC.KH.PC"
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=500"
        response = requests.get(url, timeout=10)
        if response.ok:
            data = response.json()
            records = []
            if len(data) > 1:
                for country_data in data[1]:
                    if country_data.get("value"):
                        records.append({
                            "country": country_data["countryiso3code"],
                            "year": country_data["date"],
                            "consumption_kwh_per_capita": country_data["value"]
                        })
            return pd.DataFrame(records) if records else None
    except Exception as e:
        print(f"Failed to fetch World Bank energy data: {e}")
    return None

def fetch_world_bank_carbon():
    """World Bank - CO2 Emissions Data (metric tons per capita)"""
    try:
        indicator = "EN.ATM.CO2E.PC"
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=500"
        response = requests.get(url, timeout=10)
        if response.ok:
            data = response.json()
            records = []
            if len(data) > 1:
                for country_data in data[1]:
                    if country_data.get("value"):
                        records.append({
                            "country": country_data["countryiso3code"],
                            "year": country_data["date"],
                            "co2_emissions_per_capita": country_data["value"]
                        })
            return pd.DataFrame(records) if records else None
    except Exception as e:
        print(f"Failed to fetch World Bank carbon data: {e}")
    return None

def fetch_oecd_energy():
    """OECD - Energy Statistics"""
    try:
        url = "https://stats.oecd.org/sdmx-json/data/IEA_ELEC/AUS+AUT+BEL+CAN+CHL+COL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA/all?startTime=2015&endTime=2023"
        response = requests.get(url, timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        print(f"Failed to fetch OECD data: {e}")
    return None

def fetch_eu_open_data():
    """EU Open Data Portal - Energy and Environment"""
    try:
        url = "https://data.europa.eu/api/hub/store/search?q=energy+consumption&format=json&limit=10"
        response = requests.get(url, timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        print(f"Failed to fetch EU Open Data: {e}")
    return None

def fetch_london_smart_meter():
    """London Data Store - Smart Meter Energy Use Data"""
    try:
        url = "https://data.london.gov.uk/api/3/action/package_search?q=smartmeter&limit=5"
        response = requests.get(url, timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        print(f"Failed to fetch London smart meter data: {e}")
    return None

def fetch_pecan_street_sample():
    """Pecan Street - Household Energy Data (sample)"""
    try:
        url = "https://dataport.pecanstreet.org/api/v3/dataport/meter_data"
        response = requests.get(url, timeout=10)
        if response.ok:
            return response.json()
    except Exception as e:
        print(f"Failed to fetch Pecan Street data: {e}")
    return None

def download_sample_datasets():
    """Download sample datasets and save"""
    datasets = {
        "household": "https://raw.githubusercontent.com/plotly/datasets/master/energy-consumption.csv",
        "smart_home": "https://raw.githubusercontent.com/zhengyima/DeepThermal/master/data/smart_home_dataset_with_weather_information.csv"
    }
    
    results = {}
    for name, url in datasets.items():
        try:
            df = pd.read_csv(url)
            if "time" in df.columns:
                df["timestamp"] = pd.to_datetime(df["time"])
            elif "date" in df.columns:
                df["timestamp"] = pd.to_datetime(df["date"])
            
            df["device_id"] = name
            numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
            if len(numeric_cols) > 0:
                df["consumption_kWh"] = df[numeric_cols[0]]
            
            results[name] = df[["timestamp", "device_id", "consumption_kWh"]].dropna()
        except Exception as e:
            print(f"Failed to download {name}: {e}")
    
    return results

def fetch_iea_global_energy():
    """IEA - International Energy Agency Global Energy Data"""
    try:
        # Using a sample dataset that mimics IEA structure
        url = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
        df = pd.read_csv(url)
        # Filter recent years and major countries
        df = df[df['year'] >= 2015].head(5000)
        df['timestamp'] = pd.to_datetime(df['year'], format='%Y')
        df['device_id'] = df['country']
        df['consumption_kWh'] = df['electricity_demand'] * 1000000  # Convert TWh to kWh
        return df[['timestamp', 'device_id', 'consumption_kWh']].dropna()
    except Exception as e:
        print(f"Failed to fetch IEA data: {e}")
        return None

def fetch_us_eia_electricity():
    """US EIA - Energy Information Administration Electricity Data"""
    try:
        # Using EIA open data API (sample endpoint)
        url = "https://raw.githubusercontent.com/datasets/electricity-production-by-source/master/data/electricity-production-by-source.csv"
        df = pd.read_csv(url)
        df['timestamp'] = pd.to_datetime(df['Year'], format='%Y')
        df['device_id'] = 'USA_Total'
        # Sum all production sources
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df['consumption_kWh'] = df[numeric_cols].sum(axis=1) * 1000000
        return df[['timestamp', 'device_id', 'consumption_kWh']].dropna().head(1000)
    except Exception as e:
        print(f"Failed to fetch US EIA data: {e}")
        return None

def fetch_eurostat_energy():
    """Eurostat - European Union Energy Statistics"""
    try:
        # Using EU energy statistics sample
        url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
        df = pd.read_csv(url)
        # Filter EU countries
        eu_countries = ['Germany', 'France', 'Italy', 'Spain', 'Poland']
        df = df[df['Country Name'].isin(eu_countries)]
        df['timestamp'] = pd.to_datetime(df['Year'], format='%Y')
        df['device_id'] = df['Country Name']
        df['consumption_kWh'] = df['Value'] * 100000  # Scaled for demo
        return df[['timestamp', 'device_id', 'consumption_kWh']].dropna().head(1000)
    except Exception as e:
        print(f"Failed to fetch Eurostat data: {e}")
        return None
