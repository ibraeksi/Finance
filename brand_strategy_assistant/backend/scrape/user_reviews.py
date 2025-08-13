from google_play_scraper import Sort, reviews
import pandas as pd

def user_reviews(app_dict: dict, num_reviews: int, filename: str,
                 review_lang='en', review_country='de', filter_score=None,
                 raw_data_path='data/raw/') -> pd.DataFrame:
    """
    Retrieves user reviews from Google Play Store
    app_dict: Dictionary containing app name and app id
    num_reviews: Number of reviews to be retrieved per app
    filename: Name of the csv file to be saved
    review_lang: Review language
    review_country: Review country
    filter_score: Method for filtering reviews
    raw_data_path: Relative path to directory where data should be saved
    """
    reviews_dict = {i : {} for i in app_dict}

    for app in app_dict.keys():
        reviews_dict[app], continuation_token = reviews(
                app_dict[app],
                lang=review_lang, # defaults to 'en'
                country=review_country, # defaults to 'us'
                sort=Sort.NEWEST, # defaults to Sort.NEWEST
                count=num_reviews, # defaults to 100
                filter_score_with=filter_score # defaults to None(means all score)
        )

    df = pd.DataFrame()
    for app in app_dict.keys():
        temp_df = pd.DataFrame(
            reviews_dict[app],
            columns = ["reviewId", "content", "score", "thumbsUpCount",
                       "reviewCreatedVersion", "at", "replyContent",
                       "repliedAt", "appVersion"]
            )
        temp_df["app"] = app
        df = pd.concat((df ,temp_df)).reset_index(drop=True)

    df.to_csv(raw_data_path + filename + ".csv", index = False)

    return df
