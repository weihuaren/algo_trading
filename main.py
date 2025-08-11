import csv
import pandas as pd
from collections import deque
from ta.volatility import AverageTrueRange
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator

buy_price = None
profit = 0
buy_atr = None

def read_csv_to_pandas(file_path, max_records=51):
    global buy_price, profit, buy_atr
    buffer = deque(maxlen=max_records)  # Automatically keeps only the latest N records

    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            buffer.append(row)
            df = pd.DataFrame(buffer)
            if len(df) == max_records:
                df['high'] = pd.to_numeric(df['high'], errors='coerce')
                df['low'] = pd.to_numeric(df['low'], errors='coerce')
                df['close'] = pd.to_numeric(df['close'], errors='coerce')
                df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
                atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14)
                df['ATR_14'] = atr.average_true_range()

                # --- SMA(20) ---
                sma20 = SMAIndicator(close=df['close'], window=20)
                df['SMA_20'] = sma20.sma_indicator()

                # --- VSMA(20) ---
                vsma20 = SMAIndicator(close=df['volume'], window=20)
                df['VSMA_20'] = vsma20.sma_indicator()

                # --- SMA(50) ---
                sma50 = SMAIndicator(close=df['close'], window=50)
                df['SMA_50'] = sma50.sma_indicator()

                # --- RSI(14) ---
                rsi = RSIIndicator(close=df['close'], window=14)
                df['RSI_14'] = rsi.rsi()

                # --- ATR(14) ---
                atr14 = SMAIndicator(close=df['ATR_14'], window=20)
                df['ATR_14_20'] = atr14.sma_indicator()


                current_sme20 = df.iloc[[-1]]['SMA_20'].item()
                current_sme50 = df.iloc[[-1]]['SMA_50'].item()                
                previous_sme20 = df.iloc[[-2]]['SMA_20'].item()
                previous_sme50 = df.iloc[[-2]]['SMA_50'].item()
                current_atr = df.iloc[[-1]]['ATR_14'].item()
                current_rsi = df.iloc[[-1]]['RSI_14'].item()
                current_timestamp = pd.to_datetime(df.iloc[[-1]]['timestamp'].item(), utc=True)
                current_price = df.iloc[[-1]]['close'].item()
                current_vsma20 = df.iloc[[-1]]['VSMA_20'].item()
                current_volume = df.iloc[[-1]]['volume'].item()
                current_atr20 = df.iloc[[-1]]['ATR_14_20'].item()
                if all(v is not None for v in [current_sme20, current_sme50, previous_sme20, previous_sme50]):
                    
                    # buy logic
                    if current_sme20 > current_sme50 \
                    and previous_sme20 < previous_sme50 \
                    and current_rsi > 60 \
                    and current_volume > current_vsma20 \
                    and buy_price is None:
                        print(f"Date: {current_timestamp} volume: {current_volume} volume_average: {current_vsma20} SRI14: {current_rsi} SME20: {current_sme20}, SME50: {current_sme50}, Previous SME20: {previous_sme20}, Previous SME50: {previous_sme50}")
                        buy_price = current_price
                        buy_atr = current_atr
                        print("BUY at ", buy_price)

                    # sell logic
                    if current_sme20 < current_sme50 and buy_price is not None:
                        print(f"Date: {current_timestamp} ATR: {buy_atr} SME20: {current_sme20}, SME50: {current_sme50}, Previous SME20: {previous_sme20}, Previous SME50: {previous_sme50}")
                        profit = current_price - buy_price
                        print("SOLD at ", current_price)
                        print("PROFIT:", profit)
                        buy_price = None
                        buy_atr = None
                        profit = profit + profit
                    
                    # take profit logic
                    if buy_price is not None and (current_price - buy_price) >= buy_atr * 3:
                        print(f"Date: {current_timestamp} ATR: {buy_atr} SME20: {current_sme20}, SME50: {current_sme50}, Previous SME20: {previous_sme20}, Previous SME50: {previous_sme50}")
                        profit = current_price - buy_price
                        print("TAKE PROFIT at ", current_price)
                        print("PROFIT:", profit)
                        buy_price = None
                        buy_atr = None
                        profit = profit + profit
                    
                    # stop loss logic
                    if buy_price is not None and (buy_price - current_price) >= buy_atr * 1.5:
                        print(f"Date: {current_timestamp} ATR: {buy_atr} SME20: {current_sme20}, SME50: {current_sme50}, Previous SME20: {previous_sme20}, Previous SME50: {previous_sme50}")
                        profit = current_price - buy_price 
                        print("STOP LOSS at ", current_price)
                        print("LOSS:", profit)
                        buy_price = None
                        buy_atr = None
                        profit = profit + profit
            
    print("Final Profit:", profit)            

# Example usage
read_csv_to_pandas('resources/EUR-USD_Minute_2025-07-01_to_2025-08-01.csv', max_records=51)
