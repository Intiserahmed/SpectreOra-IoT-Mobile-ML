from fastapi import FastAPI, HTTPException
import connect_AWS
import json

app = FastAPI()
@app.get("/")
async def getPredictions(userId):
    if userId == '':
        raise HTTPException(status_code=404, detail="userID is not provided")
    predictedHeartDisease = connect_AWS.predict_heart_disease(userId)
    if predictedHeartDisease:
	    predictedHeartDiseaseJson = '{"predicted heart disease": "True"}'
	    
    else:
	    predictedHeartDiseaseJson = '{"predicted heart disease": "False"}'
    
    return json.loads(predictedHeartDiseaseJson)
