from ReadDocx import ReadDocx
from Event import Event
from datetime import datetime

if __name__ == '__main__':

    read = ReadDocx()

    date_schedule = read.read_docx()

    classes = read.separate_hours(date_schedule)

    for clss in classes:
        evento = Event(datetime.today(), clss)
        is_event = evento.get_info()
        evento.print_notify()
        if is_event:
            evento.upload_Calendar()
