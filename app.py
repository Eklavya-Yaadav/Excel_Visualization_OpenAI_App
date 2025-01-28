import pandas as pd
import openai
import streamlit as st

# OpenAI API key
openai.api_key = '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'

# Function to load the file
def load_file(uploaded_file):
    try:
        # Get the file extension from the file name
        file_name = uploaded_file.name
        if file_name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        elif file_name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            raise ValueError("File format not supported. Please use .xlsx or .csv.")
        
        st.success("File loaded successfully!")
        return data
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to generate plot or analysis based on the user's prompt
def generate_plot(data, prompt):
    # Query OpenAI to interpret the user's request and suggest a solution
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given the following data structure, interpret the user's request and suggest how to visualize or analyze it.\n\nData columns: {', '.join(data.columns)}\nUser request: {prompt}",
        max_tokens=200
    )

    # Extract Open
