from fastapi import FastAPI, HTTPException
import connect_AWS
import json

app = FastAPI()


@app.get("/")
async def getPredictions(userId,gender,age,hyperTension,everMarried,workType,residenceType,AGL,BMI,smokingStatus):
    userId = '3a283a5f-a00a-4a8e-ba7b-30e3e72bb7f6'
    if userId == '':
        raise HTTPException(status_code=404, detail="userID is not provided")
    elif gender == '':
        raise HTTPException(status_code=404, detail="Gender is not provided")
    elif age == 0:
        raise HTTPException(status_code=404, detail="Age is not provided")
    elif hyperTension == '':
        raise HTTPException(status_code=404, detail="hyper tension is not provided")
    elif everMarried == '':
        raise HTTPException(status_code=404, detail="marriage status is not provided")
    elif workType == '':
        raise HTTPException(status_code=404, detail="Work type is not provided")
    elif residenceType == '':
        raise HTTPException(status_code=404, detail="Residence type is not provided")
    elif AGL == 0:
        raise HTTPException(status_code=404, detail="average glucose level is not provided")
    elif BMI == 0:
        raise HTTPException(status_code=404, detail="BMI type is not provided")
    elif smokingStatus == '':
        raise HTTPException(status_code=404, detail="Smoking status type is not provided")

    predictedHeartDisease = connect_AWS.predict_heart_disease(userId)
    predicedStrokeProba = connect_AWS.predict_stroke(
        connect_AWS.stroke_models,
        gender,
        age,
        hyperTension,
        predictedHeartDisease,
        everMarried,
        workType,
        residenceType,
        AGL,
        BMI,
        smokingStatus)


    # return json.loads(predictedHeartDiseaseJson)
