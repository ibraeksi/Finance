import pandas as pd
from backend.preprocess.kw_counter import count_kw_in_tokens
from backend.preprocess.data_prep import clean_and_tokenize
import os, sys
import json

rootpath = os.path.join(os.getcwd(), '../..')
sys.path.append(rootpath)

brand_text_data = os.path.join(rootpath, 'data/raw/', 'brands_about_us.json')
with open(brand_text_data, 'r') as brand:
    brand_text = json.load(brand)

keywords = [
    "ambition", "digital", "disruption", "diversity", "efficiency",
    "honesty", "simple", "fair", "flexibility", "community", "parity",
    "innovation", "integrity", "customer orientation", "bravery",
    "sustainability", "rationality", "self-determination", "teamwork",
    "transparency", "responsibility", "trust", "growth",
    "goal orientation", "accessibility"
]

keywords_set = set(kw.lower() for kw in keywords)

rows=[]

for brand, raw_text in brand_text.items():
    _, tokens = clean_and_tokenize(raw_text)

    kw_counts = count_kw_in_tokens(tokens, keywords_set)
    rows.append({
        "brand": brand,
        "tokens": tokens,
        "kw_counts": kw_counts
    })

df = pd.DataFrame(rows)

# 3. Wide format
df_wide = df["kw_counts"].apply(pd.Series).fillna(0)
df_wide["brand"] = df["brand"]

# 4. Save
df.to_csv("data/preprocessed/brand_tokens_kw_counts.csv", index=False)
df_wide.to_csv("data/preprocessed/brand_kw_wide.csv", index=False)
