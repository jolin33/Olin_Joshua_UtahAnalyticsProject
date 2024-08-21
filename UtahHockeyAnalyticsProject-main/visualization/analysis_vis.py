import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the data
data = pd.read_csv('data_extracts/consistency_table.csv')

data = data[(data['Goals_Playoffs'] != 0) & (~data['Goals_Playoffs'].isna())]

season = '2023-24'
players = ['Connor Mcdavid', 'Aleksander Barkov', 'Auston Matthews','Chris Kreider', 'Alex Ovechkin', 'Sam Reinhart', 'Mathew Barzal','Adam Henrique','Nathan Mackinnon', 'Joel Eriksson Ek', 'Josh Morrissey']

data = data[data['Season'] == season]

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(data['Goals_Regular'], data['Goals_Playoffs'])

line_eq = f'y = {slope:.2f} * x + {intercept:.2f}'

plt.figure(figsize=(8, 6))
sns.regplot(x='Goals_Regular', y='Goals_Playoffs', data=data, scatter=True, line_kws={'color': 'black'}, color='blue')


for i, row in data.iterrows():
  if row['Player'] in players:
    plt.annotate(
        row['Player'],  # Text label
        (row['Goals_Regular'], row['Goals_Playoffs']), 
        textcoords="offset points",  # Positioning relative to the data point
        xytext=(10, 10),  # Offset of the label (10 points right, 10 points up)
        ha='center',  # Horizontal alignment of the label
        fontsize=10,
        arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5)  # Arrow properties
    )

plt.text(1.15, 3.8, line_eq, fontsize=12, color='black')
plt.xlim(1.1, 2.7)
plt.ylim(0.4, 4.0)
plt.xlabel('Regular Season Goals Weighted Std Dev')
plt.ylabel('Playoff Goals Weighted Std Dev')
plt.title(f'Regular Season vs Playoff Goals Consistency, {season}')
plt.show()