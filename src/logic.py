# logic.py
from db import (
    create_user, get_all_users, update_user, delete_user,
    create_note, get_all_notes, get_notes_by_user, update_note, delete_note
)

#---------------- Users Manager ----------------
class UserManager:
    """
    Acts as a bridge b.w frontend (Streamlit/FastAPI) and the database.
    """
    #----- Create -----
    def add_user(self, user_name, password_hash, email, created_at=None):
        if not user_name or not password_hash:
            return {"Success": False, "Message": "user_name and password_hash are required"}

        result = create_user(user_name, password_hash, email, created_at)
        if result.get("data"):
            return {"Success": True, "Message": "User added Successfully!"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #----- Read -----
    def get_users(self):
        return get_all_users()

    #----- Update -----
    def update_user(self, user_id, new_name):
        result = update_user(user_id, new_name)
        if result.get("data"):
            return {"Success": True, "Message": "User updated successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #----- Delete -----
    def delete_user(self, user_id):
        result = delete_user(user_id)
        if result.get("data"):
            return {"Success": True, "Message": "User deleted successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}


#---------------- Notes Manager ----------------
class NoteManager:
    """
    Acts as a bridge b.w frontend (Streamlit/FastAPI) and the database for Notes.
    """
    #----- Create -----
    def add_note(self, content, qr_code_data, user_id, created_at=None):
        if not content or not user_id:
            return {"Success": False, "Message": "content and user_id are required"}

        result = create_note(content, qr_code_data, user_id, created_at)
        if result.get("data"):
            return {"Success": True, "Message": "Note added successfully!"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #----- Read -----
    def get_notes(self):
        return get_all_notes()

    def get_notes_by_user(self, user_id):
        return get_notes_by_user(user_id)

    #----- Update -----
    def update_note(self, note_id, new_content):
        result = update_note(note_id, new_content)
        if result.get("data"):
            return {"Success": True, "Message": "Note updated successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #----- Delete -----
    def delete_note(self, note_id):
        result = delete_note(note_id)
        if result.get("data"):
            return {"Success": True, "Message": "Note deleted successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}
