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
model = DecisionTreeClassifier()

# Train the model on your data
model.fit(X, y)

# 4. Save the Trained Model
print("Saving the model as 'dataset/model.joblib'...")
# Save the model to a file
joblib.dump(model, 'dataset/model.joblib')

print("\nModel trained and saved successfully!")
print("Your next step is to build the Flask app.")