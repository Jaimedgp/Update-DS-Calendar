##!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from os import unlink
from os import getcwd

from cal_setup import get_services
from readDocxFile import ReadDocxFile
from classEvent import ClassEvent
from calendarInteraction import CalendarInteraction
from downloadDocxFile import get_Docx_File

from datetime import date, timedelta

today_date = date.today()

def parameter_options(param):
    """
        Upload the class schedule for today

        :return: list with days datetime objects
    """

    features = {"-d" : [today_date],
                "-t" : [today_date+timedelta(days=1)],
                "-w" : [today_date+timedelta(days=i)
                         for i in reversed(range(8-today_date.weekday()))],
                "-m" : get_month()}

    if param in features.keys():
        return features[param]
    else:
        return [today_date]


def get_month():
    """
        Upload the class schedule for the next month

        :return: list with datetime objects for the month
    """

    days_in_month = {28:[2],
                     30:[4, 6, 9, 11],
                     31:[1, 3, 5, 7, 8, 10, 12]
                    }

    for ky, vl in days_in_month.items():
        if today_date.month in vl:
            left_days = ky-today_date.day
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

    print getcwd()

    try:
        param = sys.argv[1]
        days = parameter_options(param)
    except IndexError:
        days = [today_date]

    calendar_srvic, drive_srvic = get_services()

    file_id = '1Fs35WnSE1NNR1jRZklflA76oDE6mrSBxNMo7rN5ir9s'

    file_path = get_Docx_File(drive_srvic, file_id)

    read_doc = ReadDocxFile(file_path)
    calendar_event = CalendarInteraction(calendar_srvic)

    for dy in days:
        schedule = read_doc.read_cell(dy)

        for clss in schedule:

            lesson = ClassEvent(clss, dy)
            is_class = lesson.get_class_info()

            if is_class:
                calendar_event.set_event(lesson)
                calendar_event.push_event()

    if is_class:
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

        get_notify(title, body, "../doc/icon/icon.png")

    unlink(file_path)


