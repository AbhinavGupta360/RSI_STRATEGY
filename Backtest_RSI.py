import yfinance as yf
import pandas as pd

# Every symbol that are under Nifty50 currently

symbols = [
    "TECHM.NS","INDIGO.NS","KOTAKBANK.NS","BAJFINANCE.NS","HINDUNILVR.NS",
    "MARUTI.NS","HINDALCO.NS","HCLTECH.NS","AXISBANK.NS","ASIANPAINT.NS",
    "ITC.NS","SUNPHARMA.NS","BEL.NS","HDFCLIFE.NS","POWERGRID.NS",
    "BHARTIARTL.NS","EICHERMOT.NS","TATASTEEL.NS","COALINDIA.NS",
    "SBILIFE.NS","ULTRACEMCO.NS","SBIN.NS","DRREDDY.NS","NESTLEIND.NS",
    "GRASIM.NS","CIPLA.NS","HDFCBANK.NS","INFY.NS","M&M.NS",
    "JSWSTEEL.NS","LT.NS","TATACONSUM.NS","BAJAJ-AUTO.NS","APOLLOHOSP.NS",
    "NTPC.NS","TITAN.NS","ADANIENT.NS","TCS.NS","ONGC.NS",
    "ADANIPORTS.NS","ICICIBANK.NS","RELIANCE.NS","WIPRO.NS",
    "SHRIRAMFIN.NS","JIOFIN.NS","BAJAJFINSV.NS","ETERNAL.NS","TRENT.NS"
]

# RSI backtest

RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
MAX_BARS_IN_TRADE = 200
STOP_LOSS_PCT = 30
TARGET= 50

# Trades stored

all_trades = []

# Backtesting backend

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

for symbol in symbols:
    print(f"Backtesting {symbol}...")
    try:
        df = yf.download(symbol, period="730d", interval="1h", progress=False)
        df['RSI'] = rsi(df['Close'], RSI_PERIOD)
        df.dropna(inplace=True)

        POSITION = 0
        ENTRY_PRICE = 0
        ENTRY_BAR = 0

        for i in range(1, len(df)):
            price = df["Close"].iloc[i].item()

            # Entry

            if POSITION == 0 and df['RSI'].iloc[i-1] < RSI_OVERSOLD and df['RSI'].iloc[i] >= RSI_OVERSOLD:
                POSITION = 1
                ENTRY_PRICE = price
                ENTRY_BAR = i
                ENTRY_TIME = df.index[i]

            # Exit conditions

            elif POSITION == 1:
                exit_signal = False

                if price >= ENTRY_PRICE * (1 + TARGET/100):
                    exit_signal = True
                    exit_reason = "TARGET"
                elif price <= ENTRY_PRICE * (1 - STOP_LOSS_PCT/100):
                    exit_signal = True
                    exit_reason = "STOP LOSS"
                elif df['RSI'].iloc[i] > RSI_OVERBOUGHT:
                    exit_signal = True
                    exit_reason = "RSI OVERBOUGHT"
                elif i - ENTRY_BAR >= MAX_BARS_IN_TRADE:
                    exit_signal = True
                    exit_reason = "TIME EXIT"

                if exit_signal:
                    exit_price = price

                    all_trades.append({
                        "Stock": symbol,
                        "Entry Time": ENTRY_TIME,
                        "Exit Time": df.index[i],
                        "Entry Price": ENTRY_PRICE,
                        "Exit Price": exit_price,
                        "PnL %": (exit_price - ENTRY_PRICE)/ENTRY_PRICE*100,
                        "Exit Reason": exit_reason
                    })

                    POSITION = 0

        # Forced Exit

        if POSITION == 1:
            final_price = df["Close"].iloc[-1].item()

            all_trades.append({
                "Stock": symbol,
                "Entry Time": ENTRY_TIME,
                "Exit Time": df.index[-1],
                "Entry Price": ENTRY_PRICE,
                "Exit Price": final_price,
                "PnL %": (final_price - ENTRY_PRICE)/ENTRY_PRICE*100,
                "Exit Reason": "FORCED EXIT"
            })

            POSITION = 0

    except Exception as e:
        print(f"Error for {symbol}: {e}")
        continue

# Backtest results

trades_df = pd.DataFrame(all_trades)

returns= trades_df["PnL %"] / 100
risk_free_rate= 0 # Assuming 0 risk-free rate due to trade-based return calculation and irregular trading capital.
sharpe = (returns.mean() - risk_free_rate) / returns.std()


if not trades_df.empty:
    print(trades_df.head())
    print("\nTotal Trades:", len(trades_df))
    print("Win Rate (%):", (trades_df['PnL %'] > 0).mean() * 100)
    print("Average PnL (%):", trades_df['PnL %'].mean())
    print("Sum of Trade Returns (%):", trades_df['PnL %'].sum())
    print("Sharpe Ratio: ", sharpe)
else:
    print("No trades generated.")
