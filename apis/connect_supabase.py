import os
from supabase import create_client, Client
from fastapi import HTTPException

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=url, supabase_key=key)


def getUserReadings(user_id):
    res = supabase.table('ecg').select('*').eq(
        'user_id',
        user_id
    ).execute()
    if len(res.data) == 0:
        raise HTTPException(
            status_code=404, detail='no readings found for given user')
    ls = res.data[-5:]
    res = []
    for i in ls:
        res.append(i['values'][:1870])
    for i in range(5):
        for j in range(1870):
            res[i][j] %= 1024
            res[i][j] /= 1024
    return res


def getUserDetails(user_id):
    res = supabase.table('users').select(
        'gender',
        'marriage_status',
        'age',
        'bmi',
        'avg_glucose',
        'smoking_status',
        'hypertension',
        'work_type',
        'residence_type').eq('uid',
                             user_id
                             ).execute()
    if len(res.data) == 0:
        raise HTTPException(
            status_code=404, detail='No user found for given ID')
    return res.data[0]


def saveUserResults(userId, results):
    data = supabase.table("predictions").insert(
        {
            "uid": userId,
            "heart_disease_predicted": results['predictedHeartDisease'],
            "stroke_probability": results['predictedStrokeProba']
        }).execute()
    assert len(data.data) > 0