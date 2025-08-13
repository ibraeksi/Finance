# Define the sentiment function
def score_to_sentiment(score):
    """
    We have a column score, like star, that user gives as a review score.
    We could get a sentiment out of these scores. That is eg 3 neutral, >3 is positive, and <3 is negative.
    """
    score = int(score)
    if score >= 4:
        return "POSITIVE"
    elif score == 3:
        return "NEUTRAL"
    else:
        return "NEGATIVE"


def sentiment_to_score(sentiment):
    """
    We have a column sentiment eg from openai.
    We could get a score (between -1 and 1 out of these sentiment. That is eg 0 neutral.
    """
    sentiment = str(sentiment)
    if sentiment == "very positive":
        return 1
    elif  sentiment == "positive":
        return 0.5
    elif sentiment == "neutral":
        return 0
    elif sentiment == "negative":
        return -0.5
    else:
        return -1
