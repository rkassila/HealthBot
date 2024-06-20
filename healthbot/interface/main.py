import streamlit as st
from logic import response_generator_symptoms

MAX_COL = 5

st.title("HealthBot")

# Initialize chat history and message number
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Start the conversation with the first assistant response
    first_response = "Could you please tell me about your symptoms today?"
    st.session_state.messages.append({"role": "assistant", "content": first_response})
    st.session_state.message_number = 0

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input with a clear prompt
prompt = st.chat_input("Please type here:")

# Display user input and generate response if prompt is provided
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.message_number += 1

    # Generate symptoms
    symptoms = response_generator_symptoms(prompt)
    # Store symptoms in session state
    st.session_state.symptoms = symptoms

# Initialize radio buttons state in session_state
if "symptoms" in st.session_state:
    symptoms = st.session_state.symptoms
    for symptom in symptoms:
        scale_key = f"{symptom}_scale"
        if scale_key not in st.session_state:
            st.session_state[scale_key] = 0

scaled_symptoms = {}

# Display symptoms as radio buttons below the chat
if "symptoms" in st.session_state:
    st.markdown("### Evaluate and confirm your symptoms:")
    symptoms = st.session_state.symptoms
    num_columns = min(MAX_COL, len(symptoms))
    for i in range(0, len(symptoms), num_columns):
        cols = st.columns(num_columns)
        for col, symptom in zip(cols, symptoms[i:i + num_columns]):
            scale_key = f"{symptom}_scale"
            # Create radio buttons with a unique key
            scaled_symptoms[symptom] = col.radio(
                f"Severity for {symptom}",
                options=list(range(5)),
                index=st.session_state[scale_key],
                key=scale_key,
            )
    # Add a confirm button
    if st.button("Confirm"):
        st.markdown("### Symptom Severities")
        # Create a single-row layout for the outputs
        cols = st.columns(len(scaled_symptoms))
        for col, (symptom, severity) in zip(cols, scaled_symptoms.items()):
            col.markdown(f"**{symptom}:** {severity}")


# Ask for history and current treatments
    ###TO CODE

# Send to API for diseases prediction
# Other symptoms (predicted) displayed for confirmation

# Send to API for corrected diseases prediction

# Generate file (with every symptom and best x predictions)

# File displayed and thanks
