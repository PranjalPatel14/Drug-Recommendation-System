import pandas as pd
import joblib
from flask import Flask, render_template, request
import numpy as np
import os

app = Flask(__name__)

print("Loading model...")
model = joblib.load('dataset/model.joblib')

print("Loading content data...")
descriptions = pd.read_csv('dataset/symptom_Description.csv')
precautions = pd.read_csv('dataset/symptom_precaution.csv')
medications = pd.read_csv('dataset/medications.csv')
specialists = pd.read_csv('dataset/specialists.csv')

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
        selected_symptoms = request.form.getlist('symptoms')
        
        if not selected_symptoms:
            return render_template('result.html',
                                   disease="Error",
                                   description="Please select at least one symptom to get a prediction.",
                                   precautions=[],
                                   medications=[],
                                   specialist="General Physician")

        input_vector = np.zeros(len(symptom_columns))

        matched_symptoms = []
        for symptom in selected_symptoms:
            if symptom in symptom_columns:
                index = symptom_columns.index(symptom)
                input_vector[index] = 1
                matched_symptoms.append(symptom)
        
        if len(matched_symptoms) == 0:
            return render_template('result.html',
                                   disease="Error",
                                   description="No valid symptoms were found. Please select symptoms from the list.",
                                   precautions=[],
                                   medications=[],
                                   specialist="General Physician")

        input_df = pd.DataFrame([input_vector], columns=symptom_columns)

        predicted_disease = model.predict(input_df)[0]
        
        probabilities = model.predict_proba(input_df)[0]
        disease_classes = model.classes_
        
        predicted_row = df_train[df_train['prognosis'] == predicted_disease]
        is_valid = False
        if len(predicted_row) > 0:
            # Check if any case of this disease has all selected symptoms
            for idx, row in predicted_row.iterrows():
                symptom_values = row[symptom_columns].values
                if np.array_equal((symptom_values > 0), (input_vector > 0)):
                    is_valid = True
                    break
        
        if not is_valid:
            top_predictions = sorted(zip(probabilities, disease_classes), reverse=True)
            
            for prob, disease in top_predictions:
                disease_rows = df_train[df_train['prognosis'] == disease]
                for idx, row in disease_rows.iterrows():
                    row_symptoms = row[symptom_columns].values
                    if any((row_symptoms > 0) & (input_vector > 0)):
                        predicted_disease = disease
                        is_valid = True
                        break
                if is_valid:
                    break
        
        print(f"Selected symptoms: {matched_symptoms[:5]}...")  # Print first 5
        print(f"Predicted disease: {predicted_disease}")
        print(f"Prediction valid: {is_valid}")


        try:
            desc = descriptions.loc[descriptions['Disease'] == predicted_disease, 'Description'].iloc[0]
        except:
            desc = "No description found."

        try:
            prec_list = precautions.loc[precautions['Disease'] == predicted_disease].values[0][1:]
            prec_list = [p for p in prec_list if pd.notna(p)]
        except:
            prec_list = ["No precautions found."]

        try:
            med_list = medications.loc[medications['Disease'] == predicted_disease].values[0][1:]
            med_list = [m for m in med_list if pd.notna(m) and m != '']
        except:
            med_list = ["No medications found."]

        try:
            specialist = specialists.loc[specialists['Disease'] == predicted_disease, 'Specialist'].iloc[0]
        except:
            specialist = "General Physician"

        return render_template('result.html',
                               disease=predicted_disease,
                               description=desc,
                               precautions=prec_list,
                               medications=med_list,
                               specialist=specialist
                              )

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)