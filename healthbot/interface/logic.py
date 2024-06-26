import pandas as pd
import os
import re

# List of stop words to remove
stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'of', 'to', 'in', 'with', 'for'}

# Importing symptoms df
relative_path_symptoms = os.path.join("databases", "diseases", "Symptom-severity.csv")
symptoms_df = pd.read_csv(relative_path_symptoms)
symptoms = symptoms_df['Symptom']
mapping = {symptom: symptom.split('_') for symptom in symptoms}

# Importing diseases df
relative_path_diseases = os.path.join("databases", "diseases", "dataset.csv")
diseases_df = pd.read_csv(relative_path_diseases)


def match_symptom(symptom, test_list):
    words = mapping.get(symptom, [])
    return all(word in test_list for word in words)

def response_generator_symptoms(prompt):
    # Convert the prompt to lowercase and split into words
    words = re.findall(r'\b\w+\b', prompt.lower())
    # Remove stop words
    filtered_words = [word for word in words if word not in stop_words]
    matched_symptoms = [symptom for symptom in symptoms if match_symptom(symptom, filtered_words)]
    return matched_symptoms

def check_symptoms(row, symptoms):
    row_symptoms = row.dropna().str.strip().tolist()
    return all(symptom in row_symptoms for symptom in symptoms)

def response_new_symptoms(input_symptoms):
    matched_diseases = diseases_df[diseases_df.apply(check_symptoms, symptoms=input_symptoms, axis=1)]
    symptom_columns = [f'Symptom_{i}' for i in range(1, 18)]
    all_symptoms = pd.Series(dtype='str')
    for col in symptom_columns:
        all_symptoms = pd.concat([all_symptoms, matched_diseases[col]])
    unique_symptoms = all_symptoms.dropna().str.strip().unique()
    unique_symptoms_list = unique_symptoms.tolist()
    unique_symptoms_not_in_input = list(set(unique_symptoms_list) - set(input_symptoms))
    return unique_symptoms_not_in_input
