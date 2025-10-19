#-------------------------------------------------------------------------------
# project_7_midterm_project_leo_valladares.py
# This project analyze a Formula 1 dataset and generate vizualizations
# Author: Leonardo Valladares
# Date: 2025-10-19
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries
# --------------------------------------
import os
import pandas as pd
import plotly.graph_objects as go


# --------------------------------------
# Load data
# --------------------------------------

folder_path = "formula_1/formula1-datasets/"

filenames = [
    "formula1_2019season_raceResults.csv",
    "formula1_2020season_raceResults.csv",
    "formula1_2021season_raceResults.csv",
    "formula1_2022season_raceResults.csv",
    "formula1_2023season_raceResults.csv",
    "formula1_2024season_raceResults.csv",  
    "formula1_2025season_raceResults.csv"
]

# --------------------------------------
# Exploring and cleaning the dataset
# --------------------------------------

dfs = {}
for fname in filenames:
    full = os.path.join(folder_path, fname)
    try:
        dfs[fname] = pd.read_csv(full)
        print("Loaded", fname)
    except FileNotFoundError:
        print("Missing:", full)

# Print column names for every loaded DataFrame
# for key, df in dfs.items():
#     print(key, df.columns.tolist())

# Rename columns in 2019 and 2020 dataframes
for year in ["formula1_2019season_raceResults.csv", "formula1_2020season_raceResults.csv"]:
    if year in dfs:
        dfs[year] = dfs[year].rename(columns={
            'Total Time/Gap/Retirement': 'Time/Retired',
            'Fastest Lap': 'Fastest Lap Time'
        })
        print(f"Renamed columns in {year}")

# Rename columns in 2021 and 2022 dataframes
for year in ["formula1_2021season_raceResults.csv", "formula1_2022season_raceResults.csv"]:
    if year in dfs:
        dfs[year] = dfs[year].rename(columns={
            'Fastest Lap': 'Fastest Lap Time'
        })
        print(f"Renamed columns in {year}")


# Define the columns to keep
columns_to_keep = [
    'Track', 'Position', 'No', 'Driver', 'Team', 
    'Starting Grid', 'Laps', 'Time/Retired', 'Points', 'Fastest Lap Time'
]

# Filter each dataframe to keep only the specified columns
filtered_dfs = []
for fname, df in dfs.items():
    # Extract the season year from the filename
    season = fname.split('_')[1][:4]  # Gets "2019" from "formula1_2019season_raceResults.csv"
    
    # Check which columns exist in this dataframe
    available_cols = [col for col in columns_to_keep if col in df.columns]
    filtered_df = df[available_cols].copy()

    # Add Season column as the first column
    filtered_df.insert(0, 'Season', season)

    filtered_dfs.append(filtered_df)
    print(f"Filtered {fname}: kept {len(available_cols)} columns")

# Concatenate all dataframes into one
combined_df = pd.concat(filtered_dfs, ignore_index=True)

# Create team name crosswalk dictionary
team_crosswalk = {
    'AlphaTauri Honda': 'AlphaTauri',
    'AlphaTauri Honda RBPT': 'AlphaTauri',
    'AlphaTauri RBPT': 'AlphaTauri',
    'Aston Martin Aramco Mercedes': 'Aston Martin',
    'Aston Martin Mercedes': 'Aston Martin',
    'Alfa Romeo Ferrari': 'Ferrari',
    'Alfa Romeo Racing Ferrari': 'Ferrari',
    'Ferrari': 'Ferrari',
    'Haas Ferrari': 'Ferrari',
    'Kick Sauber Ferrari': 'Ferrari',
    'McLaren Mercedes': 'McLaren',
    'McLaren Renault': 'McLaren',
    'Mercedes': 'Mercedes',
    'Racing Point BWT Mercedes': 'Racing Point',
    'RB Honda RBPT': 'Red Bull Racing',
    'Racing Bulls Honda RBPT': 'Red Bull Racing',
    'Red Bull Racing Honda': 'Red Bull Racing',
    'Red Bull Racing Honda EBPT': 'Red Bull Racing',
    'Red Bull Racing Honda RBPT': 'Red Bull Racing',
    'Red Bull Racing RBPT': 'Red Bull Racing',
    'Alpine Renault': 'Renault',
    'Renault': 'Renault',
    'Scuderia Toro Rosso Honda': 'Toro Rosso',
    'Williams Mercedes': 'Williams'
}

