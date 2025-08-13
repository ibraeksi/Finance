import os
import pickle
import pandas as pd
from backend.preprocess.data_prep import clean_and_tokenize

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

def predict_topic(user_review: str):
    """Prediction function using a pretrained model loaded from disk

    Arguments:
    - user_review
    """
    # Load the model from the pickle file
    model_path = os.path.join(ROOT_PATH, 'models', 'mvpsimplemodel.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    # Clean and format user review
    user_input_df = pd.DataFrame({"tokens": [clean_and_tokenize(user_review)[1]]})

    # Use the model to predict the given inputs
    X_pred = user_input_df['tokens'].apply(lambda tokens: ' '.join(tokens))
    y_pred = model.predict(X_pred)

    # Create dictionary based on model classes
    convertdict = {0: 'community', 1: 'empowerment', 2: 'ethos', 3: 'growth',
                   4: 'innovation', 5: 'quality', 6: 'simplicity', 7: 'user_centricity'}

    # Convert predicted class to topic
    prediction = convertdict[int(y_pred[0])]

    return prediction
