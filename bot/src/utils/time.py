from datetime import datetime
import pytz


def now_utc():
    return datetime.utcnow().replace(tzinfo=pytz.utc)
