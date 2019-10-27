#
# downloadDocxFile 
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

def get_Docx_File(service, file_id):
    """
        Download the .docx file from Google Drive

        :return: file path
    """

    tmp_file = NamedTemporaryFile(suffix='.docx', delete=False)
    mimeType_docx = ("application/vnd.openxmlformats-officedocument."
                                                 +"wordprocessingml.document")

    source = service.files().export(fileId=file_id, mimeType=mimeType_docx)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, source)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    tmp_file.write(fh.getvalue())
    tmp_file.close()

    return tmp_file.name
