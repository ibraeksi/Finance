import streamlit as st
import pandas as pd
import json
from pathlib import Path

user_reviews_data = Path(__file__).parents[1] / 'data/raw/user_reviews_10k_v01.csv'
user_reviews_processed_data = Path(__file__).parents[1] / 'data/preprocessed/kw_counted_user_reviews_v01.csv'
user_reviews_sentiment_data = Path(__file__).parents[1] / 'data/preprocessed/final_reviews_with_topics_and_sentiment.csv'
lemmatized_brand_kw_data = Path(__file__).parents[1] / 'data/preprocessed/lemmatized_brand_kw_count.csv'

brand_customer_data = Path(__file__).parents[1] / 'data/text/brandcustomerinfo.json'
with open(brand_customer_data, 'r') as customer:
    brand_customer_info = json.load(customer)

kw_dict_data = Path(__file__).parents[1] / 'data/raw/kw_topics.json'
with open(kw_dict_data, 'r') as kw:
    kw_dict = json.load(kw)

brand_text_data = Path(__file__).parents[1] / 'data/raw/brands_about_us.json'
with open(brand_text_data, 'r') as brand:
    brand_text = json.load(brand)

from modules.navbar import navbar
from backend.visualization.kw_count_polar_plot import kw_count_polar_plot
from backend.visualization.sentiment_heatmap import sentiment_heatmap
from backend.visualization.monthly_sentiment_plot import monthly_sentiment_plot


def customeranalysis():
    st.session_state.update(st.session_state)
    navbar()

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.header("How your customers are perceiving your brand")

    left_top, gap_1, right_top = st.columns([5.5, 0.5, 4], vertical_alignment="top")

    brand_name = st.session_state['chosen_brand']

    with left_top:
        if brand_name is not None:
            df = pd.read_csv(lemmatized_brand_kw_data)
            df['strategy'] = df['brand']

            ### Use keyword matching (takes longer to execute on app)
            # user_reviews_df = get_user_kw_count_df(pd.read_csv(user_reviews_data), kw_dict)
            # user_reviews_df['strategy'] = 'Customer'

            ### Use already keyword matched data directly
            user_reviews_df = pd.read_csv(user_reviews_processed_data)
            user_reviews_df['strategy'] = 'Customer'

            ### Use preprocessed data with topics from model
            # user_reviews = pd.read_csv(user_reviews_sentiment_data)
            # user_reviews_df = user_reviews.groupby(['topic', 'app']).agg({'reviewId': 'count'}).reset_index().rename(columns={'topic': 'category', 'app': 'brand', 'reviewId': 'count'})
            # user_reviews_df['strategy'] = 'Customer'

            df = pd.concat([df, user_reviews_df]).reset_index(drop=True)

            fig = kw_count_polar_plot(df, kw_dict, brand_text, [brand_name], customer=True)
            st.plotly_chart(fig)
    with right_top:
        if brand_name is not None:
            st.subheader("Perception Gap Analysis")
            st.markdown(brand_customer_info[brand_name])


    if brand_name is not None:
        placeholder_heatmap = st.empty()
        placeholder_timeline = st.empty()
        if st.checkbox("Show Customer Sentiment Analysis"):
            sentiment_data = pd.read_csv(user_reviews_sentiment_data)
            placeholder_heatmap.plotly_chart(sentiment_heatmap(sentiment_data))
            placeholder_timeline.plotly_chart(monthly_sentiment_plot(sentiment_data, brand_name))


if __name__ == '__main__':
    customeranalysis()
