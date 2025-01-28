import pandas as pd
import openai
import streamlit as st

# OpenAI API key
openai.api_key = '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'

# Function to load the file
def load_file(file_path):
    try:
        # Check the file extension and load accordingly
        if file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
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

    # Extract OpenAI's interpretation of the user's request
    action = response.choices[0].text.strip()
    st.write(f"OpenAI's interpretation: {action}")
    
    # Return OpenAI's action to the user
    return action

# Streamlit UI
st.title('Data Analysis Assistant')

# File upload
uploaded_file = st.file_uploader("Choose an Excel (.xlsx) or CSV file", type=['xlsx', 'csv'])

if uploaded_file is not None:
    # Load the file
    file_data = load_file(uploaded_file)
    
    if file_data is not None:
        # Display the first few rows of the data
        st.write("Dataset Preview:")
        st.dataframe(file_data.head())
        
        # Get user prompt for analysis or chart
        user_prompt = st.text_input("Enter a prompt for analysis or chart (e.g., 'Generate a bar chart for 'age', 'Create a histogram for 'salary'):")

        if user_prompt:
            # Generate and show response from OpenAI
            response = generate_plot(file_data, user_prompt)
            st.write(f"Response from OpenAI: {response}")

# Run the app
if __name__ == "__main__":
    st.write("Interactive data analysis using OpenAI's language model.")
