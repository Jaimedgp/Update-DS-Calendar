from cal_setup import get_calendar_service
from datetime import datetime

class Event(object):
    """
        Script that clasified the data given from the docx file

        author: Jaimedgp
        date: 24.Oct.2019
    """

    def __init__(self, date, data):

        self.date = date
        self.data = data

        self.dt_start = None
        self.dt_end = None

        # [Subject, teacher, description]
        self.info = [None, None, None]
        self.time = None


    def get_info(self):

        for i, line in enumerate(self.data):
            if "h" in line:
                self.time = line
                break

        convert_time()

        for j in range(i, len(self.data)):
            if not self.data[j].isspace():
                self.info[0] = self.data[j]
                break

        self.info[1] = self.data[j+1]
        self.info[2] = self.data[j+2]


    def convert_time(self):

        time = [hr.remove("h") for hr in self.time.split("-")]

        self.dt_start = datetime(self.date.year, self.date.month,
                                 self.date.day, int(time[0])).isoformat()
        self.dt_end = datetime(self.date.year, self.date.month,
                                 self.date.day, int(time[1])).isoformat()


    def upload_Calendar(self):

        service = get_calendar_service()

        event_result = service.events().insert(calendarId='UC',
            body={
                "summary": self.info[0],
                "description": self.info[2]+" por el profesor "+self.info[1],
                "start": {"dateTime": self.dt_start },
                "end": {"dateTime": self.dt_end},
            }
        ).execute()



    def print_notify(self, data):

        s.call(['notify-send', "--urgency=normal",
                               "--icon=/homejaimedgp/Pictures/python.png",
                               self.info[0]+" -> "+self.time,
                               data[2]]
              )
