import pandas as pd
from ta.volatility import AverageTrueRange
from ta.trend import SMAIndicator
from ta.trend import MACD as MACDIndicator
from ta.momentum import RSIIndicator

class Data:
    def __init__(self, df: pd.DataFrame):

        # Ensure the columns have the correct data types
        df['open'] = pd.to_numeric(df['open'], errors='coerce')
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['volume'] = pd.to_numeric(df['volume'], errors='coerce')

        # calculate ATR
        atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14)
        df['ATR_14'] = atr.average_true_range()

        # calculate SMA(20)
        sma20 = SMAIndicator(close=df['close'], window=20)
        df['SMA_20'] = sma20.sma_indicator()

        # calculate SMA(50)
        sma50 = SMAIndicator(close=df['close'], window=50)
        df['SMA_50'] = sma50.sma_indicator()

        # calculate VA(20)
        va20 = SMAIndicator(close=df['volume'], window=20)
        df['VA_20'] = va20.sma_indicator()

        # calculate RSI(14)
        rsi = RSIIndicator(close=df['close'], window=14)
        df['RSI_14'] = rsi.rsi()

        # calculate MACD
        macd = MACDIndicator(close=df['close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()

        # indicators
        self.SMA_20 = df['SMA_20'].iloc[-1]
        self.SMA_50 = df['SMA_50'].iloc[-1]
        self.SMA_20_PREV = df['SMA_20'].iloc[-2]
        self.SMA_50_PREV = df['SMA_50'].iloc[-2]
        self.ATR_14 = df['ATR_14'].iloc[-1]
        self.RSI_14 = df['RSI_14'].iloc[-1]
        self.VA_20 = df['VA_20'].iloc[-1]
        self.MACD = df['MACD'].iloc[-1]
        self.MACD_signal = df['MACD_signal'].iloc[-1]
        self.MACD_diff = df['MACD_diff'].iloc[-1]
        self.MACD_diff_PREV = df['MACD_diff'].iloc[-2]

        # buy info 
        self.OPEN = df['open'].iloc[-1]
        self.HIGH = df['high'].iloc[-1]
        self.LOW = df['low'].iloc[-1]
        self.CLOSE = df['close'].iloc[-1]
        self.VOLUME = df['volume'].iloc[-1]  
        self.TIMESTAMP = df['timestamp'].iloc[-1]

    def __str__(self):
        return f"Data(TIMESTAMP={self.TIMESTAMP}, OPEN={self.OPEN}, HIGH={self.HIGH}, LOW={self.LOW}, CLOSE={self.CLOSE}, VOLUME={self.VOLUME}, SMA_20={self.SMA_20}, SMA_20_PREV={self.SMA_20_PREV},  SMA_50={self.SMA_50}, SMA_50_PREV={self.SMA_50_PREV}, ATR_14={self.ATR_14}, RSI_14={self.RSI_14}, VA_20={self.VA_20}, MACD={self.MACD}, MACD_signal={self.MACD_signal}, MACD_diff={self.MACD_diff})"
    
        