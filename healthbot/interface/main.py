import streamlit as st
from logic import response_generator_symptoms

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
prompt = st.chat_input("Please describe your symptoms:")

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

# Display assistant response in chat message container
#if st.session_state.message_number > 0:
#    with st.chat_message("assistant"):
#        st.markdown("**Symptoms have been generated. Please check the symptoms below.**")
#
#    # Add assistant response to chat history
#    st.session_state.messages.append({"role": "assistant", "content": "Symptoms generated and displayed below as checkboxes."})

# Display symptoms as checkboxes below the chat
if "symptoms" in st.session_state:
    st.markdown("## Confirm Your Symptoms:")
    symptoms = st.session_state.symptoms
    num_columns = min(4, len(symptoms))
    for i in range(0, len(symptoms), num_columns):
        cols = st.columns(num_columns)
        for col, symptom in zip(cols, symptoms[i:i + num_columns]):
            if symptom not in st.session_state:
                st.session_state[symptom] = True
            st.session_state[symptom] = col.checkbox(symptom, value=st.session_state[symptom])
   # st.markdown("### Add any symptoms missing:")
