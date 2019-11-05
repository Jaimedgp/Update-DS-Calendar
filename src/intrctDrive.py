#
# DriveInteraction 
#----------------------
# This script is a part of the Master-Schedule program to update the 
# master calendar automatically from the docx file to Google Drive
#
# author: Jaime Diez Gonzalez-Pardo (Jaimedgp)
# github: https://github.com/Jaimedgp
################################################################################

from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload
from tempfile import NamedTemporaryFile

import os


class DriveInteraction(object):

    """
        Things with Drive
    """

    def __init__(self, service):
        """
            Things
        """

        self._service = service
        self._files = []


    def dwnld_docx_file(self, file_id, save=False):
        """
            Download the .docx file from Google Drive

            :return: file path
        """

        if not save:
            path_file = NamedTemporaryFile(suffix='.docx', delete=False)
            self._files.append(path_file.name)

        mimeType_docx = ("application/vnd.openxmlformats-officedocument."
                                                    +"wordprocessingml.document")

        source = self._service.files().export(fileId=file_id, mimeType=mimeType_docx)
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, source)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        path_file.write(fh.getvalue())
        path_file.close()

        return path_file.name


    def __del__(self):

        for name in self._files:
            os.unlink(name)


