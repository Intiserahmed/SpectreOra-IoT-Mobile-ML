import urllib.request
import joblib
from catboost import CatBoostClassifier
import boto3
from botocore.config import Config
from botocore import UNSIGNED
import io

from fastapi import FastAPI

app = FastAPI()

URL = ""


def loadAllModels(url):
    models = []
    for c in ["svm1", "svm2", "logit1", "logit2", "nbc1", "nbc2", "rf1", "rf2", "errGBR"]:
        models.append(
            joblib.load(
                urllib.request.urlopen(url + "/" + "{}.pkl".format(c))
            )
        )

    return models[0], models[1], models[2], models[3], models[4], models[5], models[6], models[7], models[8]


svm1, svm2, logit1, logit2, nbc1, nbc2, rf1, rf2, errGBR = loadAllModels(URL)


def loadCatBoost():
    s3 = boto3.resource(
        service_name='s3',
        region_name='eu-central-1',
        config=Config(signature_version=UNSIGNED)
    )
    bucket = s3.Bucket('strokemodels')

    models = []

    for c in ["cb1", "cb2"]:
        obj = bucket.Object("%s" % (c))
        file_stream = io.BytesIO()
        obj.download_fileobj(file_stream)

        CB = CatBoostClassifier()
        models.append(CB.load_model(blob=file_stream.getvalue()))

    return models[0], models[1]


cb1, cb2 = loadCatBoost()


def preprocess_data(patient_data, scaler):
    columns = ['age', 'hypertension', 'heart_disease', 'ever_married',
               'work_type', 'Residence_type', 'avg_glucose_level', 'bmi',
               'smoking_status']
    df = pd.DataFrame(patient_data, index=[0], columns=columns)
    numeric_features = ['age', 'avg_glucose_level', 'bmi']
    categorical_features = ['hypertension', 'heart_disease', 'ever_married',
                            'work_type', 'Residence_type', 'smoking_status']

    df[numeric_features] = scaler.transform(df[numeric_features])

    return df


def predict_stroke_risk(patient_data):
    catboost_model, scaler = load_models()
    preprocessed_data = preprocess_data(patient_data, scaler)
    prediction = catboost_model.predict_proba(preprocessed_data)
    stroke_risk = prediction[0][1]
    confidence = stroke_risk * 100

    return stroke_risk, confidence


# Example patient_data
patient_data = {
    'age': 67,
    'hypertension': 0,
    'heart_disease': 1,
    'ever_married': 'Yes',
    'work_type': 'Private',
    'Residence_type': 'Urban',
    'avg_glucose_level': 228.69,
    'bmi': 36.6,
    'smoking_status': 'formerly smoked'
}

if __name__ == "__main__":
    stroke_risk, confidence = predict_stroke_risk(patient_data)
    print(f"Stroke risk: {stroke_risk:.3f}, Confidence: {confidence:.2f}%")


# async def save_prediction_to_supabase(data: PatientData, prediction: float):
#     patient_data = data.dict()
#     patient_data["prediction"] = prediction

#     response = await supabase.from_("your_table").insert([patient_data])

#     return response


# @app.get("/data/")
# async def get_data_from_supabase():
#     response = await supabase.from_("your_table").select("*")

#     return response.data
