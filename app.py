import streamlit as st
import pandas as pd
import openai

# Streamlit App Title
st.title("Excel Data Visualization App")

# Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the Excel file into a DataFrame
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # Display the DataFrame
        st.subheader("Uploaded Data")
        st.dataframe(df)

        # Select columns to visualize
        columns = df.columns
        selected_columns = st.multiselect("Select columns for visualization", columns)

        if selected_columns:
            st.subheader("Selected Data")
            st.dataframe(df[selected_columns])

            # Plot data
            chart_type = st.selectbox("Choose a chart type", ["Line Chart", "Bar Chart", "Area Chart"])

            if chart_type == "Line Chart":
                st.line_chart(df[selected_columns])
            elif chart_type == "Bar Chart":
                st.bar_chart(df[selected_columns])
            elif chart_type == "Area Chart":
                st.area_chart(df[selected_columns])

        # OpenAI Integration
        st.subheader("Generate Insights with OpenAI")
        openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

        if openai_api_key:
            openai.api_key = openai_api_key
            query = st.text_area("Ask a question about the data")

            if st.button("Get Insights"):
                # Generate prompt using the dataset
                prompt = f"Analyze the following data and answer the question:\n\n{df.head(10).to_string()}\n\nQuestion: {query}"

                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=150
                    )
                    st.subheader("OpenAI Response")
                    st.write(response.choices[0].text.strip())
                except Exception as e:
                    st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info("Please upload an Excel file to get started.")

# Instructions
st.sidebar.title("Instructions")
st.sidebar.info(
    "1. Upload an Excel file.\n"
    "2. Select columns for visualization.\n"
    "3. Choose a chart type to view the data.\n"
    "4. Use OpenAI to ask questions or gain insights."
)