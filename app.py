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

# Lookup player ID (Example: Gerrit Cole)
player = playerid_lookup('crochet', 'garrett')
pitcher_id = player['key_mlbam'].values[0]  # Get MLBAM ID
player_name = "Garrett Crochet"  # Store player name for plot titles

# Get pitch data for the complete 2024 season
df = statcast_pitcher('2024-03-28', '2024-10-01', pitcher_id)

if len(df) == 0:
    exit()

# Select relevant columns
df = df[['game_date', 'pitch_type', 'release_speed', 'release_spin_rate']]

# Convert date to datetime format
df['game_date'] = pd.to_datetime(df['game_date'])

# Drop any missing values
df = df.dropna()

if len(df) == 0:
    exit()

# Map pitch types to full names
df['pitch_type'] = df['pitch_type'].map(pitch_types)

# Create week number for grouping (starting from the first week of the season)
df['week'] = (df['game_date'] - df['game_date'].min()).dt.days // 7 + 1
df['week'] = 'Week ' + df['week'].astype(str)

# Count each pitch type per week
pitch_usage = df.groupby(['week', 'pitch_type']).size().unstack()

if len(pitch_usage) == 0:
    exit()

# Create and show the first plot
ax = pitch_usage.plot(kind='line', marker='o')
plt.title(f"{player_name}: Pitch Usage Evolution (2024)")
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
plt.title(f"{player_name}: Pitch Velocity Over Time (2024)")
plt.xlabel("Date")
plt.ylabel("Velocity (mph)")
plt.legend(title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()

# Create and show the third plot
plt.figure()
sns.lineplot(data=df, x='game_date', y='release_spin_rate', hue='pitch_type', ci=None)
plt.title(f"{player_name}: Pitch Spin Rate Over Time (2024)")
plt.xlabel("Date")
plt.ylabel("Spin Rate (rpm)")
plt.legend(title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()
