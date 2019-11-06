import subprocess as s
import os

from pathlib import Path

class GetNotify(object):
    """
        show notification
    """


    def __init__(self):

        path = Path(os.get(cwd))
        self.icon_path = path.parent+"doc/icon.png"


    def class_info(self, calendar):
        start_time = calendar.dt_start.split("T")[1].split(":")
        end_time = calendar.dt_end.split("T")[1].split(":")

        title = "%s ==> %s-%s" %(calendar.summary,
                                ":".join(start_time[:2]),
                                ":".join(end_time[:2])
                                )
        body = calendar.description

        self.get_notify(title, body)


    def error_messg(self):

        title = "Error found in services connection"
        body = "Maybe the error is due to the internet connection"

        self.get_notify(title, body)

    def get_notify(sefl, title, body):
        """
            Show desktop notifications for the update
            process
        """

        s.call(['notify-send', "--urgency=normal",
                "--icon="+self.icon_path,
                title, body
               ])