# Add team_common_name column using the crosswalk
combined_df['team_common_name'] = combined_df['Team'].map(team_crosswalk)

# Check for any teams that weren't mapped
unmapped_teams = combined_df[combined_df['team_common_name'].isna()]['Team'].unique()
if len(unmapped_teams) > 0:
    print(f"\nWarning: The following teams were not mapped:")
    for team in unmapped_teams:
        print(f"  - {team}")

print(f"\nCombined dataframe shape: {combined_df.shape}")
print(f"Columns in combined dataframe: {combined_df.columns.tolist()}")
print(f"\nFirst few rows:")
print(combined_df.head())

# Show unique team mappings
print(f"\nUnique original teams: {combined_df['Team'].nunique()}")
print(f"Unique standardized teams: {combined_df['team_common_name'].nunique()}")
print(f"\nStandardized team names:")
print(combined_df['team_common_name'].value_counts())

# Export to Excel
# output_file = "combined_race_results.xlsx"
# combined_df.to_excel(output_file, index=False, sheet_name='Race Results')
# print(f"\nExcel file saved to: {output_file}")

# --------------------------------------
# Creating visualizations 
# --------------------------------------

### Team Wins by Season (2019–2025)

# # Convert Position and Season to numeric
combined_df['Position'] = pd.to_numeric(combined_df['Position'], errors='coerce')

# Filter for Position = 1
first_position = combined_df[combined_df['Position'] == 1].copy()

# Count first positions by team and season
team_wins = first_position.groupby(['Season', 'team_common_name']).size().reset_index(name='wins')

# Sort by Season to ensure chronological order
team_wins = team_wins.sort_values('Season')

# Remove teams that have only 1 win across all seasons
team_total_wins = team_wins.groupby('team_common_name')['wins'].sum()
teams_to_keep = team_total_wins[team_total_wins > 1].index
team_wins_filtered = team_wins[team_wins['team_common_name'].isin(teams_to_keep)]

# ensure Season is numeric, then create the filtered table
team_wins_filtered['Season'] = pd.to_numeric(team_wins_filtered['Season'], errors='coerce').astype(int)
team_wins_filtered = team_wins_filtered.sort_values(['Season', 'team_common_name'])

# get sorted list of seasons for ticks
seasons = sorted(team_wins_filtered['Season'].unique())

# Define F1 team colors
team_colors = {
    'Ferrari': '#DC0000',           # Ferrari Red
    'Mercedes': '#00D2BE',          # Mercedes Teal
    'Red Bull Racing': '#0600EF',  # Red Bull Blue
    'McLaren': '#FF8700',          # McLaren Orange
    'Aston Martin': '#006F62',     # Aston Martin Green
    'Alpine': '#0090FF',           # Alpine Blue
    'AlphaTauri': '#2B4562',       # AlphaTauri Navy
    'Alfa Romeo': '#900000',       # Alfa Romeo Burgundy
    'Haas': '#FFFFFF',             # Haas White (will use gray for visibility)
    'Williams': '#005AFF',         # Williams Blue
    'Racing Point': '#F596C8',     # Racing Point Pink
    'Renault': '#FFF500',          # Renault Yellow
    'Toro Rosso': '#469BFF'        # Toro Rosso Blue
}

# Create the line chart
fig = go.Figure()

for team in sorted(team_wins_filtered['team_common_name'].unique()):
    team_data = team_wins_filtered[team_wins_filtered['team_common_name'] == team].sort_values('Season')
    
    # Get team color, default to gray if not found
    color = team_colors.get(team, '#808080')
    
    
    fig.add_trace(go.Scatter(
        x=team_data['Season'],
        y=team_data['wins'],
        mode='lines+markers',
        name=team,
        line=dict(width=3, color=color),
        marker=dict(size=5, color=color)
    ))

fig.update_layout(
    title='Team Wins by Season (2019–2025)',
    xaxis_title='Season',
    yaxis_title='Count of First Positions',
    xaxis=dict(
        type='linear',                    # numeric axis — preserves chronological order
        tickmode='array',
        tickvals=seasons,
        ticktext=[str(s) for s in seasons]   # optional: display as strings
    ),
    hovermode='closest',
    legend_title='Team',
    template='plotly_white',
    width=1200,
    height=600,
    # xaxis=dict(type='category')
)

