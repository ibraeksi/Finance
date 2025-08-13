
import pandas as pd

def get_monthly_sentiment_trends(df):
    """
    Returns monthly Bayesian-averaged sentiment scores for each (brand, topic) pair
    over the last 12 months (Aug 2024–Jul 2025).
    """

    # Ensure datetime and extract month
    df['at'] = pd.to_datetime(df['at'])
    df['month'] = df['at'].dt.to_period('M').astype(str)


    # Sentiment mapping
    sentiment_map = {
        "Very Negative": -2,
        "Negative": -1,
        "Neutral": 0,
        "Positive": 1,
        "Very Positive": 2
    }
    df["sentiment_score"] = df['sentiment'].map(sentiment_map)

    # Filter to last 12 months
    last_month = df['at'].max().to_period('M')
    last_12_months = pd.period_range(end=last_month, periods=7).astype(str)
    recent = df[df['month'].isin(last_12_months)].copy()

# Global prior and Bayesian weight
    global_prior = df['sentiment_score'].mean()
    k = 10

# Bayesian stats per (brand, month, topic)
    recent_stats = (
        recent.groupby(["app", "month", "topic"])["sentiment_score"]
        .agg(["count", "mean"])
        .rename(columns={"count": "n", "mean": "observed_avg"})
        .reset_index()
    )
    recent_stats["bayes_avg"] = (
        (recent_stats["n"] * recent_stats["observed_avg"] + k * global_prior)
        / (recent_stats["n"] + k)
    )

# Fallback (no month): overall topic score per brand
    fallback = (
        df.groupby(["app", "topic"])["sentiment_score"]
        .mean()
        .reset_index()
        .rename(columns={"sentiment_score": "fallback_avg"})
    )

# Merge fallback to recent_stats
    result = pd.merge(
        recent_stats,
        fallback,
        on=["app", "topic"],
        how="left"
    )

# Final score: bayesian if available, else fallback
    result["final_score"] = result["bayes_avg"].fillna(result["fallback_avg"])

# Final output format
    agent_df = result[["app", "month", "topic", "final_score"]].rename(columns={"app": "brand"})
    agent_df = agent_df.sort_values(by=["brand", "topic", "month"]).reset_index(drop=True)

    return agent_df
