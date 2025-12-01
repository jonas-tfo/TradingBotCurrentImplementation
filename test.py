
from datetime import datetime, time

def us_market_is_open():
    try:
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("America/New_York"))
        is_weekday = now.weekday() < 5
        is_trading_hours = time(9, 20) <= now.time() <= time(16, 0)
        return is_weekday and is_trading_hours
    except ImportError:
        import pytz
        EST = pytz.timezone("America/New_York")
        now = datetime.now(EST)
        is_weekday = now.weekday() < 5
        is_trading_hours = time(9, 20) <= now.time() <= time(16, 0)
        return is_weekday and is_trading_hours

print(us_market_is_open())
