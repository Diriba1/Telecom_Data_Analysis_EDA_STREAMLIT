import streamlit as st
import pandas as pd
import numpy as np
from Scripts import dataLoader

def app():
    st.title('Data Cleaning ')
    st.write('Welcome to Data cleaning page')

    st.markdown("### Given Sample Data with out any cleaning ")

    # Read your data into a pandas DataFrame
    df = dataLoader.load_from_db()
    st.write(df)
    
    #print concise summarry of data frame
    st.markdown("#### Print concise summary of a dataframe")

    col1, col2 = st.columns([1, 3])
    with col1:   
        st.write(df.dtypes)
        st.write(df.shape)
    with col2: 
        st.write(df.describe())

    st.write("The data has 55 columns and 150001 rows with 50 of the columns data types are float and the rest 5 are object data type.")


    # data cleaning
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Data Cleaning")
        st.markdown("Missing values in percentage")
        missing_percentage = (df.isnull().mean() * 100).round(2)
        missing_df = pd.DataFrame({'Column': missing_percentage.index, 'Missing Percentage': missing_percentage.values})
        st.write(missing_df)
    with col2:
        st.markdown("#### Columns to be dropped")
        st.markdown("Identifying and dropping the columns, with missing values greater than 25%")
        columns_to_drop = list(missing_df[missing_df["Missing Percentage"]>=25].Column.values)
        df = df.drop(columns_to_drop, axis=1)
        st.write(columns_to_drop)
        st.write("In addition to dropping missing values of 25%, we are have to drop the raw because it is a total row, and change the data type of 'IMEI', 'IMSI', 'MSISDN/Number' to string data type. ")
        st.write("Then identify and populate float data type columns with mean values and string data types with mode value")
    
    # List of columns to convert to string
    columns_to_convert = ['IMEI', 'IMSI', 'MSISDN/Number']

    # Convert selected columns to string data type
    df[columns_to_convert] = df[columns_to_convert].astype(str)
    # Drop the last row 
    df.drop(df.index[-1], inplace=True)

    # Identify float-type columns
    float_columns = df.select_dtypes(include='float').columns

    # Populate float-type columns with mean value
    df[float_columns] = df[float_columns].fillna(df[float_columns].mean())
    st.write("The data shape is now: ", df.shape)
    
    st.write(df)
    st.write("#### Saving the cleaned data to CSV file for easy access and further processes")

    

    