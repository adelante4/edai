import time

import streamlit as st
import ast
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from src.data.models.api_models import RequestAPIObject
from src.edai.edai import Edai
from src.utils import load_dataframe

st.title('EDAI')
st.write('Welcome to EDAI! This is a tool that performs Exploratory Data Analysis (EDA) on your dataset. '
         'Please upload a pickle file containing your dataset to get started.')


# Upload the file
uploaded_file = st.file_uploader("Choose a file", type=["pkl", "csv", "xls", "xlsx", "json"])
api_key = st.text_input('Groq API Key', '')
model_name = st.text_input('Model Name', 'llama3-70b-8192')
dataset_description = st.text_area('Dataset Description', '')
columns_description = st.text_area('Columns Description', 'A dictionary with the keys as column names and values as '
                                                          'their description. You can also not provide a column.')

if st.button('Analyse'):
    if not api_key or not model_name or not dataset_description or not columns_description:
        st.error("Please fill in all the inputs before proceeding.")
    elif uploaded_file is None:
        st.error("Please upload a file before proceeding.")
    placeholder = st.empty()
    progress_bar = st.progress(0)

    df = load_dataframe(uploaded_file)
    if df is not None:

        for i in range(5):
            placeholder.text(f"🔬 Doing Science...{'🧪' * (i % 5)}")
            time.sleep(0.5)

        Settings.llm = Groq(model=model_name, api_key=api_key)

        edai = Edai(RequestAPIObject(df=df, filename=uploaded_file.name,
                                     data_desc=dataset_description,
                                     progress_bar=progress_bar,
                                     column_desc=ast.literal_eval(columns_description),
                                     groq_model_name=model_name, groq_api_key=api_key))
        edai.eda()

        with open('edai_notebook.ipynb', 'rb') as f:
            st.download_button('Download Jupyter Notebook', f, file_name='edai_notebook.ipynb')
