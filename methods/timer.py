import datetime


def get_current_time():
    return datetime.datetime.now()


def get_end_time(amount):
    return datetime.datetime.now() + datetime.timedelta(amount)

