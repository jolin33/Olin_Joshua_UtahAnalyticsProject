import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load your data
data = pd.read_csv('../visualization/data_extracts/average_player_stats.csv')


'''
TO DO:

Add some interesting player names on each graph
Add a legend to each graph, indicating what each colour represents
Manually set the title for each category

'''

'''Goals'''

# Assuming 'data' is your DataFrame and contains columns 'Player', 'Goals_STD_Regular', 'Goals_STD_Playoffs'

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[['Goals_Regular', 'Goals_Playoffs']])

# Perform K-Means clustering with the chosen number of clusters
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(data_scaled)
data['Cluster'] = clusters

# Analyze the clusters
cluster_analysis = data.groupby('Cluster').mean(numeric_only=True)

# Map clusters to custom labels
cluster_labels_goals = {
    0: "Average Consistency",
    1: "Inconsistent",
    2: "Extremely Consistent",
    3: "Extremely Inconsistent"
}

# Visualize the clusters
plt.figure(figsize=(10, 7))
scatter = plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=clusters, cmap='viridis')

players_goals = ['Quinn Hughes','Vince Dunn','Josh Morrissey','Nico Hischier','John Carlson','Elias Pettersson','Anze Kopitar','Alex Debrincat','Nick Suzuki','Aleksander Barkov','Sydney Crosby','Joe Pavelsi','Sam Reinhart','Leon Draisaitl','Nathan Mackinnon','Auston Matthews','Connor Mcdavid','Brad Marchand','Joe Pavelski','J.T. Miller','Jesper Bratt','Gustav Nyquist','Jared Mccann']

# Add player names to the plot
for i, player in enumerate(data['Player']):
    if player in players_goals:
        plt.annotate(
            player,  # Text label
            (data_scaled[i, 0], data_scaled[i, 1]), 
            textcoords="offset points",
            xytext=(10, 10),
            ha='center',  # Horizontal alignment of the label
            fontsize=9,
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5)  # Arrow properties
        )

# Add title and labels
plt.title('Goals Clusters')
plt.xlabel('Goals Regular Season (Standardized)')
plt.ylabel('Goals Playoffs (Standardized)')

# Create custom legend
handles, _ = scatter.legend_elements()
custom_legend = [handles[0], handles[1], handles[2], handles[3]]
labels = [cluster_labels_goals[i] for i in range(4)]
plt.legend(custom_legend, labels, title="Cluster Types")

# Show the plot
plt.show()


'''Assists'''
# scaler = StandardScaler()
# data_scaled = scaler.fit_transform(data[['Assists_Regular', 'Assists_Playoffs']])

# # Perform K-Means clustering with the chosen number of clusters
# kmeans = KMeans(n_clusters=4, random_state=42)
# clusters = kmeans.fit_predict(data_scaled)
# data['Cluster'] = clusters

# # Analyze the clusters
# cluster_analysis = data.groupby('Cluster').mean(numeric_only=True)

# # Map clusters to custom labels
# cluster_labels_assists = {
#     0: "Average Consistency",
#     1: "Playoff Performer",
#     2: "Extremely Consistent",
#     3: "Inconsistent"
# }

# # Visualize the clusters
# plt.figure(figsize=(10, 7))
# scatter = plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=clusters, cmap='viridis')

# players_assists = ['Josh Morrissey','John Carlson','Anze Kopitar','Alex Debrincat','Aleksander Barkov','Sydney Crosby','Joe Pavelsi','Sam Reinhart','Leon Draisaitl','Nathan Mackinnon','Auston Matthews','Connor Mcdavid','Brad Marchand','Jesper Bratt','Owen Tippett', 'Cole Caufield', 'Dylan Strome', 'Jordan Kyrou','Adam Henrique','Kevin Fiala','Frank Vatrano','Nick Foligno']

# # Add player names to the plot
# for i, player in enumerate(data['Player']):
#     if player in players_assists:
#         plt.annotate(
#             player,  # Text label
#             (data_scaled[i, 0], data_scaled[i, 1]), 
#             textcoords="offset points",
#             xytext=(10, 10),
#             ha='center',  # Horizontal alignment of the label
#             fontsize=9,
#             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5)  # Arrow properties
#         )

# # Add title and labels
# plt.title('Assists Clusters')
# plt.xlabel('Assists Regular Season (Standardized)')
# plt.ylabel('Assists Playoffs (Standardized)')

# # Create custom legend
# handles, _ = scatter.legend_elements()
# custom_legend = [handles[0], handles[1], handles[2], handles[3]]
# labels = [cluster_labels_assists[i] for i in range(4)]# Manually setting the legend box coordinates
# plt.legend(custom_legend, labels, title="Cluster Types", fontsize='small', borderpad=0.5, frameon=True, loc='upper left',
#            bbox_to_anchor=(0.1, 0.9)) 

# # Show the plot
# plt.show()

# '''Takeaways'''

# scaler = StandardScaler()
# data_scaled = scaler.fit_transform(data[['Takeaways_Regular', 'Takeaways_Playoffs']])

# # Perform K-Means clustering with the chosen number of clusters
# kmeans = KMeans(n_clusters=4, random_state=42)
# clusters = kmeans.fit_predict(data_scaled)
# data['Cluster'] = clusters

# # Analyze the clusters
# cluster_analysis = data.groupby('Cluster').mean(numeric_only=True)

# # Map clusters to custom labels
# cluster_labels_takeaways = {
#     0: "Average Consistency",
#     1: "Playoff Inconsistency",
#     2: "Regular Season Inconsistency",
#     3: "Extremely Consistent"
# }

# # Visualize the clusters
# plt.figure(figsize=(10, 7))
# scatter = plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=clusters, cmap='viridis')

# players_takeaways = ['Vince Dunn','Josh Morrissey','John Carlson','Anze Kopitar','Alex Debrincat','Aleksander Barkov','Sydney Crosby','Joe Pavelsi','Sam Reinhart','Leon Draisaitl','Nathan Mackinnon','Auston Matthews','Connor Mcdavid','Brad Marchand','J.T. Miller','Owen Tippett', 'Cole Caufield', 'Jordan Kyrou','Adam Henrique','Kevin Fiala','Frank Vatrano','Nick Foligno','Mathew Barzal','Elias Pettersson','Matthew Tkachuk','Cale Makar','Martin Necas']

# # Add player names to the plot
# for i, player in enumerate(data['Player']):
#     if player in players_takeaways:
#         plt.annotate(
#             player,  # Text label
#             (data_scaled[i, 0], data_scaled[i, 1]), 
#             textcoords="offset points",
#             xytext=(10, 10),
#             ha='center',  # Horizontal alignment of the label
#             fontsize=9,
#             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5)  # Arrow properties
#         )

# # Add title and labels
# plt.title('Takeaways Clusters')
# plt.xlabel('Takeaways Regular Season (Standardized)')
# plt.ylabel('Takeaways Playoffs (Standardized)')

# # Create custom legend
# handles, _ = scatter.legend_elements()
# custom_legend = [handles[0], handles[1], handles[2], handles[3]]
# labels = [cluster_labels_takeaways[i] for i in range(4)]# Manually setting the legend box coordinates
# plt.legend(custom_legend, labels, title="Cluster Types",frameon=True, loc='upper left') 

# # Show the plot
# plt.show()
