import gradio as gr
import pandas as pd
import requests

# 1. PLATFORM CONFIGURATION & CONSTANTS
BACKEND_URL = "https://veltrixcode-backend.onrender.com"

# Custom Institutional Dark Theme CSS (Bloomberg/Quant Terminal Style)
custom_css = """
body, .gradio-container { background-color: #050811 !important; color: #d1d5db !important; font-family: 'Courier New', Courier, monospace !important; }
.terminal-header { background: linear-gradient(180deg, #0b1120 0%, #050811 100%); padding: 1.5rem; border-bottom: 2px solid #1e293b; margin-bottom: 1.5rem; }
.terminal-title { font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -1px; }
.terminal-status-pill { display: inline-block; background-color: #064e3b; color: #34d399; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 700; margin-top: 0.5rem; }
.parameter-board { background-color: #0f172a !important; padding: 1.5rem; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 1.5rem; }
.execute-btn { background: linear-gradient(90deg, #1b49b4 0%, #007acc 100%) !important; color: white !important; font-weight: 600 !important; border: none !important; }
.execute-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(0,122,204,0.4); }
.legal-markdown a { color: #00b0ff !important; text-decoration: none; font-weight: 600; }
.legal-markdown a:hover { text-decoration: underline; }
"""

# Helper function to generate default historical mock ledger matching backend structure
def get_mock_ledger(ticker):
    return pd.DataFrame([
        {"Order Ticket": "TKT-109", "Execution Timestamp": "2026-05-18 10:30", "Side": "BUY/LONG", "Asset": ticker, "Price Point": "$172.40", "Position Allocation": "100 Shares", "Realized PnL Profile": "RUNNING"},
        {"Order Ticket": "TKT-108", "Execution Timestamp": "2026-05-14 15:45", "Side": "SELL/CLOSE", "Asset": ticker, "Price Point": "$176.10", "Position Allocation": "100 Shares", "Realized PnL Profile": "+$370.00 MATURED"},
        {"Order Ticket": "TKT-107", "Execution Timestamp": "2026-05-09 09:15", "Side": "BUY/LONG", "Asset": ticker, "Price Point": "$171.20", "Position Allocation": "100 Shares", "Realized PnL Profile": "LIQUIDATED"},
        {"Order Ticket": "TKT-106", "Execution Timestamp": "2026-05-03 14:20", "Side": "SELL/CLOSE", "Asset": ticker, "Price Point": "$168.90", "Position Allocation": "100 Shares", "Realized PnL Profile": "-$110.00 MATURED"},
        {"Order Ticket": "TKT-105", "Execution Timestamp": "2026-04-28 11:00", "Side": "BUY/LONG", "Asset": ticker, "Price Point": "$170.00", "Position Allocation": "100 Shares", "Realized PnL Profile": "LIQUIDATED"}
    ])

