import plotly.express as px
import pandas as pd
import numpy as np

def kw_count_polar_plot(df, kw_dict, brand_text,
                        brand_name_list: list, customer=False):
    if customer:
        strategy_list = brand_name_list + ['Customer']
        selected_df = df[(df['brand'].isin(brand_name_list)) & (df['strategy'].isin(strategy_list))].reset_index(drop=True)

        groupdf = selected_df.groupby(['category', 'brand', 'strategy']).agg({'count':'sum'}).reset_index()
        modgroupdf = pd.DataFrame()
        missing_cat_rows = []

        for cat in kw_dict.keys():
            temp = groupdf[groupdf['category'] == cat].reset_index(drop=True)
            for brand in brand_text.keys():
                # If the brand does not have a keyword in the category,
                # add a placeholder value of 0.1 for visualization
                if brand not in set(temp['brand']):
                    temp = pd.concat([temp, pd.DataFrame({'category': [cat], 'brand': [brand], 'strategy': [brand], 'count':[0.1]})])
                    missing_cat_rows.append({'category': cat, 'brand': brand, 'strategy': 'Customer', 'count':0.1})

            modgroupdf = pd.concat([modgroupdf, temp]).reset_index(drop=True)

        modgroupdf = pd.concat([modgroupdf, pd.DataFrame(missing_cat_rows)]).reset_index(drop=True)

        totcountdictbrand = {}
        totcountdictcustomer = {}
        for brand in brand_text.keys():
            totcountdictbrand[brand] = np.floor(modgroupdf[(modgroupdf['brand'] == brand) & (modgroupdf['strategy'] == brand)]['count'].sum())
            totcountdictcustomer[brand] = np.floor(modgroupdf[(modgroupdf['brand'] == brand) & (modgroupdf['strategy'] == 'Customer')]['count'].sum())

        modgroupdf.loc[modgroupdf['strategy'] != 'Customer', 'totkwcount'] = modgroupdf['strategy'].map(totcountdictbrand)
        modgroupdf.loc[modgroupdf['strategy'] == 'Customer', 'totkwcount'] = modgroupdf['brand'].map(totcountdictcustomer)
        modgroupdf['catcountperc'] = 100*modgroupdf['count']/modgroupdf['totkwcount']

        fig = px.line_polar(modgroupdf,
                        r='catcountperc',
                        theta='category',
                        color='strategy',
                        line_close=True,
                        color_discrete_map={'Klarna': '#990099', 'N26': '#109618',
                                            'Trade Republic': '#DC3912',
                                            'Bunq': '#3366CC', 'Revolut': '#FF9900',
                                            'Customer': '#565656'},
                        range_theta=[0,360], start_angle=0)
    else:
        selected_df = df[df['brand'].isin(brand_name_list)].reset_index(drop=True)
        groupdf = selected_df.groupby(['category', 'brand']).agg({'count':'sum'}).reset_index()

        modgroupdf = pd.DataFrame()
        for cat in kw_dict.keys():
            temp = groupdf[groupdf['category'] == cat].reset_index(drop=True)
            for brand in brand_text.keys():
                # If the brand does not have a keyword in the category,
                # add a placeholder value of 0.1 for visualization
                if brand not in set(temp['brand']):
                    temp = pd.concat([temp, pd.DataFrame({'category': [cat], 'brand': [brand], 'count':[0.1]})])

            modgroupdf = pd.concat([modgroupdf, temp]).reset_index(drop=True)

        totcountdict = {}
        for brand in brand_text.keys():
            totcountdict[brand] = np.floor(modgroupdf[modgroupdf['brand'] == brand]['count'].sum())

        modgroupdf['totkwcount'] = modgroupdf['brand'].map(totcountdict)
        modgroupdf['catcountperc'] = 100*modgroupdf['count']/modgroupdf['totkwcount']

        fig = px.line_polar(modgroupdf,
                        r='catcountperc',
                        theta='category',
                        color='brand',
                        line_close=True,
                        color_discrete_map={'Klarna': '#990099', 'N26': '#109618',
                                            'Trade Republic': '#DC3912',
                                            'Bunq': '#3366CC', 'Revolut': '#FF9900'},
                        range_theta=[0,360], start_angle=0)
                        #width=800,height=800)

    if not customer:
        if len(brand_name_list) == 1:
            fig.update_layout(showlegend=False)

    if customer:
        for trace in fig['data']:
            if (not trace['name'] in strategy_list):
                trace['showlegend'] = False
    else:
        for trace in fig['data']:
            if (not trace['name'] in brand_name_list):
                trace['showlegend'] = False

    fig.update_layout(
        template=None,
        polar = dict(
            radialaxis = dict(showticklabels=False, ticks='', showline=False, range=[0,45], showgrid=False),
            angularaxis = dict(labelalias={'quality_usability': 'quality<br>usability',
                                        'innovation_technology': 'innovation<br>technology',
                                        'trust_ethics': 'trust<br>ethics',
                                        'empowerment_control': 'empowerment<br>control',
                                        'user_centricity_support': 'user centricity<br>support',
                                        'community_belonging': 'community<br>belonging',
                                        'growth_ambition': 'growth<br>ambition'},
                            categoryarray=['empowerment_control', 'trust_ethics', 'innovation_technology', 'quality_usability',
                                            'growth_ambition', 'community_belonging', 'user_centricity_support'],
                            direction='counterclockwise')
        ),
        legend=dict(
        orientation="v",
        yanchor="top",
        y=1.1,
        xanchor="left",
        x=1.0
        )
    )
    fig.update_traces(fill='toself')
    fig.update_polars(bgcolor='white')

    return fig
