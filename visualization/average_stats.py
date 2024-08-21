import pandas as pd

# Load the dataset
file_path = '../input/nhl_player_stats_refined.csv'
df = pd.read_csv(file_path)

# Group by player and season, then calculate the mean for each group
player_season_avg = df.groupby(['Player', 'Season']).mean().reset_index()

# Save the result to a new CSV file
player_season_avg.to_csv('data_extracts/player_season_avg.csv', index=False)

print("New CSV file with average stats per player per season created successfully.")
