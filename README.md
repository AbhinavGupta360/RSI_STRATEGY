# RSI-Based Trading System (Nifty 50)

This repository contains a **research-focused RSI strategy** and a **live RSI scanner** applied to Nifty 50 stocks using hourly data.

The project is built for **strategy research and signal generation**, not portfolio simulation.

This repository contains:

1. **RSI Backtest**  
   - Hourly data for Nifty 50 stocks (last 2 years)
   - Entry: RSI crosses above 30 from oversold
   - Exit: Target, Stop Loss, RSI > 70, or Max bars in trade
   - Position size fixed to 1 unit (returns are percentage-based)
   - Metrics: Win rate, Avg PnL %, Total PnL %, Sharpe ratio
   - Focus: Strategy research (no capital compounding, no transaction costs)

2. **RSI Oversold Scanner (Live)**  
   - Flags stocks with RSI < 30 for 1-hour candles
   - Intended for swing-trade idea generation
   - Risk guidelines: 3% stop loss, 20% target, max holding 1 month

## Limitations
- Yahoo Finance hourly data availability varies by stock
- No transaction costs or slippage included
- Results are for research and educational purposes only

## 📈 Future Improvements
- Transaction cost modeling
- Volatility-based position sizing
- Strategy optimization & parameter sweep
- Live execution integration
