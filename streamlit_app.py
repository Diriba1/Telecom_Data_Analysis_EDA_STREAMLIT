from StreamlitFiles import DataCleaning, UserOverview, UserEngagement,UserExperiance, UserSatisfaction

import streamlit as st

st.set_page_config(page_title="Telecom Data Analytics", layout="wide") 

PAGES = {
    "Data Cleaning": DataCleaning,
    "User Overview": UserOverview,
    "User Engagement": UserEngagement,
    "User Experiance": UserExperiance,
    "User Satisfaction": UserSatisfaction
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Pages", list(PAGES.keys()))
page = PAGES[selection]
page.app()
