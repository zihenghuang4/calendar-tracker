"""
Metrics calculation for time tracking
"""

from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
from config import COLOR_CATEGORIES, DEEP_WORK_CATEGORIES


class TimeTracker:
    def __init__(self, calendar_client):
        self.client = calendar_client

    def categorize_event(self, event):
        """
        Categorize an event based on its color

        Args:
            event: Event dictionary from Google Calendar API

        Returns:
            Category name or 'Uncategorized'
        """
        color_id = self.client.get_event_color(event)

        if color_id in COLOR_CATEGORIES:
            return COLOR_CATEGORIES[color_id]

        return 'Uncategorized'

    def calculate_daily_metrics(self, date):
        """
        Calculate metrics for a single day

        Args:
            date: datetime object for the day

        Returns:
            Dictionary with category breakdowns and deep work time
        """
        start = datetime.combine(date, datetime.min.time())
        end = start + timedelta(days=1)

        events = self.client.get_events(start, end)

        category_hours = defaultdict(float)
        deep_work_hours = 0

        # Track first and last event times for chores calculation
        first_event_time = None
        last_event_time = None
        non_chores_total = 0

        for event in events:
            category = self.categorize_event(event)
            duration = self.client.get_event_duration(event)

            # Track event times (skip all-day events)
            event_start = event['start'].get('dateTime')
            event_end = event['end'].get('dateTime')

            if event_start and 'T' in event_start:  # Not an all-day event
                event_start_dt = datetime.fromisoformat(
                    event_start.replace('Z', '+00:00'))
                event_end_dt = datetime.fromisoformat(
                    event_end.replace('Z', '+00:00'))

                if first_event_time is None or event_start_dt < first_event_time:
                    first_event_time = event_start_dt
                if last_event_time is None or event_end_dt > last_event_time:
                    last_event_time = event_end_dt

            # Add duration for non-chores categories
            if category != 'Chores & Misc':
                category_hours[category] += duration
                non_chores_total += duration

            if category in DEEP_WORK_CATEGORIES:
                deep_work_hours += duration

        # Calculate chores & misc using the formula
        if first_event_time and last_event_time:
            total_span = (last_event_time -
                          first_event_time).total_seconds() / 3600
            category_hours['Chores & Misc'] = max(
                0, total_span - non_chores_total)

        return {
            'date': date,
            'category_hours': dict(category_hours),
            'deep_work_hours': deep_work_hours,
            'total_hours': sum(category_hours.values())
        }

    def calculate_weekly_metrics(self, start_date):
        """
        Calculate metrics for a week starting from start_date

        Args:
            start_date: datetime object for the start of the week

        Returns:
            Dictionary with weekly aggregated metrics
        """
        category_hours = defaultdict(float)
        deep_work_hours = 0
        daily_metrics = []

        for i in range(7):
            day = start_date + timedelta(days=i)
            day_metrics = self.calculate_daily_metrics(day)
            daily_metrics.append(day_metrics)

            for category, hours in day_metrics['category_hours'].items():
                category_hours[category] += hours

            deep_work_hours += day_metrics['deep_work_hours']

        return {
            'start_date': start_date,
            'end_date': start_date + timedelta(days=6),
            'category_hours': dict(category_hours),
            'deep_work_hours': deep_work_hours,
            'total_hours': sum(category_hours.values()),
            'daily_metrics': daily_metrics
        }

    def calculate_monthly_metrics(self, year, month):
        """
        Calculate metrics for a specific month

        Args:
            year: Year (int)
            month: Month (int, 1-12)

        Returns:
            Dictionary with monthly aggregated metrics
        """
        from calendar import monthrange

        start_date = datetime(year, month, 1)
        _, last_day = monthrange(year, month)

        category_hours = defaultdict(float)
        deep_work_hours = 0
        daily_metrics = []

        for day in range(1, last_day + 1):
            current_date = datetime(year, month, day)
            day_metrics = self.calculate_daily_metrics(current_date)
            daily_metrics.append(day_metrics)

            for category, hours in day_metrics['category_hours'].items():
                category_hours[category] += hours

            deep_work_hours += day_metrics['deep_work_hours']

        return {
            'year': year,
            'month': month,
            'category_hours': dict(category_hours),
            'deep_work_hours': deep_work_hours,
            'total_hours': sum(category_hours.values()),
            'daily_metrics': daily_metrics
        }

    def get_events_with_categories(self, start_date, end_date):
        """
        Get all events with their categories for debugging/inspection

        Args:
            start_date: datetime object
            end_date: datetime object

        Returns:
            List of dictionaries with event details
        """
        events = self.client.get_events(start_date, end_date)

        result = []
        for event in events:
            result.append({
                'summary': event.get('summary', 'No Title'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'duration_hours': self.client.get_event_duration(event),
                'color_id': self.client.get_event_color(event),
                'category': self.categorize_event(event)
            })

        return result
