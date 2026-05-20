import streamlit as st

st.set_page_config(
    page_title="Privacy Policy", 
    page_icon="📋", 
    layout="centered"
)

st.title("📋 Privacy Policy")
st.divider()

st.write("""
This AI Strategy Analyzer Tool does not provide financial, investment, legal, or trading advice. The platform is designed only for educational, research, and strategy backtesting purposes.

We may collect limited user data such as email address, uploaded strategy files, usage analytics, and technical information to improve platform performance and user experience.

We do not guarantee the accuracy, profitability, completeness, or reliability of any backtesting result, AI-generated analysis, market data, or trading insight shown by the platform.

Users are fully responsible for their own trading and investment decisions. Any financial loss, market loss, or damages resulting from the use of this platform are solely the user's responsibility.

We do not sell personal user data to third parties. However, third-party services such as payment gateways, analytics providers, APIs, or cloud hosting services may process certain technical data as required for platform functionality.

By using this platform, users agree to this Privacy Policy and consent to the collection and processing of data as described above.
""")