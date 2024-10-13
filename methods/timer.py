import datetime


def get_current_time():
    return datetime.datetime.now()


def get_end_time(amount):
    return datetime.datetime.now() + datetime.timedelta(amount)


def start_at():
    return datetime.datetime(2024, 10, 15, 1, 00)