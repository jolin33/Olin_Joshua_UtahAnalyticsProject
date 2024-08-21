import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Define the features you want to use for clustering
features = ['Goals_STD_Regular', 'Goals_STD_Playoffs', 'Assists_STD_Regular', 'Assists_STD_Playoffs', 'TKA_STD_Regular', 'TKA_STD_Playoffs']

# Standardize the features
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[features])

# Perform KMeans clustering
kmeans = KMeans(n_clusters=4, random_state=42)
data['Cluster'] = kmeans.fit_predict(data_scaled)

# Now you can proceed with the logistic regression code

# Load the data
data = pd.read_csv('../visualization/data_extracts/average_player_stats.csv')

# Display the first few rows to understand the structure
print(data.head())

# Check for missing values and handle them (e.g., drop or fill)
data = data.dropna()

# For binary classification, we need to define the target variable.
# Let's assume we define a player as "consistent" if they belong to certain clusters.

# Create a binary target variable
# Example: Label players as consistent (1) if they belong to cluster 0, otherwise inconsistent (0)
data['Target'] = data['Cluster'].apply(lambda x: 1 if x == 0 else 0)

# Define features and target
X = data[['Goals_STD_Regular', 'Goals_STD_Playoffs', 'Assists_STD_Regular', 'Assists_STD_Playoffs', 'TKA_STD_Regular', 'TKA_STD_Playoffs']]
y = data['Target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the feature data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the Logistic Regression model
logreg = LogisticRegression(random_state=42)
logreg.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = logreg.predict(X_test_scaled)

# Evaluate the model's performance
print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
