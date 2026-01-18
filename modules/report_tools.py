import streamlit as st
import plotly.express as px
import pandas as pd
from modules import translations

def t(key):
    """Translation helper"""
    return translations.get_text(key, st.session_state.get('language', 'en'))

def download_buttons(df, analysis):
    st.download_button(t("download_csv"), df.to_csv(index=False), file_name="data.csv")
    if st.button(t("download_pdf")):
        pdf_bytes = generate_pdf_report(df, analysis)
        st.download_button(t("download_pdf_generated"), pdf_bytes, file_name="report.pdf")

def visualize(df, analysis):
    import plotly.graph_objects as go
    
    # Set the default theme for all plots
    plot_bgcolor = 'rgba(0,0,0,0)'
    paper_bgcolor = 'rgba(0,0,0,0)'
    font_color = '#1f2937'
    grid_color = '#e5e7eb'
    
    # Common layout for all figures
    common_layout = dict(
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor,
        font=dict(color=font_color, family='Inter, sans-serif'),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=1,
            linecolor=grid_color,
            linewidth=1,
            showline=True,
            mirror=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=1,
            linecolor=grid_color,
            linewidth=1,
            showline=True,
            mirror=True
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    
    def format_number(num):
        """Format large numbers with K/M suffixes"""
        if abs(num) >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif abs(num) >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return f"{num:.1f}"
    
    # Enhanced Summary Metrics with new additions
    st.markdown(f"""
        <div style='text-align: center; margin: 2rem 0 1.5rem 0;'>
            <h2 style='background: linear-gradient(135deg, #0071e3 0%, #0056b3 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
                {t('performance_insights')}
            </h2>
            <p style='color: #86868b; font-size: 1.1rem;'>{t('key_metrics')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Add tooltip CSS
    st.markdown("""
        <style>
        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.2rem 1rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.2s ease;
            position: relative;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #10b981;
            margin-bottom: 0.3rem;
            line-height: 1.2;
            white-space: nowrap;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #6b7280;
            line-height: 1.3;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.3rem;
        }
        .tooltip-icon {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #d1d5db;
            color: white;
            font-size: 10px;
            line-height: 14px;
            text-align: center;
            cursor: help;
            position: relative;
        }
        .tooltip-icon:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 120%;
            left: 50%;
            transform: translateX(-50%);
            background: #1f2937;
            color: white;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-size: 0.8rem;
            white-space: normal;
            width: 200px;
            text-align: left;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            pointer-events: none;
        }
        .tooltip-icon:hover::before {
            content: '';
            position: absolute;
            bottom: 110%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: #1f2937;
            z-index: 1001;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # First row - Savings metrics
    col1, col2, col3 = st.columns(3)
    
    savings_kwh = analysis['summary']['tasarruf_kwh']
    savings_carbon = analysis['summary']['tasarruf_carbon']
    savings_usd = analysis['summary']['tasarruf_tl']
    
    with col1:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{format_number(savings_kwh)}</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-bolt' style='color: #10b981;'></i> 
                        {t('energy_savings')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_energy_savings")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>{format_number(savings_carbon)}</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-leaf' style='color: #10b981;'></i> 
                        {t('carbon_reduction')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_carbon_reduction")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value'>${format_number(savings_usd)}</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-dollar-sign' style='color: #10b981;'></i> 
                        {t('cost_savings')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_cost_savings")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second row - New analytical metrics
    col4, col5, col6, col7 = st.columns(4)
    
    # Calculate additional metrics
    total_consumption = df['consumption_kWh'].sum()
    avg_consumption = df['consumption_kWh'].mean()
    max_consumption = df['consumption_kWh'].max()
    efficiency_score = min(100, (1 - (avg_consumption / max_consumption)) * 100) if max_consumption > 0 else 0
    
    with col4:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value' style='font-size: 1.6rem;'>{format_number(total_consumption)}</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-database' style='color: #3b82f6;'></i> 
                        {t('total_usage')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_total_usage")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value' style='font-size: 1.6rem;'>{format_number(avg_consumption)}</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-chart-line' style='color: #3b82f6;'></i> 
                        {t('average')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_average")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    with col6:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value' style='font-size: 1.6rem;'>{format_number(max_consumption)}</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-triangle-exclamation' style='color: #f59e0b;'></i> 
                        {t('peak_load')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_peak_load")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    with col7:
        st.markdown(f"""<div class='metric-card'>
                    <div class='metric-value' style='font-size: 1.6rem; color: #10b981;'>{efficiency_score:.0f}%</div>
                    <div class='metric-label'>
                        <i class='fa-solid fa-gauge-high' style='color: #10b981;'></i> 
                        {t('efficiency_score')}
                        <span class='tooltip-icon' data-tooltip='{t("tooltip_efficiency_score")}'>?</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    
    # Consumption Timeline
    st.markdown(f"""
        <div style='margin-top: 3rem; margin-bottom: 1rem;'>
            <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; 
                       border-left: 4px solid #0071e3; padding-left: 1rem;'>
                <i class='fa-solid fa-chart-area' style='color: #0071e3;'></i> {t('consumption_timeline')}
            </h3>
            <p style='color: #86868b; margin-left: 1.5rem; margin-top: 0.5rem;'>
                {t('realtime_usage')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    fig = px.line(df, x='timestamp', y='consumption_kWh', color='device_id')
    fig.update_layout(
        **common_layout,
        xaxis_title=t('time'),
        yaxis_title=t('consumption_kwh'),
        legend_title=t('device_id'),
        legend=dict(
            bgcolor='white',
            bordercolor=grid_color,
            borderwidth=1
        ),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily Aggregation
    st.markdown(f"""
        <div style='margin-top: 3rem; margin-bottom: 1rem;'>
            <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; 
                       border-left: 4px solid #10b981; padding-left: 1rem;'>
                <i class='fa-solid fa-calendar-days' style='color: #10b981;'></i> {t('daily_energy_profile')}
            </h3>
            <p style='color: #86868b; margin-left: 1.5rem; margin-top: 0.5rem;'>
                {t('total_consumption_day')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    daily = analysis['summary']['daily_total']
    fig2 = px.bar(x=list(daily.keys()), y=list(daily.values()), 
                 labels={'x':t('day'), 'y':t('total_kwh')})
    fig2.update_layout(
        **common_layout,
        xaxis_title=t('day'),
        yaxis_title=t('total_kwh'),
        showlegend=False,
        height=400
    )
    fig2.update_traces(
        marker_color='#10b981',
        marker_line_color='#0d8f6e',
        marker_line_width=1.5,
        opacity=0.8
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Hourly Pattern Analysis
    st.markdown(f"""
        <div style='margin-top: 3rem; margin-bottom: 1rem;'>
            <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; 
                       border-left: 4px solid #3b82f6; padding-left: 1rem;'>
                <i class='fa-solid fa-clock' style='color: #3b82f6;'></i> {t('hourly_usage_patterns')}
            </h3>
            <p style='color: #86868b; margin-left: 1.5rem; margin-top: 0.5rem;'>
                {t('average_by_hour')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    hourly = analysis['summary']['hourly_avg']
    fig3 = px.bar(x=list(hourly.keys()), y=list(hourly.values()), 
                 labels={'x':t('hour'), 'y':t('average_kwh')})
    fig3.update_layout(
        **common_layout,
        xaxis_title=t('hour'),
        yaxis_title=t('average_kwh'),
        showlegend=False,
        height=400
    )
    fig3.update_traces(
        marker_color='#3b82f6',
        marker_line_color='#2563eb',
        marker_line_width=1.5,
        opacity=0.8
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Anomaly Detection
    st.markdown(f"""
        <div style='margin-top: 3rem; margin-bottom: 1rem;'>
            <h3 style='color: #1d1d1f; font-size: 1.5rem; font-weight: 600; 
                       border-left: 4px solid #ef4444; padding-left: 1rem;'>
                <i class='fa-solid fa-magnifying-glass-chart' style='color: #ef4444;'></i> {t('anomaly_detection')}
            </h3>
            <p style='color: #86868b; margin-left: 1.5rem; margin-top: 0.5rem;'>
                {t('unusual_patterns')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    anomalies = analysis['summary']['anomalies']
    if anomalies:
        anom_df = pd.DataFrame(anomalies)
        
        # Style the anomalies dataframe
        st.markdown("""
        <style>
            .stDataFrame {
                border: 1px solid #e5e7eb !important;
                border-radius: 8px !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
            }
            .stDataFrame th {
                background-color: #f9fafb !important;
                color: #1f2937 !important;
                font-weight: 600 !important;
                border-bottom: 1px solid #e5e7eb !important;
            }
            .stDataFrame td {
                color: #1f2937 !important;
                border-bottom: 1px solid #f3f4f6 !important;
            }
            .stDataFrame tr:hover {
                background-color: #f9fafb !important;
            }
            .metric-card {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .metric-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #10b981;
                margin-bottom: 0.5rem;
            }
            .metric-label {
                font-size: 0.9rem;
                color: #6b7280;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Display with Pandas Styler to force light theme
        st.dataframe(
            anom_df.style.set_properties(**{
                'background-color': '#ffffff',
                'color': '#1f2937',
                'border-color': '#e5e7eb'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f9fafb'), ('color', '#1f2937'), ('font-weight', '600')]},
                {'selector': 'td', 'props': [('color', '#1f2937')]}
            ]),
            width="stretch"
        )
        
        # Anomaly plot
        fig4 = go.Figure()
        
        # Main line
        fig4.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['consumption_kWh'], 
            mode='lines', 
            name='Consumption',
            line=dict(color='#3b82f6', width=2),
            opacity=0.8
        ))
        
        # Anomaly points
        fig4.add_trace(go.Scatter(
            x=anom_df['timestamp'], 
            y=anom_df['consumption_kWh'], 
            mode='markers', 
            name='Anomaly', 
            marker=dict(
                color='#ef4444',
                size=10,
                line=dict(color='white', width=1)
            )
        ))
        
        fig4.update_layout(
            **common_layout,
            xaxis_title=t('time'),
            yaxis_title=t('consumption_kwh'),
            legend=dict(
                bgcolor='white',
                bordercolor=grid_color,
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info(t("no_anomalies"))

def generate_pdf_report(df, analysis):
    from fpdf import FPDF
    import io
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="OctoGreen Energy Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Estimated Savings: {analysis['summary']['tasarruf_kwh']:.2f} kWh", ln=True)
    pdf.cell(200, 10, txt=f"Carbon Savings: {analysis['summary']['tasarruf_carbon']:.2f} kg CO2", ln=True)
    pdf.cell(200, 10, txt=f"USD Savings: {analysis['summary']['tasarruf_tl']:.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Recommendations:", ln=True)
    for rec in analysis['recommendations']:
        pdf.multi_cell(0, 10, rec)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Daily Totals:", ln=True)
    for day, val in analysis['summary']['daily_total'].items():
        pdf.cell(200, 10, txt=f"{day}: {val:.2f} kWh", ln=True)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()
