import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import os, sys
import json

rootpath = os.path.join(os.getcwd(), '../..')
sys.path.append(rootpath)

kw_dict_data = os.path.join(rootpath, 'data/raw/', 'kw_topics.json')
with open(kw_dict_data, 'r') as kw:
    values_keywords = json.load(kw)

def keyword_2d_reduction(model, words=None, sample=0):
    """
    Reduces the word vectors to 2D for visualization
    model: Pre-trained word2vec model
    words: List of keywords
    sample: Number of words to be sampled, if there are no keywords provided
    """
    if words == None:
        if sample > 0:
            words = np.random.choice(list(model.vocab.keys()), sample)
        else:
            words = [ word for word in model.vocab ]

    vectors = []

    for w in words:
        if ' ' in w:
            multiple = w.split()
            vectors.append(model[multiple[0]] + model[multiple[1]])
        elif '-' in w:
            multiple = w.split('-')
            vectors.append(model[multiple[0]] + model[multiple[1]])
        else:
            vectors.append(model[w])

    word_vectors = np.array(vectors)

    keycoors = PCA().fit_transform(word_vectors)[:,:2]

    return keycoors


def convert_2dwords_todf(model, kw_dict=values_keywords):
    """
    Saves the x and y coordinates of the keywords in a dataframe
    model: Pre-trained word2vec model
    kw_dict: Dictionary of keywords and categories
    """
    keywords = []
    reverse_kw_dict = {}

    for key in kw_dict.keys():
        for value in kw_dict[key]:
            keywords.append(value)
            reverse_kw_dict[value] = key

    keycoors = keyword_2d_reduction(model, keywords)

    df = pd.concat([pd.DataFrame(keywords, columns=['keyword']), pd.DataFrame(keycoors, columns=['x', 'y'])], axis=1)
    df['category'] = df['keyword'].map(reverse_kw_dict)

    return df
