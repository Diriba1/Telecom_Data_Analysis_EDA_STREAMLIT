from StreamlitFiles import DataCleaning, UserOverview, UserEngagement,UserExperiance, UserSatisfaction

import streamlit as st

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
