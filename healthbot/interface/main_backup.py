import streamlit as st
from logic import response_generator_symptoms, response_new_symptoms  # To be replaced by symptoms detector

MAX_COL = 5

# Create two columns for the title and the reload button
col1, col2 = st.columns([4, 1])

with col1:
    st.title("HealthBot")

with col2:
    # Reload button to reset the app
    if st.button("Reload app"):
        st.session_state.clear()
        st.rerun()

# Initialize chat history and phase state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Could you please tell me about your symptoms today?"})
    st.session_state.phase = 1
    st.session_state.confirm_clicked = False
    st.session_state.scaled_symptoms = {}

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Phase 1: Ask for symptoms, scale, and confirm
if st.session_state.phase == 1:
    prompt = st.chat_input("Please type here", key="initial_input")

    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate symptoms
        symptoms = response_generator_symptoms(prompt)
        # Store symptoms in session state
        st.session_state.symptoms = symptoms

    if "symptoms" in st.session_state and st.session_state.symptoms:
        st.markdown("### Evaluate and confirm your symptoms:")
        num_columns = min(MAX_COL, len(st.session_state.symptoms))
        for i in range(0, len(st.session_state.symptoms), num_columns):
            cols = st.columns(num_columns)
            for col, symptom in zip(cols, st.session_state.symptoms[i:i + num_columns]):
                scale_key = f"{symptom}_scale"
                if scale_key not in st.session_state:
                    st.session_state[scale_key] = 0
                st.session_state.scaled_symptoms[symptom] = col.radio(
                    f"Severity for {symptom}",
                    options=list(range(5)),
                    index=st.session_state[scale_key],
                    key=scale_key,
                )

        if st.button("Confirm Symptoms"):
            st.session_state.confirm_clicked = True
            st.rerun()

    if st.session_state.confirm_clicked:
        cols = st.columns(len(st.session_state.symptoms))
        symptom_severity_message = ""
        for col, symptom in zip(cols, st.session_state.symptoms):
            severity = st.session_state[f"{symptom}_scale"]
            if severity != 0:
                # col.markdown(f"**{symptom}:** {severity}")
                symptom_severity_message += f"**{symptom}:** {severity}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

        st.session_state.messages.append({"role": "assistant", "content": symptom_severity_message})

        # Move to Phase 2
        st.session_state.messages.append({"role": "assistant", "content": "Please describe any current treatments and relevant health history"})
        st.session_state.phase = 2
        st.session_state.confirm_clicked = False
        st.rerun()

# Phase 2: Describe treatments and history
if st.session_state.phase == 2:
    prompt = st.chat_input("Please describe your treatments and history here", key="next_prompt_input")

    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Response
        roger_response = "Sending your informations for analysis..."
        st.session_state.messages.append({"role": "assistant", "content": roger_response})
        st.chat_message("assistant").markdown(roger_response)

        # Move to Phase 3
        st.session_state.phase = 3
        st.rerun()

# Phase 3: Other symptoms displayed for confirmation
if st.session_state.phase == 3:

    # Send to API for diseases prediction (TO DO)
    new_symptoms_list = response_new_symptoms(st.session_state.symptoms)
    st.session_state.new_scaled_symptoms = {}

    if "new_symptoms" not in st.session_state:
        st.session_state.new_symptoms = new_symptoms_list

    if not st.session_state.new_symptoms:
        st.markdown("### Click confirm please")
    else:
        st.markdown("### Have you been experiencing the following symptoms:")
        num_columns = min(MAX_COL, len(st.session_state.new_symptoms))
        for i in range(0, len(st.session_state.new_symptoms), num_columns):
            cols = st.columns(num_columns)
            for col, symptom in zip(cols, st.session_state.new_symptoms[i:i + num_columns]):
                scale_key = f"new_{symptom}_scale"
                if scale_key not in st.session_state:
                    st.session_state[scale_key] = 0
                st.session_state.new_scaled_symptoms[symptom] = col.radio(
                    f"Severity for {symptom}",
                    options=list(range(5)),
                    index=st.session_state[scale_key],
                    key=scale_key,
                )

    if st.button("Confirm"):
        st.session_state.confirm_clicked = True
        st.rerun()

    if st.session_state.confirm_clicked:
        new_symptom_severity_message = ""
        if st.session_state.new_symptoms:
            cols = st.columns(len(st.session_state.new_symptoms))
            for col, symptom in zip(cols, st.session_state.new_symptoms):
                severity = st.session_state[f"new_{symptom}_scale"]
                if severity != 0:
                    new_symptom_severity_message += f"**{symptom}:** {severity}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

        if new_symptom_severity_message:
            st.session_state.messages.append({"role": "assistant", "content": new_symptom_severity_message})

        # Send to API for corrected diseases prediction
        # Generate file (with every symptom and best x predictions)
        # File displayed and thanks
        st.session_state.messages.append({"role": "assistant", "content": "Thank you for your input!"})
        st.session_state.phase = 4
        st.rerun()


# Send to API for corrected diseases prediction
# TO CODE

# Generate file (with every symptom and best x predictions)
# TO CODE

# File displayed and thanks
# TO CODE
