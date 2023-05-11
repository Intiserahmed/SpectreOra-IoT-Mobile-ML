

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=  url,supabase_key= key)


response = supabase.table('ecg').select("*").execute()

print(response)


