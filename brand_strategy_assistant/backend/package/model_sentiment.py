from transformers import pipeline

pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

def review_sentiment(user_review: str) -> str:
    """sentiment prediction function using a multilingual model
    Args: str user_review
    Returns: str with predicted sentiment"""
    output = pipe(user_review)
    return output[0]['label']
