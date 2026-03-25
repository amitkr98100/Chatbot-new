import streamlit as st
from chatbot.logic import generate_response
from chatbot.data_loader import load_data_from_files

st.title("💬 Local Neo4j QA Chatbot")

# File uploader
json_file = st.file_uploader("Upload JSON file", type=["json"])
yaml_file = st.file_uploader("Upload YAML file", type=["yaml","yml"])

if st.button("Load Questions"):
    load_data_from_files(json_file, yaml_file)

user_input = st.text_input("Ask me something:")

if user_input:
    try:
        response = generate_response(user_input)
        st.write(response)
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")