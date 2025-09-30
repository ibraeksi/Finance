import streamlit as st
import pandas as pd
from pathlib import Path

ai_brand_kw_data = Path(__file__).parents[1] / 'data/preprocessed/ai_brand_kw_count.csv'
ai_review_kw_data = Path(__file__).parents[1] / 'data/preprocessed/ai_review_kw_count.csv'

from modules.navbar import navbar
from backend.models.agent import *

### For local run with environment variable
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv("OpenAI_API_KEY")

def chatbot():
    st.session_state.update(st.session_state)
    navbar()

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    brand_kw_df = pd.read_csv(ai_brand_kw_data)
    review_kw_df = pd.read_csv(ai_review_kw_data)

    # Streamlit app setup
    st.title("💬 Brand Strategy Assistant")
    st.caption("🚀 A brand expert chatbot powered by OpenAI")
    st.markdown("""I analyze brand perception, user sentiment, and market positioning
                to support your strategy. Just name a brand or challenge —
                I’ll start with a quick diagnosis and offer more detail if needed.
                """)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state["messages"] = [{"role": "assistant", "content": "Ready to shape your next branding move?"}]

    ### To ask user for API key
    # left, right = st.columns([4,4], vertical_alignment="bottom")
    # with left:
    #     if not st.session_state.get("chatbot_api_key"):
    #         text_input_container = st.empty()
    #         text_input_container.warning("Please enter your OpenAI API Key to continue.")
    #         openai_api_key = text_input_container.text_input("🔐 OpenAI API Key", key="chatbot_api_key", type="password")

    if "last_brands" not in st.session_state:
        st.session_state.last_brands = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        # Call your custom agent
        secrets_file = Path(__file__).parents[1] / ".streamlit/secrets.toml"
        if secrets_file.is_file():
            msg = handle_query(
                question = prompt,
                brand_kw_df=brand_kw_df,
                review_kw_df=review_kw_df,
                api_key=st.secrets["OpenAI_API_KEY"],
                chat_history=st.session_state.messages,
                last_brands=st.session_state.last_brands
                )

            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
        else:
            st.markdown("""Chatbot is missing a /.streamlit/secrets.toml file
                        in the project directory where an API key has to be
                        provided in the following format:""")
            st.markdown("""OpenAI_API_KEY = \"your OpenAI key\"""")

if __name__ == '__main__':
    chatbot()
