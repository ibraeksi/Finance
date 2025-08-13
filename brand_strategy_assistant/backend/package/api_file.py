from fastapi import FastAPI
from backend.package.predict_topic import predict_topic

# FastAPI instance
app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {'greeting':"hello"}

# Prediction endpoint
@app.get("/predict")
def predict(user_review):
    # Use the function in our package to run the prediction
    prediction = predict_topic(user_review)

    # Return prediction
    return {"prediction": prediction}


#### Following code is for using with the dummy.py function
#### to show the API can read csv file in the data folder
# from backend.package.dummy import calculate_function
# # Calculate endpoint
# @app.get("/calculate")
# def calculate(bankname):
#     # Use the function in our package to run the prediction
#     df = calculate_function(bankname)

#     # Return figure
#     return {'pred': float(df)}
