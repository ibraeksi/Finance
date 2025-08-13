import plotly.express as px
import pandas as pd
import numpy as np

def sentiment_heatmap(df):
    """
    Creates a heatmap using the average sentiment score based on given dataframe
    df = Dataframe with topics and sentiment scores per review
    """
    # Ensure 'at' column is datetime
    df["at"] = pd.to_datetime(df["at"])

    sentiment_map = {
            "Very Negative": -2,
            "Negative": -1,
            "Neutral": 0,
            "Positive": 1,
            "Very Positive": 2
        }
    df["sentiment_score"] = df['sentiment'].map(sentiment_map)

    # Filter to last 3 months
    last_3_months = df["at"].max() - pd.DateOffset(months=3)
    recent = df[df["at"] >= last_3_months].copy()

    # Global sentiment prior (baseline)
    global_prior = df["sentiment_score"].mean()

    # Compute recent (brand, topic) stats
    recent_stats = (
        recent.groupby(["app", "topic"])["sentiment_score"]
        .agg(["count", "mean"])
        .rename(columns={"count": "n", "mean": "observed_avg"})
        .reset_index()
    )

    # Apply Bayesian average
    k = 10  # smoothing strength
    recent_stats["bayes_avg"] = (
        (recent_stats["n"] * recent_stats["observed_avg"] + k * global_prior) /
        (recent_stats["n"] + k)
    )

    # Get fallback from full data
    fallback = (
        df.groupby(["app", "topic"])["sentiment_score"]
        .mean()
        .reset_index()
        .rename(columns={"sentiment_score": "fallback_avg"})
    )

    # Merge Bayesian results with fallback
    result = pd.merge(fallback, recent_stats[["app", "topic", "bayes_avg"]], on=["app", "topic"], how="left")

    # Final score: Bayesian if exists, otherwise fallback
    result["final_score"] = result["bayes_avg"].fillna(result["fallback_avg"])

    # Pivot for heatmap
    heatmap_df = result.pivot(index="app", columns="topic", values="final_score")
    fig = px.imshow(heatmap_df.to_numpy(),
                    title="Bayesian-Smoothed Sentiment per Topic Across Brands (Last 3 Months)",
                    #labels=dict(x="Review Topic", y="Brand", color="Sentiment Score"),
                    x=['community<br>belonging', 'empowerment<br>control', 'growth<br>ambition',
                    'innovation<br>technology', 'quality<br>usability', 'trust<br>ethics', 'user centricity<br>support'],
                    y=['Bunq', 'Klarna', 'Trade Republic', 'Revolut', 'N26'],
                    color_continuous_scale='RdYlGn')

    fig.update_layout(
        showlegend = True,
        width = 1000, height = 700,
        autosize = False
    )

    fig.update_traces(text=np.around(heatmap_df.to_numpy(), 2), texttemplate="%{text}")
                    #textfont=dict(size=14))

    return fig
