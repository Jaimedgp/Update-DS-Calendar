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

    def __init__(self, class_event):
        """
            Upload the class event to the Google Calendar application
            with the needed information. The program must be able to
            create the new calendar 'Data-Science' if it does not exists
        """

        self._class_event = class_event

        self.service = get_calendar_service()
        self.calendar_id = self.get_id_calendar()

        self.summary = self._class_event.subject
        self.description = "%s by professor %s" %(self._class_event.topic,
                                                  self._class_event.teacher)

        self.dt_start = self._class_event.date
        self.dt_end = self.dt_start + timedelta(self._class_event.duration)


    def get_id_calendar(self):
        """
            Check if 'Data-Science' calendar already exists or create it
            if it is not. Then obtain its id
        """

        calendars_result = self.service.calendarList().list().execute()
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

            created_calendar = (service.calendars().
                                insert(body=calendar).execute())

        return created_calendar['id']


    def event_exists(self):
        """
            Check if there is an event at that time already
        """

        events_result = self.service.events().list(
                                            calendarId=self.calendar_id,
                                            timeMin=self.dt_start.isoformat(),
                                            maxResults=2,
                                            singleEvents=True,
                                            orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            return False
        for event in events:
            start = event['start'].get('dateTime')
            if start == self.dt_start.isoformat():
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
            service.events().update(calendarId=self.calendar_id,
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
            service.events().update(calendarId=self.calendar_id,
                                body={
                                    "summary": self.summary,
                                    "description": self.description,
                                    "start": {"dateTime": self.dt_start,
                                            "timeZone": 'Europe/Amsterdam'},
                                    "end": {"dateTime": self.dt_end,
                                            "timeZone": 'Europe/Amsterdam'},
                                     },
                                    ).execute()
