

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


    def get_info(self):

        for i, line in enumerate(self.data):
            if "h" in line:
                hour = line
                break

        convert_time(hour)

        for j in range(i, len(self.data)):
            if not self.data[j].isspace():
                self.info[0] = self.data[j]
                break

        self.info[1] = self.data[j+1]
        self.info[2] = self.data[j+2]


    def convert_time(self, hour):

        time = [hr.remove("h") for hr in hour.split("-")]

        self.dt_start = datetime(self.date.year, self.date.month,
                                 self.date.day, int(time[0])).isoformat()
        self.dt_end = datetime(self.date.year, self.date.month,
                                 self.date.day, int(time[1])).isoformat()


