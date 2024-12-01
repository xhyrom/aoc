from datetime import datetime


def current_year() -> int:
    """Returns the current year"""
    return datetime.now().year


def current_month() -> int:
    """Returns the current month of the year"""
    return datetime.now().month


def current_day() -> int:
    """Returns the current day of the month"""
    return datetime.now().day


def advent_time() -> bool:
    """Returns True if it's December 1st to December 25th"""
    return current_month() == 12 and 1 <= current_day() <= 25


def until_advent() -> int:
    """ "Returns the number of days until advent starts"""
    now = datetime.now()
    december = datetime(now.year, 12, 1)

    if now.month == 12:
        if now.day > 25:
            december = datetime(now.year + 1, 12, 1)
        else:
            return 0

    return (december - now).days
