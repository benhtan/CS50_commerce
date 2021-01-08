from datetime import datetime
from .models import User, Listing, Watchlist, Bid, Comment
from django.utils.timezone import now, get_current_timezone_name, get_default_timezone_name, get_default_timezone

def duration(dateTime):
    x = datetime(2021, 1, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=get_default_timezone(), fold=0)
    dateTimeNow = now()
    duration = dateTimeNow - x

    print(f'Start: {x}')
    print(f'Now: {dateTimeNow}')
    print(f'Duration: {duration}')
    # print(f'Days: {delta.days}')
    # print(f'Hours: {delta.seconds/3600}')
    # print(f'Minutes: {delta.seconds/60}')
    # print(f'Seconds: {delta.seconds}')

    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
