import DataCleaning
import UserOverview
import UserEngagement
import UserExperiance
import UserSatisfaction

import streamlit as st

PAGES = {
    "Data Cleaning": DataCleaning,
    "User Overview": UserOverview
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
