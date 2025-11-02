import pandas as pd
import joblib
from flask import Flask, render_template, request
import numpy as np
import os

# 1. Initialize your Flask app
app = Flask(__name__)

# 2. Load your ML model and content files
print("Loading model...")
model = joblib.load('dataset/model.joblib')

print("Loading content data...")
# Load description and precaution data
descriptions = pd.read_csv('dataset/symptom_Description.csv')
precautions = pd.read_csv('dataset/symptom_precaution.csv')
medications = pd.read_csv('dataset/medications.csv')
specialists = pd.read_csv('dataset/specialists.csv')
# diets = pd.read_csv('dataset/diets.csv')

# 3. Get the list of all symptoms from Training.csv
# This list is needed to build the input vector for the model
df_train = pd.read_csv('dataset/Training.csv')
symptom_columns = df_train.drop('prognosis', axis=1).columns.tolist()


# 4. Create the Home Page Route
@app.route('/')
def home():
    # Pass the list of symptoms to your index.html template
    return render_template('index.html', symptoms=symptom_columns)

# 5. Create the Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get symptoms from the form
        # The form sends a list of symptom names that were checked
        selected_symptoms = request.form.getlist('symptoms')

        # Create the input vector (132 zeros)
        input_vector = np.zeros(len(symptom_columns))

        # Set the corresponding indices to 1 for selected symptoms
        for symptom in selected_symptoms:
            if symptom in symptom_columns:
                index = symptom_columns.index(symptom)
                input_vector[index] = 1

        # Reshape the vector to be 2D (1 row, 132 columns) for the model
        input_vector = [input_vector]

        # Make the prediction
        predicted_disease = model.predict(input_vector)[0]

        # --- Get Content for the Predicted Disease ---

        # Get Description
        try:
            desc = descriptions.loc[descriptions['Disease'] == predicted_disease, 'Description'].iloc[0]
        except:
            desc = "No description found."

        # Get Precautions (they are in 4 columns: Precaution_1, Precaution_2, etc.)
        try:
            prec_list = precautions.loc[precautions['Disease'] == predicted_disease].values[0][1:]
            # Filter out any 'nan' or empty values
            prec_list = [p for p in prec_list if pd.notna(p)]
        except:
            prec_list = ["No precautions found."]

        # Get Medications (they are in 4 columns: Medicine_1, Medicine_2, etc.)
        try:
            med_list = medications.loc[medications['Disease'] == predicted_disease].values[0][1:]
            # Filter out any 'nan' or empty values
            med_list = [m for m in med_list if pd.notna(m) and m != '']
        except:
            med_list = ["No medications found."]

        # Get Specialist recommendation
        try:
            specialist = specialists.loc[specialists['Disease'] == predicted_disease, 'Specialist'].iloc[0]
        except:
            specialist = "General Physician"

        # Pass all the information to the result.html template
        return render_template('result.html',
                               disease=predicted_disease,
                               description=desc,
                               precautions=prec_list,
                               medications=med_list,
                               specialist=specialist
                              )

# 6. Run the app
if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)