import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
stats = pd.read_csv('../input/nhl_player_stats_refined.csv')

def calculate_weighted_mean(data, metric):
  # Ensure there are no NaN values in the columns used
  data = data.dropna(subset=[metric])

  # Check if data is empty
  if data.empty:
      return np.nan

  # Calculate the weighted mean
  total_games = len(data)  # Number of rows should represent the number of games
  if total_games == 0:
      return np.nan

  weighted_sum = data[metric].sum()
  weighted_mean = weighted_sum / total_games
  return weighted_mean


# Example for one player
player_name = 'William Nylander'
player_data = stats[stats['Player'] == player_name]

# Regular season data
reg_season_data = player_data[player_data['Playoff/Regular'] == 'Regular']
reg_season_weighted_mean = calculate_weighted_mean(reg_season_data, 'G')

# Playoffs data
playoffs_data = player_data[player_data['Playoff/Regular'] == 'Playoff']
playoffs_weighted_mean = calculate_weighted_mean(playoffs_data, 'G')

# Print results
print(f"Regular Season Weighted Mean: {reg_season_weighted_mean}")
print(f"Playoffs Weighted Mean: {playoffs_weighted_mean}")

# Calculate the percentage change
if not np.isnan(reg_season_weighted_mean) and reg_season_weighted_mean != 0:
    percentage_change = ((playoffs_weighted_mean - reg_season_weighted_mean) / reg_season_weighted_mean) * 100
else:
    percentage_change = np.nan

print(f"Percentage Change: {percentage_change}%")
# Assume we have a list of player names
player_names = ['Player X', 'Player Y', 'Player Z']

# Initialize lists to store results
reg_season_means = []
playoffs_means = []

for player_name in player_names:
    player_data = stats[stats['Player'] == player_name]
    reg_season_data = player_data[player_data['Playoff/Regular'] == 'Regular']
    playoffs_data = player_data[player_data['Playoff/Regular'] == 'Playoff']

    reg_season_weighted_mean = calculate_weighted_mean(reg_season_data, 'G')
    playoffs_weighted_mean = calculate_weighted_mean(playoffs_data, 'G')

    reg_season_means.append(reg_season_weighted_mean)
    playoffs_means.append(playoffs_weighted_mean)

# Handle NaN values
player_names = [name for name in player_names if not np.isnan(reg_season_means[player_names.index(name)]) and not np.isnan(playoffs_means[player_names.index(name)])]
reg_season_means = [mean for mean in reg_season_means if not np.isnan(mean)]
playoffs_means = [mean for mean in playoffs_means if not np.isnan(mean)]

# Plotting
plt.figure(figsize=(10, 6))
width = 0.4
indices = range(len(player_names))
plt.bar(indices, reg_season_means, width=width, label='Regular Season', align='center')
plt.bar([i + width for i in indices], playoffs_means, width=width, label='Playoffs', align='center')
plt.xlabel('Players')
plt.ylabel('Goals per Game')
plt.title('Goals per Game: Regular Season vs Playoffs')
plt.xticks([i + width / 2 for i in indices], player_names)
plt.legend()
plt.show()
