import streamlit as st
import pandas as pd
from modules.navbar import navbar
from pages.welcome import welcome
from pages.brandanalysis import brandanalysis
from pages.companalysis import companalysis
from pages.customeranalysis import customeranalysis
from pages.chatbot import chatbot
from pages.aboutus import aboutus


def main():
    st.session_state.update(st.session_state)

    #--- Initialize session_state
    if 'active_page' not in st.session_state:
        st.session_state.active_page = 'Welcome'
        st.session_state['chosen_brand'] = None

    # Get current values of states
    st.session_state.active_page = st.session_state.active_page
    st.session_state['chosen_brand'] = st.session_state['chosen_brand']

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    #--- Run the active page
    if st.session_state.active_page == 'Welcome':
        welcome()
    elif st.session_state.active_page == 'Brand Analysis':
        brandanalysis()
    elif st.session_state.active_page == 'Competition Analysis':
        companalysis()
    elif st.session_state.active_page == 'Customer Analysis':
        customeranalysis()
    elif st.session_state.active_page == 'AI Chatbot':
        chatbot()
    elif st.session_state.active_page == 'About Us':
        aboutus()


if __name__ == '__main__':
    main()
