from collections import Counter
import pandas as pd
from backend.preprocess.lem_counter import count_stem_kws
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


def get_brand_counts(brand_text, keywords):
    """ Counts occurrences of specified keywords in brand descriptions.

    Args:
        brand_text (dict): Dictionary with brand names as keys and their descriptions as values.
        keywords (list): List of keywords to count in the brand descriptions.

    Returns:
        pd.DataFrame: DataFrame with brands as index and keyword counts as columns.
        Each column corresponds to a keyword, and the values are the counts of that keyword in the brand's description.
    """

    keywords_set = set(kw.lower() for kw in keywords)

    rows = []
    for brand, raw_text in brand_text.items():
        _, tokens = clean_and_tokenize(raw_text)
        kw_counts = count_stem_kws(tokens, keywords_set)
        rows.append({
            "brand": brand,
            "kw_counts": kw_counts
        })

    df = pd.DataFrame(rows)
    df_wide = df["kw_counts"].apply(pd.Series).fillna(0)
    df_wide["brand"] = df["brand"]
    return df_wide.set_index("brand")
