# Install pybaseball if you haven't
#!pip install pybaseball pandas matplotlib seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup

# Set figure size globally for consistent plots
plt.rcParams['figure.figsize'] = [15, 8]

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

# Calculate game appearances and innings pitched
unique_games = df['game_date'].nunique()
outs_per_inning = df.groupby('game_date').agg({'inning': 'max', 'outs_when_up': 'last'})
total_innings = outs_per_inning['inning'].sum() + (outs_per_inning['outs_when_up'].sum() / 3)

# Select relevant columns
df = df[['game_date', 'pitch_type', 'release_speed', 'release_spin_rate']]

# Convert date to datetime format
df['game_date'] = pd.to_datetime(df['game_date'])

# Drop any missing values
df = df.dropna()

if len(df) == 0:
    print("No valid pitch data available after cleaning")
    exit()

# Calculate average velocity and spin rate per pitch type
avg_velocity = df.groupby('pitch_type')['release_speed'].mean().round(1)
avg_spin_rate = df.groupby('pitch_type')['release_spin_rate'].mean().round(0)

# Map pitch types to full names
df['pitch_type'] = df['pitch_type'].map(pitch_types)
avg_velocity.index = avg_velocity.index.map(pitch_types)
avg_spin_rate.index = avg_spin_rate.index.map(pitch_types)

# Count pitches by type for each game appearance
pitch_usage = df.groupby(['game_date', 'pitch_type']).size().unstack(fill_value=0)

if len(pitch_usage) == 0:
    print("No pitch usage data available")
    exit()

# Function to create plot with stats
def create_plot_with_stats(plot_func, title, ylabel):
    plt.figure(figsize=(15, 8))
    
    # Create main plot
    ax = plt.subplot2grid((5, 1), (0, 0), rowspan=4)  # Increased rowspan for more space
    plot_func(ax)
    plt.title(title)
    plt.xlabel("Game Date")
    plt.ylabel(ylabel)
    
    # Get the actual handles and labels from the plot
    handles, labels = ax.get_legend_handles_labels()
    
    # Create a mapping of pitch types to their stats
    legend_labels = {}
    for pitch_type in df['pitch_type'].unique():  # Only include pitch types that exist in the data
        if pitch_type in avg_velocity.index:
            velocity = avg_velocity[pitch_type]
            spin_rate = avg_spin_rate[pitch_type]
            legend_labels[pitch_type] = f"{pitch_type}\n({velocity} mph, {spin_rate:.0f} rpm)"
    
    # Update the labels in the same order as they appear in the plot
    updated_labels = [legend_labels[label] for label in labels]
    
    # Create legend with the updated labels
    legend = ax.legend(handles, updated_labels, title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add season statistics below the legend
    basic_stats = f"Season Statistics:\nGame Appearances: {unique_games}\nInnings Pitched: {total_innings:.1f}"
    ax.text(1.05, 0.5, basic_stats, transform=ax.transAxes, fontsize=10, va='top')
    
    plt.grid(True)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

# Create and show the first plot (Pitch Usage)
def plot_pitch_usage(ax):
    pitch_usage.plot(kind='line', marker='o', ax=ax)

create_plot_with_stats(
    plot_pitch_usage,
    f"{player_name}: Pitch Usage by Game ({season})",
    "Number of Pitches"
)

# Create and show the second plot (Velocity)
def plot_velocity(ax):
    sns.lineplot(data=df, x='game_date', y='release_speed', hue='pitch_type', ci=None, marker='o', ax=ax)

create_plot_with_stats(
    plot_velocity,
    f"{player_name}: Pitch Velocity by Game ({season})",
    "Velocity (mph)"
)

# Create and show the third plot (Spin Rate)
def plot_spin_rate(ax):
    sns.lineplot(data=df, x='game_date', y='release_spin_rate', hue='pitch_type', ci=None, marker='o', ax=ax)

create_plot_with_stats(
    plot_spin_rate,
    f"{player_name}: Pitch Spin Rate by Game ({season})",
    "Spin Rate (rpm)"
)
