import os
import pandas as pd
from google import genai


api_key = "AIzaSyBUk9SaPWSfWXyK64YpH2MCCoo_JSyTZcY"
client = genai.Client(api_key=api_key)

def generate_signals(df: pd.DataFrame, user_strategy_text: str):
    """
    The Infinite Strategy Engine: Uses GenAI to convert ANY raw English text
    into executable Python Pandas code on the fly, then runs it.
    """
    local_df = df.copy()
    local_df['signal'] = 'HOLD'
    
    system_instruction = """
    You are an expert algorithmic trading engineer. Your job is to convert raw human trading strategies into executable Python code using the pandas library.
    You will be given a pandas DataFrame named 'df' with columns: ['open', 'high', 'low', 'close', 'volume'].
    Set the 'signal' column to 'BUY' or 'SELL' based on the user's rules. If no conditions match, leave it as 'HOLD'.
    Return ONLY valid, raw executable Python code. Do not wrap code in markdown blocks or backticks. No comments, no explanations.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Convert this strategy into code: {user_strategy_text}",
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )
        
        generated_code = response.text.strip()
        
        print("\n=== [AI DYNAMIC CODE GENERATED] ===")
        print(generated_code)
        print("===================================\n")
        
        environment_variables = {'df': local_df}
        exec(generated_code, globals(), environment_variables)
        
        processed_df = environment_variables['df']
        return processed_df

    except Exception as e:
        print(f"--- [AI ENGINE ERROR] Fallback applied due to: {e} ---")
        return local_df