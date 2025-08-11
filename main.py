import csv
import pandas as pd
from collections import deque
from src.Data import Data

# Global variables to track the current order and profit
# These will be used to manage the state of the trading strategy
CURRENT_ORDER = None
PROFIT = 0

def read_csv_to_pandas(file_path, max_records=51):
    global CURRENT_ORDER, PROFIT
    buffer = deque(maxlen=max_records)  # Automatically keeps only the latest N records

    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            buffer.append(row)
            df = pd.DataFrame(buffer)
            if len(df) == max_records:
                data = Data(df)

                # buy logic
                if data.SMA_20 > data.SMA_50 \
                and data.SMA_20_PREV < data.SMA_50_PREV \
                and data.RSI_14 > 50 \
                and data.VOLUME > data.VA_20 \
                and data.MACD > data.MACD_signal \
                and data.MACD > 0 \
                and data.MACD_diff > 0 \
                and data.MACD_diff_PREV < data.MACD_diff \
                and CURRENT_ORDER is None:
                    CURRENT_ORDER = data
                    continue

                # sell logic
                if CURRENT_ORDER is not None and \
                data.SMA_20 < data.SMA_50 and \
                data.MACD < data.MACD_signal and \
                data.MACD_diff < 0 \
                and data.MACD_diff_PREV > data.MACD_diff :
                    profit = data.CLOSE - CURRENT_ORDER.CLOSE
                    print({
                        "buy": str(CURRENT_ORDER),
                        "sell": str(data),
                        "profit": profit,
                        "category": "WIN" if profit > 0 else "LOSE",
                        "SELL_TRIGGER": "SMA"
                    })
                    PROFIT += profit
                    CURRENT_ORDER = None
                    
                    
                # take profit logic
                if  CURRENT_ORDER is not None and (data.CLOSE - CURRENT_ORDER.CLOSE) >= CURRENT_ORDER.ATR_14 * 4:
                    profit = data.CLOSE - CURRENT_ORDER.CLOSE
                    print({
                        "buy": str(CURRENT_ORDER),
                        "sell": str(data),
                        "profit": profit,
                        "category": "WIN" if profit > 0 else "LOSE",
                        "SELL_TRIGGER": "TAKE PROFIT"
                    })
                    PROFIT += profit
                    CURRENT_ORDER = None
                    

                # stop loss logic
                if CURRENT_ORDER is not None and (CURRENT_ORDER.CLOSE - data.CLOSE) >= CURRENT_ORDER.ATR_14 * 2:
                    profit = data.CLOSE - CURRENT_ORDER.CLOSE
                    print({
                        "buy": str(CURRENT_ORDER),
                        "sell": str(data),
                        "profit": profit,
                        "category": "WIN" if profit > 0 else "LOSE",
                        "SELL_TRIGGER": "STOP LOSS"
                    })
                    PROFIT += profit
                    CURRENT_ORDER = None
            
    print("Final Profit:", PROFIT)            

# Example usage
read_csv_to_pandas('resources/EUR-USD_Minute_2025-07-01_to_2025-08-01.csv')
