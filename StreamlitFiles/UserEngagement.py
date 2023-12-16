import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from Scripts import dataLoader

def app():
    st.title('User Engagement')
    st.write('Welcome to User Engagement Page The Dataframe we are working on Lookslike This')


    # Read your data into a pandas DataFrame
    df = dataLoader.clean_data_loader()
    st.write(df)
    df.dropna()

    # Calculate the number of sessions per user
    session_frequency = df.groupby('MSISDN/Number')['Bearer Id'].count().reset_index()
    session_frequency.columns = ['MSISDN/Number', 'Sessions Frequency']
    

    # Calculate the total session duration per user
    session_duration = df.groupby('MSISDN/Number')['Dur. (ms)'].sum().reset_index()
    session_duration.columns = ['MSISDN/Number', 'Total Session Duration (ms)']
    session_duration['Total Session Duration (s)'] = session_duration['Total Session Duration (ms)'] / 1000
    

    col1, clo2 = st.columns(2)
    with col1:
        st.write("#### Calculate the number of sessions per user")
        st.write(session_frequency.sort_values(by=['Sessions Frequency'], ascending=False))
    
    with clo2:
        st.write("#### Calculate the total session duration per user")
        st.write(session_duration.sort_values(by=['Total Session Duration (s)'], ascending=False))



    #### Calculate the total traffic (download and upload) per user
    total_traffic = df.groupby('MSISDN/Number')[['Total DL (Bytes)', 'Total UL (Bytes)']].sum().reset_index()
    total_traffic['Total Traffic (Bytes)'] = total_traffic['Total DL (Bytes)'] + total_traffic['Total UL (Bytes)']

    #### Merge the calculated metrics into a single DataFrame based on the user's MSISDN/Number
    engagement_metrics = pd.merge(session_frequency, session_duration, on='MSISDN/Number')
    engagement_metrics = pd.merge(engagement_metrics, total_traffic[['MSISDN/Number', 'Total Traffic (Bytes)']], on='MSISDN/Number')

    
    st.write("#### Merge the calculated metrics into a single DataFrame based on the user's MSISDN/Number")
    st.write(engagement_metrics)

    st.write("#### Now, engagement_metrics DataFrame contains the calculated engagement metrics")
    sns.scatterplot(x='Total Session Duration (s)', y='Total Traffic (Bytes)', data=engagement_metrics)
    plt.title('Session Duration vs. Total Traffic')
    plt.xlabel('Total Session Duration (s)')
    plt.ylabel('Total Traffic (Bytes)')
    st.pyplot(plt)

    sns.scatterplot(x='Total Session Duration (s)', y='Sessions Frequency', data=engagement_metrics)
    plt.title('Session Duration vs. Sessions Frequency')
    plt.xlabel('Total Session Duration (s)')
    plt.ylabel('Sessions Frequency')
    st.pyplot(plt)

    sns.scatterplot(x='Total Traffic (Bytes)', y='Sessions Frequency', data=engagement_metrics)
    plt.title('Total Traffic (Bytes) vs. Sessions Frequency')
    plt.xlabel('Total Traffic (Bytes)')
    plt.ylabel('Sessions Frequency')
    st.pyplot(plt)


    # Aggregate engagement metrics per customer ID
    engagement_metrics_per_customer = pd.merge(session_frequency, session_duration, on='MSISDN/Number')
    engagement_metrics_per_customer = pd.merge(engagement_metrics_per_customer, total_traffic[['MSISDN/Number', 'Total Traffic (Bytes)']], on='MSISDN/Number')

    # Aggregate metrics per customer ID
    agg_metrics_per_customer = engagement_metrics_per_customer.groupby('MSISDN/Number').agg({
        'Sessions Frequency': 'sum',
        'Total Session Duration (s)': 'sum',
        'Total Traffic (Bytes)': 'sum'
    }).reset_index()

    # Report the top 10 customers for each engagement metric
    top_10_sessions_frequency = agg_metrics_per_customer.nlargest(10, 'Sessions Frequency')
    top_10_session_duration = agg_metrics_per_customer.nlargest(10, 'Total Session Duration (s)')
    top_10_total_traffic = agg_metrics_per_customer.nlargest(10, 'Total Traffic (Bytes)')

    # Display the results

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("#### Top 10 Customers by Sessions Frequency")
        st.write(top_10_sessions_frequency)
    with col2:
        st.write("#### Top 10 Customers by Total Session Duration")
        st.write(top_10_session_duration)
    with col3:
        st.write("#### Top 10 Customers by Total Traffic")
        st.write(top_10_total_traffic)


    st.write("#### Normalize each engagement metric and run a k-means (k=3) to classify customers in three groups of engagement")
    # Extract the engagement metrics
    engagement_metrics = agg_metrics_per_customer[['Sessions Frequency', 'Total Session Duration (s)', 'Total Traffic (Bytes)']]

    # Normalize the engagement metrics using StandardScaler
    scaler = StandardScaler()
    normalized_engagement_metrics = scaler.fit_transform(engagement_metrics)

    # Run KMeans clustering with k=3
    kmeans = KMeans(n_clusters=3, random_state=42)
    agg_metrics_per_customer['Cluster'] = kmeans.fit_predict(normalized_engagement_metrics)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Sessions Frequency', y='Total Traffic (Bytes)', hue='Cluster', data=agg_metrics_per_customer, palette='Dark2')
    plt.title('K-Means Clustering of Customers')
    plt.xlabel('Sessions Frequency')
    plt.ylabel('Total Traffic (Bytes)')

    # display

    col1, col2 = st.columns([1,3])
    with col1:
        st.write("#### Customer Clusters:")
        st.write(agg_metrics_per_customer[['MSISDN/Number', 'Cluster']])
    with col2:
        st.pyplot(plt)


    st.write("#### Compute the minimum, maximum, average & total non-normalized metrics for each cluster")
    
    # Extract the engagement metrics
    engagement_metrics = agg_metrics_per_customer[['MSISDN/Number', 'Sessions Frequency', 'Total Session Duration (s)', 'Total Traffic (Bytes)']]

    # Add the cluster labels to the engagement_metrics DataFrame
    engagement_metrics['Cluster'] = agg_metrics_per_customer['Cluster']

    # Compute non-normalized metrics for each cluster
    cluster_metrics_summary = engagement_metrics.groupby('Cluster').agg({
        'Sessions Frequency': ['min', 'max', 'mean', 'sum'],
        'Total Session Duration (s)': ['min', 'max', 'mean', 'sum'],
        'Total Traffic (Bytes)': ['min', 'max', 'mean', 'sum']
    }).reset_index()

    # Display the results
    st.write("Cluster Metrics Summary:")
    st.write(cluster_metrics_summary)

    # Example: Bar plot for Sessions Frequency
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Cluster', y=('Sessions Frequency', 'mean'), data=cluster_metrics_summary)
    plt.title('Average Sessions Frequency by Cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Average Sessions Frequency')
    st.pyplot(plt)


    st.write("#### Aggregate user total traffic per application and derive the top 10 most engaged users per application")
    # Select columns related to different applications
    applications_columns = ['Social Media DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']

    # Create a new DataFrame with user ID and total traffic for each application
    user_application_traffic = df[['MSISDN/Number'] + applications_columns].copy()

    # Sum the traffic for each user across all applications
    user_application_traffic['Total Traffic'] = user_application_traffic[applications_columns].sum(axis=1)

    # Sort users based on total traffic for each application
    top_users_by_application = user_application_traffic.sort_values(by='Total Traffic', ascending=False)

    # Display the top 10 users for each application
    top_10_users_per_application = {}
    for app_column in applications_columns:
        top_10_users = top_users_by_application[['MSISDN/Number', app_column]].nlargest(10, app_column)
        top_10_users_per_application[app_column] = top_10_users

    # Print or further analyze the top 10 users for each application
    for app_column, top_users in top_10_users_per_application.items():
        st.write(f"\nTop 10 Users for {app_column}:")
        st.write(top_users)

    st.write("#### 	Plot the top 3 most used applications using appropriate charts")
    # Select the top 3 applications
    top_3_applications = top_users_by_application[['Social Media DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)']]

    # Calculate the total traffic for each application
    total_traffic_per_application = top_3_applications.sum()

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x=total_traffic_per_application.index, y=total_traffic_per_application.values)
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Application')
    plt.ylabel('Total Traffic (Bytes)')
    st.pyplot(plt)

    st.write("#### Using k-means clustering algorithm, group users in k engagement clusters based on the engagement metrics")

    # Extract the engagement metrics
    engagement_metrics = engagement_metrics_per_customer[['Sessions Frequency', 'Total Session Duration (s)', 'Total Traffic (Bytes)']]

    # Normalize the engagement metrics using StandardScaler
    scaler = StandardScaler()
    normalized_engagement_metrics = scaler.fit_transform(engagement_metrics)

    # Run k-means clustering for a range of values of k
    inertia_values = []
    possible_k_values = range(1, 11)  # You can adjust the range based on your data and requirements

    for k in possible_k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(normalized_engagement_metrics)
        inertia_values.append(kmeans.inertia_)

    # Plot the elbow curve
    plt.figure(figsize=(10, 6))
    plt.plot(possible_k_values, inertia_values, marker='o')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia (Sum of Squared Distances)')
    st.pyplot(plt)