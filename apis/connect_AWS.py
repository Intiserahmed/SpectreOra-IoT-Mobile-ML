import os
from tensorflow import keras
import pickle
import connect_supabase
import pandas as pd
import numpy as np


# download the s3 bucket in local railway  environment
os.system('aws s3 sync s3://userdatastrokeprediction .')

# laod the models
ecg_model = keras.models.load_model('ecg_prediction/')
heartDiseaseModel = pickle.load(open(f'heartDiseaseModel', 'rb'))
stroke_models = []
models = os.listdir('stroke prediction models/')
for i in models:
    stroke_models.append(pickle.load(
        open(f'stroke prediction models/{i}', 'rb')))

# fetch the data from supabase using the user_id


def getUserReadings(userId):
    dflist = []
    ecgReadings = connect_supabase.getUserReadings(userId)
    for i in range(len(ecgReadings)):
        ecgReadings[i] = np.array(ecgReadings[i], dtype=float).reshape((-1, 187))
        dflist.append(pd.DataFrame(ecgReadings[i], columns=range(187), index=range(10)))
    ecgReadingsDf = pd.concat(dflist)
    ecgReadingsDf.reset_index(drop=True, inplace=True)
    ecgReadingsDf = pd.DataFrame(ecgReadingsDf.mean(axis=0)).T
    print(ecgReadingsDf)
    return ecgReadingsDf


# preprocessing
fullProcessor = pickle.load(open('fullprocessor', 'rb'))

# predict functions

def predict_heart_disease(userID):
    ecgModel = ecg_model
    ecgReadings = getUserReadings(userID)

    prediction = ecgModel.predict(ecgReadings)
    res = np.array(prediction).argmax()
    if res == 0:
        return res
    else:
        heartDiseaseType = heartDiseaseModel.predict(ecgReadings)
        return heartDiseaseType[0]
    return res


def predict_stroke(stroke_models, gender, age, hyperTension, predictedHeartDisease, everMarried, workType, residenceType, AGL, BMI, smokinStatus):
    colNames = ['gender', 'age', 'hypertension', 'heart_disease',
                'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']
    data = [[gender, float(age), hyperTension, predictedHeartDisease,
            everMarried, workType, residenceType, float(AGL), float(BMI), smokinStatus]]
    df = pd.DataFrame(columns=colNames, data=data)
    for col in colNames:
        if df[col].dtype == int:
            df[col] = df[col].astype(str)
    processedData = fullProcessor.transform(df)
    stroke_predictions = []
    for model in stroke_models:
        stroke_predictions.append(model.predict_proba(processedData))
    avg = 0
    for i in stroke_predictions:
        avg += i[0][1]
    avg /= 2
    return avg*100