try:
    import googleapiclient
except ImportError:
    import pip

    pip.main(['install', 'google-api-python-client'])

import readDocxFile
import classEvent
import calendarInteraction
import downloadDocxFile

