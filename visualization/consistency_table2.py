import pandas as pd

# Load the CSV file
file_path = './data_extracts/consistency_table.csv'
data = pd.read_csv(file_path)

# Step 1: Filter out rows where any playoff stats (G, A, TKA) are NaN or 0
filtered_data = data.dropna(subset=['Assists_Playoffs', 'Goals_Playoffs', 'Takeaways_Playoffs'])
filtered_data = filtered_data[(filtered_data['Assists_Playoffs'] != 0) & 
                              (filtered_data['Goals_Playoffs'] != 0) & 
                              (filtered_data['Takeaways_Playoffs'] != 0)]

# Step 2: Calculate the average of regular season stats (G, A, TKA) for each player
average_stats = filtered_data.groupby('Player').mean()[['Assists_Playoffs', 'Goals_Playoffs', 'Takeaways_Playoffs','Assists_Regular', 'Goals_Regular', 'Takeaways_Regular']]

average_stats = average_stats.round(3)

# Reset the index to have a clean DataFrame with players as rows
average_stats.reset_index(inplace=True)

# Step 3: Save the resulting table to a new CSV file (optional)
output_file_path = './data_extracts/average_player_stats.csv'
average_stats.to_csv(output_file_path, index=False)

# Display the first few rows of the new table
print(average_stats.head())

