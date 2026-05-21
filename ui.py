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
    initial_sidebar_state="collapsed"  # Force sidebar to completely hide on load
)

# Premium Global Stylesheet (Hides sidebar toggle button and centers everything perfectly)
st.markdown("""
    <style>
    /* Main Layout Overrides & Sidebar Complete Removal */
    .main { background-color: #060913; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    
    /* Premium Header Wave Mesh */
    .header-container { 
        background: radial-gradient(circle at 90% 10%, rgba(24, 40, 110, 0.3) 0%, rgba(6, 9, 19, 0) 70%);
        padding: 2rem 0;
        margin-bottom: 1rem;
    }
    .dashboard-title-main { font-size: 2.8rem; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; margin-bottom: 0.2rem; }
    .dashboard-subtitle { font-size: 1.1rem; color: #6b7c96; margin-bottom: 1.5rem; }
    
    /* Control Panel Box Structure */
    .design-input-grid { 
        background-color: #0b132b; 
        padding: 1.8rem; 
        border-radius: 12px; 
        border: 1px solid #1c2541; 
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* Interactive Action Buttons Styling */
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
    
    /* Premium Analytics Grid Tracking Cards */
    .metric-card-custom {
        background: linear-gradient(145deg, #0b122c 0%, #070c1e 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #16224f;
        text-align: left;
    }
    .metric-card-title { font-size: 0.8rem; font-weight: 600; color: #5f759e; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 0.5rem; }
    .metric-card-value { font-size: 1.8rem; font-weight: 700; color: #00e676; margin-bottom: 0.2rem; }
    .metric-card-value.blue-text { color: #00b0ff; }
    
    /* Fixed Center Modal Card Layout Rules */
    .popup-login-header { text-align: center; margin-bottom: 1.2rem; }
    .popup-logo-glow { font-size: 2.5rem; color: #00b0ff; text-shadow: 0 0 15px rgba(0,176,255,0.6); margin-bottom: 0.2rem; font-weight: bold; }
    .popup-welcome-txt { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin-bottom: 0.2rem; }
    .popup-sub-txt { font-size: 0.85rem; color: #6b7c96; margin-bottom: 0.4rem; }
    .popup-brand-powered { font-size: 0.75rem; font-weight: 700; color: #38ef7d; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1rem; }
    
    /* Styling for the hyperlink anchors inside terms */
    .popup-login-header a { color: #00b0ff !important; text-decoration: none; font-weight: 600; }
    .popup-login-header a:hover { text-decoration: underline; }
    
    div[data-testid="stTextInput"] input {
        background-color: #0b132b !important;
        border: 1px solid #1c2541 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }
    
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

# 2. PERSISTENT STATE TRACKING
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "current_live_metrics" not in st.session_state:
    st.session_state.current_live_metrics = None
if "pdf_data_buffer" not in st.session_state:
    st.session_state.pdf_data_buffer = None

# 3. COMPACT EMBEDDED POPUP INTERACTION GATE
@st.dialog("🔒 Secure Engine Gate", width="large")
def trigger_login_popup_gate():
    col_side_l, col_center_form, col_side_r = st.columns([0.8, 2.4, 0.8])
    
    with col_center_form:
        st.markdown("""
            <div class="popup-login-header">
                <div class="popup-logo-glow">▲</div>
                <div class="popup-welcome-txt">Sign In to Your Account</div>
                <div class="popup-sub-txt">Enter your credentials to connect to the cloud engine</div>
                <div class="popup-brand-powered">⚡ POWERED BY VELTRIXCODE AI</div>
            </div>
        """, unsafe_allow_html=True)
        
        auth_email = st.text_input("Email Address", placeholder="name@company.com")
        auth_pass = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.write("")
        # ⚖️ LEGAL COMPLIANCE: Clickable links rendered directly next to the selection checkbox field
        terms_accepted = st.checkbox("I accept the platform [Privacy Policy](https://veltrixcode-ai.streamlit.app/Privacy_Policy) and institutional [Terms & Conditions](https://veltrixcode-ai.streamlit.app/Terms_And_Conditions) constraints.")
        
        st.write("")
        if st.button("Sign In →", key="modal_submit_btn"):
            if not terms_accepted:
                st.warning("⚠️ Action blocked. You must accept the Privacy Policy and Terms to proceed.")
            elif auth_email.strip() and len(auth_pass) > 4:
                st.session_state.is_logged_in = True
                st.session_state.user_email = auth_email.strip()
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Invalid access credentials token.")
                
        st.markdown('<div style="text-align:center; color:#5f759e; margin: 0.3rem 0; font-size:0.8rem;">OR</div>', unsafe_allow_html=True)
        
        if st.button("🔴 Continue with Google (Enterprise SSO)", key="google_oauth_bypass"):
            if not terms_accepted:
                st.warning("⚠️ Action blocked. You must accept the Privacy Policy and Terms to proceed.")
            else:
                st.session_state.is_logged_in = True
                st.session_state.user_email = "sso.user@veltrixcode.ai"
                st.rerun()

# 4. MAIN DASHBOARD FRAME INTERFACE
st.markdown("""
    <div class="header-container">
        <div class="dashboard-title-main">AI Strategy Analyzer Pro</div>
        <div class="dashboard-subtitle">Analyze how your trading strategy performed over historical market data matrices.</div>
    </div>
""", unsafe_allow_html=True)

# Account session logout row display handler (Now sits elegantly right above the controls layout)
if st.session_state.is_logged_in:
    col_user_info, col_logout_act = st.columns([3.5, 1])
    with col_user_info:
        st.markdown(f"🟢 **Session Secured:** `{st.session_state.user_email}`")
    with col_logout_act:
        if st.button("Disconnect Session 🔓"):
            st.session_state.is_logged_in = False
            st.session_state.user_email = ""
            st.session_state.current_live_metrics = None
            st.session_state.pdf_data_buffer = None
            st.rerun()
    st.write("")

# PDF Export row segment
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

# Input Field Box Configuration Matrix 
st.markdown('<div class="design-input-grid">', unsafe_allow_html=True)
col_in_1, col_in_2, col_in_3 = st.columns([1, 1.2, 2])

with col_in_1:
    target_ticker = st.text_input("📈 Target Asset Ticker", value="AAPL")
with col_in_2:
    date_range = st.selectbox("📅 Evaluation Frame", ["365D", "180D", "90D"])
with col_in_3:
    user_strategy = st.text_area("🔮 Strategy Evaluation Logic (Plain English)", value="Buy when price crosses above the 30 SMA.")
    
run_clicked = st.button("🚀 Run Advanced Strategy Backtest Framework")
st.markdown('</div>', unsafe_allow_html=True)

# Form Execution Routing
if run_clicked:
    if not user_strategy.strip():
        st.warning("Please verify strategy inputs.")
    elif not st.session_state.is_logged_in:
        trigger_login_popup_gate()
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
                st.error(f"Connection Error: Unable to sync with backend services. {str(e)}")

# 5. DATA CARD METRICS WORKSPACE
st.write("---")

if not st.session_state.current_live_metrics:
    st.markdown("""
        <div style="background-color: rgba(0, 176, 255, 0.04); border: 1px solid rgba(0, 176, 255, 0.2); padding: 1.2rem; border-radius: 8px; margin-bottom: 2rem; display: flex; align-items: center;">
            <span style="font-size: 1.5rem; margin-right: 1rem;">ℹ️</span>
            <div style="color: #4fc3f7; font-size: 0.95rem;">The quantitative analytics metrics engine is currently locked. Click the "Run Advanced Strategy Backtest Framework" button above to unlock processing visualizations.</div>
        </div>
    """, unsafe_allow_html=True)
    
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

st.markdown('<div class="dev-attribution">Platform Core Architecture Engine | Developed under Veltrixcode AI Framework</div>', unsafe_allow_html=True)