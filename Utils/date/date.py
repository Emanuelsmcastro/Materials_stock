import datetime


def get_date():
    """
    this function the time it was called
    :return: Return time formatted
    """
    date_year = datetime.datetime.now().year
    date_month = datetime.datetime.now().month
    date_day = datetime.datetime.now().day
    date_hour = datetime.datetime.now().hour
    date_minute = datetime.datetime.now().minute
    date_second = datetime.datetime.now().second
    return f'{date_day}/{date_month}/{date_year} - {date_hour}:{date_minute}:{date_second}'