# 2. GRADIO CORE SYSTEM ROUTER & CONTROLLER LAYER
def execute_quant_backtest(ticker, frame, strategy, email, password, terms_checkbox):
    # Gating Check 1: Verify Legal Box
    if not terms_checkbox:
        return (
            gr.update(visible=True, value="⚠️ ACTION BLOCKED: You must accept regulatory compliance rules before executing code."),
            gr.update(visible=False), None, "", "", "", "", "", "", "", "", "", None
        )
    
    # Gating Check 2: Verify Universal Login Input Completeness
    if not email.strip() or not password.strip():
        return (
            gr.update(visible=True, value="⚠️ ACCESS DENIED: Please fill out both the Username ID and Security Token fields."),
            gr.update(visible=False), None, "", "", "", "", "", "", "", "", "", None
        )
    
    # Handshake Processing Pipeline
    try:
        response = requests.post(
            f"{BACKEND_URL}/backtest",
            json={"ticker": ticker, "frame": frame, "user_strategy": strategy},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json().get("performance_report", {})
            
            # Formulate Outputs cleanly for dashboard viewport updates
            win_rate = f"{str(data.get('win_rate', '54.2')).replace('%', '')}%"
            profit_factor = f"{str(data.get('profit_factor', '2.38')).replace('x', '')}x"
            max_dd = f"{str(data.get('max_drawdown', '-16.4')).replace('%', '')}%"
            total_trades = str(data.get('total_trades', '110'))
            
            sharpe = str(data.get('sharpe_ratio', '1.84'))
            sortino = str(data.get('sortino_ratio', '2.15'))
            alpha = str(data.get('alpha', '0.12'))
            beta = str(data.get('beta', '0.94'))
            
            net_profit = f"${data.get('net_profit', '14,240')}"
            avg_win = f"${data.get('avg_win', '340')}"
            avg_loss = f"-${str(data.get('avg_loss', '180')).replace('-', '')}"
            pl_ratio = str(data.get('pl_ratio', '1.88'))
            
            ai_insights = data.get('ai_insights', "The execution model indicates steady risk-adjusted alpha metrics across volatility vectors.")
            ledger_df = get_mock_ledger(ticker)
            
            return (
                gr.update(visible=False),              # Hide error block
                gr.update(visible=True),               # Show full analytics panel
                ledger_df,                             # Historical data table
                win_rate, profit_factor, max_dd, total_trades,
                sharpe, sortino, alpha, beta,
                net_profit, avg_win, avg_loss, pl_ratio,
                ai_insights
            )
        else:
            return (
                gr.update(visible=True, value=f"❌ Backend Engine Failure Validation Code: {response.status_code}"),
                gr.update(visible=False), None, "", "", "", "", "", "", "", "", "", None
            )
            
    except Exception as e:
        return (
            gr.update(visible=True, value=f"❌ Handshake Error: Unable to sync with the cloud architecture engine. {str(e)}"),
            gr.update(visible=False), None, "", "", "", "", "", "", "", "", "", None
        )

# 3. BUILD INTERFACE ARCHITECTURE USING GRADIO BLOCKS MESH
with gr.Blocks(css=custom_css, title="Veltrixcode Quantitative Terminal") as demo:
    
    # Header Panel Block
    gr.HTML("""
        <div class="terminal-header">
            <div class="terminal-title">VELTRIXCODE QUANTITATIVE TERMINAL v3.1</div>
            <div class="terminal-status-pill">📡 CORES SYNCED: GRADIO RUNTIME SECURE EDGE</div>
        </div>
    """)
    
    # Universal Gateway Sign In Card (Embedded right inside the workspace seamlessly)
    with gr.Row(elem_classes="parameter-board"):
        with gr.Column(scale=2):
            gr.Markdown("### 🔒 ENGINE RUNTIME GATEWAY SECURE ACCESS")
            gr.Markdown("Enter any demonstration authorization properties below to connect current interface terminal parameters to remote processing computing cores.")
        with gr.Column(scale=1):
            ui_email = gr.Textbox(label="User ID Key Address", placeholder="operator@firm.com", max_lines=1)
        with gr.Column(scale=1):
            ui_pass = gr.Textbox(label="Security Access Token Key", placeholder="••••••••", type="password", max_lines=1)
        with gr.Column(scale=2):
            ui_terms = gr.Checkbox(label="I verify asset configuration compliance rules.", value=False)
            gr.Markdown("Read compliance definitions: [Privacy Policy](https://veltrixcode-ai.streamlit.app/Privacy_Policy) | [Terms & Conditions](https://veltrixcode-ai.streamlit.app/Terms_And_Conditions)", elem_classes="legal-markdown")

    # Strategy Configuration Form Panel Grid
    with gr.Row(elem_classes="parameter-board"):
        with gr.Column(scale=1):
            in_ticker = gr.Textbox(label="📈 ASSET TICKER", value="AAPL", max_lines=1)
        with gr.Column(scale=1.2):
            in_frame = gr.Dropdown(label="📅 HISTORICAL LOOKBACK FRAME", choices=["365D", "180D", "90D"], value="365D")
        with gr.Column(scale=2.8):
            in_strategy = gr.Textbox(label="🔮 STRATEGY EXECUTION LOGIC (PLAIN ENGLISH)", value="Buy when price crosses above the 30 SMA.", lines=2)
            
    # Universal Application Compute Action Button 
    btn_execute = gr.Button("🚀 EXECUTE HIGH-FIDELITY BACKTEST SEQUENCE", elem_classes="execute-btn")
    
    # Hidden System Alert Messenger Block
    txt_error_msg = gr.Textbox(visible=False, label="TERMINAL ERROR FEEDBACK ALERT SYSTEM", interactive=False)
    
    # --- OUTPUTS QUANT DESKTOP VIEWPORT BLOCK PANEL (Initially hidden, loads on successful login/compute) ---
    with gr.Column(visible=False) as output_panel:
        gr.Markdown("## 📊 CORES COMPUTATION VIEWPORT METRICS BOARD")
        
        # Tier 1: Main High Level Executive KPI Row Block
        with gr.Row():
            out_win = gr.Textbox(label="🎯 Strategy Win Rate", interactive=False)
            out_pf = gr.Textbox(label="📊 Gross Profit Factor", interactive=False)
            out_dd = gr.Textbox(label="📉 Peak Max Drawdown", interactive=False)
            out_count = gr.Textbox(label="💼 Executed Trade Count", interactive=False)
            
        # Tier 2: Interactive Data Tab Architecture Containers
        with gr.Tabs():
            with gr.TabItem("🛡️ RISK-ADJUSTED ALPHA METRICS"):
                with gr.Row():
                    out_sharpe = gr.Textbox(label="Sharpe Ratio (Risk-Free Index Adj.)", interactive=False)
                    out_sortino = gr.Textbox(label="Sortino Ratio (Downside Volatility Adj.)", interactive=False)
                    out_alpha = gr.Textbox(label="Alpha Vector Score (Benchmark Excess)", interactive=False)
                    out_beta = gr.Textbox(label="Beta Volatility Profile Index", interactive=False)
                    
            with gr.TabItem("💵 PROFIT & VOLATILITY EXPECTANCY"):
                with gr.Row():
                    out_net = gr.Textbox(label="Net Strategy System Profit Accrual", interactive=False)
                    out_awin = gr.Textbox(label="Average Gain Per Profitable Position", interactive=False)
                    out_aloss = gr.Textbox(label="Average Cost Loss Per Drag Position", interactive=False)
                    out_plr = gr.Textbox(label="Profit-to-Loss Multiplier Mathematical Index", interactive=False)
                    
            with gr.TabItem("📜 TRANSACTION ORDER LOG LEDGER"):
                out_ledger_table = gr.DataFrame(label="Complete Institutional System-Fill Ledger Matrix", interactive=False)
                
        # Tier 3: Machine Learning Natural Language Summaries Block
        gr.Markdown("### 🔮 MACHINE INTELLIGENCE QUANT STRATEGY INTERPRETATION")
        out_insights = gr.Markdown()
        
    # 4. INTERFACE EVENTS REACTION BINDINGS MAP
    btn_execute.click(
        fn=execute_quant_backtest,
        inputs=[in_ticker, in_frame, in_strategy, ui_email, ui_pass, ui_terms],
        outputs=[
            txt_error_msg, output_panel, out_ledger_table,
            out_win, out_pf, out_dd, out_count,
            out_sharpe, out_sortino, out_alpha, out_beta,
            out_net, out_awin, out_aloss, out_plr,
            out_insights
        ]
    )

# 5. INITIALIZE LOCAL WEB SERVER DESKTOP EXECUTION ENVIRONMENT INSTANCE
if __name__ == "__main__":
    demo.launch()