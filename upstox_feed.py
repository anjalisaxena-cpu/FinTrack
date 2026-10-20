import threading
import time

from config import Config


_feed_lock = threading.Lock()
_feed_thread = None
_feed_status = {"connected": False, "error": None}


def feed_status():
    with _feed_lock:
        return dict(_feed_status)


def start_feed(access_token):
    global _feed_thread
    if not access_token:
        return {"connected": False, "error": "missing access token"}
    with _feed_lock:
        if _feed_thread and _feed_thread.is_alive():
            return dict(_feed_status)
        _feed_status.update({"connected": False, "error": None})
        _feed_thread = threading.Thread(target=_run_feed, args=(access_token,), daemon=True)
        _feed_thread.start()
    return feed_status()


def _run_feed(access_token):
    try:
        import upstox_client

        configuration = upstox_client.Configuration()
        configuration.access_token = access_token
        api_client = upstox_client.ApiClient(configuration)
        instrument_keys = list(Config.UPSTOX_INSTRUMENTS.values())
        streamer = upstox_client.MarketDataStreamerV3(api_client, instrument_keys, "full")
        streamer.on("open", _mark_connected)
        streamer.on("message", _handle_message)
        streamer.on("error", _mark_error)
        streamer.connect()
    except Exception as error:
        _mark_error(error)


def _mark_connected(*_args):
    with _feed_lock:
        _feed_status.update({"connected": True, "error": None})


def _mark_error(error):
    with _feed_lock:
        _feed_status.update({"connected": False, "error": str(error)})


def _handle_message(message):
    if isinstance(message, bytes):
        return
    feeds = message.get("feeds", {}) if isinstance(message, dict) else {}
    for instrument_key, feed in feeds.items():
        ltpc = feed.get("ltpc", {}) if isinstance(feed, dict) else {}
        price = _find_price(ltpc) or _find_price(feed)
        if price is None:
            continue
        symbol = next((name for name, key in Config.UPSTOX_INSTRUMENTS.items() if key == instrument_key), None)
        if symbol:
            from market_data import record_websocket_tick

            timestamp = float(ltpc.get("ltt") or message.get("currentTs") or time.time())
            if timestamp > 1_000_000_000_000:
                timestamp /= 1000
            record_websocket_tick(symbol, price, timestamp, float(ltpc.get("cp") or 0), int(ltpc.get("ltq") or 0))


def _find_price(value):
    if isinstance(value, dict):
        for key in ("ltp", "last_price"):
            if key in value:
                try:
                    return float(value[key])
                except (TypeError, ValueError):
                    return None
        for child in value.values():
            price = _find_price(child)
            if price is not None:
                return price
    return None
