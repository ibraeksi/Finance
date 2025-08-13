from collections import Counter
import pandas as pd

def count_kw_in_tokens(tokens, keywords_set):
    return Counter([t for t in tokens if t in keywords_set])
