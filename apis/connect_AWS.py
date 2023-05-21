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
ecg_model = keras.models.load_model('ecg_prediction/')
stroke_models = []
models = os.listdir('stroke prediction models/')
for i in models:
    stroke_models.append(pickle.load(
        open(f'stroke prediction models/{i}', 'rb')))
# fetch the data from supabase using the user_id
ecgReadings = connect_supabase.getUserData(
    '3a283a5f-a00a-4a8e-ba7b-30e3e72bb7f6')
ecgReadingsDf = pd.DataFrame(ecgReadings).T
ecgReadingsDf.columns = list(range(187))
# predict functions


def predict_heart_disease(ecg_model, ecgReadings):
    prediction = ecg_model.predict(ecgReadings)
    return np.array(prediction).argmax()


def predict_stroke(stroke_models, predicted_heart):
    stroke_prediction = []
    for i in stroke_models:
        stroke_prediction.append(i.predict())
# return predicted values to supabase to be read from the front end


print("heart disease predicted:", predict_heart_disease(
    ecg_model=ecg_model, ecgReadings=ecgReadingsDf))
