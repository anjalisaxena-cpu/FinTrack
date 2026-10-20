import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.environ.get(
        "FINTRACK_SECRET_KEY",
        "fintrack-development-key-change-me"
    )

    DATABASE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "fintrack.db"
    )

    UPSTOX_ACCESS_TOKEN = os.environ.get("UPSTOX_ACCESS_TOKEN", "")
    UPSTOX_CLIENT_ID = os.environ.get("UPSTOX_CLIENT_ID", "")
    UPSTOX_CLIENT_SECRET = os.environ.get("UPSTOX_CLIENT_SECRET", "")
    UPSTOX_REDIRECT_URI = os.environ.get("UPSTOX_REDIRECT_URI", "http://127.0.0.1:5000/upstox/callback")
    UPSTOX_API_BASE_URL = os.environ.get("UPSTOX_API_BASE_URL", "https://api.upstox.com")
    UPSTOX_INSTRUMENTS = {
        "RELIANCE": "NSE_EQ|INE002A01018",
        "TCS": "NSE_EQ|INE467B01029",
        "INFY": "NSE_EQ|INE009A01021",
        "HDFCBANK": "NSE_EQ|INE040A01034",
        "ICICIBANK": "NSE_EQ|INE090A01021",
        "SBIN": "NSE_EQ|INE062A01020",
        "BHARTIARTL": "NSE_EQ|INE397D01024",
        "ITC": "NSE_EQ|INE154A01025",
        "LT": "NSE_EQ|INE018A01030",
        "HINDUNILVR": "NSE_EQ|INE030A01027",
        "BAJFINANCE": "NSE_EQ|INE296A01024",
        "KOTAKBANK": "NSE_EQ|INE237A01028",
        "AXISBANK": "NSE_EQ|INE238A01034",
        "MARUTI": "NSE_EQ|INE585B01010",
        "SUNPHARMA": "NSE_EQ|INE044A01036",
        "TATAMOTORS": "NSE_EQ|INE155A01022",
        "TATASTEEL": "NSE_EQ|INE081A01020",
        "ADANIENT": "NSE_EQ|INE423A01024",
        "WIPRO": "NSE_EQ|INE075A01022",
        "M&M": "NSE_EQ|INE101A01026",
    }