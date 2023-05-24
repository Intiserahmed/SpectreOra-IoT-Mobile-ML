from fastapi import FastAPI, HTTPException
import connect_AWS
import json

app = FastAPI()


@app.get("/")
async def getPredictions(userId='3a283a5f-a00a-4a8e-ba7b-30e3e72bb7f6'):
    if userId == '':
        raise HTTPException(status_code=404, detail="userID is not provided")
    predictedHeartDisease = connect_AWS.predict_heart_disease(userId)
    if predictedHeartDisease:
        predictedHeartDiseaseJson = '{"predicted heart disease": "True"}'

    else:
        predictedHeartDiseaseJson = '{"predicted heart disease": "False"}'

    return json.loads(predictedHeartDiseaseJson)
