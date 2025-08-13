import streamlit as st
import os, sys
import pandas as pd
import json

rootpath = os.path.join(os.getcwd(), '..')
sys.path.append(rootpath)
lemmatized_brand_kw_data = os.path.join(rootpath, 'data/preprocessed/', 'lemmatized_brand_kw_count.csv')
brand_comparison_data = os.path.join(rootpath, 'frontend/modules/text/', 'brandcompareinfo.json')
with open(brand_comparison_data, 'r') as comp:
    brand_comparison_info = json.load(comp)

kw_dict_data = os.path.join(rootpath, 'data/raw/', 'kw_topics.json')
with open(kw_dict_data, 'r') as kw:
    kw_dict = json.load(kw)

brand_text_data = os.path.join(rootpath, 'data/raw/', 'brands_about_us.json')
with open(brand_text_data, 'r') as brand:
    brand_text = json.load(brand)

from frontend.modules.navbar import navbar
from backend.visualization.kw_count_polar_plot import kw_count_polar_plot


def companalysis():
    st.session_state.update(st.session_state)
    navbar()

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.header("Your brand compared to its competitive environment")

    st.markdown("""The competitive environment is shaped by a rapidly evolving
                European fintech landscape, where digital-native firms compete
                to win over mobile-first consumers. Many of these companies started
                in distinct niches—Klarna in payments, Trade Republic in investing,
                Revolut and N26 in neobanking, and bunq in flexible personal finance
                —but their offers are increasingly converging.
                """)

    st.markdown("""
                See if your company is differentiating itself communicatively in
                this highly dynamic, fragmented market.
                """)

    brand_name = st.session_state['chosen_brand']
    allbrands = ["Bunq", "Revolut", "Trade Republic", "Klarna", "N26"]
    competitors = [x for x in allbrands if x != brand_name]

    if brand_name is not None:
        st.write(f"Selected brand **{brand_name}**")
    else:
        st.write("Please select a brand on the Brand Analysis Page to continue")

    left_bottom, gap_1, right_bottom = st.columns([5.5, 0.5, 4], vertical_alignment="top")

    with left_bottom:
        if brand_name is not None:
            brands_to_compare = st.multiselect(
                "Which competitors would you like to compare?",
                options=competitors,
                ## To save current selection
                # key='chosen_competitors',
                max_selections=4, width="stretch",
                accept_new_options=False,
                default=None,
                placeholder="Choose the competitors"
            )

            if brands_to_compare is not None:
                df = pd.read_csv(lemmatized_brand_kw_data)
                brands_to_compare.append(brand_name)
                fig = kw_count_polar_plot(df, kw_dict, brand_text, brand_name_list=brands_to_compare)
                st.plotly_chart(fig)

    with right_bottom:
        if brand_name is not None:
            if brands_to_compare is not None:
                st.subheader("Comparison of brand's positioning")
                st.markdown(brand_comparison_info[brand_name])

if __name__ == '__main__':
    companalysis()
