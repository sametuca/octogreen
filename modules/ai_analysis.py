import pandas as pd
import numpy as np

def calculate_savings_scenarios(df, summary):
    """Calculate 6 actionable savings scenarios with global impact"""
    carbon_factor = 0.4  # kg CO2 per kWh
    kwh_price = 1.5  # USD per kWh
    
    # Constants for global impact
    TREE_CO2_PER_YEAR = 21  # kg CO2 absorbed by 1 tree per year
    HOME_DAILY_KWH = 30  # Average home consumption per day
    CAR_CO2_PER_DAY = 4.6  # kg CO2 per car per day
    
    scenarios = []
    
    # Scenario 1: Turn off top device for 1 hour daily
    top_device = summary['top_device']
    device_hourly = df[df['device_id'] == top_device].groupby(df['timestamp'].dt.hour)['consumption_kWh'].mean()
    peak_hour = device_hourly.idxmax()
    s1_kwh = device_hourly.max() * 30  # Monthly (30 days)
    s1_carbon = s1_kwh * carbon_factor
    s1_cost = s1_kwh * kwh_price
    scenarios.append({
        'title_en': f'Turn off "{top_device}" at {peak_hour}:00 daily',
        'title_tr': f'"{top_device}" cihazını her gün saat {peak_hour}:00\'da kapatın',
        'kwh': s1_kwh,
        'carbon': s1_carbon,
        'cost': s1_cost,
        'trees': s1_carbon / TREE_CO2_PER_YEAR * 365,
        'homes': s1_kwh / HOME_DAILY_KWH,
        'cars': s1_carbon / CAR_CO2_PER_DAY
    })
    
    # Scenario 2: Shut down all devices 1 hour earlier
    late_night = df[df['timestamp'].dt.hour == 23]['consumption_kWh'].sum()
    s2_kwh = late_night * 30
    s2_carbon = s2_kwh * carbon_factor
    s2_cost = s2_kwh * kwh_price
    scenarios.append({
        'title_en': 'End daily operations 1 hour earlier',
        'title_tr': 'Günlük işlemleri 1 saat erken bitirin',
        'kwh': s2_kwh,
        'carbon': s2_carbon,
        'cost': s2_cost,
        'trees': s2_carbon / TREE_CO2_PER_YEAR * 365,
        'homes': s2_kwh / HOME_DAILY_KWH,
        'cars': s2_carbon / CAR_CO2_PER_DAY
    })
    
    # Scenario 3: Reduce peak hour consumption by 20%
    peak_hour_data = df.groupby(df['timestamp'].dt.hour)['consumption_kWh'].mean()
    peak_hour_val = peak_hour_data.max()
    peak_hour_num = peak_hour_data.idxmax()
    s3_kwh = peak_hour_val * 0.2 * 30
    s3_carbon = s3_kwh * carbon_factor
    s3_cost = s3_kwh * kwh_price
    scenarios.append({
        'title_en': f'Reduce consumption by 20% during peak hour ({peak_hour_num}:00)',
        'title_tr': f'Pik saatte ({peak_hour_num}:00) tüketimi %20 azaltın',
        'kwh': s3_kwh,
        'carbon': s3_carbon,
        'cost': s3_cost,
        'trees': s3_carbon / TREE_CO2_PER_YEAR * 365,
        'homes': s3_kwh / HOME_DAILY_KWH,
        'cars': s3_carbon / CAR_CO2_PER_DAY
    })
    
    # Scenario 4: Match weekend consumption to weekday average
    df['is_weekend'] = df['timestamp'].dt.dayofweek >= 5
    if df['is_weekend'].any():
        weekend_avg = df[df['is_weekend']]['consumption_kWh'].mean()
        weekday_avg = df[~df['is_weekend']]['consumption_kWh'].mean()
        if weekend_avg > weekday_avg:
            weekend_count = df[df['is_weekend']].shape[0]
            s4_kwh = (weekend_avg - weekday_avg) * weekend_count
            s4_carbon = s4_kwh * carbon_factor
            s4_cost = s4_kwh * kwh_price
            scenarios.append({
                'title_en': 'Reduce weekend consumption to weekday levels',
                'title_tr': 'Hafta sonu tüketimini hafta içi seviyelerine düşürün',
                'kwh': s4_kwh,
                'carbon': s4_carbon,
                'cost': s4_cost,
                'trees': s4_carbon / TREE_CO2_PER_YEAR * 365,
                'homes': s4_kwh / HOME_DAILY_KWH,
                'cars': s4_carbon / CAR_CO2_PER_DAY
            })
    
    # Scenario 5: Eliminate anomalies (bring them to average)
    if len(summary['anomalies']) > 0:
        anomaly_df = pd.DataFrame(summary['anomalies'])
        anomaly_excess = anomaly_df['consumption_kWh'].sum() - (df['consumption_kWh'].mean() * len(anomaly_df))
        if anomaly_excess > 0:
            s5_kwh = anomaly_excess
            s5_carbon = s5_kwh * carbon_factor
            s5_cost = s5_kwh * kwh_price
            scenarios.append({
                'title_en': 'Fix unusual consumption spikes',
                'title_tr': 'Olağandışı tüketim artışlarını düzeltin',
                'kwh': s5_kwh,
                'carbon': s5_carbon,
                'cost': s5_cost,
                'trees': s5_carbon / TREE_CO2_PER_YEAR * 365,
                'homes': s5_kwh / HOME_DAILY_KWH,
                'cars': s5_carbon / CAR_CO2_PER_DAY
            })
    
    # Scenario 6: Overall 10% reduction
    total_consumption = df['consumption_kWh'].sum()
    s6_kwh = total_consumption * 0.1
    s6_carbon = s6_kwh * carbon_factor
    s6_cost = s6_kwh * kwh_price
    scenarios.append({
        'title_en': 'Achieve 10% overall consumption reduction',
        'title_tr': 'Genel tüketimde %10 azalma sağlayın',
        'kwh': s6_kwh,
        'carbon': s6_carbon,
        'cost': s6_cost,
        'trees': s6_carbon / TREE_CO2_PER_YEAR * 365,
        'homes': s6_kwh / HOME_DAILY_KWH,
        'cars': s6_carbon / CAR_CO2_PER_DAY
    })
    
    return scenarios

