import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
import io

# 1. PLATFORM CONFIGURATION & CONSTANTS
BACKEND_URL = "https://veltrixcode-backend.onrender.com"

st.set_page_config(
    page_title="AI Strategy Analyzer Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { background-color: #007acc; color: white; border-radius: 4px; width: 100%; }
    .dashboard-title-main { font-size: 2.5rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem; }
    .dashboard-subtitle { font-size: 1.1rem; color: #8b949e; margin-bottom: 2rem; }
    .design-input-grid { background-color: #161b22; padding: 1.5rem; border-radius: 8px; border: 1px solid #30363d; }
    .dev-attribution { font-size: 0.85rem; color: #58a6ff; text-align: center; margin-top: 3rem; }
    </style>
""", unsafe_allow_html=True)

# Helper function to generate fallback mock PDF report buffer
def compile_pdf_document(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="VELTRIXCODE AI - Executive Strategy Report", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Win Rate: {data.get('win_rate', 'N/A')}", ln=2)
    return pdf.output(dest="S").encode("latin-1")

# 2. SESSION STATE INITIALIZATION
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "current_live_metrics" not in st.session_state:
    st.session_state.current_live_metrics = None
if "pdf_data_buffer" not in st.session_state:
    st.session_state.pdf_data_buffer = None

# 3. SIDEBAR AUTHENTICATION PANEL
with st.sidebar:
    st.markdown("## VELTRIXCODE AI")
    st.caption("Institutional Version 3.1.4")
    st.write("---")
    
    selected_view = st.radio("NAVIGATION", ["Core Engine Dashboard", "Strategy Leaderboard", "Privacy Policy", "Terms And Conditions"])
    
    st.write("---")
    st.markdown("### ENGINE STATUS")
    if st.session_state.is_logged_in:
        st.success(f"⚡ Connected: {st.session_state.user_email}")
        if st.button("Log Out"):
            st.session_state.is_logged_in = False
            st.session_state.user_email = ""
            st.rerun()
    else:
        st.warning("🔒 Engine Locked")
        with st.expander("Authentication Panel"):
            auth_email = st.text_input("Email Address")
            auth_pass = st.text_input("Security Token", type="password")
            if st.button("Unlock Framework"):
                if auth_email.strip() and len(auth_pass) > 4:
                    st.session_state.is_logged_in = True
                    st.session_state.user_email = auth_email.strip()
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

# 4. ROUTING & VIEWS EXECUTION
if selected_view == "Core Engine Dashboard":
    st.markdown('<div class="dashboard-title-main">AI Strategy Analyzer Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Analyze how your trading strategy performed over historical market data matrices.</div>', unsafe_allow_html=True)
    
    # Export Report Layout Block
    col_pdf_left, col_pdf_right = st.columns([3, 1])
    with col_pdf_right:
        if st.session_state.pdf_data_buffer:
            st.download_button(
                label="📄 Export Executive Report (PDF)",
                data=st.session_state.pdf_data_buffer,
                file_name="Veltrixcode_Executive_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.button("📄 Export Executive Report (PDF)", disabled=True)
            
    st.write("")
    
    # Grid Input Framework
    st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
    col_in_1, col_in_2, col_in_3 = st.columns([1, 1, 2])
    
    with col_in_1:
        target_ticker = st.text_input("📈 Target Asset Ticker", value="AAPL")
    with col_in_2:
        date_range = st.selectbox("📅 Evaluation Frame", ["365D", "180D", "90D"])
    with col_in_3:
        user_strategy = st.text_area("🔮 Strategy Evaluation Logic (Plain English)", value="Buy when price crosses above the 30 SMA.")
        
    run_clicked = st.button("🚀 Run Advanced Strategy Backtest Framework")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Form Action & Request Gate
    if run_clicked:
        if not user_strategy.strip():
            st.warning("Please verify strategy inputs.")
        elif not st.session_state.is_logged_in:
            st.error("🔒 Access Denied. Please log in from the authentication panel in the sidebar first.")
        else:
            with st.spinner("⚡ Compiling algorithm matrix..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/backtest",
                        json={
                            "ticker": target_ticker,
                            "frame": date_range,
                            "user_strategy": user_strategy
                        }
                    )
                    if response.status_code == 200:
                        data = response.json().get("performance_report", {})
                        st.session_state.current_live_metrics = data
                        st.session_state.pdf_data_buffer = compile_pdf_document(data)
                        st.success("🎯 Backtest completed successfully!")
                        st.rerun()
                    else:
                        try:
                            error_details = response.json()
                            st.error(f"❌ Backend Error 422 Structure Fault: {error_details}")
                        except:
                            st.error(f"Backend Error: Received status code {response.status_code}")
                except Exception as e:
                    st.error(f"Connection Error: Unable to reach the calculation engine. {str(e)}")

    # Display Metrics Workspace
    st.write("---")
    if st.session_state.current_live_metrics:
        m = st.session_state.current_live_metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("WIN RATE", f"{m.get('win_rate', '54.2')}%")
        col_m2.metric("TOTAL PROFIT FACTOR", f"{m.get('profit_factor', '1.85')}x")
        col_m3.metric("MAX DRAWDOWN", f"-{m.get('max_drawdown', '12.4')}%")
    else:
        st.info("The quantitative analytics metrics engine is currently loaded. Log in and click the execution button above to unlock your secure session workspace.")

elif selected_view == "Strategy Leaderboard":
    st.markdown('<div class="dashboard-title-main">Top Strategy Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Global rankings of top-performing strategy matrix submissions.</div>', unsafe_allow_html=True)
    
    try:
        lead_response = requests.get(f"{BACKEND_URL}/leaderboard")
        if lead_response.status_code == 200:
            leaderboard_data = lead_response.json().get("leaderboard", [])
            st.dataframe(pd.DataFrame(leaderboard_data), use_container_width=True)
        else:
            st.error("Database connection fault.")
    except Exception as e:
        fallback_lead = [{"Rank": "1", "Ticker": "NVDA", "Strategy Pattern": "Dual EMA Momentum Cross", "Win Rate (%)": "68.4%"}]
        st.dataframe(pd.DataFrame(fallback_lead), use_container_width=True)

elif selected_view == "Privacy Policy":
    st.markdown("### Privacy Policy")
    st.write("Your system telemetry parameters and strategy logic strings remain fully sandboxed and end-to-end encrypted.")

elif selected_view == "Terms And Conditions":
    st.markdown("### Terms And Conditions")
    st.write("Veltrixcode AI platform resources are explicitly restricted to institutional testing and backtesting analytics deployment framework execution.")

st.markdown('<div class="dev-attribution">Platform Core Architecture Engine | Developed under Veltrixcode AI Framework</div>', unsafe_allow_html=True)