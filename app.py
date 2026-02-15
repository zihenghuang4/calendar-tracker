"""
Streamlit Dashboard for Calendar Time Tracker
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from calendar_client import CalendarClient
from metrics import TimeTracker

# Page configuration
st.set_page_config(
    page_title="Calendar Time Tracker",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'tracker' not in st.session_state:
    try:
        client = CalendarClient()
        st.session_state.tracker = TimeTracker(client)
        st.session_state.initialized = True
    except FileNotFoundError as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = f"Error initializing: {str(e)}"

# Title
st.title("📊 Calendar Time Tracker")

# Check if initialized
if not st.session_state.initialized:
    st.error(st.session_state.error)
    st.info("Please follow the setup instructions in SETUP.md to configure Google Calendar API access.")
    st.stop()

# Sidebar for date selection
st.sidebar.header("Date Range Selection")

view_type = st.sidebar.radio(
    "View Type",
    ["Daily", "Weekly", "Monthly"]
)

if view_type == "Daily":
    selected_date = st.sidebar.date_input(
        "Select Date",
        value=datetime.now()
    )
    
elif view_type == "Weekly":
    selected_date = st.sidebar.date_input(
        "Week Starting",
        value=datetime.now() - timedelta(days=datetime.now().weekday())
    )
    
else:  # Monthly
    col1, col2 = st.sidebar.columns(2)
    selected_month = col1.selectbox(
        "Month",
        range(1, 13),
        index=datetime.now().month - 1,
        format_func=lambda x: datetime(2000, x, 1).strftime('%B')
    )
    selected_year = col2.selectbox(
        "Year",
        range(2020, 2030),
        index=datetime.now().year - 2020
    )

# Calculate metrics button
if st.sidebar.button("Calculate Metrics", type="primary"):
    with st.spinner("Fetching calendar data..."):
        try:
            if view_type == "Daily":
                metrics = st.session_state.tracker.calculate_daily_metrics(
                    datetime.combine(selected_date, datetime.min.time())
                )
                st.session_state.current_metrics = metrics
                st.session_state.view_type = "Daily"
                
            elif view_type == "Weekly":
                metrics = st.session_state.tracker.calculate_weekly_metrics(
                    datetime.combine(selected_date, datetime.min.time())
                )
                st.session_state.current_metrics = metrics
                st.session_state.view_type = "Weekly"
                
            else:  # Monthly
                metrics = st.session_state.tracker.calculate_monthly_metrics(
                    selected_year, selected_month
                )
                st.session_state.current_metrics = metrics
                st.session_state.view_type = "Monthly"
            
            st.success("Metrics calculated successfully!")
        except Exception as e:
            st.error(f"Error calculating metrics: {str(e)}")

# Display metrics if available
if 'current_metrics' in st.session_state:
    metrics = st.session_state.current_metrics
    
    # Display date range
    if st.session_state.view_type == "Daily":
        st.subheader(f"Metrics for {metrics['date'].strftime('%B %d, %Y')}")
    elif st.session_state.view_type == "Weekly":
        st.subheader(f"Weekly Metrics: {metrics['start_date'].strftime('%b %d')} - {metrics['end_date'].strftime('%b %d, %Y')}")
    else:
        st.subheader(f"Monthly Metrics: {datetime(metrics['year'], metrics['month'], 1).strftime('%B %Y')}")
    
    # Key metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Tracked Time",
            f"{metrics['total_hours']:.1f} hrs"
        )
    
    with col2:
        st.metric(
            "Deep Work Time",
            f"{metrics['deep_work_hours']:.1f} hrs"
        )
    
    with col3:
        if metrics['total_hours'] > 0:
            deep_work_percentage = (metrics['deep_work_hours'] / metrics['total_hours']) * 100
        else:
            deep_work_percentage = 0
        st.metric(
            "Deep Work %",
            f"{deep_work_percentage:.1f}%"
        )
    
    st.divider()
    
    # Category breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Time by Category")
        
        if metrics['category_hours']:
            # Create DataFrame
            df = pd.DataFrame([
                {'Category': cat, 'Hours': hrs}
                for cat, hrs in metrics['category_hours'].items()
            ]).sort_values('Hours', ascending=False)
            
            # Display table
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No events found for this period")
    
    with col2:
        st.subheader("Category Distribution")
        
        if metrics['category_hours']:
            # Pie chart
            fig = px.pie(
                df,
                values='Hours',
                names='Category',
                title='Time Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Daily breakdown for weekly/monthly views
    if st.session_state.view_type in ["Weekly", "Monthly"] and 'daily_metrics' in metrics:
        st.divider()
        st.subheader("Daily Breakdown")
        
        # Prepare daily data
        daily_data = []
        for day_metric in metrics['daily_metrics']:
            row = {
                'Date': day_metric['date'].strftime('%Y-%m-%d'),
                'Total Hours': day_metric['total_hours'],
                'Deep Work': day_metric['deep_work_hours']
            }
            # Add categories
            for cat, hrs in day_metric['category_hours'].items():
                row[cat] = hrs
            daily_data.append(row)
        
        daily_df = pd.DataFrame(daily_data)
        
        # Line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_df['Date'],
            y=daily_df['Total Hours'],
            name='Total Hours',
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=daily_df['Date'],
            y=daily_df['Deep Work'],
            name='Deep Work Hours',
            mode='lines+markers'
        ))
        fig.update_layout(
            title='Daily Time Tracking',
            xaxis_title='Date',
            yaxis_title='Hours',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily table
        st.dataframe(daily_df, use_container_width=True, hide_index=True)

else:
    st.info("👈 Select a date range and click 'Calculate Metrics' to view your time tracking data")

# Debug section (collapsible)
with st.expander("🔍 Debug: View Color Mappings"):
    st.write("Use this section to identify your Google Calendar color IDs and update config.py")
    
    debug_date = st.date_input("Select date to inspect", value=datetime.now())
    
    if st.button("Show Events"):
        start = datetime.combine(debug_date, datetime.min.time())
        end = start + timedelta(days=1)
        
        events = st.session_state.tracker.get_events_with_categories(start, end)
        
        if events:
            debug_df = pd.DataFrame(events)
            st.dataframe(debug_df, use_container_width=True)
            
            st.info("""
            **Update config.py with your color IDs:**
            
            Look at the 'color_id' column above to see which numeric IDs correspond to your calendar colors.
            Then update the COLOR_CATEGORIES dictionary in config.py to map these IDs to your categories.
            
            For example, if your yellow (Personal Development) events show color_id '5', update:
            ```python
            COLOR_CATEGORIES = {
                '5': 'Personal Development',  # Yellow
                # ... etc
            }
            ```
            """)
        else:
            st.warning("No events found for this date")
