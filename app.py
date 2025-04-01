# Install pybaseball if you haven't
#!pip install pybaseball pandas matplotlib seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup

# Set figure size globally for consistent plots
plt.rcParams['figure.figsize'] = [15, 6]

# Define pitch type mapping
pitch_types = {
    'FF': 'Four-Seam Fastball',
    'SI': 'Sinker',
    'CH': 'Changeup',
    'SL': 'Slider',
    'CU': 'Curveball',
    'FC': 'Cutter',
    'ST': 'Sweeper',
    'FS': 'Splitter'
}

# Define season date ranges
season_dates = {
    2021: ('2021-04-01', '2021-10-03'),
    2022: ('2022-04-07', '2022-10-05'),
    2023: ('2023-03-30', '2023-10-01'),
    2024: ('2024-03-28', '2024-10-01'),
    2025: ('2025-03-28', '2025-10-01')
}

# Get player name from user
player_input = input("Enter player name (First Last): ")
first_name, last_name = player_input.split()

# Get season from user
while True:
    try:
        season = int(input("Enter season (2021-2025): "))
        if season in season_dates:
            break
        print("Please enter a valid season between 2021 and 2025")
    except ValueError:
        print("Please enter a valid year")

# Get season date range
start_date, end_date = season_dates[season]

# Lookup player ID
player = playerid_lookup(last_name.lower(), first_name.lower())
if len(player) == 0:
    print(f"Could not find player: {player_input}")
    exit()

pitcher_id = player['key_mlbam'].values[0]  # Get MLBAM ID
player_name = f"{first_name} {last_name}"  # Store player name for plot titles

# Get pitch data for the selected season
df = statcast_pitcher(start_date, end_date, pitcher_id)

if len(df) == 0:
    print(f"No data available for {player_name} in {season}")
    exit()

# Select relevant columns
df = df[['game_date', 'pitch_type', 'release_speed', 'release_spin_rate']]

# Convert date to datetime format
df['game_date'] = pd.to_datetime(df['game_date'])

# Drop any missing values
df = df.dropna()

if len(df) == 0:
    print("No valid pitch data available after cleaning")
    exit()

# Map pitch types to full names
df['pitch_type'] = df['pitch_type'].map(pitch_types)

# Create week number for grouping (starting from the first week of the season)
df['week'] = (df['game_date'] - df['game_date'].min()).dt.days // 7 + 1
df['week'] = 'Week ' + df['week'].astype(str)

# Count each pitch type per week
pitch_usage = df.groupby(['week', 'pitch_type']).size().unstack()

if len(pitch_usage) == 0:
    print("No pitch usage data available")
    exit()

# Create and show the first plot
ax = pitch_usage.plot(kind='line', marker='o')
plt.title(f"{player_name}: Pitch Usage Evolution ({season})")
plt.xlabel("Week of Season")
plt.ylabel("Number of Pitches")
plt.legend(title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()

# Create and show the second plot
plt.figure()
sns.lineplot(data=df, x='game_date', y='release_speed', hue='pitch_type', ci=None)
plt.title(f"{player_name}: Pitch Velocity Over Time ({season})")
plt.xlabel("Date")
plt.ylabel("Velocity (mph)")
plt.legend(title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()

# Create and show the third plot
plt.figure()
sns.lineplot(data=df, x='game_date', y='release_spin_rate', hue='pitch_type', ci=None)
plt.title(f"{player_name}: Pitch Spin Rate Over Time ({season})")
plt.xlabel("Date")
plt.ylabel("Spin Rate (rpm)")
plt.legend(title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()
