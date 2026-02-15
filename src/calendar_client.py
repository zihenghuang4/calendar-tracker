"""
Google Calendar API client
"""

import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES


class CalendarClient:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "credentials.json not found. Please follow the setup instructions "
                        "in SETUP.md to create Google Calendar API credentials."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def get_events(self, start_date, end_date, calendar_id='primary'):
        """
        Fetch events from Google Calendar for a date range
        
        Args:
            start_date: datetime object for start of range
            end_date: datetime object for end of range
            calendar_id: Calendar ID (default: 'primary')
        
        Returns:
            List of event dictionaries
        """
        # Convert to RFC3339 format
        time_min = start_date.isoformat() + 'Z'
        time_max = end_date.isoformat() + 'Z'
        
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return events
    
    def get_event_duration(self, event):
        """
        Calculate duration of an event in hours
        
        Args:
            event: Event dictionary from Google Calendar API
        
        Returns:
            Duration in hours (float)
        """
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        # Handle all-day events
        if 'T' not in start:
            # All-day event - assume 8 hours or skip
            return 8.0
        
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
        
        duration = (end_dt - start_dt).total_seconds() / 3600  # Convert to hours
        return duration
    
    def get_event_color(self, event):
        """
        Get the color ID of an event
        
        Args:
            event: Event dictionary from Google Calendar API
        
        Returns:
            Color ID string or None
        """
        return event.get('colorId', None)
    
    def list_calendars(self):
        """List all available calendars"""
        calendar_list = self.service.calendarList().list().execute()
        return calendar_list.get('items', [])
