
def check_expire(date: str) -> bool:
    import time
    import datetime

    days_expire = 10
    seconds_expire = days_expire * 86400

    current_timestamp = int(time.time())
    expiry_timestamp = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple()))
    print(current_timestamp)
    print(expiry_timestamp)
    if (expiry_timestamp - current_timestamp) > seconds_expire:
        return True
    else:
        return False


print(check_expire('2022-06-24T09:42:00'))
