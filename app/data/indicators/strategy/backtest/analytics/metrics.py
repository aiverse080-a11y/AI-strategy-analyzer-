import pandas as pd

def calculate_metrics(trades_df: pd.DataFrame) -> dict:
    """
    Calculates detailed performance statistics, including Win Probability,
    from the executed trades data frame.
    """
    # If no trades were executed, return a clean empty report
    if trades_df.empty:
        return {
            "total_trades": 0,
            "win_probability_pct": "0.0%",
            "winning_trades": 0,
            "losing_trades": 0,
            "net_profit": 0.0,
            "effectiveness_rating": "No trades executed to determine effectiveness."
        }
    
    total_trades = len(trades_df)
    
    # In your simulator, winning trades are where profit > 0
    winning_trades = len(trades_df[trades_df['profit'] > 0])
    losing_trades = total_trades - winning_trades
    
    # Calculate Win Probability
    win_prob = (winning_trades / total_trades) * 100
    
    # Determine an effectiveness rating text based on the probability
    if win_prob >= 60:
        rating = "Highly Effective 🔥"
    elif win_prob >= 45:
        rating = "Moderate Effectiveness ⚖️"
    else:
        rating = "Low Effectiveness 📉"
        
    net_profit = trades_df['profit'].sum()
    
    return {
        "total_trades": total_trades,
        "win_probability_pct": f"{round(win_prob, 2)}%",
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "net_profit": round(net_profit, 2),
        "effectiveness_rating": rating
    }
