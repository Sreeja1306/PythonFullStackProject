# db.py
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

supabase = create_client(url, key)

#--------- Users table Operations ---------
def create_user(user_name, password_hash, email, created_at=None):
    if created_at is None:
        from datetime import datetime
        created_at = datetime.utcnow().isoformat()

    return supabase.table("Users").insert({
        "User_Name": user_name,
        "password_hash": password_hash,
        "email": email,
        "created_at": created_at
    }).execute()

def get_all_users():
    return supabase.table("Users").select("*").order("created_at").execute()

def update_user(user_id, user_name):
    return supabase.table("Users").update({"User_Name": user_name}).eq("id", user_id).execute()

def delete_user(user_id):
    return supabase.table("Users").delete().eq("id", user_id).execute()

#--------- Notes table Operations ---------
def create_note(content, qr_code_data, user_id, created_at=None):
    if created_at is None:
        from datetime import datetime
        created_at = datetime.utcnow().isoformat()

    return supabase.table("Notes").insert({
        "content": content,
        "qr_code_data": qr_code_data,
        "user_id": user_id,
        "created_at": created_at
    }).execute()

def get_all_notes():
    return supabase.table("Notes").select("*").order("created_at").execute()

def get_notes_by_user(user_id):
    return supabase.table("Notes").select("*").eq("user_id", user_id).order("created_at").execute()

def update_note(note_id, content):
    return supabase.table("Notes").update({"content": content}).eq("id", note_id).execute()

def delete_note(note_id):
    return supabase.table("Notes").delete().eq("id", note_id).execute()
