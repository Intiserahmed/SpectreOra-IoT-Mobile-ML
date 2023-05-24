import os
from tensorflow import keras
import pickle
import connect_supabase
import pandas as pd
import numpy as np
# set credentials in heroku as environment variables

# download the s3 bucket in local heroku environment

os.system('aws s3 sync s3://userdatastrokeprediction .')

# laod the models
def loadECGModel():
    ecg_model = keras.models.load_model('ecg_prediction/')
    stroke_models = []
    models = os.listdir('stroke prediction models/')
    for i in models:
        stroke_models.append(pickle.load(
            open(f'stroke prediction models/{i}', 'rb')))
    return ecg_model
    # fetch the data from supabase using the user_id
def getUserReadings(userId):
    ecgReadings = connect_supabase.getUserData(userId)
    ecgReadingsDf = pd.DataFrame(ecgReadings).T
    ecgReadingsDf.columns = list(range(187))
    return ecgReadingsDf





# user details as a variable till the app is ready & preprocessing 
# user_details = {
#     'gender': 'male',
#     'age': 24,
#     'hypertension':1,
#     'ever_married': 'Yes',
#     'work_type': 'Private',
#     'Residence_type': 1,
#     'avg_glucose_level': 120,
#     'bmi': 21.5,
#     'smoking_status': 'formerly smoked'
# }

# predict functions


def predict_heart_disease(userID):
    ecgModel = loadECGModel()
    ecgReadings = getUserReadings(userID)
    prediction = ecgModel.predict(ecgReadings)
    return np.array(prediction).argmax()


def predict_stroke(stroke_models, predicted_heart, user_details):
    stroke_predictions = []
    for model in stroke_models:
        stroke_prediction.append(model.predict())
# return predicted values to supabase to be read from the front end


# print("Storke predicted:", predict_stroke(
#     stroke_models=stroke_models,
#     predicted_haert_disease=predict_heart_disease(ecg_model, ecgReadings),
#     user_details= processed_data
# )
# )
