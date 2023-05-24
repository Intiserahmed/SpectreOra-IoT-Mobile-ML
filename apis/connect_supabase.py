import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=url, supabase_key=key)

<<<<<<< HEAD

=======
>>>>>>> 3d051bb (Changes to be committed:)
def getUserData(user_id):
	res = supabase.table('ecg').select('*').eq(
		'user_id',
	    user_id
		).execute()
<<<<<<< HEAD
	return res.data[-1]['values'][-187:]
=======
	return res.data[3]['values'][-187:]


>>>>>>> 3d051bb (Changes to be committed:)
