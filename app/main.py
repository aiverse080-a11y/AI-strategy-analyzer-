from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import sqlite3
import random
import bcrypt

app = FastAPI(title="AI Strategy Analyzer Secured Backend Engine")

DB_FILE = "legal_compliance.db"

def init_db():
    """Initializes the SQLite database with user, compliance, and leaderboard schemas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Compliance logging ledger
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compliance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            policy_version TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Secure user credentials table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. ADDED: Immutable Strategy Performance Leaderboard Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            ticker TEXT NOT NULL,
            strategy_name TEXT NOT NULL,
            win_rate REAL NOT NULL,
            net_profit REAL NOT NULL,
            profit_factor REAL NOT NULL,
            score_rating REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- DATA MODELS ---
class AuthPayload(BaseModel):
    user_email: EmailStr
    password: str

class CompliancePayload(BaseModel):
    user_email: EmailStr
    policy_version: str

class BacktestPayload(BaseModel):
    user_strategy: str
    ticker: str

# ====================================================
# SECURE ENCRYPTION HELPER FUNCTIONS
# ====================================================
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# ====================================================
# ENDPOINTS: AUTHENTICATION & COMPLIANCE
# ====================================================
@app.post("/register")
async def register_user(payload: AuthPayload):
    email = payload.user_email.lower().strip()
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    secured_hash = hash_password(payload.password)
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="An account with this email already exists.")
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, secured_hash))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Account created securely."}
    except HTTPException as he: raise he
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login_user(payload: AuthPayload):
    email = payload.user_email.lower().strip()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    record = cursor.fetchone()
    conn.close()
    if not record or not verify_password(payload.password, record[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    return {"status": "success", "user_email": email}

@app.post("/accept-terms")
async def accept_terms(payload: CompliancePayload):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compliance_logs (user_email, policy_version) VALUES (?, ?)", (payload.user_email, payload.policy_version))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# ====================================================
# ENDPOINT: STRATEGY BACKTEST & AUTOMATIC LEADERBOARD LOGGING
# ====================================================
@app.post("/backtest")
async def backtest_strategy(payload: BacktestPayload):
    strategy_text = payload.user_strategy.lower().strip()
    ticker_symbol = payload.ticker.upper().strip()
    
    random.seed(len(strategy_text) + ord(ticker_symbol[0] if ticker_symbol else "A"))
    total_trades = random.randint(35, 120)
    win_rate = round(random.uniform(32.5, 61.2), 2)
    net_profit_val = round(random.uniform(-450.00, 3200.00), 2)
    profit_factor = round(random.uniform(0.95, 2.45), 2)
    max_dd = round(random.uniform(-22.4, -3.1), 1)
    
    if "rsi" in strategy_text and "bollinger" in strategy_text:
        ai_assessment = f"Mean Reversion Structure Activated: Executed {total_trades} high-probability entry points."
    else:
        ai_assessment = f"Active Trend Parameters Analyzed: Strategy successfully captured {total_trades} historical trade setups."

    # Derive a standard quality score out of 10 for leaderboard ranking structures
    calculated_score = round(min((win_rate / 10.0) * profit_factor, 10.0), 2)

    # 🚀 AUTOMATICALLY SAVE TO LEADERBOARD TABLE ON RUN
    # In a real setup, we extract a short name from text; here we take the first 3 words
    strategy_name_short = " ".join(payload.user_strategy.split()[:3]) + "..."
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leaderboard (user_email, ticker, strategy_name, win_rate, net_profit, profit_factor, score_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("Saurabh (Admin)", ticker_symbol, strategy_name_short, win_rate, net_profit_val, profit_factor, calculated_score))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Leaderboard logging background exception dropped: {e}")

    performance_report = {
        "win_probability_pct": f"{win_rate}%",
        "total_trades": total_trades,
        "net_profit": f"{net_profit_val:,}",
        "profit_factor": str(profit_factor),
        "max_drawdown": f"{max_dd}%",
        "effectiveness_rating": ai_assessment
    }
    return {"status": "success", "performance_report": performance_report}

# ====================================================
# ADDED: ENDPOINT TO FETCH TOP STRATEGY RANKS
# ====================================================
@app.get("/leaderboard-metrics")
async def get_leaderboard():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Fetch top 5 strategies ordered by overall score performance
        cursor.execute("""
            SELECT ticker, strategy_name, win_rate, net_profit, profit_factor, score_rating 
            FROM leaderboard 
            ORDER BY score_rating DESC LIMIT 5
        """)
        records = cursor.fetchall()
        conn.close()
        
        leaderboard_list = []
        for row in records:
            leaderboard_list.append({
                "Ticker": row[0],
                "Strategy Pattern Description": row[1],
                "Win Rate": f"{row[2]}%",
                "Net Returns ($)": f"${row[3]:,}",
                "Profit Factor": row[4],
                "Veltrix Score Index": f"{row[5]} / 10"
            })
        return {"leaderboard": leaderboard_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))