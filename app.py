import streamlit as st
import pandas as pd
import openai

# Function to load data from Excel or CSV
def load_data(file):
    if file is not None:
        try:
            if file.name.endswith(".xlsx"):
                return pd.read_excel(file)
            elif file.name.endswith(".csv"):
                return pd.read_csv(file)
            else:
                st.error("Invalid file format. Please upload an Excel or CSV file.")
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    return None

# Function to generate visualization code
def generate_visualization_code(df, api_key, user_prompt):
    try:
        openai.api_key = api_key

        # Convert dataframe to string to send to OpenAI
        data_str = df.head().to_string()

        # Create prompt for OpenAI to generate visualization code
        prompt = f"""
        Here is a preview of some data:
        {data_str}

        User requested the following:
        {user_prompt}

        Generate Python code using Plotly or Matplotlib to visualize this data based on the user's request.
        """
        
        # Call the OpenAI API using the correct method
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-4" or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes Python code for data visualization."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.5,
        )

        visualization_code = response['choices'][0]['message']['content'].strip()
        return visualization_code
    except Exception as e:
        st.error(f"Error generating code: {e}")
        return None

# Function to execute the generated visualization code
def execute_visualization_code(visualization_code):
    try:
        exec(visualization_code)
    except Exception as e:
        st.error(f"Error executing the code: {e}")

# Streamlit UI
st.title("AI-Powered Data Visualization App")
st.write("Upload an Excel or CSV file, provide your OpenAI API key, enter a prompt, and let AI generate a visualization.")

# File uploader for data input
uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

# Load the data
df = load_data(uploaded_file)

# API key input
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# User prompt input
user_prompt = st.text_input("Enter your visualization or data analysis prompt")

if df is not None:
    st.write("### Data Preview", df.head())

    if api_key and user_prompt:
        st.write("Generating visualization...")

        # Generate the code using OpenAI
        visualization_code = generate_visualization_code(df, api_key, user_prompt)
        
        if visualization_code:
            st.code(visualization_code, language='python')

            # Execute the generated code
            execute_visualization_code(visualization_code)
        else:
            st.error("Failed to generate visualization code.")
    else:
        st.write("Please enter your OpenAI API key and a prompt to proceed.")
