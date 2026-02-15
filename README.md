# Calendar Time Tracker 📊

Track your time across different categories using Google Calendar color coding. Analyze your productivity with daily, weekly, and monthly views.

## Features

✅ **Category Tracking**: Automatically categorize events by calendar color
- Personal Development (Yellow)
- Work (Green)
- Personal Projects (Blue)
- Chores & Misc (Grey)
- Wasted Time (Red)

✅ **Deep Work Analysis**: Calculate time spent on focused work (Work + Personal Projects)

✅ **Multiple Time Ranges**: View metrics by day, week, or month

✅ **Visual Dashboard**: Interactive charts and graphs with Streamlit

✅ **Color Debugging**: Built-in tool to identify your calendar color IDs

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Calendar API** (see [SETUP.md](SETUP.md) for detailed instructions):
   - Create Google Cloud Project
   - Enable Google Calendar API
   - Download `credentials.json`

3. **Configure categories**:
   - Run the app and use the Debug section to find your color IDs
   - Update `config.py` with your mappings

4. **Launch dashboard**:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
calendar-tracker/
├── app.py                 # Streamlit dashboard
├── config.py             # Configuration and color mappings
├── requirements.txt      # Python dependencies
├── SETUP.md             # Detailed setup guide
├── credentials.json     # Google API credentials (you create this)
└── src/
    ├── calendar_client.py   # Google Calendar API wrapper
    └── metrics.py           # Time tracking calculations
```

## How It Works

1. **Data Source**: Pulls events from your Google Calendar via the API
2. **Categorization**: Maps calendar color IDs to your custom categories
3. **Calculation**: Computes time spent per category and deep work hours
4. **Visualization**: Displays metrics in an interactive dashboard

## Configuration

Edit `config.py` to customize:

```python
# Map color IDs to categories
COLOR_CATEGORIES = {
    '5': 'Personal Development',
    '10': 'Work',
    '9': 'Personal Projects',
    '8': 'Chores & Misc',
    '11': 'Wasted Time',
}

# Define what counts as deep work
DEEP_WORK_CATEGORIES = ['Work', 'Personal Projects']

# Set your timezone
TIMEZONE = 'America/New_York'
```

## Screenshots

The dashboard provides:
- **Summary Cards**: Total time, deep work hours, deep work percentage
- **Category Table**: Hours spent in each category
- **Pie Chart**: Visual breakdown of time distribution
- **Daily Trends**: Line charts showing time patterns (weekly/monthly views)
- **Debug Tools**: Inspect events and color IDs

## Requirements

- Python 3.8+
- Google account with Calendar access
- Active Google Cloud project with Calendar API enabled

## Privacy

- All data stays on your machine
- Read-only access to your calendar
- OAuth tokens stored locally in `token.pickle`
- No data sent to third parties

## Future Enhancements

Ideas for expansion:
- [ ] Export data to CSV/Excel
- [ ] Historical data database
- [ ] Goal setting and progress tracking
- [ ] Week-over-week comparisons
- [ ] Automated weekly reports
- [ ] Multiple calendar support
- [ ] Custom category definitions
- [ ] Time-of-day analysis
- [ ] Productivity insights and recommendations

## Troubleshooting

See [SETUP.md](SETUP.md) for common issues and solutions.

Quick fixes:
- **Events not categorized**: Update color IDs in `config.py`
- **No events showing**: Check date range and calendar access
- **Authentication errors**: Delete `token.pickle` and re-authorize

## Tech Stack

- **Backend**: Python 3.8+
- **Calendar API**: google-api-python-client
- **Dashboard**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas

## Contributing

This is a personal productivity tool, but feel free to:
- Fork and customize for your own use
- Add new features
- Improve the UI
- Fix bugs

## License

MIT License - feel free to use and modify for personal use.

## Support

For setup help, see [SETUP.md](SETUP.md)

For issues:
1. Check the Troubleshooting section
2. Use the Debug feature in the dashboard
3. Verify your `config.py` settings
