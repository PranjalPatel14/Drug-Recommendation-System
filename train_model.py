import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib # Used to save your model

# 1. Load your training data
print("Loading training data...")
df = pd.read_csv("dataset/Training.csv")

# 2. Separate Features (X) and Target (y)
print("Separating features and target...")
# 'prognosis' is the column you want to predict (the disease)
y = df['prognosis']

# All other columns are the symptoms (features)
# We drop 'prognosis' to create our feature set X
X = df.drop('prognosis', axis=1)

# 3. Create and Train the Model
print("Training the Decision Tree model...")
# Initialize the Decision Tree Classifier
# Removing restrictive parameters to allow the tree to learn properly
# Using default settings which work well for this dataset
model = DecisionTreeClassifier(random_state=42)

# Train the model on your data
model.fit(X, y)

# Check model accuracy on training data (for verification)
from sklearn.metrics import accuracy_score
predictions = model.predict(X)
accuracy = accuracy_score(y, predictions)
print(f"Training accuracy: {accuracy*100:.2f}%")

# Verify predictions on sample cases
print("\nVerifying predictions on sample cases:")
sample_indices = [0, 100, 200, 500, 1000]
for idx in sample_indices:
    actual = y.iloc[idx]
    predicted = predictions[idx]
    match = "OK" if actual == predicted else "FAIL"
    print(f"  Row {idx}: Actual={actual}, Predicted={predicted} [{match}]")

# 4. Save the Trained Model
print("Saving the model as 'dataset/model.joblib'...")
# Save the model to a file
joblib.dump(model, 'dataset/model.joblib')

print("\nModel trained and saved successfully!")
print("Your next step is to build the Flask app.")