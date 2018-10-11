from google.oauth2 import service_account
from googleapiclient.discovery import build
import googleapiclient.discovery
import datetime

class GOAuthHandler:
    
    def __init__(self):
        print("GOAuthHandler initialized")
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.credentials = service_account.Credentials.from_service_account_file("oscar/oauth.json", scopes=self.SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=self.credentials)
    
    def getUpcomingEvents(self):
        
        print("Upcoming events:")
    
        now = datetime.datetime.utcnow().isoformat() + 'Z' # Z = utc time
        events_result = self.service.events().list(calendarId='l7tjei0aeg59j6s9fj8gd92tv0@group.calendar.google.com', timeMin=now,
                                            maxResults=1000, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    def createEvent(self, dStart, dEnd, name):
        event = {
        'summary': 'Room Booked By ' + name,
          'description': 'Booking By ' + name,
          'start': {
            'dateTime': dStart + ':00+09:00',
            'timeZone': 'Asia/Seoul',
          },
          'end': {
            'dateTime': dEnd + ':00+09:00',
            'timeZone': 'Asia/Seoul',
          },
        }
        self.service.events().insert(calendarId='l7tjei0aeg59j6s9fj8gd92tv0@group.calendar.google.com', body=event).execute()
    def __str__(self):
        return "<GOAuthHandler Class>"