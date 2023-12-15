import streamlit as st
import pandas as pd
import numpy as np

def app():
    st.title('Data Cleaning ')
    st.write('Welcome to Data cleaning page')

    st.markdown("### Sample Data")

    # Read your data into a pandas DataFrame
    try:
        clean_data = pd.read_csv('../data/clean_data.csv')
    except BaseException:
        logging.error('either file not found or wrong format')
        
    st.write(df)