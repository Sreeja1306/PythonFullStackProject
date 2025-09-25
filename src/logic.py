# logic.py
from db import DatabaseManager

#---------------- Users Manager ----------------
class UserManager:
    """
        Acts as a bridge b.w frontend (Streamlit/FastAPI) and the database.
    """
    def __init__(self):
        # Create a database manager instance (this will handle actual db operations)
        self.db = DatabaseManager()

    #----- Create -----
    def add_user(self, user_name, password_hash, email, created_at):
        """
            Add a new user to the database 
            Return the success message if the user is added.
        """
        if not user_name or not password_hash:
            return {"Success": False, "Message": "user_name and password_hash are required"}
    
        # call DB method to insert User
        result = self.db.create_user(user_name, password_hash, email, created_at)

        if result.get("Success"):
            return {"Success": True, "Message": "User added Successfully!"}
        else:
            return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #---- Read ----
    def get_users(self):
        """
            Get all the users from the database
        """
        return self.db.get_users()

    #--- Update ---
    def update_user(self, Id, new_name):
        """
        Update a user's name in the database
        """
        result = self.db.update_user(Id, new_name)
        if result.get("Success"):
            return {"Success": True, "Message": "User updated successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #------- Delete --------
    def delete_user(self, Id):
        """
        Delete a user from Database
        """
        result = self.db.delete_user(Id)
        if result.get("Success"):
            return {"Success": True, "Message": "User deleted successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}


#---------------- Notes Manager ----------------
class NoteManager:
    """
        Acts as a bridge b.w frontend (Streamlit/FastAPI) and the database.
    """
    def __init__(self):
        # Create a database manager instance
        self.db = DatabaseManager()

    #----- Create -----
    def add_note(self, content, qr_code_data, user_id, created_at):
        """
            Add a new note to the database
        """
        if not content or not user_id:
            return {"Success": False, "Message": "content and user_id are required"}

        # call DB method to insert Note
        result = self.db.create_note(content, qr_code_data, user_id, created_at)

        if result.get("Success"):
            return {"Success": True, "Message": "Note added successfully!"}
        else:
            return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #---- Read ----
    def get_notes(self):
        """
            Get all notes from the database
        """
        return self.db.get_notes()

    def get_notes_by_user(self, user_id):
        """
            Get all notes for a specific user
        """
        return self.db.get_notes_by_user(user_id)

    #--- Update ---
    def update_note(self, Id, new_content):
        """
            Update the content of a note
        """
        result = self.db.update_note(Id, new_content)
        if result.get("Success"):
            return {"Success": True, "Message": "Note updated successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}

    #------- Delete --------
    def delete_note(self, Id):
        """
            Delete a note from the database
        """
        result = self.db.delete_note(Id)
        if result.get("Success"):
            return {"Success": True, "Message": "Note deleted successfully"}
        return {"Success": False, "Message": f"Error: {result.get('error')}"}
