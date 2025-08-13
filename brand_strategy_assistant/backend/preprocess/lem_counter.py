from collections import Counter
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def count_stem_kws(tokens, keywords_set):
    lem_keyword = {lemmatizer.lemmatize(k) for k in keywords_set}
    lem_tokens=[lemmatizer.lemmatize(token) for token in tokens]
    return Counter([t for t in lem_tokens if t in lem_keyword])
