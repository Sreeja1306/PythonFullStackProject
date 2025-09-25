# API/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# import UserManager and NoteManager from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.logic import UserManager, NoteManager

#--------------- App Setup ------------

app = FastAPI(title="STUDYQR", version="1.0")

#--------------- Allow frontend (Streamlit/React) to call the API

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (frontend apps)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Manager Instances (business Logic)
user_manager = UserManager()
note_manager = NoteManager()

#-------- Data Models -------

class UserCreate(BaseModel):
    User_Name: str
    password_hash: str
    email: str
    created_at: str

class UserUpdate(BaseModel):
    User_Name: str

class NoteCreate(BaseModel):
    content: str
    qr_code_data: str
    user_id: int
    created_at: str

class NoteUpdate(BaseModel):
    content: str

#-------- Endpoints for Users -----
@app.get("/Users")
def get_users():
    """
        Get all users
    """
    return user_manager.get_users()

@app.post("/Users")
def create_user(user: UserCreate):
    """
        Add a new user
    """
    result = user_manager.add_user(user.User_Name, user.password_hash, user.email, user.created_at)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/Users/{id}")
def update_user(id: int, user: UserUpdate):
    """
        Update a user's name
    """
    result = user_manager.update_user(id, user.User_Name)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/Users/{id}")
def delete_user(id: int):
    """
        Delete a user
    """
    result = user_manager.delete_user(id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result


#-------- Endpoints for Notes -----
@app.get("/Notes")
def get_notes():
    """
        Get all notes
    """
    return note_manager.get_notes()

@app.get("/Notes/user/{user_id}")
def get_notes_by_user(user_id: int):
    """
        Get all notes for a specific user
    """
    return note_manager.get_notes_by_user(user_id)

@app.post("/Notes")
def create_note(note: NoteCreate):
    """
        Add a new note
    """
    result = note_manager.add_note(note.content, note.qr_code_data, note.user_id, note.created_at)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/Notes/{id}")
def update_note(id: int, note: NoteUpdate):
    """
        Update a note's content
    """
    result = note_manager.update_note(id, note.content)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/Notes/{id}")
def delete_note(id: int):
    """
        Delete a note
    """
    result = note_manager.delete_note(id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result


#-------- Health Check -----
@app.get("/")
def home():
    return {"message": "STUDYQR API is running!"}


#----- Run -----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
