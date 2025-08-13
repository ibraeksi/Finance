import plotly.express as px
import pandas as pd
from backend.package.sentiment_trends import get_monthly_sentiment_trends

def monthly_sentiment_plot(df, brand_name):
    """
    Creates a scatter plot using the average sentiment score based on given dataframe
    df = Dataframe with topics and sentiment scores per review
    """
    agent_df = get_monthly_sentiment_trends(df)

    brand_df = agent_df[agent_df["brand"].str.contains(brand_name)]

    # Group and sort
    monthly_sentiment = (
        brand_df.groupby(["month", "topic"])["final_score"]
        .mean()
        .reset_index()
        .sort_values("month")
    )

    # Ensure 'month' is datetime for proper sorting
    monthly_sentiment["month"] = pd.to_datetime(monthly_sentiment["month"])

    # Sort by datetime month
    filtered = monthly_sentiment[monthly_sentiment["month"].dt.year == 2025].copy()

    # Plot
    fig = px.line(filtered, x='month', y='final_score', color='topic', markers=True)

    fig.update_layout(
        showlegend = True,
        width = 1000, height = 700,
        autosize = False,
        plot_bgcolor='white'
    )
    fig.update_xaxes(
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white'
    )
    fig.update_yaxes(
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='white'
    )

    return fig
