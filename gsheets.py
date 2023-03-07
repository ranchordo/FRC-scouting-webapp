# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import data_handler
import ssl

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
sheet_service = None


def initialize():
    global sheet_service
    creds = None
    if os.path.exists('token_creds.json'):
        creds = Credentials.from_authorized_user_file(
            'token_creds.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_creds.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet_service = service.spreadsheets()
        print("Success: Got google sheets service handle")
    except HttpError as err:
        print(err)
        print("gsheets: initialize: HttpError when instantiating spreadsheet service. Cannot proceed.")


def getSheetNames():
    try:
        data = sheet_service.get(
            spreadsheetId=data_handler.spreadsheetId).execute()
        return [i['properties']['title'] for i in data.get('sheets', [])]
    except HttpError as err:
        print(err)
        print("gsheets: getSheetNames: HttpError.")
        return []


def addSheet(name, color):
    try:
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': name,
                    }
                }
            }]
        }
        if color is not None:
            body['requests'][0]['addSheet']['properties']['tabColor'] = {
                'red': color[0],
                'green': color[1],
                'blue': color[2]
            }
        sheet_service.batchUpdate(
            spreadsheetId=data_handler.spreadsheetId, body=body).execute()
    except HttpError as err:
        print(err)
        print("gsheets: addSheet: HttpError.")


def appendRow(sheet, values):
    try:
        sheet_service.values().append(spreadsheetId=data_handler.spreadsheetId, range=f'{ sheet }!A1:Z1', body={
            'range': f'{ sheet }!A1:Z1',
            'values': [values],
            'majorDimension': 'ROWS'
        }, valueInputOption="USER_ENTERED").execute()
    except HttpError as err:
        print(err)
        print("gsheets: appendRow: HttpError.")

def trySSL(func, default, *values):
    try:
        return func(*values)
    except ssl.SSLError:
        return func(*values)
    finally:
        print("No SSL! Bad!")
        return default