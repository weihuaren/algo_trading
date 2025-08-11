# PLAN

## Simple Moving Average Crossover Strategy

1. 20 and 50 SMA
2. Buy: 20 SMA > 50 + volume > volumeAverage(20) + RSI > 50   
3. Sell: 20 SMA < 50 SMA 
4. Stop-loss: 2*ATR(14)
5. Take-profit: 3X ATR(14)
5. Position Size 1~2% of account per trade

## Where to get free historical data?

https://www.dukascopy.com/swiss/english/marketwatch/historical/

## How to backtest?

I want to trade Futures FX major pair such as 6 month EUR/USD (M6E)
Since spot and futures follows close to each other, I will use spot for backtesting