from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from datetime import datetime
import bcrypt

try:
    from src.logic import UserManager, NoteManager
except ModuleNotFoundError:
    # Ensure project root is on sys.path when running via different CWDs
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.logic import UserManager, NoteManager

user_manager = UserManager()
note_manager = NoteManager()

app = FastAPI(title="STUDYQR API", version="1.0")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Pydantic Models -----------------
class User(BaseModel):
    username: str
    password: str
    email: str

class Login(BaseModel):
    email: str
    password: str

class Note(BaseModel):
    content: str
    subject: str
    qr_code_data: str = ""
    user_id: int
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))

# ----------------- User Endpoints -----------------
@app.post("/register")
def register_user(user: User):
    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    result = user_manager.add_user(user.username, hashed_pw, user.email)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return {"success": True, "data": result["data"]}

@app.post("/login")
def login_user(login: Login):
    result = user_manager.login_user(login.email, login.password)
    if not result.get("Success"):
        raise HTTPException(status_code=401, detail=result.get("Message"))
    return {"success": True, "user_id": result["user_id"], "user_name": result["user_name"]}

@app.get("/users")
def get_users():
    return {"success": True, "data": user_manager.get_users()}

# ----------------- Notes Endpoints -----------------
# Create note via multipart form (optional file)
@app.post("/notes")
def create_note(
    content: str = Form(...),
    subject: str = Form(...),
    user_id: int = Form(...),
    file: UploadFile | None = File(default=None)
):
    file_name = None
    file_bytes = None
    if file is not None:
        file_name = file.filename
        file_bytes = file.file.read()
    result = note_manager.add_note(content, "", user_id, subject, str(datetime.utcnow()), file_name=file_name, file_data=file_bytes)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return {"success": True, "data": result["data"]}

@app.get("/notes/user/{user_id}")
def get_user_notes(user_id: int):
    notes = note_manager.get_notes_by_user(user_id)
    return {"success": True, "data": notes}

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    note = note_manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"success": True, "data": note}

# Human-friendly view for QR scan: show content and link to file
@app.get("/notes/view/{note_id}", response_class=HTMLResponse)
def view_note(note_id: int):
    note = note_manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    file_section = ""
    if note.get("file_name"):
        file_section = f"<p><a href=\"/notes/download/{note_id}\">Download file ({note['file_name']})</a></p>"
    html = f"""
    <html>
      <head><title>{note.get('subject','Note')}</title></head>
      <body>
        <h2>{note.get('subject','')}</h2>
        <pre style=\"white-space: pre-wrap; font-family: inherit; border: 1px solid #ddd; padding: 12px;\">{note.get('content','')}</pre>
        {file_section}
      </body>
    </html>
    """
    return HTMLResponse(content=html)

# Download attached file if present
@app.get("/notes/download/{note_id}")
def download_note_file(note_id: int):
    note = note_manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    from src import db
    row = db.get_note_by_id_db(note_id)
    if not row or len(row) < 8 or row[7] is None:
        raise HTTPException(status_code=404, detail="No file for this note")
    file_name = row[6] or "attachment"
    file_bytes = row[7]
    return StreamingResponse(iter([file_bytes]), media_type="application/octet-stream", headers={
        "Content-Disposition": f"attachment; filename=\"{file_name}\""
    })

@app.put("/notes/{note_id}")
def update_note(note_id: int, content: str, user_id: int):
    note = note_manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
    result = note_manager.update_note(note_id, content)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return {"success": True, "data": result["data"]}

@app.put("/notes/{note_id}/qr")
def update_note_qr(note_id: int, qr_code_data: str):
    result = note_manager.update_qr_data(note_id, qr_code_data)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return {"success": True, "data": result["data"]}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, user_id: int):
    note = note_manager.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    result = note_manager.delete_note(note_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return {"success": True, "data": result["data"]}

@app.get("/")
def root():
    return {"message": "STUDYQR API is running!", "routes": ["/register", "/login", "/users", "/notes", "/notes/user/{user_id}", "/notes/{note_id}", "/notes/view/{note_id}", "/notes/download/{note_id}"]}
