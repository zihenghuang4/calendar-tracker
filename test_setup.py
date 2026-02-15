"""
Test script to verify Google Calendar API setup
Run this before launching the full dashboard
"""

import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("Calendar Time Tracker - Setup Verification")
    print("=" * 60)
    print()
    
    # Check if credentials.json exists
    print("1. Checking for credentials.json...")
    if os.path.exists('credentials.json'):
        print("   ✓ credentials.json found")
    else:
        print("   ✗ credentials.json NOT found")
        print("   → Please download OAuth credentials from Google Cloud Console")
        print("   → See SETUP.md for detailed instructions")
        return False
    
    print()
    
    # Try to import dependencies
    print("2. Checking Python dependencies...")
    try:
        import google.auth
        import googleapiclient
        import streamlit
        import pandas
        import plotly
        print("   ✓ All dependencies installed")
    except ImportError as e:
        print(f"   ✗ Missing dependency: {e}")
        print("   → Run: pip install -r requirements.txt")
        return False
    
    print()
    
    # Try to initialize calendar client
    print("3. Testing Google Calendar API connection...")
    try:
        from calendar_client import CalendarClient
        client = CalendarClient()
        print("   ✓ Successfully authenticated with Google Calendar")
        
        # Try to list calendars
        calendars = client.list_calendars()
        print(f"   ✓ Found {len(calendars)} calendar(s) in your account")
        
    except FileNotFoundError as e:
        print(f"   ✗ Error: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Error connecting to Google Calendar: {e}")
        print("   → Check your internet connection")
        print("   → Verify Google Calendar API is enabled")
        return False
    
    print()
    
    # Try to fetch some events
    print("4. Testing event retrieval...")
    try:
        from metrics import TimeTracker
        tracker = TimeTracker(client)
        
        # Get events from today
        today = datetime.now()
        start = datetime.combine(today, datetime.min.time())
        end = start + timedelta(days=1)
        
        events = tracker.get_events_with_categories(start, end)
        print(f"   ✓ Successfully retrieved {len(events)} event(s) for today")
        
        if events:
            print()
            print("   Sample events:")
            for i, event in enumerate(events[:3], 1):
                print(f"     {i}. {event['summary']}")
                print(f"        Color ID: {event['color_id'] or 'None'}")
                print(f"        Category: {event['category']}")
                print(f"        Duration: {event['duration_hours']:.1f} hours")
        else:
            print("   ℹ No events found for today")
            print("   → This is normal if your calendar is empty today")
        
    except Exception as e:
        print(f"   ✗ Error retrieving events: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✓ Setup verification complete!")
    print()
    print("Next steps:")
    print("1. Check the color IDs shown above")
    print("2. Update config.py with your color mappings")
    print("3. Run: streamlit run app.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup verification cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