fig.show()

### Drivers Points by Season (Mercedes & Red Bull Racing) Chart

# Filter for Mercedes and Red Bull Racing
top_teams = combined_df[combined_df['team_common_name'].isin(['Mercedes', 'Red Bull Racing'])].copy()

# Calculate total points by driver
driver_total_points = top_teams.groupby('Driver')['Points'].sum().sort_values(ascending=False)

# Get top 4 drivers
top_4_drivers = driver_total_points.head(4).index.tolist()

# Filter data for top 4 drivers
top_drivers_data = top_teams[top_teams['Driver'].isin(top_4_drivers)].copy()

# Group by Season and Driver, sum the points
driver_season_points = top_drivers_data.groupby(['Season', 'Driver'])['Points'].sum().reset_index()

# Sort by Season
driver_season_points = driver_season_points.sort_values('Season')

# Define driver colors (variations of team colors)
driver_colors = {
    'Lewis Hamilton': '#00A19C',      # Mercedes Teal (darker)
    'George Russell': '#70F4E8',      # Mercedes Teal (lighter)
    'Max Verstappen': '#1E41FF',      # Red Bull Blue (brighter)
    'Sergio Perez': '#0A0080'         # Red Bull Blue (darker)
}

# Create the line chart
fig = go.Figure()

for driver in top_4_drivers:
    driver_data = driver_season_points[driver_season_points['Driver'] == driver].sort_values('Season')
    
    # Get driver color, default to gray if not found
    color = driver_colors.get(driver, '#808080')
    
    fig.add_trace(go.Scatter(
        x=driver_data['Season'],
        y=driver_data['Points'],
        mode='lines+markers',
        name=driver,
        line=dict(width=3, color=color),
        marker=dict(size=5, color=color)
    ))

fig.update_layout(
    title='Top Drivers Points by Season (Mercedes & Red Bull Racing)',
    xaxis_title='Season',
    yaxis_title='Sum of Points',
    hovermode='closest',
    legend_title='Driver',
    template='plotly_white',
    width=1200,
    height=600,
    xaxis=dict(type='category')
)

fig.show()

### Races with No Points (Consistency of Top Drivers - Mercedes & Red Bull Racing)

# Filter for Mercedes and Red Bull Racing, and Points = 0
zero_points_data = combined_df[
    (combined_df['team_common_name'].isin(['Mercedes', 'Red Bull Racing'])) & 
    (combined_df['Points'] == 0)
].copy()

# Filter for top 4 drivers (using the same drivers from previous chart)
zero_points_top4 = zero_points_data[zero_points_data['Driver'].isin(top_4_drivers)].copy()

# Convert Season to numeric to ensure proper sorting
zero_points_top4['Season'] = pd.to_numeric(zero_points_top4['Season'], errors='coerce')

# Count occurrences by Season and Driver
driver_zero_points_count = zero_points_top4.groupby(['Season', 'Driver']).size().reset_index(name='count')

# Sort by Season
driver_zero_points_count = driver_zero_points_count.sort_values('Season')

# Create the line chart
fig = go.Figure()

for driver in top_4_drivers:
    driver_data = driver_zero_points_count[driver_zero_points_count['Driver'] == driver].sort_values('Season')
    
    # Get driver color (same as previous chart)
    color = driver_colors.get(driver, '#808080')
    
    fig.add_trace(go.Scatter(
        x=driver_data['Season'],
        y=driver_data['count'],
        mode='lines+markers',
        name=driver,
        line=dict(width=3, color=color),
        marker=dict(size=5, color=color)
    ))

fig.update_layout(
    title='Races with No Points (Consistency of Top Drivers - Mercedes & Red Bull Racing)',
    xaxis_title='Season',
    yaxis_title='Count of Driver',
    hovermode='closest',
    legend_title='Driver',
    template='plotly_white',
    width=1200,
    height=600,
    xaxis=dict(
        type='linear',
        tickmode='linear',
        tick0=2019,
        dtick=1
    )
)

fig.show()