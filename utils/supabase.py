import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def init_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

supabase_client = init_supabase_client()
