import plotly.express as px

def kw_count_bubble_plot(df):
    """
    Creates a bubble plot using 2D coordinates of selected keywords and number of matches in a given text
    df = Dataframe with counts and the x and y coordinates of the respective keywords
    """
    # Create the bubble plot
    fig = px.scatter(df, y="y", x="x", color="brand", size="count", text="keyword", width=1000, height=800)
    fig.update_traces(textposition='top center')
    fig.update_layout(
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
