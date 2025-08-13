import streamlit as st
import os, sys
import pandas as pd
import json

rootpath = os.path.join(os.getcwd(), '..')
sys.path.append(rootpath)
lemmatized_brand_kw_data = os.path.join(rootpath, 'data/preprocessed/', 'lemmatized_brand_kw_count.csv')
company_desc_data = os.path.join(rootpath, 'frontend/modules/text/', 'companydesc.json')
with open(company_desc_data, 'r') as desc:
    companydesc = json.load(desc)

brand_analysis_data = os.path.join(rootpath, 'frontend/modules/text/', 'brandinfo.json')
with open(brand_analysis_data, 'r') as info:
    brand_analysis_info = json.load(info)

kw_dict_data = os.path.join(rootpath, 'data/raw/', 'kw_topics.json')
with open(kw_dict_data, 'r') as kw:
    kw_dict = json.load(kw)

brand_text_data = os.path.join(rootpath, 'data/raw/', 'brands_about_us.json')
with open(brand_text_data, 'r') as brand:
    brand_text = json.load(brand)

from frontend.modules.navbar import navbar
from backend.visualization.kw_count_polar_plot import kw_count_polar_plot

def refresh_competitors():
    brand_name = st.session_state['chosen_brand']
    allbrands = ["Bunq", "Revolut", "Trade Republic", "Klarna", "N26"]
    competitors = [x for x in allbrands if x != brand_name]
    st.session_state['chosen_competitors'] = competitors

def brandanalysis():
    st.session_state.update(st.session_state)

    navbar()

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.header("Analyse your company")

    left_top, gap, right_top, gap_2 = st.columns([3, 1, 4, 1], vertical_alignment="top")

    with left_top:
        brand_name = st.selectbox('Which company would you like to analyze?', key='chosen_brand',
                                options=("Bunq", "Revolut", "Trade Republic", "Klarna", "N26"),
                                index=None, placeholder="Choose your company",
                                on_change=refresh_competitors)

    with right_top:
        if brand_name is not None:
            st.write(companydesc[brand_name])

    st.subheader("Your brand's positioning")

    left_bottom, gap_3, right_bottom = st.columns([5, 0.5, 4.5], vertical_alignment="top")

    with left_bottom:
        if brand_name is not None:

            df = pd.read_csv(lemmatized_brand_kw_data)

            brand_name_list = []
            brand_name_list.append(brand_name)

            fig = kw_count_polar_plot(df, kw_dict, brand_text, brand_name_list=brand_name_list)

            st.plotly_chart(fig)

    with right_bottom:
        if brand_name is not None:
            st.subheader("Analysis of brand's positioning")

            #selected_df = df[df['brand'] == brand_name].reset_index(drop=True)
            #pivot_table = selected_df.pivot_table(values='count', index=['category', 'keyword'], columns='brand', aggfunc='sum')
            #pivot_table[pivot_table.columns] = pivot_table[pivot_table.columns].fillna(0).astype(int)
            #st.dataframe(pivot_table)

            st.markdown(brand_analysis_info[brand_name])

if __name__ == '__main__':
    brandanalysis()
