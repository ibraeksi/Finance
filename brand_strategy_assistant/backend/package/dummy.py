import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_function(bankname):
    df = pd.read_csv('data/raw/user_reviews_10k_v01.csv')

    temp = df[df['app'] == bankname].dropna(subset=['reviewCreatedVersion']).reset_index(drop=True)

    temp['Version'] = temp['reviewCreatedVersion'].apply(lambda x: x.split('.')[0]).astype(int)
    temp = temp.sort_values('Version').reset_index(drop=True)
    plotdf = temp.groupby('Version').agg({'score': 'mean', 'reviewId': 'count'}).reset_index()

    return len(plotdf)
