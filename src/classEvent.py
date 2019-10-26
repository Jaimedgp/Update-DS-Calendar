#
# ClassEvent 
#-----------------
# This script is a part of the Master-Schedule program to update the 
# master calendar automatically from the docx file to Google Drive
#
# This class is developed in order to obtain the information about
# the class lesson
#
# author: Jaime Diez Gonzalez-Pardo (Jaimedgp)
# github: https://github.com/Jaimedgp
################################################################################

from datetime import datetime, time

class ClassEvent(object):

    """
        Obtain the main information about the class lesson from
        a list of strigs passed as prameter. The class is defined
        by the subject, the date and hour, duration, teacher name
        and the topic of the lesson
    """

    def __init__(self, dy_schedule, date):
        """
            Separate the subject, the date and hour, the teacher's
            name and the topic of the lesson from the readed_docx
            list of strings

            :readed_docx: ReadDocxFile object

        """

        self._dy_schedule = dy_schedule
        self._class_day = date

        self.subject = None
        self.date = None
        self.duration = None
        self.teacher = None
        self.topic = None


    def get_class_info(self):
        """
            Fill in class information from each line of the dy_schedule
            attribure of ReadDocxFile object. The time must be convert
            a part in order to obtain start time and duration,

            :return: 1 if the information is filled correct
                     0 if there is not information to fill
        """

        class_info = self._dy_schedule

        for i, line in enumerate(class_info):
            if "h" in line:
                self.get_class_date(line)
                break
        else:
            return 0

        for j in range(i+1,len(class_info)):
            if not class_info[j].isspace():
                self.subject = class_info[j]
                break
        else:
            return 0

        self.teacher = class_info[j+1]
        self.topic = class_info[j+2]

        return 1

    def get_class_date(self, time_string):
        """
            Obtain the time to start class and the duration
            from the string line identified as time in get_class_info

            :time_string: string line with the time information
        """

        hours = [hr.replace("h", "") for hr in time_string.split("-")]

        self.date = datetime.combine(self._class_day,
                                     time(int(hours[0]))).isoformat()

        self.duration = int(hours[1]) - int(hours[0])

