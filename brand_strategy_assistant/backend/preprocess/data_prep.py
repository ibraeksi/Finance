import re
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def clean_and_tokenize(raw_text: str) -> str:
    """
    Clean Brand's 'About Us' text.
    Clean the input text and returns both:
    - cleaned text (str)
    - tokenized list of words (List[str])
    """
    # Normalize unicode dashes, quotes, etc.
    # Fixes weird characters (like curly quotes → straight quotes, long dashes → `-`)
    text = unicodedata.normalize("NFKC", raw_text)

    # Lowercase
    text = text.lower()

    # Remove weird line breaks and extra spacing
    text = re.sub(r'\n{2,}', '\n', text)      # Multiple blank lines into single ones (removes visual spacing)
    text = re.sub(r'[ \t]{2,}', ' ', text)    # Multiple spaces/tabs into just one (normalization)
    text = re.sub(r'[^a-z0-9\s]', '', text)   # Removes special charachters, keeps only alphabet, digit, and spaces
    text = re.sub(r'<[^>]+>', '', text)       # Remove html <>

    clean_text = text.strip()

    # Tockenizing the text
    tockenized_text = word_tokenize(text)
    # Remove stopwords
    filtered_tokens = [word for word in tockenized_text if word not in stop_words]

    return clean_text, filtered_tokens
