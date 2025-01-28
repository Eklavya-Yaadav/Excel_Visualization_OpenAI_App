{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "6d364bc8-121a-40da-929b-da7ee6c7b8cf",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-01-28 14:33:20.346 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.350 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.353 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.356 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.360 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.362 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.364 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.367 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.369 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.372 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.374 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.378 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-01-28 14:33:20.379 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator(_root_container=1, _parent=DeltaGenerator())"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import openai\n",
    "\n",
    "# Streamlit App Title\n",
    "st.title(\"Excel Data Visualization App\")\n",
    "\n",
    "# Upload Excel File\n",
    "uploaded_file = st.file_uploader(\"Upload an Excel file\", type=[\"xlsx\"])\n",
    "\n",
    "if uploaded_file is not None:\n",
    "    # Load the Excel file into a DataFrame\n",
    "    try:\n",
    "        df = pd.read_excel(uploaded_file)\n",
    "        st.success(\"File uploaded successfully!\")\n",
    "\n",
    "        # Display the DataFrame\n",
    "        st.subheader(\"Uploaded Data\")\n",
    "        st.dataframe(df)\n",
    "\n",
    "        # Select columns to visualize\n",
    "        columns = df.columns\n",
    "        selected_columns = st.multiselect(\"Select columns for visualization\", columns)\n",
    "\n",
    "        if selected_columns:\n",
    "            st.subheader(\"Selected Data\")\n",
    "            st.dataframe(df[selected_columns])\n",
    "\n",
    "            # Plot data\n",
    "            chart_type = st.selectbox(\"Choose a chart type\", [\"Line Chart\", \"Bar Chart\", \"Area Chart\"])\n",
    "\n",
    "            if chart_type == \"Line Chart\":\n",
    "                st.line_chart(df[selected_columns])\n",
    "            elif chart_type == \"Bar Chart\":\n",
    "                st.bar_chart(df[selected_columns])\n",
    "            elif chart_type == \"Area Chart\":\n",
    "                st.area_chart(df[selected_columns])\n",
    "\n",
    "        # OpenAI Integration\n",
    "        st.subheader(\"Generate Insights with OpenAI\")\n",
    "        openai_api_key = st.text_input(\"Enter your OpenAI API key\", type=\"password\")\n",
    "\n",
    "        if openai_api_key:\n",
    "            openai.api_key = openai_api_key\n",
    "            query = st.text_area(\"Ask a question about the data\")\n",
    "\n",
    "            if st.button(\"Get Insights\"):\n",
    "                # Generate prompt using the dataset\n",
    "                prompt = f\"Analyze the following data and answer the question:\\n\\n{df.head(10).to_string()}\\n\\nQuestion: {query}\"\n",
    "\n",
    "                try:\n",
    "                    response = openai.Completion.create(\n",
    "                        engine=\"text-davinci-003\",\n",
    "                        prompt=prompt,\n",
    "                        max_tokens=150\n",
    "                    )\n",
    "                    st.subheader(\"OpenAI Response\")\n",
    "                    st.write(response.choices[0].text.strip())\n",
    "                except Exception as e:\n",
    "                    st.error(f\"Error: {e}\")\n",
    "\n",
    "    except Exception as e:\n",
    "        st.error(f\"Error reading the file: {e}\")\n",
    "else:\n",
    "    st.info(\"Please upload an Excel file to get started.\")\n",
    "\n",
    "# Instructions\n",
    "st.sidebar.title(\"Instructions\")\n",
    "st.sidebar.info(\n",
    "    \"1. Upload an Excel file.\\n\"\n",
    "    \"2. Select columns for visualization.\\n\"\n",
    "    \"3. Choose a chart type to view the data.\\n\"\n",
    "    \"4. Use OpenAI to ask questions or gain insights.\"\n",
    ")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
