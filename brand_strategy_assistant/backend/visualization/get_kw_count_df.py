import pandas as pd
from backend.preprocess.lem_counter import count_stem_kws
from backend.preprocess.data_prep import clean_and_tokenize

def get_kw_count_df(kw_dict, text, kw_coors=None):
    """
    Counts the number of keywords in a given text and exports as dataframe
    kw_dict = Dictionary of keywords and categories
    text = String containing the text to be analyzed
    kw_coors = [Optional] Dataframe with the x and y coordinates of the respective keywords
    """
    rows=[]
    for cat in kw_dict.keys():
        keywords_set = set(kw.lower() for kw in kw_dict[cat])

        for brand, raw_text in text.items():
            _, tokens = clean_and_tokenize(raw_text)
            kw_counts = count_stem_kws(tokens, keywords_set)
            for item in kw_counts.items():
                rows.append({
                    "brand": brand,
                    # "tokens": tokens,
                    "category": cat,
                    "keyword": item[0],
                    "count": item[1]
                })

    df = pd.DataFrame(rows)

    if kw_coors is not None:
        # Add coordinates for visualization
        mapx = dict(zip(kw_coors['keyword'], kw_coors['x']))
        mapy = dict(zip(kw_coors['keyword'], kw_coors['y']))
        df['x'] = df['keyword'].map(mapx)
        df['y'] = df['keyword'].map(mapy)

    return df
