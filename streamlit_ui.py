import streamlit as st
import plotly.graph_objects as go
from gameplan import Gameplan
import datetime
import colorsys

def parse_date(date_str, year):
    """Parse date string in ddmm format with specified year"""
    date_str = date_str.zfill(4)
    day = int(date_str[:2])
    month = int(date_str[2:])
    return datetime.date(year, month, day)

def generate_distinct_colors(num_colors):
    """Generate visually distinct colors"""
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.9)
        return_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0]*255), 
            int(rgb[1]*255), 
            int(rgb[2]*255)
        )
        colors.append(return_color)
    return colors

def create_match_grid(gameplan, current_date):
    # Sort teams by rank
    teams = sorted(gameplan.teams.items(), key=lambda x: x[1].rank)
    
    # Generate distinct colors for teams
    team_colors = {team.abbr: color for (_, team), color in zip(teams, generate_distinct_colors(len(teams)))}


    team_colors = {
    "MI": "#045093",  # Mumbai Indians - Blue
    "CSK": "#FFBB33",  # Chennai Super Kings - Yellow
    "RCB": "#E10600",  # Royal Challengers Bangalore - Red
    "KKR": "#4B0082",  # Kolkata Knight Riders - Purple
    "DC": "#1E90FF",  # Delhi Capitals - Blue
    "RR": "#E14D2A",  # Rajasthan Royals - Pinkish Red
    "SRH": "#FF4500",  # Sunrisers Hyderabad - Orange
    "PK": "#1A4D2E",  # Punjab Kings - Dark Green
    "LSG": "#3DBA76",  # Lucknow Super Giants - Green
    "GT": "#128C7E",  # Gujarat Titans - Teal
}



    
    # Prepare weekdays and venues
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    venues = list(set(match.venue.sym for match in gameplan.matches))
    
    # Prepare data for grid
    x_values = []
    y_values = []
    colors = []
    hover_texts = []
    
    # Add team rows
    for name, team in teams:
        for i in range(1, 71):
            match = next((m for m in team.matches if m.id == i), None)
            
            x_values.append(i)
            y_values.append(name)
            
            if match:
                match_date = parse_date(match.date, current_date.year)
                status = "Upcoming" if match_date > current_date else "Completed"
                hover_text = f"{match.date}: {match.teams[0].name} vs {match.teams[1].name}\nVenue: {match.venue.name}\nDay: {match.day}\nStatus: {status}"
                if status == "Completed":
                    colors.append("grey")
                else:
                    colors.append(team_colors[name])
                hover_texts.append(hover_text)
            else:
                colors.append('#000000')  # Light gray for no match
                # hover_texts.append("No Match")
    
    # # Add weekday row
    # for i in range(1, 71):
    #     x_values.append(i)
    #     y_values.append('Weekdays')
    #     colors.append('white')
    #     hover_texts.append(weekdays[(i-1) % 7])
    
    # # Add venue row
    # for i in range(1, 71):
    #     x_values.append(i)
    #     y_values.append('Venues')
    #     colors.append('white')
    #     hover_texts.append(venues[(i-1) % len(venues)])
    
    # Create scatter plot as grid
    fig = go.Figure(data=go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(
            size=7,
            color=colors,
            # line=dict(width=0, color='DarkSlateGray')
        ),
        text=hover_texts,
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Match Schedule Grid',
        xaxis_title='Match Number',
        yaxis_title='Teams & Metadata',
        height=400,
        width=1200
    )
    
    return fig

def main():
    st.set_page_config(layout="wide", page_title="Match Schedule Dashboard")
    
    # Initialize Gameplan
    gameplan = Gameplan("teams.tsv", "venues.tsv", "fixtures.tsv")
    
    # Sidebar for date selection
    st.sidebar.header("Match Dashboard Controls")
    
    # Year selector
    year = st.sidebar.selectbox(
        "Select Year", 
        options=[2024, 2025, 2026],
        index=1  # Default to 2025
    )
    
    # Date input with selected year
    current_date = st.sidebar.date_input(
        "Select Current Date", 
        value=datetime.date(year, 3, 1)
    )
    
    # Main dashboard
    st.title("Match Schedule Analytics")
    
    # Interactive Grid
    grid_fig = create_match_grid(gameplan, current_date)
    st.plotly_chart(grid_fig, use_container_width=True)

if __name__ == "__main__":
    main()