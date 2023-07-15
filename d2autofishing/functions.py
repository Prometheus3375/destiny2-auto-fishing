from datetime import datetime


def current_datetime_ms_str() -> str:
    """
    Takes current date and time and converts to a string.
    The result always have 3 digits for fraction part of seconds.
    """
    dt = datetime.now()
    ms = round(dt.microsecond / 1000)
    dt = dt.replace(microsecond=0)
    return f'{dt}.{ms:03}'


__all__ = 'current_datetime_ms_str',
