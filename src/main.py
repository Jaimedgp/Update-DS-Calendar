import os
import sys

from datesGenerator import *
from cal_setup import get_services
from intrctDrive import DriveInteraction
from intrctCalendar import CalendarInteraction
from readDocxFile import ReadDocxFile

features = {"-d" : today_date(),
            "-t" : tomorrow_date(),
            "-w" : rest_week_date(),
            "-m" : rest_month_date()}


file_id = '1Fs35WnSE1NNR1jRZklflA76oDE6mrSBxNMo7rN5ir9s'

if __name__ == '__main__':

    abs_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(abs_path)

    try:
        services = get_services()
    except Exception:
        print("Not Internet Connection")
        sys.exit()
    try:
        param = sys.argv[1]
    except IndexError:
        param = "-d"

    drive_srvic = DriveInteraction(services[1])  ##
    calendar_srvic = CalendarInteraction(services[0])  ##

    docx_file = ReadDocxFile(drive_srvic.dwnld_docx_file(file_id)) ###

    for dy in features[param]:
        class_dy = docx_file.read_cell(dy)

        for clss in class_dy:
            if clss.get_class_info():
                calendar_srvic.set_class_event(clss)

    del drive_srvic
