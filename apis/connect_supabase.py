import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=url, supabase_key=key)


def getUserData(user_id):
    res = supabase.table('ecg').select('*').eq(
        'user_id',
        user_id
    ).execute()
    return res.data[-1]['values'][-187:]
