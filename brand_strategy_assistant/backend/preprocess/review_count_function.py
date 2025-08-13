from collections import Counter
import pandas as pd
from backend.preprocess.kw_counter import count_kw_in_tokens
from backend.preprocess.data_prep import clean_and_tokenize
import os, sys
import json

rootpath = os.path.join(os.getcwd(), '..')
sys.path.append(rootpath)

kw_dict_data = os.path.join(rootpath, 'data/raw/', 'kw_topics.json')
with open(kw_dict_data, 'r') as kw:
    values_keywords = json.load(kw)

keywords = [
    word
    for words in values_keywords.values()
    for word in words
]


def get_review_counts(df_reviews, keywords):
    """ Counts occurrences of specified keywords in app reviews.

    Args:
        df_reviews (pd.DataFrame): DataFrame containing app reviews with columns 'app' and 'content'.
        keywords (list): List of keywords to count in the reviews.

    Returns:
        pd.DataFrame: DataFrame with apps as index and keyword counts as columns.
        Each column corresponds to a keyword, and the values are the counts of that keyword in the app's reviews.
    """

    keywords_set = set(kw.lower() for kw in keywords)

    rows = []
    for app in df_reviews["app"].unique():
        app_text = " ".join(df_reviews[df_reviews["app"] == app]["content"].astype(str))
        _, tokens = clean_and_tokenize(app_text)
        kw_counts = count_kw_in_tokens(tokens, keywords_set)
        rows.append({
            "brand": app,
            "kw_counts": kw_counts
        })

    df = pd.DataFrame(rows)
    df_wide = df["kw_counts"].apply(pd.Series).fillna(0)
    df_wide["brand"] = df["brand"].replace({"TradeRepublic": "Trade Republic"})
    return df_wide.set_index("brand")
