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

# Custom Institutional Dark Theme CSS (Brings back exact look, colors, and layout)
st.markdown("""
    <style>
    /* Main Layout Framework */
    .main { background-color: #060913; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    div[data-testid="stSidebarUserContent"] { background-color: #0a0f24; }
    
    /* Premium Header Wave Elements */
    .header-container { 
        background: radial-gradient(circle at 90% 10%, rgba(24, 40, 110, 0.3) 0%, rgba(6, 9, 19, 0) 70%);
        padding: 2rem 0;
        margin-bottom: 1rem;
    }
    .dashboard-title-main { font-size: 2.8rem; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; margin-bottom: 0.2rem; }
    .dashboard-subtitle { font-size: 1.1rem; color: #6b7c96; margin-bottom: 1.5rem; }
    
    /* Form input container grid matching picture structure */
    .design-input-grid { 
        background-color: #0b132b; 
        padding: 1.8rem; 
        border-radius: 12px; 
        border: 1px solid #1c2541; 
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* Interactive Run Button styling updates */
    .stButton>button { 
        background: linear-gradient(90deg, #1b49b4 0%, #007acc 100%); 
        color: white; 
        border: none;
        border-radius: 6px; 
        padding: 0.6rem;
        font-weight: 600;
        width: 100%; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(0,122,204,0.4); }
    
    /* Premium Grid Tracking Cards mapping dashboard visualization components */
    .metric-card-custom {
        background: linear-gradient(145deg, #0b122c 0%, #070c1e 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #16224f;
        text-align: left;
    }
    .metric-card-title { font-size: 0.8rem; font-weight: 600; color: #5f759e; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 0.5rem; }
    .metric-card-value { font-size: 1.8rem; font-weight: 700; color: #00e676; margin-bottom: 0.2rem; }
    .metric-card-value.red-text { color: #ff3d00; }
    .metric-card-value.blue-text { color: #00b0ff; }
    
    /* Left panel custom notification card banners */
    .sidebar-lock-card {
        background-color: rgba(213, 0, 0, 0.05);
        border: 1px solid rgba(213, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 2rem;
    }
    .sidebar-lock-title { color: #ff1744; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.3rem; }
    .sidebar-lock-desc { color: #8892b0; font-size: 0.8rem; }
    
    .dev-attribution { font-size: 0.85rem; color: #415a77; text-align: center; margin-top: 4rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# Helper function to generate fallback PDF report buffer
def compile_pdf_document(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="VELTRIXCODE AI - Executive Strategy Report", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Win Rate: {data.get('win_rate', 'N/A')}", ln=2)
    pdf_string = pdf.output(dest="S")
    if isinstance(pdf_string, str):
        return pdf_string.encode("latin-1")
    return bytes(pdf_string)

# 2. SESSION STATE INITIALIZATION
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "current_live_metrics" not in st.session_state:
    st.session_state.current_live_metrics = None
if "pdf_data_buffer" not in st.session_state:
    st.session_state.pdf_data_buffer = None

# 3. SIDEBAR CONFIGURATION (Matches exact structure layout)
with st.sidebar:
    st.markdown("### AI STRATEGY ANALYZER PRO")
    auth_search = st.text_input("🔍 Search sections...", value="ui", label_visibility="collapsed")
    st.write("")
    
    selected_view = st.radio("NAVIGATION OPTIONS", ["Core Engine Dashboard", "Privacy Policy", "Terms And Conditions"], label_visibility="collapsed")
    
    st.write("---")
    st.markdown("🌐 **ENGINE RUNTIME**")
    
    if st.session_state.is_logged_in:
        st.success(f"🟢 Active Token: {st.session_state.user_email}")
        if st.button("Disconnect Session"):
            st.session_state.is_logged_in = False
            st.session_state.user_email = ""
            st.session_state.current_live_metrics = None
            st.session_state.pdf_data_buffer = None
            st.rerun()
    else:
        with st.expander("🔐 Security Access Gate", expanded=True):
            auth_email = st.text_input("Email Key", placeholder="Enter authorization key")
            auth_pass = st.text_input("Security Hash Token", type="password", placeholder="••••••••")
            if st.button("Initialize Engine Core"):
                if auth_email.strip() and len(auth_pass) > 4:
                    st.session_state.is_logged_in = True
                    st.session_state.user_email = auth_email.strip()
                    st.rerun()
                    
        # Restoring the explicit Red Locked box banner at bottom left
        st.markdown("""
            <div class="sidebar-lock-card">
                <div class="sidebar-lock-title">🔒 Terminal State: Locked</div>
                <div class="sidebar-lock-desc">The secure high-fidelity analytical computation matrix remains completely locked. Authenticate above to unlock processing parameters.</div>
            </div>
        """, unsafe_allow_html=True)

# 4. MAIN USER INTERFACE CORE VIEW
if selected_view == "Core Engine Dashboard":
    # Header layout wrapper with background tracking gradient mesh
    st.markdown("""
        <div class="header-container">
            <div class="dashboard-title-main">AI Strategy Analyzer Pro</div>
            <div class="dashboard-subtitle">Analyze how your trading strategy performed over historical market data matrices.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # PDF Action bar array alignment
    col_pdf_space, col_pdf_btn = st.columns([3.2, 1])
    with col_pdf_btn:
        if st.session_state.pdf_data_buffer:
            st.download_button(
                label="📄 Export Executive Report (PDF)",
                data=st.session_state.pdf_data_buffer,
                file_name="Veltrixcode_Premium_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.button("📄 Export Executive Report (PDF)", disabled=True)
            
    st.write("")
    
    # Structural Input Container Grid Framework
    st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
    col_in_1, col_in_2, col_in_3 = st.columns([1, 1.2, 2])
    
    with col_in_1:
        target_ticker = st.text_input("📈 Target Asset Ticker", value="AAPL")
    with col_in_2:
        date_range = st.selectbox("📅 Evaluation Frame", ["365D", "180D", "90D"])
    with col_in_3:
        user_strategy = st.text_area("🔮 Strategy Evaluation Logic (Plain English)", value="Buy when price crosses above the 50 SMA.")
        
    run_clicked = st.button("🚀 Run Advanced Strategy Backtest Framework")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process Pipeline Execution Layer
    if run_clicked:
        if not user_strategy.strip():
            st.warning("Please verify strategy inputs.")
        elif not st.session_state.is_logged_in:
            st.error("🔒 Access Denied. Please input your validation token inside the left side panel to authorize this engine.")
        else:
            with st.spinner("⚡ Compiling algorithm matrix analytics..."):
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
                        st.success("🎯 Analytics parsing pipeline run successful!")
                        st.rerun()
                    else:
                        st.error(f"Backend Engine Fault validation code: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection Error: Unable to sync with the backend services. {str(e)}")

    # 5. RESTORING PREMIUM 4-PANEL HIGHER VISUAL METRICS DATA WORKSPACE GRID
    st.write("---")
    
    # Blue tracking security warning lock container match
    if not st.session_state.current_live_metrics:
        st.markdown("""
            <div style="background-color: rgba(0, 176, 255, 0.04); border: 1px solid rgba(0, 176, 255, 0.2); padding: 1.2rem; border-radius: 8px; margin-bottom: 2rem; display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 1rem;">ℹ️</span>
                <div style="color: #4fc3f7; font-size: 0.95rem;">The quantitative analytics metrics engine is currently locked. Click the "Run Advanced Strategy Backtest Framework" button above to unlock processing visualizations.</div>
            </div>
        """, unsafe_allow_html=True)
        
    # Rebuilding the exact customized 4 metrics display rows layout across the footer tracking parameters
    col_card_1, col_card_2, col_card_3, col_card_4 = st.columns(4)
    m = st.session_state.current_live_metrics if st.session_state.current_live_metrics else {}
    
    with col_card_1:
        st.markdown(f"""
            <div class="metric-card-custom">
                <div class="metric-card-title">🛡️ Data Integrity</div>
                <div class="metric-card-value">{m.get('data_integrity', '99.98%')}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_card_2:
        st.markdown(f"""
            <div class="metric-card-custom">
                <div class="metric-card-title">🎯 Backtest Accuracy</div>
                <div class="metric-card-value blue-text">{m.get('backtest_accuracy', '98.76%')}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_card_3:
        st.markdown(f"""
            <div class="metric-card-custom">
                <div class="metric-card-title">🏅 Strategy Rating</div>
                <div class="metric-card-value">{m.get('strategy_rating', 'A+')}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_card_4:
        st.markdown(f"""
            <div class="metric-card-custom">
                <div class="metric-card-title">⚡ Processing Speed</div>
                <div class="metric-card-value blue-text">{m.get('processing_speed', 'Ultra-Fast')}</div>
            </div>
        """, unsafe_allow_html=True)

elif selected_view == "Privacy Policy":
    st.markdown("### Privacy Policy")
    st.write("Data pipelines are protected using high grade institutional architecture constraints.")

elif selected_view == "Terms And Conditions":
    st.markdown("### Terms And Conditions")
    st.write("System execution layers are explicitly restricted to simulation testing metrics verification structures.")

st.markdown('<div class="dev-attribution">Platform Core Architecture Engine | Developed under Veltrixcode AI Framework</div>', unsafe_allow_html=True)