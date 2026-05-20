import pandas as pd
import numpy as np

def fetch_market_data(ticker: str) -> pd.DataFrame:
    """
    Generates 365 days of mock historical market data for testing the AI engine.
    """
    # Create a range of dates for the last 365 days (1 full year)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=365, freq='D')
    
    # Generate mock price action data with a slight upward drift
    np.random.seed(42)
    base_price = 150.0 if ticker == "AAPL" else 100.0
    price_changes = np.random.normal(loc=0.001, scale=0.02, size=365)
    price_path = base_price * np.exp(np.cumsum(price_changes))
    
    df = pd.DataFrame(index=dates)
    df['close'] = price_path
    df['open'] = df['close'].shift(1).fillna(base_price)
    df['high'] = df[['open', 'close']].max(axis=1) + np.random.uniform(0, 2, size=365)
    df['low'] = df[['open', 'close']].min(axis=1) - np.random.uniform(0, 2, size=365)
    df['volume'] = np.random.randint(100000, 1000000, size=365)
    
    return df