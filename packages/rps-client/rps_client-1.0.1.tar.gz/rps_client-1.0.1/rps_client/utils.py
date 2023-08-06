import time


def current_milli_time():
    return round(time.time() * 1000)

def safe_get_value_from_dict(data, key, default=None):
    if data is None:
        return default
    if key not in data:
        return default
    return data[key]