def analyze(df):
    from sklearn.ensemble import IsolationForest
    summary = {}
    recommendations = []
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Daily total, average, peak hours
    daily = df.groupby(df['timestamp'].dt.date)['consumption_kWh'].sum()
    hourly = df.groupby(df['timestamp'].dt.hour)['consumption_kWh'].mean()
    summary['daily_total'] = daily.to_dict()
    summary['hourly_avg'] = hourly.to_dict()
    # Anomaly detection: IsolationForest
    model = IsolationForest(contamination=0.03, random_state=42)
    df['anomaly'] = model.fit_predict(df[['consumption_kWh']])
    anomalies = df[df['anomaly'] == -1]
    summary['anomalies'] = anomalies.to_dict('records')
    # Device-based analysis and recommendations
    device_totals = df.groupby('device_id')['consumption_kWh'].sum()
    device_hourly = df.groupby(['device_id', df['timestamp'].dt.hour])['consumption_kWh'].mean().unstack()
    top_device = device_totals.idxmax()
    peak_hour = device_hourly.loc[top_device].idxmax()
    savings_kwh = device_totals.max() * 0.15
    carbon_factor = 0.4
    savings_carbon = savings_kwh * carbon_factor
    kwh_price = 1.5  # USD/kWh example
    savings_usd = savings_kwh * kwh_price
    recommendations.append(
        f"For 15% savings, turn off {top_device} device around {peak_hour}:00. Estimated savings: {savings_kwh:.2f} kWh, {savings_carbon:.2f} kg CO2, ${savings_usd:.2f}"
    )
    # Scenario: If all devices shut down 1 hour earlier
    scenario_saving = df[df['timestamp'].dt.hour == 23]['consumption_kWh'].sum()
    scenario_carbon = scenario_saving * carbon_factor
    scenario_usd = scenario_saving * kwh_price
    recommendations.append(
        f"If all devices shut down 1 hour earlier: {scenario_saving:.2f} kWh, {scenario_carbon:.2f} kg CO2, ${scenario_usd:.2f} savings."
    )
    # Summary
    summary['top_device'] = top_device
    summary['peak_hour'] = int(peak_hour)
    summary['tasarruf_kwh'] = float(savings_kwh)
    summary['tasarruf_carbon'] = float(savings_carbon)
    summary['tasarruf_tl'] = float(savings_usd)
    
    # Calculate savings scenarios
    scenarios = calculate_savings_scenarios(df, summary)
    
    return {'summary': summary, 'recommendations': recommendations, 'scenarios': scenarios}

