# FinTrack

FinTrack is a Flask-based personal finance and investment tracker with a dashboard, market data integration, paper trading, watchlist, expense tracking, goals, risk analysis, and learning content.

## Setup

1. Open a terminal in the project folder.
2. Create a virtual environment:
   `python -m venv .venv`
3. Activate it:
   `.venv\Scripts\activate`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your keys.
6. Start the app:
   `python app.py`

## Environment

- `FINTRACK_SECRET_KEY` – Flask secret key
- `ALPHA_VANTAGE_API_KEY` – free-tier market data key from Alpha Vantage
- `TWELVE_DATA_API_KEY` – optional Twelve Data key for REST quotes and historical candles; obtain a free key at [Twelve Data](https://twelvedata.com/register)
- `UPSTOX_*` – optional Upstox OAuth configuration

## Notes

- Paper trading tracks 20 NSE companies plus AAPL. Connect Upstox for exchange WebSocket ticks and live tick-sized candlesticks; Twelve Data's free Basic plan requires an account key and limits WebSocket testing to 8 trial symbols.
- Candlestick sizes below one second group received exchange ticks; they do not create additional market updates. Without a provider quote, the app marks data unavailable rather than inventing prices or candles.
- This is a paper-trading student project and does not place real trades.
