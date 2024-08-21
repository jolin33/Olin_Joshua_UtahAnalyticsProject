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
data = pd.read_csv('../input/nhl_player_stats_refined.csv')

data = data[data["Season"] == '2023-24']
data = data[data["Player"] == 'Mitchell Marner']

data = data[::-1]

print(data)

# Time Series Plots
plt.figure(figsize=(14, 7))
# for player in data['Player'].unique()[:3]:
# player_data = data[data['Player'] == player]
# plt.plot(data['Date'], data['G'], 'bo--', linewidth=2, markersize=12)
# sns.lineplot(data=data, x='Date', y='G', hue='Playoff/Regular', markers=True, dashes=False)
for key, grp in data.groupby(['Playoff/Regular']):
    plt.plot(grp['Date'], grp['G'], label=key)


plt.title('Goals over Time')
plt.xlabel('Date')
plt.ylabel('G')
print('hi')
# plt.legend()
plt.show()

# Box Plots
plt.figure(figsize=(14, 7))
sns.boxplot(x='Playoff/Regular', y='G', data=data)
plt.title('Distribution of Goals in Regular Season vs Playoffs')
plt.show()

# Scatter Plot
regular_season = data[data['Playoff/Regular'] == 'Regular']
playoffs = data[data['Playoff/Regular'] == 'Playoffs']
plt.figure(figsize=(14, 7))
plt.scatter(regular_season['Date'], regular_season['G'])
plt.scatter(playoffs['Date'], playoffs['G'])
plt.title('Regular Season Goals vs Playoff Goals')
plt.xlabel('Regular Season Goals')
plt.ylabel('Playoff Goals')
plt.show()

# Heatmap
corr_matrix = data[['G', 'A', 'TKA']].corr()
plt.figure(figsize=(14, 7))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()
