import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveService:
    def __init__(self):
        self._SCOPES = ["https://www.googleapis.com/auth/drive"]

        _base_path = os.path.dirname(__file__)
        _credential_path = os.path.join(_base_path, "creds.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _credential_path

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), self._SCOPES
        )
        service = build("drive", "v3", credentials=creds)

        return service
