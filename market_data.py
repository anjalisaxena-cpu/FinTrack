from services.market_data_service import MarketDataService

_SERVICE = MarketDataService()


def _normalize_symbol(symbol):
    return _SERVICE.normalize_symbol(symbol)


def get_all_stocks(access_token=None):
    return _SERVICE.get_stocks(access_token=access_token)


def get_stock(symbol, access_token=None):
    return _SERVICE.get_stock(symbol, access_token=access_token)


def generate_candles(symbol, interval="1d", points=24, access_token=None):
    del access_token
    return _SERVICE.get_historical_data(symbol, interval=interval, range_name="1M")[:points]


def get_market_snapshot(symbol=None, interval="1m", access_token=None):
    del access_token
    return _SERVICE.get_market_snapshot(symbol=symbol, interval=interval)


def get_market_overview():
    return _SERVICE.get_market_overview()


def record_websocket_tick(symbol, price, timestamp, previous_close=None, volume=0):
    return _SERVICE.record_websocket_tick(symbol, price, timestamp, previous_close, volume)


def get_websocket_ticks(symbol, after_id=0):
    return _SERVICE.get_websocket_ticks(symbol, after_id=after_id)


SIMULATED_MARKET = {
    symbol: {"name": data["name"], "price": data.get("price", 0)}
    for symbol, data in _SERVICE.market_map.items()
}
