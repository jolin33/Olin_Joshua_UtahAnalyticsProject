import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def convert_date(date_str, season_str):
    # Extract month and day from date_str
    _, date_part = date_str.split()
    month, day = map(int, date_part.split('/'))

    # Extract the start and end years from season_str
    start_year, end_year = map(int, season_str.split('-'))

    # Determine the correct year
    if month < 7:
        year = end_year+2000  # Use the later year if month < 7
    else:
        year = start_year  # Use the earlier year if month >= 7

    # Create the datetime object
    date_obj = datetime(year, month, day)

    return date_obj


# Load the data
file_path = '../input/nhl_player_stats.csv'
data = pd.read_csv(file_path)

# Convert 'DATE' to datetime (you might need to adjust the format if there are issues)
data['Date'] = data.apply(lambda row: convert_date(row['DATE'], row['Season']), axis=1)

# Rename 'MonthOrPlayoff' for clarity
data.rename(columns={'MonthOrPlayoff': 'Playoff/Regular'}, inplace=True)
data['Playoff/Regular'] = data['Playoff/Regular'].map({'Y': 'Playoffs', 'N': 'Regular'})

# Select a few key players for comparison
key_players = data['Player'].unique()[:5]  # Select the first 5 unique players for this example

# Create individual plots for each player
for player in key_players:
    player_data = data[data['Player'] == player]

    plt.figure(figsize=(14, 7))

    # Goals
    plt.subplot(3, 1, 1)
    sns.lineplot(data=player_data, x='DATE', y='G', hue='Playoff/Regular', marker='o')
    plt.title(f'{player} - Goals over Time')
    plt.xlabel('Date')
    plt.ylabel('Goals')

    # Assists
    plt.subplot(3, 1, 2)
    sns.lineplot(data=player_data, x='DATE', y='A', hue='Playoff/Regular', marker='o')
    plt.title(f'{player} - Assists over Time')
    plt.xlabel('Date')
    plt.ylabel('Assists')

    # Takeaways
    plt.subplot(3, 1, 3)
    sns.lineplot(data=player_data, x='DATE', y='TKA', hue='Playoff/Regular', marker='o')
    plt.title(f'{player} - Takeaways over Time')
    plt.xlabel('Date')
    plt.ylabel('Takeaways')

    plt.tight_layout()
    plt.show()
