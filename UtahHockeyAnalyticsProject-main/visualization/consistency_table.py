import pandas as pd

# Load the data
data = pd.read_csv('../input/nhl_player_stats_refined.csv')
season_avg = pd.read_csv('data_extracts/player_season_avg.csv')

# Merge the data with the season averages
merged_data = pd.merge(data, season_avg, on=['Player', 'Season'], suffixes=('', '_Avg'))

# Normalize the statistics by the player's average for that season
merged_data['G_normalized'] = merged_data['G'] / merged_data['G_Avg']
merged_data['A_normalized'] = merged_data['A'] / merged_data['A_Avg']
merged_data['TKA_normalized'] = merged_data['TKA'] / merged_data['TKA_Avg']

# Group by Player, Season, and Playoff/Regular, then calculate the standard deviation for normalized stats
std_dev_table_normalized = merged_data.groupby(['Player', 'Season', 'Playoff/Regular']).agg({
    'G_normalized': lambda x: round(x.std(), 2),
    'A_normalized': lambda x: round(x.std(), 2),
    'TKA_normalized': lambda x: round(x.std(), 2)
}).reset_index()

# Pivot the data so that Regular and Playoff values are in the same row
std_dev_pivot_normalized = std_dev_table_normalized.pivot_table(
    index=['Player', 'Season'], 
    columns='Playoff/Regular', 
    values=['G_normalized', 'A_normalized', 'TKA_normalized']
).reset_index()

# Flatten the MultiIndex columns
std_dev_pivot_normalized.columns = ['_'.join(col).strip() if col[1] else col[0] for col in std_dev_pivot_normalized.columns.values]

# Rename the columns for clarity
std_dev_pivot_normalized.rename(columns={
    'G_normalized_Regular': 'Goals_Regular',
    'G_normalized_Playoffs': 'Goals_Playoffs',
    'A_normalized_Regular': 'Assists_Regular',
    'A_normalized_Playoffs': 'Assists_Playoffs',
    'TKA_normalized_Regular': 'Takeaways_Regular',
    'TKA_normalized_Playoffs': 'Takeaways_Playoffs'
}, inplace=True)

# Display the final table
print(std_dev_pivot_normalized)

# Save the final table to a CSV file
std_dev_pivot_normalized.to_csv('normalized_consistency_table.csv', index=False)










