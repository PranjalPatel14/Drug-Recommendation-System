import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib # Used to save your model

print("Loading training data...")
df = pd.read_csv("dataset/Training.csv")

print("Separating features and target...")
y = df['prognosis']


X = df.drop('prognosis', axis=1)

# 3. Create and Train the Model
print("Training the Decision Tree model...")
model = DecisionTreeClassifier(random_state=42)

model.fit(X, y)

from sklearn.metrics import accuracy_score
predictions = model.predict(X)
accuracy = accuracy_score(y, predictions)
print(f"Training accuracy: {accuracy*100:.2f}%")

print("\nVerifying predictions on sample cases:")
sample_indices = [0, 100, 200, 500, 1000]
for idx in sample_indices:
    actual = y.iloc[idx]
    predicted = predictions[idx]
    match = "OK" if actual == predicted else "FAIL"
    print(f"  Row {idx}: Actual={actual}, Predicted={predicted} [{match}]")

print("Saving the model as 'dataset/model.joblib'...")
joblib.dump(model, 'dataset/model.joblib')

print("\nModel trained and saved successfully!")
print("Your next step is to build the Flask app.")