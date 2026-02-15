# Calendar Time Tracker - Setup Guide

This guide will help you set up the Calendar Time Tracker to analyze your time usage from Google Calendar.

## Prerequisites

- Python 3.8 or higher
- Google account with Google Calendar
- Basic command line knowledge

## Step 1: Install Python Dependencies

Navigate to the project directory and install required packages:

```bash
cd calendar-tracker
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
cd calendar-tracker
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## Step 2: Set Up Google Calendar API Access

### 2.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project (e.g., "Calendar Time Tracker")
4. Click "Create"

### 2.2 Enable Google Calendar API

1. In your new project, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### 2.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted to configure consent screen:
   - Click "Configure Consent Screen"
   - Choose "External" (unless you have a Google Workspace account)
   - Fill in required fields:
     - App name: "Calendar Time Tracker"
     - User support email: your email
     - Developer contact: your email
   - Click "Save and Continue"
   - Skip adding scopes (click "Save and Continue")
   - Add your email as a test user
   - Click "Save and Continue"
4. Back on the Credentials page:
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Calendar Tracker Desktop"
   - Click "Create"
5. Download the credentials:
   - Click the download icon next to your newly created OAuth client
   - Save the file as `credentials.json` in the `calendar-tracker` directory

### 2.4 Verify File Structure

Your directory should look like this:

```
calendar-tracker/
├── credentials.json       ← Your downloaded credentials
├── requirements.txt
├── config.py
├── app.py
└── src/
    ├── calendar_client.py
    └── metrics.py
```

## Step 3: Configure Color Mappings

Google Calendar uses numeric color IDs (1-11) for event colors. You need to map these to your categories.

### 3.1 Find Your Color IDs

1. Run the app for the first time:
   ```bash
   streamlit run app.py
   ```

2. When prompted, authorize the app in your browser (this creates `token.pickle`)

3. In the dashboard, scroll down to the "Debug: View Color Mappings" section

4. Select today's date and click "Show Events"

5. Look at the `color_id` column to see which numbers correspond to your colors

### 3.2 Update config.py

Open `config.py` and update the `COLOR_CATEGORIES` dictionary with your color IDs:

```python
COLOR_CATEGORIES = {
    '5': 'Personal Development',  # Replace '5' with your yellow color ID
    '10': 'Work',                 # Replace '10' with your green color ID
    '9': 'Personal Projects',     # Replace '9' with your blue color ID
    '8': 'Chores & Misc',        # Replace '8' with your grey color ID
    '11': 'Wasted Time',          # Replace '11' with your red color ID
}
```

### 3.3 Update Timezone (Optional)

Update the `TIMEZONE` setting in `config.py` to match your location:

```python
TIMEZONE = 'America/New_York'  # or 'Europe/London', 'Asia/Tokyo', etc.
```

## Step 4: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser (usually at `http://localhost:8501`)

## Using the Dashboard

1. **Select View Type**: Choose Daily, Weekly, or Monthly
2. **Pick Date Range**: Select the specific date/week/month
3. **Calculate Metrics**: Click the "Calculate Metrics" button
4. **View Results**: 
   - Total tracked time
   - Deep work hours (Work + Personal Projects)
   - Category breakdown with charts
   - Daily trends (for weekly/monthly views)

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the OAuth credentials from Google Cloud Console
- Place the file in the `calendar-tracker` directory (not in `src/`)

### "Token has been expired or revoked"
- Delete `token.pickle` and run the app again
- Re-authorize when prompted

### Events showing as "Uncategorized"
- Your color IDs in `config.py` don't match your actual calendar colors
- Use the Debug section to find the correct color IDs
- Update `COLOR_CATEGORIES` in `config.py`

### "No events found"
- Make sure you have events in your calendar for the selected date range
- Check that you're using the correct calendar (defaults to 'primary')
- Verify the events have colors assigned in Google Calendar

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- If using a virtual environment, make sure it's activated

## Next Steps

Once everything is working, you can:

1. **Add more features**: 
   - Export data to CSV
   - Set goals and track progress
   - Compare weeks/months
   - Add custom categories

2. **Automate tracking**:
   - Run daily scripts to cache data
   - Set up scheduled reports
   - Create alerts for low deep work time

3. **Database integration**:
   - Store historical data in SQLite/PostgreSQL
   - Enable faster analysis of long time periods

## Getting Help

If you run into issues:
1. Check the error message carefully
2. Verify all setup steps were completed
3. Use the Debug section in the dashboard to inspect your events
4. Make sure your calendar has events with assigned colors

## Privacy & Security

- `credentials.json` contains sensitive API credentials - never share it
- `token.pickle` contains your access token - keep it private
- Add both files to `.gitignore` if using version control
- The app only requests read-only access to your calendar
