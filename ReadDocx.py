from docx import Document
from datetime import datetime


class ReadDocx:
    """
        Read tables in the docx
    """

    calendar = "/home/jaimedgp/Desktop/Calendario Master 2019_2020.docx"

    def read_docx():

        doc = Document(calendar)
        date = get_date()

        all_tables = []

        for table in doc.tables:

            data = []

            for i, row in enumerate(table.rows):
                text = (cell.text for cell in row.cells)

                row_data = tuple(text)
                data.append(row_data)

            all_tables.append(data)

        return [line for line in all_tables[date[0]]
                                        [date[1]]
                                        [date[2]].split("\n") if line != '']


    def separate_hours(event):

        for i, item in enumerate(event):
            if "----" in item:
                day_schedule = [event[1:i], event[i+1:]]
                break
        else:
            day_schedule = event[1:]

        return day_schedule




    def get_date():
        """
            Get date index to find cell in the docx
        """

        today = datetime.today()

        day_week  = today.weekday() + 1
        num_week = (today.isocalendar()[1]
                    - today.replace(day=1).isocalendar()[1] + 2)

        month = today.month - 10

        return month, num_week, day_week


    def print_notify(data):

        s.call(['notify-send', "--urgency=normal",
                               "--icon=/homejaimedgp/Pictures/python.png",
                               data[1]+" -> "+data[0],
                               data[3]]
              )
