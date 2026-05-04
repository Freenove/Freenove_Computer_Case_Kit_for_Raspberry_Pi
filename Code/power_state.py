import json
import datetime

try:
    import redis as _redis_module
    _REDIS_AVAILABLE = True
except ImportError:
    _REDIS_AVAILABLE = False

_client = None
_RATE_NIGHT = 22.98  # 平日23:00-6:00, 休日22:00-8:00
_RATE_DAY   = 20.05  # 平日9:00-16:00, 休日8:00-22:00
_RATE_LIFE  = 32.65  # 平日6:00-9:00 および 16:00-23:00（ライフタイム）
_JST = datetime.timezone(datetime.timedelta(hours=9))


def _get_client():
    global _client
    if _client is None and _REDIS_AVAILABLE:
        try:
            _client = _redis_module.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        except Exception:
            pass
    return _client


def get_power_reading():
    """Return current power consumption in watts from Redis, or None on failure."""
    client = _get_client()
    if client is None:
        return None
    try:
        raw = client.get('my_key')
        if raw is None:
            return None
        data = json.loads(raw)
        return float(data['POWER']['value'])
    except Exception:
        return None


def get_current_rate_yen_per_kwh():
    """Return electricity rate (yen/kWh) based on current JST time and day type."""
    now = datetime.datetime.now(tz=_JST)
    hour = now.hour
    is_weekend = now.weekday() >= 5  # 5=土, 6=日

    if is_weekend:
        if hour >= 22 or hour < 8:
            return _RATE_NIGHT
        else:
            return _RATE_DAY
    else:
        if hour >= 23 or hour < 6:
            return _RATE_NIGHT
        elif 9 <= hour < 16:
            return _RATE_DAY
        else:
            return _RATE_LIFE


def get_hourly_cost_yen(watts):
    """Return estimated cost in yen if watts were consumed for 1 hour, or None."""
    if watts is None:
        return None
    return watts / 1000.0 * get_current_rate_yen_per_kwh()
