import time
import re

# List of stop words to remove
stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'of', 'to', 'in', 'with', 'for'}

# Streamed response emulator
def response_generator_symptoms(prompt):
    # Convert the prompt to lowercase and split into words
    words = re.findall(r'\b\w+\b', prompt.lower())
    # Remove stop words
    filtered_words = [word for word in words if word not in stop_words]

    return filtered_words

    # Join the filtered words into a cleaned sentence
    #cleaned_sentence = ' '.join(filtered_words)

    #yield "Symptoms:"

    #for word in cleaned_sentence.split():
    #    yield word + " "
    #    time.sleep(0.05)
