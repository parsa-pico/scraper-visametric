import datetime
from utils import log


def time_delta(time: str, days_delta: int):
    hour, minute = map(int, time.split(":"))
    now = datetime.datetime.now()
    new_time = now + datetime.timedelta(days=days_delta)
    new_time = datetime.datetime(
        new_time.year, new_time.month, new_time.day, hour, minute)
    return new_time


def time_passed(time: str, days_delta: int):
    start = time_delta(time, days_delta)
    now = datetime.datetime.now()
    diff = (now-start).total_seconds()
    log("time diff:", diff)
    log("time passed:", diff >= 0)
    return True if diff >= 0 else False


if __name__ == "__main__":
    print(time_passed("09:39", 1))
