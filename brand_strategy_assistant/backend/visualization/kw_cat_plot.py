import plotly.express as px

def kw_cat_plot(df):
    """
    Creates a scatterplot using 2d coordinates of selected keywords
    df = Dataframe with categories and the x and y coordinates of the respective keywords
    """
    fig = px.scatter(df, y="y", x="x", color="category", text="keyword", width=1000, height=800)
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
