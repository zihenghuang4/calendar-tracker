# Quick Start Guide - Calendar Time Tracker

Get your time tracker running in 15 minutes!

## What You'll Get

A beautiful dashboard that shows:
- Time spent in each category (Personal Development, Work, Projects, Chores, Wasted Time)
- Deep work hours (Work + Personal Projects)
- Daily, weekly, and monthly breakdowns
- Interactive charts and graphs

## Installation (5 minutes)

### Step 1: Install Python packages

```bash
cd calendar-tracker
pip install -r requirements.txt
```

**Using virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Get Google Calendar credentials

1. Go to https://console.cloud.google.com/
2. Create new project → Name it "Calendar Tracker"
3. Enable Google Calendar API:
   - APIs & Services → Library
   - Search "Google Calendar API" → Enable
4. Create credentials:
   - APIs & Services → Credentials
   - Create Credentials → OAuth client ID
   - Configure consent screen (use your email)
   - Application type: Desktop app
   - Download as `credentials.json` → Save in calendar-tracker folder

## Configuration (5 minutes)

### Step 1: Test your setup

```bash
python test_setup.py
```

This will:
- Connect to Google Calendar (authorize in browser when prompted)
- Show your recent events
- Display their color IDs

### Step 2: Map your colors

Open `config.py` and update the color IDs based on what you saw in the test:

```python
COLOR_CATEGORIES = {
    '5': 'Personal Development',  # Update with YOUR yellow color ID
    '10': 'Work',                 # Update with YOUR green color ID
    '9': 'Personal Projects',     # Update with YOUR blue color ID
    '8': 'Chores & Misc',        # Update with YOUR grey color ID
    '11': 'Wasted Time',          # Update with YOUR red color ID
}
```

**How to find your color IDs:**
- The test script shows them, OR
- Run the app and use the Debug section at the bottom

## Launch (2 minutes)

```bash
streamlit run app.py
```

Your browser will open to `http://localhost:8501`

## Using the Dashboard

**Left Sidebar:**
1. Choose view: Daily / Weekly / Monthly
2. Select date range
3. Click "Calculate Metrics"

**Main Display:**
- Summary cards (total time, deep work, %)
- Category breakdown table
- Pie chart of time distribution
- Daily trends (for weekly/monthly)

**Debug Section:**
- Expand at bottom
- View events and their color IDs
- Verify your color mappings

## Troubleshooting

**"credentials.json not found"**
→ Download OAuth credentials from Google Cloud Console (Step 2 above)

**Events show as "Uncategorized"**
→ Update color IDs in `config.py` to match your actual calendar colors

**"No events found"**
→ Make sure your calendar has events with assigned colors for the selected dates

**Browser doesn't open**
→ Manually go to http://localhost:8501

## Tips

1. **Color your events**: Make sure all events in Google Calendar have a color assigned
2. **Consistent coloring**: Use the same color for the same category
3. **Regular tracking**: Check your dashboard weekly to spot patterns
4. **Deep work goal**: The 80% deep work you mentioned is ambitious - track progress!

## What's Next?

Once it's working:
- Export data to spreadsheets
- Set up weekly automated reports  
- Add custom categories
- Track progress toward time goals
- Analyze productivity patterns

## Need Help?

- Check `SETUP.md` for detailed troubleshooting
- Use the Debug feature to inspect your events
- Verify color mappings in `config.py`

## Privacy Note

- Your data stays on your computer
- Read-only calendar access
- No data sent anywhere
- `credentials.json` and `token.pickle` are private - don't share them

---

**Ready?** Run `python test_setup.py` to begin! 🚀
