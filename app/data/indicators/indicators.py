import pandas as pd
import numpy as np

def add_rsi(df: pd.DataFrame, periods: int = 14):
    """
    Calculates the 14-day Relative Strength Index (RSI) 
    and adds it as a column to the DataFrame.
    """
    close_delta = df['close'].diff()

    # Separate positive gains and negative losses
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    # Calculate exponential moving averages
    ma_up = up.ewm(com=periods - 1, adjust=False).mean()
    ma_down = down.ewm(com=periods - 1, adjust=False).mean()
        
    # Handle division by zero edge-cases
    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    
    # Fill initial NaN rows with a default neutral RSI value of 50
    df['rsi'] = rsi.fillna(50.0)
    return df