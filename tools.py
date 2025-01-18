import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def readDataFromSpreadsheet(spreadsheetId,range_name):
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = spreadsheetId 
    SAMPLE_RANGE_NAME = range_name 
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID
                                , range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values

def writeDataToSpreadsheet(spreadsheetId,range_name,inputList):
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = spreadsheetId 
    SAMPLE_RANGE_NAME = range_name 
    SAMPLE_VALUE_INPUT_OPTION = "USER_ENTERED"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    body = {
        'values': inputList
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID
        , range=SAMPLE_RANGE_NAME
        , valueInputOption=SAMPLE_VALUE_INPUT_OPTION
        , body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def writeMultipleRangesToSpreadsheet(spreadsheetId,data):
    SAMPLE_SPREADSHEET_ID = spreadsheetId 
    SAMPLE_VALUE_INPUT_OPTION = "USER_ENTERED"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('sheets', 'v4', credentials=creds)
    
    body = {
        'valueInputOption': SAMPLE_VALUE_INPUT_OPTION,
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID
        , body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

def clearDataSpreadsheetRange(spreadsheetId,range_name):
    SAMPLE_SPREADSHEET_ID = spreadsheetId 
    SAMPLE_RANGE_NAME = range_name 
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
    response = request.execute()
    print("Cleared "+ range_name)

def appendDataToSpreadsheet(spreadsheetId,range_name,inputList):
    SAMPLE_SPREADSHEET_ID = spreadsheetId 
    SAMPLE_RANGE_NAME = range_name 
    SAMPLE_VALUE_INPUT_OPTION = "USER_ENTERED"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    body = {
        'values': inputList
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID
        , range=SAMPLE_RANGE_NAME
        , valueInputOption=SAMPLE_VALUE_INPUT_OPTION
        , body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))

