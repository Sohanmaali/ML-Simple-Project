import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('weather_data.csv')

# Convert 'Date' to datetime and extract features
df['Date'] = pd.to_datetime(df['Date'])
df['DayOfYear'] = df['Date'].dt.dayofyear
df['Month'] = df['Date'].dt.month
df['Weekday'] = df['Date'].dt.weekday

# Select features and target variable
X = df[['DayOfYear', 'Humidity', 'WindSpeed', 'Pressure']]
y = df['Temperature']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R² Score: {r2}')

# Visualize the results
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Temperature')
plt.ylabel('Predicted Temperature')
plt.title('Actual vs Predicted Temperature')
plt.show()

# Predict today's temperature (example: using today's date and sample feature values)
today_features = np.array([[pd.to_datetime('2025-10-14').dayofyear, 65, 15, 1012]])  # Example values
today_temp = model.predict(today_features)
print(f"Predicted Temperature for Today: {today_temp[0]:.2f}°C")
