import yfinance as yf
import pandas as pd

RSI_PERIOD = 14
RSI_OVERSOLD = 30

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

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

signals = []

for symbol in symbols:
    try:
        df = yf.download(symbol, interval="1h", period="14d", progress=False)

        df["RSI"] = compute_rsi(df["Close"])
        df.dropna(inplace=True)

        last_rsi = df["RSI"].iloc[-1]
        last_price = df["Close"].iloc[-1]

        # ENTRY
        if last_rsi < RSI_OVERSOLD:
            signals.append({
                "Stock": symbol
            })

    except Exception as e:
        print(f"Error in {symbol}: {e}")

signals_df = pd.DataFrame(signals)

print("\n LIVE BUYING SIGNALS FOR 1 HOUR INTERVAL SWING TRADES.")
if not signals_df.empty:
    print(signals_df.to_string(index=False))
    print("Keep STOP LOSS 3% below CURRENT PRICE.\nTake TARGET 20% above CURRENT PRICE.\nDo NOT hold it for more than a MONTH.")
else:
    print("No Trading Setup For Now.")

