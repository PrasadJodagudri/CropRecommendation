import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Step 1: Load the dataset
print("Loading dataset...")
df = pd.read_csv('Crop.csv')
print("Dataset loaded successfully.")

# Step 2: Prepare the data
# Features are all columns except the last one ('label')
X = df.drop('label', axis=1)
# Target is the 'label' column
y = df['label']
print("Data prepared for training.")

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into training and testing sets.")

# Step 4: Train the Random Forest Classifier model
print("Training the model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# Step 5: Save the trained model to a file
print("Saving the model as crop_model.pkl...")
with open('crop_model.pkl', 'wb') as file:
    pickle.dump(model, file)
print("Model saved successfully!")