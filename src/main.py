#
# main 
#-----------------
# This script is the main script of the Master-Schedule program to 
# update the master calendar automatically from the docx file to Google Drive
#
# author: Jaime Diez Gonzalez-Pardo (Jaimedgp)
# github: https://github.com/Jaimedgp
################################################################################

import subprocess as s
import sys

from readDocxFile import ReadDocxFile
from classEvent import ClassEvent
from calendarInteraction import CalendarInteraction

from datetime import date, timedelta

def update_day():
    """
        Upload the class schedule for today

        :return: list with today() datetime object
    """

    return [date.today()]


def update_tomorrow():
    """
        Upload the class schedule for tomorrow

        :return: list with datetime object for tomorrow
    """

    today_date = date.today()

    return [today_date+timedelta(days=1)]


def update_week():
    """
        Upload the class schedule for the next 7 days

        :return: list with datetime objects for the week
    """

    today_date = date.today()

    return [today_date+timedelta(days=i) for i in reversed(range(8))]


def update_month():
    """
        Upload the class schedule for the next month

        :return: list with datetime objects for the month
    """

    today_date = date.today()

    days_in_month = {28:[2],
                     30:[4, 6, 9, 11],
                     31:[1, 3, 5, 7, 8, 10, 12]
                    }

    for ky, vl in day_in_month.items():
        if today_date.month in vl:
            return [today_date+timedelta(days=i)
                                        for i in reversed(range(ky))]
    else:
        sys.exit()




def get_notify(title, body, icon_path):
    """
        Show desktop notifications for the update process
    """

    s.call(['notify-send', "--urgency=normal",
                           "--icon="+icon_path,
                           title, body
           ])


if __name__ == '__main__':

    try:
        param = sys.argv[1]

        if "-t" == param:
            days = update_tomorrow()
        elif "-w" == param:
            days = update_week()
        elif "-m" == param:
            days = update_month()
        else:
            days = update_day()
    except Exception:
        days = update_day()

    calendar_doc = "../doc/Calendario Master 2019_2020.docx"

    read_doc = ReadDocxFile(calendar_doc)
    calendar_event = CalendarInteraction()

    for dy in days:
        schedule = read_doc.read_cell(dy)

        for clss in schedule:

            lesson = ClassEvent(clss, dy)
            is_class = lesson.get_class_info()

            if is_class:
                calendar_event.set_event(lesson)
                calendar_event.push_event()

                exc_correct = True

            else:

                exc_correct = False

    if len(days) < 2:
        if exc_correct:
            start_time = calendar_event.dt_start.split("T")[1].split(":")
            end_time = calendar_event.dt_end.split("T")[1].split(":")

            title = "%s ==> %s-%s" %(calendar_event.summary,
                                    ":".join(start_time[:2]),
                                    ":".join(end_time[:2])
                                    )
            body = calendar_event.description

        else:
            title = "No Class Information"
            body = "No body information found in calendar for today"

        get_notify(title, body, "/homejaimedgp/Pictures/python.png")


