import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def calendar_event(event_data, attendees):

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    """Shows basic usage of the Google Calendar API.

    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    pickle_file = 'lessons/meet_link/token.pickle'
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lessons/meet_link/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    event = {
        'summary': str(event_data['title']),
        'description': str(event_data['subject']),
        'start': {
            'dateTime': str(event_data['start']),
            'timeZone': 'Asia/Kolkata'
        },
        'end': {
            'dateTime': str(event_data['end']),
            'timeZone': 'Asia/Kolkata'
        },
        'attendees': attendees,
        'reminders': {
            'useDefault': True
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    return event
