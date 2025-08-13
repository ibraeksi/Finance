import pandas as pd
from backend.preprocess.kw_counter import count_kw_in_tokens
from backend.preprocess.data_prep import clean_and_tokenize

def get_user_kw_count_df(df_reviews, kw_dict):
    """
    Counts the number of keywords in a given review dataframe and exports as dataframe
    df_reviews = Dataframe with user reviews
    kw_dict = Dictionary of keywords and categories
    """
    rows = []
    for cat in kw_dict.keys():
        keywords_set = set(kw.lower() for kw in kw_dict[cat])
        for app in df_reviews["app"].unique():
            app_text = " ".join(df_reviews[df_reviews["app"] == app]["content"].astype(str))
            _, tokens = clean_and_tokenize(app_text)
            kw_counts = count_kw_in_tokens(tokens, keywords_set)
            for item in kw_counts.items():
                rows.append({
                    "brand": app,
                    #"kw_counts": kw_counts,
                    "category": cat,
                    "keyword": item[0],
                    "count": item[1]
                })

    user_df = pd.DataFrame(rows)

    return user_df
