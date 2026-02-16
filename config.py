"""
Configuration file for Calendar Time Tracker
"""

# Color ID to category mapping
# Google Calendar uses numeric IDs (1-11) for colors
# You'll need to identify which IDs match your colors in Google Calendar
# To find your color IDs, run the script and it will show you the colors of your events

COLOR_CATEGORIES = {
    # Update these mappings based on your actual Google Calendar color IDs
    '5': 'Personal Development',  # Yellow
    '10': 'Work',                 # Green
    '7': 'Personal Projects',     # Blue
    None: 'Chores & Misc',        # Grey
    '11': 'Wasted Time',          # Red

    # Add alternative mappings if needed
    # '1': 'Personal Development',
    # '2': 'Work',
    # etc.
}

# Deep work categories
DEEP_WORK_CATEGORIES = ['Work', 'Personal Projects']

# Default timezone
TIMEZONE = 'America/New_York'  # Update to your timezone

# Google Calendar API settings
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
