import csv
import pandas as pd
from collections import deque
from src.record import Record

# Global variables to track the current order and profit
# These will be used to manage the state of the trading strategy
BUY_ORDER = None
PROFIT = 0

def read_csv_to_pandas(file_path, max_records=200):
    global BUY_ORDER, PROFIT
    buffer = deque(maxlen=max_records)  # Automatically keeps only the latest N records

    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            buffer.append(row)

            df = pd.DataFrame(buffer)
            if len(df) == max_records:
                data = Record(df)
                # buy logic
                if data.CLOSE > data.SMA_200 \
                and data.RSI_14 > 70 \
                and data.VOLUME > data.VA_20 \
                and data.MACD > data.MACD_signal \
                and data.MACD > 0 \
                and data.MACD_diff > 0 \
                and data.MACD_diff_PREV < data.MACD_diff \
                and BUY_ORDER is None:
                    BUY_ORDER = data
                    continue

                # sell logic
                if BUY_ORDER is not None and (\
                data.CLOSE < data.SMA_200 or \
                data.MACD < data.MACD_signal or \
                data.MACD_diff < 0 \
                or data.MACD_diff_PREV > data.MACD_diff ):
                    profit = data.CLOSE - BUY_ORDER.CLOSE
                    print({
                        "buy": str(BUY_ORDER),
                        "sell": str(data),
                        "profit": profit,
                        "category": "WIN" if profit > 0 else "LOSE",
                        "SELL_TRIGGER": "SMA"
                    })
                    PROFIT += profit
                    BUY_ORDER = None
                    
                    
                # take profit logic
                if  BUY_ORDER is not None and (data.CLOSE - BUY_ORDER.CLOSE) >= BUY_ORDER.ATR_14 * 2:
                    profit = data.CLOSE - BUY_ORDER.CLOSE
                    print({
                        "buy": str(BUY_ORDER),
                        "sell": str(data),
                        "profit": profit,
                        "category": "WIN" if profit > 0 else "LOSE",
                        "SELL_TRIGGER": "TAKE PROFIT"
                    })
                    PROFIT += profit
                    BUY_ORDER = None
                    

                # stop loss logic
                if BUY_ORDER is not None and (BUY_ORDER.CLOSE - data.CLOSE) >= BUY_ORDER.ATR_14 * 1.5:
                    profit = data.CLOSE - BUY_ORDER.CLOSE
                    print({
                        "buy": str(BUY_ORDER),
                        "sell": str(data),
                        "profit": profit,
                        "category": "WIN" if profit > 0 else "LOSE",
                        "SELL_TRIGGER": "STOP LOSS"
                    })
                    PROFIT += profit
                    BUY_ORDER = None
            
    print("Final Profit:", PROFIT)            

# Example usage
# read_csv_to_pandas('resources/EUR-USD_Minute_2022-05-01_to_2025-05-01.csv')

read_csv_to_pandas('resources/EUR-USD_Minute_2025-05-01_to_2025-08-01.csv')
