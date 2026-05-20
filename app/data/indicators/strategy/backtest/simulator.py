import pandas as pd

def run_backtest(df: pd.DataFrame, initial_capital: float = 10000.0, stop_loss_pct: float = 0.02, take_profit_pct: float = 0.06):
    """
    Simulates trading based on BUY/SELL signals in the DataFrame.
    Enforces a strict Stop-Loss and Take-Profit rule.
    """
    balance = initial_capital
    position = 0.0        # How many units of the asset we currently hold
    entry_price = 0.0     # The price we bought at
    trades = []           # List to store history of completed trades
    in_position = False

    # Loop through the data row by row (simulating time moving forward)
    for index, row in df.iterrows():
        current_price = row['close']
        signal = row.get('signal', 'HOLD')

        # Case 1: We are NOT in a trade, look for a BUY signal
        if not in_position:
            if signal == 'BUY':
                position = balance / current_price  # Go all-in with current balance
                entry_price = current_price
                balance = 0.0
                in_position = True
                # Log the entry point
                trades.append({
                    'entry_time': index,
                    'entry_price': entry_price,
                    'type': 'LONG'
                })

        # Case 2: We ARE currently in a trade, monitor exit conditions
        else:
            # Calculate current price movement relative to our entry
            price_change_pct = (current_price - entry_price) / entry_price
            
            # Check for standard SELL signal OR Hit Safety Net (Stop-Loss / Take-Profit)
            hit_stop_loss = price_change_pct <= -stop_loss_pct
            hit_take_profit = price_change_pct >= take_profit_pct
            
            if signal == 'SELL' or hit_stop_loss or hit_take_profit:
                # Sell everything and get back our cash balance
                balance = position * current_price
                profit_loss = balance - (initial_capital if len(trades) == 1 else (position * entry_price))
                
                # Determine what triggered the exit for cleaner reporting
                exit_reason = "SIGNAL"
                if hit_stop_loss:
                    exit_reason = "STOP_LOSS"
                elif hit_take_profit:
                    exit_reason = "TAKE_PROFIT"

                # Update the last trade entry with exit details
                trades[-1].update({
                    'exit_time': index,
                    'exit_price': current_price,
                    'profit': balance - (position * entry_price),
                    'exit_reason': exit_reason
                })
                
                position = 0.0
                entry_price = 0.0
                in_position = False

    # If a trade is still left open at the very end of the historical data, close it out
    if in_position:
        balance = position * df.iloc[-1]['close']
        trades[-1].update({
            'exit_time': df.index[-1],
            'exit_price': df.iloc[-1]['close'],
            'profit': balance - (position * entry_price),
            'exit_reason': "FORCE_CLOSE"
        })

    return trades