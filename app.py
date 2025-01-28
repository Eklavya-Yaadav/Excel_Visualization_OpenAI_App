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

# Function to generate code or perform actions using OpenAI
def process_data_with_openai(df, api_key, user_prompt):
    try:
        openai.api_key = api_key

        # Convert a preview of the dataframe to a string to include in the prompt
        data_preview = df.head().to_string()

        # Create prompt for OpenAI
        prompt = f"""
        Here is a preview of the data:
        {data_preview}

        Based on the following user request:
        {user_prompt}

        Generate Python code or provide the required information to fulfill the request.
        """

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Change model if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant that works with data Analyst and Python code."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=700,
            temperature=0.5,
        )

        # Extract the response content
        output = response['choices'][0]['message']['content'].strip()
        return output
    except Exception as e:
        st.error(f"Error processing request: {e}")
        return None

# Streamlit UI
st.title("AI-Powered Data Assistant App")
st.write("Upload an Excel or CSV file, provide your OpenAI API key, enter a prompt, and let AI assist with your request.")

# File uploader for data input
uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

# Load the data
df = load_data(uploaded_file)

# API key input
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# User prompt input
user_prompt = st.text_area("Enter your request (e.g., data analysis, visualization, summary, etc.)")

if df is not None:
    st.write("### Data Preview", df.head())

    if api_key and user_prompt:
        st.write("Processing your request...")

        # Process the request using OpenAI
        output = process_data_with_openai(df, api_key, user_prompt)
        
        if output:
            st.write("### AI Response")
            st.code(output, language='python' if 'import' in output else None)

            # Execute Python code if applicable
            if "import" in output:  # Check if the response is Python code
                try:
                    exec(output)
                except Exception as e:
                    st.error(f"Error executing the code: {e}")
        else:
            st.error("Failed to process your request.")
    else:
        st.write("Please enter your OpenAI API key and a prompt to proceed.")
