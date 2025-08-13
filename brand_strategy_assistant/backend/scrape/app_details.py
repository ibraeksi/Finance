from google_play_scraper import app
import pandas as pd

def app_details(app_dict: dict, filename: str,
                 raw_data_path='data/raw/') -> pd.DataFrame:
    """
    Retrieves app details from Google Play Store
    app_dict: Dictionary containing app name and app id
    filename: Name of the csv file to be saved
    raw_data_path: Relative path to directory where data should be saved
    """
    details_dict = {i : {} for i in app_dict}

    for item in app_dict.keys():
        details_dict[item] = app(
            app_dict[item],
            lang='en', # defaults to 'en'
            country='de' # defaults to 'us'
        )

    df = pd.DataFrame()
    for item in app_dict.keys():
        temp_df = pd.DataFrame(
            details_dict[item],
            columns = ['title', 'description', 'descriptionHTML', 'summary',
                    'installs', 'minInstalls', 'realInstalls', 'score',
                    'ratings', 'reviews', 'histogram', 'price', 'free',
                    'currency', 'sale', 'saleTime', 'originalPrice',
                    'saleText', 'offersIAP', 'inAppProductPrice',
                    'genre', 'genreId', 'contentRating', 'contentRatingDescription',
                    'adSupported', 'containsAds',
                    'released', 'lastUpdatedOn', 'updated', 'version', 'appId'])

        temp_df["app"] = item
        df = pd.concat((df, temp_df.loc[:0])).reset_index(drop=True)

    df.to_csv(raw_data_path + filename + ".csv", index = False)

    return df
