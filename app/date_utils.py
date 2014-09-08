
import datetime

def convert_string_date(str):
    if(str and len(str) == 8):
        date =  datetime.datetime(int(str[:-4]), int(str[4:-2]), int(str[6:]))
    elif (str and len(str) == 10):
        date =  datetime.datetime(int(str[:-6]), int(str[4:-4]), int(str[6:8]), int(str[8:]))
    else:
        date = None
    return date

def get_current_date():
    now = datetime.datetime.today()
    return datetime.datetime(now.year, now.month, now.day)

def get_next_day(date):
    return date + datetime.timedelta(days=1)
