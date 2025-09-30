import streamlit as st
from modules.navbar import navbar


def welcome():
    st.session_state.update(st.session_state)
    navbar()

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Brand Strategy AI Assistant")

    st.markdown("""An automated analysis serving as a fundament for all brand strategies -
                positioning, marketing, design, communication.""")

    with st.popover("What is value-based brand strategy?"):
        st.markdown("""Building a brand's identity, messaging, and positioning
                    around the core human values it communicates. Instead of
                    focusing solely on product features or visual identity, it asks:
                    *What does this brand stand for? What deeper motivations does it
                    connect with in people's lives?* By aligning brand communication
                    with the values that resonate most with target audiences,
                    companies can create stronger emotional bonds, stand out in
                    competitive markets, and build more consistent, meaningful brand
                    experiences across all touchpoints.""")

    left, center, right = st.columns(3)

    with left:
        st.subheader("Brand Analysis")

        st.markdown("""
                    - Classifies the **core values** your brand communicates
                    - Analyzes language from **advertising, website content, and product messaging**
                    - Identifies and visualizes the brand’s **communicative positioning** within a value framework
        """)

    with center:
        st.subheader("Competitor Analysis")

        st.markdown("""
                    - Compares your brand’s value signals with those of key competitors
                    - Identifies areas of **strategic overlap** or **white-space opportunities**
                    - Enables **data-informed brand differentiation** and **distinct communicative positioning**
        """)

    with right:
        st.subheader("Customer Analysis")

        st.markdown("""
                    - Overlays **consumer value profiles** with your brand’s communicative values
                    - Detects **value misalignments** or **missed opportunities**
                    - Helps tailor content and messaging to **resonate more deeply** with your audience
                    - Supports **targeted campaign planning** based on motivational fit
        """)

if __name__ == '__main__':
    welcome()
