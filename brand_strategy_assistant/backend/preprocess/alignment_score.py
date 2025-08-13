from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os, sys
import json

rootpath = os.path.join(os.getcwd(), '..')
sys.path.append(rootpath)

kw_dict_data = os.path.join(rootpath, 'data/raw/', 'kw_topics.json')
with open(kw_dict_data, 'r') as kw:
    values_keywords = json.load(kw)

def reverse_keyword_mapping(values_keywords: dict) -> dict:
    keyword_to_category = {}
    for category, keywords in values_keywords.items():
        for keyword in keywords:
            keyword_to_category[keyword.lower()] = category.lower()
    return keyword_to_category

def get_alignment_summary(brand, brand_kw_df, review_kw_df, top_n=3):
    if brand not in brand_kw_df.index or brand not in review_kw_df.index:
        return {"error": f"Brand '{brand}' not found in both datasets."}

    # Ensure same columns
    all_keywords = sorted(set(brand_kw_df.columns).union(set(review_kw_df.columns)))
    brand_vec = brand_kw_df.reindex(columns=all_keywords, fill_value=0).loc[brand].values.reshape(1, -1)
    review_vec = review_kw_df.reindex(columns=all_keywords, fill_value=0).loc[brand].values.reshape(1, -1)

    # Normalize
    brand_vec_norm = normalize(brand_vec, norm="l1")
    review_vec_norm = normalize(review_vec, norm="l1")

    # Cosine similarity
    alignment_score = float(cosine_similarity(brand_vec_norm, review_vec_norm)[0][0])

    # Top keywords
    top_brand_keywords = brand_kw_df.loc[brand].sort_values(ascending=False).head(top_n).index.tolist()
    top_review_keywords = review_kw_df.loc[brand].sort_values(ascending=False).head(top_n).index.tolist()

    # Map to categories
    kw_to_cat = reverse_keyword_mapping(values_keywords)
    top_brand_values = list({kw_to_cat.get(k.lower(), k) for k in top_brand_keywords})
    top_review_values = list({kw_to_cat.get(k.lower(), k) for k in top_review_keywords})

    # Categorical overlap score
    top_value_alignment_score = len(set(top_brand_values) & set(top_review_values)) / top_n

    # Identify misalignment
    gaps_brand = [val for val in top_brand_values if val not in top_review_values]
    gaps_review = [val for val in top_review_values if val not in top_brand_values]

    recommendation = (
        f"{brand} emphasizes {', '.join(gaps_brand)} in its messaging, but these values are not strongly perceived by users."
        f"Consider reinforcing them in UX, marketing, or customer service."
        f"Users perceive {', '.join(gaps_review)} as important, but these are not highlighted in the brand's communication."
        f"Consider reinforcing them in the brand communication."
        if gaps_brand else f"{brand} is well-aligned in its brand values and user perception."
    )

    return {
        "brand": brand,
        "Totall alignment_score": round(alignment_score, 3),
        "Top values alignment score: ": round(top_value_alignment_score, 3),
        "top_brand_values": top_brand_values,
        "top_user_values": top_review_values,
        "misaligned_values": gaps_brand + gaps_review,
        "recommendation": recommendation
    }
