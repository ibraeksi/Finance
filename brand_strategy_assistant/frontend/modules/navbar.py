import streamlit as st

def navbar():
    with st.sidebar:
        st.header('Navigation')
        st.page_link('ValueMapApp.py', label='Welcome', icon='👍')
        st.subheader('Analyses')
        st.page_link('pages/brandanalysis.py', label='Brand Analysis', icon='🔥')
        st.page_link('pages/companalysis.py', label='Competition Analysis', icon='🥇')
        st.page_link('pages/customeranalysis.py', label='Customer Analysis', icon='👑')
        st.subheader('Campaign & Content Optimization')
        st.page_link('pages/chatbot.py', label='AI Chatbot', icon='👽')
        st.markdown("---")
        st.page_link('pages/aboutus.py', label='About Us', icon='🥳')
