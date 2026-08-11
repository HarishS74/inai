from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

print("URL =", repr(SUPABASE_URL))
print("KEY starts with =", SUPABASE_KEY[:15] if SUPABASE_KEY else "None")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)