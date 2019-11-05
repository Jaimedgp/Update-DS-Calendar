from datetime import date, timedelta
import numpy as np

today_dt = date.today()
wk_day = today_dt.weekday()

def today_date():
    """
        Upload the class schedule for today

        :return: list with today() datetime object
    """

    if wk_day < 5:
        return [today_dt]
    else:
        return []


def tomorrow_date():
    """
        Upload the class schedule for tomorrow

        :return: list with datetime object for tomorrow
    """

    if wk_day < 4:
        return [today_dt+timedelta(days=1)]
    else:
        next_dy = 7-wk_day
        return [today_dt+timedelta(days=next_dy)]


def rest_week_date():
    """
        Upload the class schedule for the next 7 days

        :return: list with datetime objects for the week
    """

    rest_dys = None

    if wk_day < 3:
        rest_dys = np.arange(5-wk_day)

    elif wk_day < 5:
        next_wk = np.arange(5)
        next_wk += (7 - wk_day)
        rest_dys = np.concatenate((np.arange(4 - wk_day), next_wk))

    else:
        rest_dys = np.arange(5)
        rest_dys += (7 - wk_day)

    return [today_dt+timedelta(days=int(i)) for i in rest_dys[::-1]]


def rest_month_date():
    """
        Upload the class schedule for the next month

        :return: list with datetime objects for the month
    """

    days_in_month = {29:[2],
                     30:[4, 6, 9, 11],
                     31:[1, 3, 5, 7, 8, 10, 12]
                    }

    rest_month = []

    for ky, vl in days_in_month.items():
        if today_dt.month in vl:
            rest_dys = np.arange(ky - today_dt.day)

            # pop weekend days
            for i in rest_dys[::-1]:
                day = today_dt+timedelta(days=int(i))

                if day.weekday() < 5:
                    rest_month.append(day)

            return rest_month

    else:
        return None


