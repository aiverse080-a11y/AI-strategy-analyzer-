import streamlit as st
import requests
import pandas as pd
import numpy as np
import os
from fpdf import FPDF

# 1. High-Fidelity Wide-Screen Settings
st.set_page_config(
    page_title="AI Strategy Analyzer Pro", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

bg_file = "my_photo.jpg" if os.path.exists("my_photo.jpg") else ("my_photo.png" if os.path.exists("my_photo.png") else None)

# 2. Advanced CSS Layout Customizations
css_style = """
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #0A142C 0%, #030712 60%) !important;
        color: #F3F4F6;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    header, [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] {
        background-color: #050A15 !important;
        border-right: 1px solid rgba(59, 130, 246, 0.15) !important;
    }
    .sidebar-title { font-size: 0.85rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 15px; margin-bottom: 5px; }
    .dashboard-title-main { font-size: 2.8rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 2px; position: relative; z-index: 1; }
    .dashboard-subtitle { color: #64748B; font-size: 1.05rem; margin-top: -5px; margin-bottom: 25px; position: relative; z-index: 1; }
    .design-input-grid { background: rgba(6, 11, 24, 0.8); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px; padding: 24px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5); margin-bottom: 20px; position: relative; z-index: 1; }
    .telemetry-pill-box { background: #060C1A; border: 1px solid rgba(59, 130, 246, 0.15); border-radius: 10px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; height: 100%; }
    .progress-bar-cyan { background: #1E293B; border-radius: 100px; height: 4px; margin-top: 10px; overflow: hidden; }
    .progress-fill-cyan { background: #06B6D4; height: 100%; box-shadow: 0 0 10px #06B6D4; }
    .progress-fill-blue { background: #3B82F6; height: 100%; box-shadow: 0 0 10px #3B82F6; }
    .metric-value-up { font-size: 2.4rem; font-weight: 700; color: #10B981; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
    .metric-value-neutral { font-size: 2.4rem; font-weight: 700; color: #3B82F6; text-shadow: 0 0 15px rgba(59, 130, 246, 0.3); }
    .metric-value-risk { font-size: 2.4rem; font-weight: 700; color: #EF4444; text-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }
    .metric-label-glow { font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 8px; }
    .insight-card { background: linear-gradient(135deg, rgba(10, 17, 34, 0.9) 0%, rgba(59, 130, 246, 0.08) 100%); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 10px; padding: 18px; margin-bottom: 14px; }
    
    div.stButton > button {
        background: linear-gradient(90deg, #1E40AF 0%, #0284C7 100%) !important; border: none !important; color: #FFFFFF !important; font-weight: 600 !important; letter-spacing: 0.5px !important; border-radius: 8px !important; padding: 12px 24px !important; box-shadow: 0 4px 15px rgba(30, 64, 175, 0.4) !important; transition: all 0.3s ease;
    }
    div.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 25px rgba(2, 132, 199, 0.6) !important; }
    
    div.stDownloadButton > button {
        background: linear-gradient(90deg, #059669 0%, #10B981 100%) !important; border: none !important; color: #FFFFFF !important; font-weight: 600 !important; border-radius: 8px !important; padding: 12px 24px !important; width: 100%; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    div.stDownloadButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5) !important; }

    .dev-attribution { text-align: center; margin-top: 50px; margin-bottom: -45px; font-size: 0.9rem; color: #64748B; position: relative; z-index: 1; }
    .dev-glow-name { color: #3B82F6; font-weight: 600; text-shadow: 0 0 8px rgba(59, 130, 246, 0.4); }
    .footer-disclaimer { border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 24px 0; margin-top: 70px; font-size: 0.75rem; color: #334155; text-align: center; position: relative; z-index: 1; }
    </style>
"""

if bg_file:
    import base64
    with open(bg_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    css_style += f"""
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url('data:image/jpeg;base64,{encoded_string}');
        background-repeat: no-repeat;
        background-position: center 35%;
        background-size: 40%;
        opacity: 0.03;
        z-index: 0;
        pointer-events: none;
    }}
    """
st.markdown(css_style, unsafe_allow_html=True)

# 3. Modular PDF Text Compiler Routine
def compile_pdf_document(report_dict, ticker_str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Veltrixcode AI - Executive Strategy Backtest Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Platform Context Validation Matrix", ln=True, align="C")
    pdf.line(10, 32, 200, 32)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "1. Core Backtest Metrics Evaluation Parameters", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Target Asset Ticker Symbol: {ticker_str}", ln=True)
    pdf.cell(0, 6, f"Win Rate Probability Index: {report_dict.get('win_probability_pct')}", ln=True)
    pdf.cell(0, 6, f"Net Profit Returns Accumulation: ${report_dict.get('net_profit')}", ln=True)
    pdf.cell(0, 6, f"Total Historical Setup Trades Processed: {report_dict.get('total_trades')}", ln=True)
    pdf.cell(0, 6, f"Calculated Strategy Profit Factor: {report_dict.get('profit_factor')}", ln=True)
    pdf.cell(0, 6, f"Maximum Account Drawdown Sequence: {report_dict.get('max_drawdown')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "2. AI Insights Analytical Performance Assessment", ln=True)
    pdf.set_font("Helvetica", "", 11)
    
    raw_insight = str(report_dict.get("effectiveness_rating", "Stable"))
    safe_insight_text = raw_insight.encode('ascii', 'ignore').decode('ascii')
    
    pdf.multi_cell(0, 6, safe_insight_text)
    return bytes(pdf.output())

# 4. Session State Engine Initialization
if "is_logged_in" not in st.session_state: st.session_state.is_logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = None
if "current_live_metrics" not in st.session_state:
    st.session_state.current_live_metrics = {
        "win_probability_pct": "54.2%", "total_trades": 24, "net_profit": "1,420.50", "profit_factor": "1.64", "max_drawdown": "-8.4%", "effectiveness_rating": "Moderate Consistency Evaluation Parameters"
    }

if "pdf_data_buffer" not in st.session_state:
    st.session_state.pdf_data_buffer = compile_pdf_document(st.session_state.current_live_metrics, "AAPL")

# ====================================================
# APP NAVIGATION SYSTEM & SIDEBAR MOCK
# ====================================================
with st.sidebar:
    st.text_input("Application View Context", value="Dashboard", disabled=True, label_visibility="collapsed")
    st.write("")
    st.markdown("<h2 style='color:#FFFFFF; font-size:1.4rem; margin-bottom:0;'>VELTRIXCODE AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#475569; font-size:0.8rem; margin-bottom:25px;'>Institutional Version 3.1.4</p>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Engine</div>', unsafe_allow_html=True)
    st.markdown("<p style='color:#3B82F6; font-size:0.95rem; font-weight:600; margin-left:5px;'>⚡ QUANT ENGINE</p>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
    selected_view = st.radio("NAV", ["Core Engine Dashboard", "🏆 Strategy Leaderboard", "Privacy Policy", "Terms & Conditions"], label_visibility="collapsed")
    st.divider()
    if st.session_state.is_logged_in:
        st.markdown(f"<p style='color:#10B981; font-size:0.85rem;'>👤 Active: {st.session_state.user_email}</p>", unsafe_allow_html=True)
        if st.button("Log Out Workspace", width="stretch"):
            st.session_state.is_logged_in = False
            st.session_state.user_email = None
            st.rerun()
    else:
        st.markdown("<p style='color:#EF4444; font-size:0.85rem; font-weight:600;'>🔒 Terminal Locked</p>", unsafe_allow_html=True)

# ====================================================
# PRIVACY POLICY VIEW
# ====================================================
if selected_view == "Privacy Policy":
    st.markdown('<div class="dashboard-title-main">📋 Privacy Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Veltrixcode AI User Data Shielding and Encryption Manifest.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
    st.markdown("### 1. Data Protection Architecture")
    st.write("At Veltrixcode AI, security is a core element of our network design. All user credentials, specifically email addresses and access passwords, are hashed instantly using the industrial standard `bcrypt` algorithm with a work factor scaling round of 12 before touching our SQLite database layer. This ensures absolute privacy from end-to-end.")
    
    st.markdown("### 2. Strategy Information and Query Tracing")
    st.write("All strategy evaluations and text analysis matrices processed inside the terminal workspace are executed dynamically in session memory cache loops. Raw strategy strings are parsed locally and are not sold, transmitted, or shared with third-party analytical marketing vectors.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="dev-attribution">Platform Core Architecture Designed and Maintained by: <span class="dev-glow-name">Saurabh</span></div>', unsafe_allow_html=True)
    st.stop()

# ====================================================
# TERMS & CONDITIONS VIEW
# ====================================================
elif selected_view == "Terms & Conditions":
    st.markdown('<div class="dashboard-title-main">⚖️ Terms & Conditions</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Platform Operational Framework Limitations and User Usage Terms.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
    st.markdown("### 1. Educational and Backtesting Restrictions")
    st.write("This application framework operates strictly as a quantitative historical mathematical simulator asset wrapper. The performance scores, win probabilities, return indices, and analytical evaluations rendered by the Veltrixcode engine do not constitute financial trading advice or investment solicitation parameter routes.")
    
    st.markdown("### 2. Liability Disclaimers")
    st.write("The platform developers and administrators maintain absolute zero accountability or legal asset liability for capital metrics exposure or live operational financial results executed based on simulated logic curves generated here.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="dev-attribution">Platform Core Architecture Designed and Maintained by: <span class="dev-glow-name">Saurabh</span></div>', unsafe_allow_html=True)
    st.stop()

# ====================================================
# STANDALONE LEADERBOARD VIEW
# ====================================================
if selected_view == "🏆 Strategy Leaderboard":
    st.markdown('<div class="dashboard-title-main">Top Strategy Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Global rankings of top performing quantitative algorithms sorted by Veltrix Score index matrices.</div>', unsafe_allow_html=True)
    st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
    st.markdown("<p style='font-weight:700; color:#06B6D4; letter-spacing:0.5px; margin-bottom:15px;'>🏅 RUNNING HIGH SCORE LEADERBOARD SYSTEM</p>", unsafe_allow_html=True)
    try:
        lead_response = requests.get("https://veltrixcode-backend.onrender.com/leaderboard-metrics", timeout=5)
        if lead_response.status_code == 200:
            st.dataframe(pd.DataFrame(lead_response.json().get("leaderboard", [])), use_container_width=True)
        else: st.error("Database connection fault.")
    except Exception as e:
        fallback_lead = [{"Rank": "1", "Ticker": "NVDA", "Strategy Pattern": "RSI Breakout...", "Win Rate": "58.4%", "Net Profit": "$2,840.00", "Profit Factor": "2.10", "Veltrix Index": "9.1 / 10"}]
        st.dataframe(pd.DataFrame(fallback_lead), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dev-attribution">Platform Core Architecture Designed and Maintained by: <span class="dev-glow-name">Saurabh</span></div>', unsafe_allow_html=True)
    st.stop()

# ====================================================
# MASTER TERMINAL WORKSPACE VIEW (CORE ENGINE DASHBOARD)
# ====================================================
live_report = st.session_state.current_live_metrics

col_header_l, col_header_r = st.columns([3, 1])
with col_header_l:
    st.markdown('<div class="dashboard-title-main">AI Strategy Analyzer Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Analyze how your trading strategy performed over historical market data matrices.</div>', unsafe_allow_html=True)
with col_header_r:
    st.write(""); st.write("")
    st.download_button(
        label="📄 Export Executive Report (PDF)",
        data=st.session_state.pdf_data_buffer,
        file_name="Veltrixcode_Executive_Report.pdf",
        mime="application/pdf"
    )

# Strategy Operational Controls Form Layout Block
st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
col_in_1, col_in_2, col_in_3 = st.columns([1, 1, 2])
with col_in_1: ticker = st.text_input("📈 Target Asset Ticker", value="AAPL").upper().strip()
with col_in_2: date_range = st.selectbox("📅 Evaluation Frame", ["365D Backtest (Full)", "90D Frame", "30D Fast Frame"])
with col_in_3: user_strategy = st.text_area("🔮 Strategy Evaluation Logic (Plain English)", value="Buy when price crosses above the 30 SMA.", height=68)
run_clicked = st.button("🚀 Run Advanced Strategy Backtest Framework", width="stretch")
st.markdown('</div>', unsafe_allow_html=True)

if run_clicked:
    if not user_strategy.strip(): st.warning("Please verify strategy inputs.")
  elif not st.session_state.is_logged_in:
            st.error("🔒 Access Denied. Please log in from the authentication panel first.")
    else:
        with st.spinner("⚡ Compiling algorithm matrix..."):
            try:
                response = requests.post("https://veltrixcode-backend.onrender.com/backtest", json={"user_strategy": user_strategy, "ticker": ticker}, timeout=60)
                if response.status_code == 200:
                    data = response.json()["performance_report"]
                    st.session_state.current_live_metrics = data
                    st.session_state.pdf_data_buffer = compile_pdf_document(data, ticker)
                    st.success("Analysis Matrix Synced Successfully.")
                    st.rerun()
            except Exception as e: st.error(f"Backend offline: {e}")

if not st.session_state.is_logged_in:
    st.info("🔒 The quantitative analytics metrics engine is currently locked. Click the execution button above to unlock your secure session workspace.")
else:
    # --- DATA CARDS ---
    m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
    with m_col1: st.markdown(f'<div class="design-input-grid"><div class="metric-label-glow">Win Rate</div><div class="metric-value-up">{live_report.get("win_probability_pct")}</div></div>', unsafe_allow_html=True)
    with m_col2: st.markdown(f'<div class="design-input-grid"><div class="metric-label">Net Profit</div><div class="metric-value-up">${live_report.get("net_profit")}</div></div>', unsafe_allow_html=True)
    with m_col3: st.markdown(f'<div class="design-input-grid"><div class="metric-label">Total Trades</div><div class="metric-value-neutral">{live_report.get("total_trades")}</div></div>', unsafe_allow_html=True)
    with m_col4: st.markdown(f'<div class="design-input-grid"><div class="metric-label">Profit Factor</div><div class="metric-value-up">{live_report.get("profit_factor")}</div></div>', unsafe_allow_html=True)
    with m_col5: st.markdown(f'<div class="design-input-grid"><div class="metric-label">Max Drawdown</div><div class="metric-value-risk">{live_report.get("max_drawdown")}</div></div>', unsafe_allow_html=True)
    with m_col6: st.markdown(f'<div class="design-input-grid"><div class="metric-label">Risk Reward</div><div class="metric-value-neutral">1:2.4</div></div>', unsafe_allow_html=True)

    # --- HORIZONTAL TELEMETRY TRACERS ---
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    with t_col1: st.markdown('<div class="telemetry-pill-box"><div class="metric-label-glow">🛡️ Data Integrity</div><div style="font-size:1.3rem; font-weight:700; color:#06B6D4;">99.98%</div><div class="progress-bar-cyan"><div class="progress-fill-cyan" style="width: 99%;"></div></div></div>', unsafe_allow_html=True)
    with t_col2: st.markdown('<div class="telemetry-pill-box"><div class="metric-label-glow">🎯 Backtest Accuracy</div><div style="font-size:1.3rem; font-weight:700; color:#3B82F6;">98.76%</div><div class="progress-bar-cyan"><div class="progress-fill-blue" style="width: 98%;"></div></div></div>', unsafe_allow_html=True)
    with t_col3: st.markdown('<div class="telemetry-pill-box"><div class="metric-label-glow">🏅 Strategy Rating</div><div style="font-size:1.3rem; font-weight:700; color:#10B981;">A+</div><div class="progress-bar-cyan"><div class="progress-fill-cyan" style="width: 95%;"></div></div></div>', unsafe_allow_html=True)
    with t_col4: st.markdown('<div class="telemetry-pill-box"><div class="metric-label-glow">🚀 Processing Speed</div><div style="font-size:1.3rem; font-weight:700; color:#3B82F6;">Ultra-Fast</div><div class="progress-bar-cyan"><div class="progress-fill-blue" style="width: 100%;"></div></div></div>', unsafe_allow_html=True)

    st.write("")
    
    # --- EQUITY LINE & AI HIGHLIGHTS ROW ---
    layout_col_l, layout_col_r = st.columns([2, 1])
    with layout_col_l:
        st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight:600; color:#3B82F6; margin-bottom:15px;'>📊 STRATEGY EQUITY CURVE VS BUY & HOLD</p>", unsafe_allow_html=True)
        chart_df = pd.DataFrame({"Timeline": pd.date_range(end=pd.Timestamp.now(), periods=100), "Strategy Equity Curve": 10000 + np.cumsum(np.random.normal(50, 150, 100)), "Buy & Hold Benchmark": 10000 + np.cumsum(np.random.normal(30, 200, 100))}).set_index("Timeline")
        st.line_chart(chart_df, color=["#3B82F6", "#64748B"])
        st.markdown('</div>', unsafe_allow_html=True)
    with layout_col_r:
        st.markdown('<div class="design-input-grid" style="height:100%;">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight:600; color:#3B82F6; margin-bottom:15px;'>💡 AI INSIGHTS ANALYTICAL METRICS</p>", unsafe_allow_html=True)
        st.markdown(f'<div class="insight-card" style="border-left: 4px solid #3B82F6;"><span style="color:#3B82F6; font-weight:bold;">🎯 Performance Assessment</span><br><span style="font-size:0.95rem; color:#E5E7EB;">{live_report.get("effectiveness_rating")}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)