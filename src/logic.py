from datetime import datetime
import bcrypt
from src import db

class UserManager:
    def add_user(self, user_name, password_hash, email):
        created_at = str(datetime.utcnow())
        user, error = db.add_user_db(user_name, email, password_hash, created_at)
        if error:
            return {"Success": False, "Message": error}
        return {"Success": True, "data": {"Id": user[0], "User_Name": user[1], "email": user[2]}}

    def login_user(self, email, password):
        user = db.get_user_by_email_db(email)
        if not user:
            return {"Success": False, "Message": "User not found"}
        stored_hash = user[3]
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return {"Success": True, "user_id": user[0], "user_name": user[1]}
        return {"Success": False, "Message": "Invalid credentials"}

    def get_users(self):
        users = db.get_all_users_db()
        return [{"Id": u[0], "User_Name": u[1], "email": u[2]} for u in users]

class NoteManager:
    def add_note(self, content, qr_code_data, user_id, subject, created_at=None, file_name=None, file_data=None):
        if not created_at:
            created_at = str(datetime.utcnow())
        note, error = db.add_note_db(content, qr_code_data, user_id, subject, created_at, file_name, file_data)
        if error:
            return {"Success": False, "Message": error}
        return {"Success": True, "data": {"Id": note[0], "content": note[1], "qr_code_data": note[2], 
                                          "user_id": note[3], "subject": note[4], "created_at": note[5],
                                          "file_name": note[6] is not None and str(note[6]) or None}}

    def get_notes_by_user(self, user_id):
        notes = db.get_notes_by_user_db(user_id)
        return [{"Id": n[0], "content": n[1], "qr_code_data": n[2], "user_id": n[3], 
                 "subject": n[4], "created_at": n[5], "file_name": n[6] if len(n) > 6 else None} for n in notes]

    def get_note_by_id(self, note_id):
        note = db.get_note_by_id_db(note_id)
        if not note:
            return None
        return {"Id": note[0], "content": note[1], "qr_code_data": note[2], 
                "user_id": note[3], "subject": note[4], "created_at": note[5],
                "file_name": note[6] if len(note) > 6 else None}

    def update_note(self, note_id, new_content):
        note, error = db.update_note_db(note_id, new_content)
        if error:
            return {"Success": False, "Message": error}
        return {"Success": True, "data": {"Id": note[0], "content": note[1]}}

    def update_qr_data(self, note_id, qr_code_data):
        note, error = db.update_note_qr_db(note_id, qr_code_data)
        if error:
            return {"Success": False, "Message": error}
        return {"Success": True, "data": {"Id": note[0], "qr_code_data": note[2]}}

    def delete_note(self, note_id):
        note, error = db.delete_note_db(note_id)
        if error:
            return {"Success": False, "Message": error}
        return {"Success": True, "data": {"Id": note[0], "content": note[1]}}
