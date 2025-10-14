import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.title("FloatChat 🌊")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to know about ARGO floats?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call backend API
    try:
        response = requests.post(
            "http://backend:8000/api/chat",
            json={"session_id": "123", "message": prompt}
        )
        response.raise_for_status()
        data = response.json()

        llm_response = data.get("llm_response", "Sorry, I couldn't process that.")
        provenance = data.get("provenance", [])

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(llm_response)
            if provenance:
                st.write("**Retrieved Profiles:**")
                st.json(provenance)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response})

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
