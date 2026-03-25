import streamlit as st
from chatbot.logic import generate_response
from chatbot.data_loader import load_data_from_files  # correct import

st.title("💬 Local Neo4j QA Chatbot")

# Load seed data first time
load_data_from_files()  # <- yahi correct function call hai

# User input box
user_input = st.text_input("Ask me something:")

if user_input:
    try:
        response = generate_response(user_input)
        st.write(response)
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")