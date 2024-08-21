import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('../input/nhl_player_stats_refined.csv')

player = 'Aleksander Barkov'
season = '2015-16'

data = data[::-1]

# Filter for player and season
player_data = data[data['Player'] == player]

player_data_2024 = player_data[data['Season'] == season]

print(player_data_2024.head())

# Time Series Plots for player in 2023-2024
plt.figure(figsize=(14, 7))
plt.subplot(3, 1, 1)
sns.lineplot(data=player_data_2024, x='Date', y='G', hue='Playoff/Regular', marker='o')
plt.title(f'{player} - Goals {season}')
plt.xlabel('Date')
plt.xticks(rotation=90)
xticks = plt.xticks()[0]
n = 3
xtick_labels = [label.get_text()[5:] for label in plt.gca().get_xticklabels()[::n]]
plt.xticks(xticks[::n], labels=xtick_labels)
plt.ylabel('Goals')
plt.yticks([0,1,2,3])

plt.subplot(3, 1, 2)
sns.lineplot(data=player_data_2024, x='Date', y='A', hue='Playoff/Regular', marker='o')
plt.title(f'{player} - Assists {season}')
plt.xlabel('Date')
plt.xticks(rotation=90)
xticks = plt.xticks()[0]
n = 3
xtick_labels = [label.get_text()[5:] for label in plt.gca().get_xticklabels()[::n]]
plt.xticks(xticks[::n], labels=xtick_labels)
plt.ylabel('Assists')
plt.yticks([0,1,2,3,4])

plt.subplot(3, 1, 3)
sns.lineplot(data=player_data_2024, x='Date', y='TKA', hue='Playoff/Regular', marker='o')
plt.title(f'{player} - Takeaways {season}')
plt.xlabel('Date')
plt.xticks(rotation=90)
xticks = plt.xticks()[0]
n = 3
xtick_labels = [label.get_text()[5:] for label in plt.gca().get_xticklabels()[::n]]
plt.xticks(xticks[::n], labels=xtick_labels)
plt.ylabel('Takeaways')
plt.yticks([0,1,2,3,4])


plt.legend()
plt.tight_layout()
plt.show()









# Box Plots - Distribution of Goals in Regular Season vs Playoffs for McDavid in 2023-2024
# plt.figure(figsize=(14, 7))
# sns.boxplot(x='Playoff/Regular', y='G', data=player_data_2024)
# plt.title('Connor McDavid - Distribution of Goals in Regular Season vs Playoffs (2023-2024)')
# plt.xlabel('Playoff or Regular Season')
# plt.ylabel('Goals')
# plt.show()

# # Scatter Plot - Regular Season Goals vs Playoff Goals for McDavid in 2023-2024
# regular_season = player_data_2024[player_data_2024['Playoff/Regular'] == 'Regular']
# playoffs = player_data_2024[player_data_2024['Playoff/Regular'] == 'Playoffs']

# # Make sure both datasets have the same length for comparison
# min_length = min(len(regular_season), len(playoffs))
# regular_season = regular_season.iloc[:min_length]
# playoffs = playoffs.iloc[:min_length]

# plt.figure(figsize=(14, 7))
# plt.scatter(regular_season['G'], playoffs['G'])
# plt.title('Connor McDavid - Regular Season Goals vs Playoff Goals (2023-2024)')
# plt.xlabel('Regular Season Goals')
# plt.ylabel('Playoff Goals')
# plt.show()

# # Heatmap - Correlation Matrix for McDavid in 2023-2024
# corr_matrix = player_data_2024[['G', 'A', 'TKA']].corr()
# plt.figure(figsize=(14, 7))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.title('Connor McDavid - Correlation Matrix of Goals, Assists, and Takeaways (2023-2024)')
# plt.show()
