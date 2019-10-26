#
# ReadDocxFile 
#-----------------
# This script is a part of the Master-Schedule program to update the 
# master calendar automatically from the docx file to Google Drive
#
# This class is developed in order to read an expecific .docx file
# structured as a calendar with a table for each month of classes.
#
# author: Jaime Diez Gonzalez-Pardo (Jaimedgp)
# github: https://github.com/Jaimedgp
################################################################################

from docx import Document
from datetime import date

class ReadDocxFile(object):

    """
        Read the information from the 'Master en Ciencia de Datos' calendar
        obtaining the classes information from the cell corresponding to a
        centain date
    """

    def __init__(self, doc_name, date='today'):
        """
            Read a .docx file formed by tables (per month) as a calendar

            :doc_name: name of the .docx file 'path/to/file.docx'
            :date: date to read <class type='datetime'>
        """
        self._doc = Document(doc_name)
        if date == 'today':
            self._date = date.today()
        else:
            self._date = date

        # Cell coordinates for the day
        self.num_month, self.num_week, self.day_week = None, None, None

        self.dy_schedule = None


    def get_date_coordinates(self):
        """
            get atributees coordinates (num_month, num_week, day_week) for the
            date's cell
        """

        self.day_week  = self._date.weekday() + 1
        self.num_week = (self._date.isocalendar()[1]
                        - self._date.replace(day=1).isocalendar()[1] + 2)

        self.num_month = self._date.month - 10

        if self.num_month < 0:
            self.num_month += 12


    def read_cell(self):
        """
            Read the string of the coordinates' cell
        """

        cell_string =  tuple(self._doc.tables[self.num_month]
                                             [self.num_week]
                                             [self.day_week].text
                            )

        return [ line for line in cell_string.split("\n") if line != '']


    def split_classes(self):
        """
            Some cells have two classes information separated by
            a '----' line, so it is necessary to split both strings
        """

        event = self.read_cell()

        for i, item in enumerate(event):
            if "----" in item:
                self.dy_schedule = [event[1:i], event[i+1:]]
                break
        else:
            self.dy_schedule = event[1:]


