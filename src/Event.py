import subprocess as s
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
        """
            get info for the class from the cell ReadDocx

            return: 1 if all is correct
                    0 if not info founded
        """

        for i, line in enumerate(self.data):
            if "h" in line:
                self.time = line
                break
        else:
            self.info = ["Not class Info", None,
                         "No body info found in calendar for today"]
            self.time = "free"
            return 0

        self.convert_time()

        for j in range(i+1, len(self.data)):
            if not self.data[j].isspace():
                self.info[0] = self.data[j]
                break

        self.info[1] = self.data[j+1]
        self.info[2] = self.data[j+2]

        return 1


    def convert_time(self):

        time = [hr.replace("h", "") for hr in self.time.split("-")]

        self.dt_start = datetime(self.date.year, self.date.month,
                                 self.date.day, int(time[0])).isoformat()

        self.dt_end = datetime(self.date.year, self.date.month,
                                 self.date.day, int(time[1])).isoformat()


    def upload_Calendar(self):

        service = get_calendar_service()

        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            return
        for calendar in calendars:
            if calendar['summary'] == 'Master':
                ident = calendar['id']
                break
        else:
            calendar = {
                    'summary': 'Master',
                    'timeZone': 'Europe/Amsterdam'
            }

            created_calendar = (service.calendars().
                                insert(body=calendar).execute())

            ident = created_calendar['id']


        event_result = service.events().insert(calendarId=ident,
            body={
                "summary": self.info[0],
                "description": self.info[2]+" por el profesor "+self.info[1],
                "start": {"dateTime": self.dt_start,
                          "timeZone" : 'Europe/Amsterdam'},
                "end": {"dateTime": self.dt_end,
                        "timeZone" : 'Europe/Berlin'},
            }
        ).execute()



    def print_notify(self):

        s.call(['notify-send', "--urgency=normal",
                               "--icon=/homejaimedgp/Pictures/python.png",
                               self.info[0]+" -> "+self.time,
                               self.info[2]]
              )
