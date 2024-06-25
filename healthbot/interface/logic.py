import pandas as pd
import os
import re

# List of stop words to remove
stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'of', 'to', 'in', 'with', 'for'}

# Creating mapping diseases df
relative_path = os.path.join("databases", "diseases", "Symptom-severity.csv")
symptoms_df = pd.read_csv(relative_path)
symptoms = symptoms_df['Symptom']
mapping = {symptom: symptom.split('_') for symptom in symptoms}

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
