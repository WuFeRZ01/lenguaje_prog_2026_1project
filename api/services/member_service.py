from api.db.supabase_client import supabase

def get_members():
    response = supabase.table("members").select("*").execute()
    return response.data

def create_member(data):
    response = supabase.table("members").insert(data).execute()
    return response.data