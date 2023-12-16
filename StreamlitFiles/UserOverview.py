import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from Scripts import dataLoader

def app():
    st.title('User Overview')

    st.write("### User Overview analysis") 
    st.write("- identifying the top 10 handsets used by the customers")
    st.write("- identify the top 3 handset manufacturers")
    st.write("- identify the top 5 handsets per top 3 handset manufacturer")

    # Read your data into a pandas DataFrame
    df = dataLoader.clean_data_loader()
    st.write(df)
    df.dropna()
    
    
    col1, col2 = st.columns(2)
    with col1:
        # top 10 handsets used by the customers
        top_handsets = df['Handset Type'].value_counts().head(10)
        fig, ax = plt.subplots()
        top_handsets.plot(kind='bar', color=['teal', 'green', 'blue', 'purple', 'pink'], ax=ax)
        ax.set_ylabel('Count')
        ax.set_xlabel('Handset Type')
        ax.set_title('Top 10 Handset Types')
        st.pyplot(fig)
    with col2:
        # top 3 handset manufacturers
        top_manufacturers = df['Handset Manufacturer'].value_counts().head(3)
        fig, ax = plt.subplots()
        top_manufacturers.plot(kind='bar', color=['green', 'blue', 'purple'], ax=ax)
        ax.set_ylabel('Count')
        ax.set_xlabel('Handset Manufacturer')
        ax.set_title('Top 3 Handset Manufacturers')
        st.pyplot(fig)

    # top 5 handsets per top 3 handset manufacturer
    st.write("#### top 5 handsets per top 3 handset manufacturer ")
    handset_man = df[df['Handset Manufacturer'].isin(['Apple', 'Samsung', 'Huawei'])]
    handset = handset_man.groupby('Handset Manufacturer')['Handset Type'].value_counts()
    apple = handset['Apple'][:5]
    samsung = handset['Samsung'][:5]
    huawei = handset['Huawei'][:5]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Apple')
        fig, ax = plt.subplots()
        ax.bar(apple.keys(), apple.values, tick_label=apple.keys(), width=.5, color=['blue', 'green', 'orange'])
        ax.tick_params(axis='x', labelrotation=90)
        st.pyplot(fig)

    with col2:
        st.subheader('Samsung')
        fig, ax = plt.subplots()
        ax.bar(samsung.keys(), samsung.values, tick_label=samsung.keys(), width=0.8, color=['blue', 'green', 'orange'])
        ax.tick_params(axis='x', labelrotation=90)
        st.pyplot(fig)

    with col3:
        st.subheader('Huawei')
        fig, ax = plt.subplots()
        ax.bar(huawei.keys(), huawei.values, tick_label=huawei.keys(), width=0.8, color=['blue', 'green', 'orange'])
        ax.tick_params(axis='x', labelrotation=90)
        st.pyplot(fig)

    # mean, median, mode, min, max
    central_tendency_measure = pd.DataFrame(
    { 
     'mean': df.mean(numeric_only=True).values, 
     'median': df.median(numeric_only=True).values,
     'mode': df.mode(numeric_only=True).rename(columns={0: "mode"}).iloc[0].values,
     'min': df.min(numeric_only=True).values,
     'max': df.max(numeric_only=True).values
    }, index=df.select_dtypes(include=np.number).columns.tolist())
    st.write("#### mean, median, mode, min, max")
    st.write(central_tendency_measure)


    
    # plot histogram function
    def plot_hist(data, column, color):
        fig, ax = plt.subplots()
        data[column].plot(kind='hist', color=color, edgecolor='black', ax=ax)
        ax.set_title(f'Histogram of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
    # Scatter plot function
    def scatter_plot(data):
        fig, ax = plt.subplots()
        sns.scatterplot(x='Avg Bearer TP DL (kbps)', y='Avg Bearer TP UL (kbps)', data=data, ax=ax)
        ax.set_title('Scatter Plot')
        ax.set_xlabel('Avg Bearer TP DL (kbps)')
        ax.set_ylabel('Avg Bearer TP UL (kbps)')
        st.pyplot(fig)

    # Distribution
    st.write("#### Distributions ")
    col1, col2 = st.columns(2)

    with col1:
        # Plot histogram for "Total DL (Bytes)" column
        plot_hist(df, "Total DL (Bytes)", "blue")
    with col2:
        # # Plot histogram for "Total uL (Bytes)" column
        plot_hist(df, "Total UL (Bytes)", "green")

    scatter_plot(df)

    # Select numeric columns
    numeric_df = df.select_dtypes(include=['int64', 'float64'])

    # Compute correlation matrix
    correlation_matrix = numeric_df.corr()

    # Streamlit app
    st.write("#### Correlation Matrix Heatmap in Streamlit")

    # Plot correlation matrix heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
    st.write("#### Correlation Matrix Heatmap")
    st.pyplot(fig)


    df['Dur. (s)'] = df['Dur. (ms)'] / 1000
    user_summary = df.groupby('MSISDN/Number').agg({
        'Dur. (s)': 'sum',
        'Total DL (Bytes)': 'sum',
        'Total UL (Bytes)': 'sum'
    }).reset_index()

    # Compute deciles based on total duration
    user_summary['Duration Decile'] = pd.qcut(user_summary['Dur. (s)'], q=[0, 0.2, 0.4, 0.6, 0.8, 1], labels=False)

    # Group by decile class and calculate total data for each decile
    decile_summary = user_summary.groupby('Duration Decile').agg({
        'Total DL (Bytes)': 'sum',
        'Total UL (Bytes)': 'sum'
    }).reset_index()

    # Create Streamlit app
    st.write('#### Total Data (DL+UL) per Decile Class')

    # Display the decile_summary DataFrame
    st.write(decile_summary)

    # Create and display the bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Duration Decile', y='Total DL (Bytes)', data=decile_summary, label='DL')
    sns.barplot(x='Duration Decile', y='Total UL (Bytes)', data=decile_summary, label='UL', color='orange')
    plt.xlabel('Duration Decile')
    plt.ylabel('Total Data (Bytes)')
    plt.title('Total Data (DL+UL) per Decile Class')
    plt.legend()
    st.pyplot(plt)  # Display the plot using st.pyplot

