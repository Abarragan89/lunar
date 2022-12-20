import datetime
from calendar import monthrange


def days_until_first():
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    num_days = monthrange(current_year, current_month)[1]
    count_down = num_days - current_date.day + 1
    print(count_down)
    return count_down
