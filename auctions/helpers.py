from datetime import datetime
from .models import User, Listing, Watchlist, Bid, Comment
from django.utils.timezone import now, get_current_timezone_name, get_default_timezone_name, get_default_timezone

# Calculate delta time between now and models.DateTimeField
# returns string of delta time in year, month, day, min or sec
def duration(dateTime):
    #x = datetime(2020, 8, 8, hour=20, minute=3, second=0, microsecond=0, tzinfo=get_default_timezone(), fold=0)
    dateTimeNow = now()
    duration = dateTimeNow - dateTime

    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    years = days // 365
    months = days // 30

    # print(f'Start: {dateTime}')
    # print(f'Now: {dateTimeNow}')
    # print(f'Duration: {duration}') 
    # print(f'Days: {days}')
    # print(f'Hours: {hours}')
    # print(f'Minutes: {minutes}')
    # print(f'Seconds: {seconds}') 

    
    if years > 0:
        unit = ' year' if years == 1 else ' years' 
        return str(years) + unit + ' ago'
    elif months > 0:
        unit = ' month' if months == 1 else ' months'
        return str(months) + unit + ' ago'
    elif days > 0:
        unit = ' day' if days == 1 else ' days'
        return str(days) + unit + ' ago'
    elif hours > 0:
        unit = ' hour' if hours == 1 else ' hours'
        return str(hours) + unit + ' ago'
    elif minutes > 0:
        unit = ' minute' if minutes == 1 else ' minutes'
        return str(minutes) + unit + ' ago'
    elif seconds > 0:
        unit = ' second' if seconds == 1 else ' seconds'
        return str(seconds) + unit + ' ago'
    else:
        return 'just now'

    
