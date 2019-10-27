#
# CalendarInteraction 
#----------------------
# This script is a part of the Master-Schedule program to update the 
# master calendar automatically from the docx file to Google Drive
#
# This class is developed in order to interact with the Google Calendar API
# to syncronized the google calendar with the class information
#
# author: Jaime Diez Gonzalez-Pardo (Jaimedgp)
# github: https://github.com/Jaimedgp
################################################################################

from cal_setup import get_calendar_service
from datetime import timedelta

class CalendarInteraction(object):

    """
        Keep Google Calendar up to date with the
        'Master en Ciencia de Datos' calendar uploading
        the class event
    """

    def __init__(self):
        """
            Upload the class event to the Google Calendar application
            with the needed information. The program must be able to
            create the new calendar 'Data-Science' if it does not exists
        """

        self._service = get_calendar_service()
        self._calendar_id = self.get_id_calendar()

        self.summary, self.description = None, None
        self.dt_start, self.dt_end = None, None


    def get_id_calendar(self):
        """
            Check if 'Data-Science' calendar already exists or create it
            if it is not. Then obtain its id
        """

        calendars_result = self._service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            return
        for calendar in calendars:
            if calendar['summary'] == 'Data-Science':
                return calendar['id']
        else:
            calendar = {
                    'summary': 'Data-Science',
                    'timeZone': 'Europe/Amsterdam'
            }

            created_calendar = (self._service.calendars().
                                insert(body=calendar).execute())

        return created_calendar['id']


    def set_event(self, class_event):
        """
            read and store class event information
        """

        self.summary = class_event.subject
        self.description = "%s by professor %s" %(class_event.topic,
                                                  class_event.teacher)

        self.dt_start = class_event.date.isoformat()
        self.dt_end = (class_event.date
                       + timedelta(hours=class_event.duration)).isoformat()


    def event_exists(self):
        """
            Check if there is an event at that time already
        """

        events_result = (self._service.events().list(
                                            calendarId=self._calendar_id,
                                            timeMin=self.dt_start+'Z',
                                            maxResults=2,
                                            singleEvents=True,
                                            orderBy='startTime').execute())

        events = events_result.get('items', [])

        if not events:
            return False
        for event in events:
            start = event['start'].get('dateTime')
            if start == self.dt_start:
                return event['id']
        else:
            return False


    def push_event(self):
        """
            Push the event to the Google Calendar 'Data-Science'
            If an event at the same time already exists, just upload,
            if not, create it
        """

        is_event = self.event_exists()

        if is_event:
            self._service.events().update(
                                calendarId=self._calendar_id,
                                eventId=is_event,
                                body={
                                    "summary": self.summary,
                                    "description": self.description,
                                    "start": {"dateTime": self.dt_start,
                                            "timeZone": 'Europe/Amsterdam'},
                                    "end": {"dateTime": self.dt_end,
                                            "timeZone": 'Europe/Amsterdam'},
                                     },
                                         ).execute()
        else:
            self._service.events().insert(
                                calendarId=self._calendar_id,
                                body={
                                    "summary": self.summary,
                                    "description": self.description,
                                    "start": {"dateTime": self.dt_start,
                                            "timeZone": 'Europe/Amsterdam'},
                                    "end": {"dateTime": self.dt_end,
                                            "timeZone": 'Europe/Amsterdam'},
                                     },
                                         ).execute()
