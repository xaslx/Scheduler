from datetime import datetime, timedelta

import pytz

moscow_tz = pytz.timezone("Europe/Moscow")


async def generate_time_intervals(
    start_time, end_time, interval_minutes: int
) -> list[str]:
    start: datetime = datetime.combine(datetime.today(), start_time)
    end: datetime = datetime.combine(datetime.today(), end_time)

    if end <= start:
        end += timedelta(days=1)

    intervals: list[str] = []

    while start < end:
        intervals.append(start.time().strftime("%H:%M"))
        start += timedelta(minutes=interval_minutes)

    return intervals
