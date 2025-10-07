import sqlite3

# --- Persistent database ---
conn = sqlite3.connect("studyqr.db", check_same_thread=False)
cursor = conn.cursor()

# --- Users table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    User_Name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

# --- Notes table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    qr_code_data TEXT,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    created_at TEXT NOT NULL,
    file_name TEXT,
    file_data BLOB,
    FOREIGN KEY(user_id) REFERENCES users(Id)
)
""")
conn.commit()

# --- User operations ---
def add_user_db(user_name, email, password_hash, created_at):
    try:
        cursor.execute(
            "INSERT INTO users (User_Name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (user_name, email, password_hash, created_at)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        return cursor.fetchone(), None
    except Exception as e:
        return None, str(e)

def get_user_by_email_db(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone()

def get_all_users_db():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Note operations ---
def add_note_db(content, qr_code_data, user_id, subject, created_at, file_name=None, file_data=None):
    try:
        cursor.execute(
            "INSERT INTO notes (content, qr_code_data, user_id, subject, created_at, file_name, file_data) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (content, qr_code_data, user_id, subject, created_at, file_name, file_data)
        )
        conn.commit()
        cursor.execute("SELECT * FROM notes WHERE Id = last_insert_rowid()")
        return cursor.fetchone(), None
    except Exception as e:
        return None, str(e)

def get_notes_by_user_db(user_id):
    cursor.execute("SELECT * FROM notes WHERE user_id=?", (user_id,))
    return cursor.fetchall()

def get_note_by_id_db(note_id):
    cursor.execute("SELECT * FROM notes WHERE Id=?", (note_id,))
    return cursor.fetchone()

def update_note_db(note_id, new_content):
    try:
        cursor.execute("UPDATE notes SET content=? WHERE Id=?", (new_content, note_id))
        conn.commit()
        return get_note_by_id_db(note_id), None
    except Exception as e:
        return None, str(e)

def update_note_qr_db(note_id, qr_code_data):
    try:
        cursor.execute("UPDATE notes SET qr_code_data=? WHERE Id=?", (qr_code_data, note_id))
        conn.commit()
        return get_note_by_id_db(note_id), None
    except Exception as e:
        return None, str(e)

def delete_note_db(note_id):
    try:
        note = get_note_by_id_db(note_id)
        cursor.execute("DELETE FROM notes WHERE Id=?", (note_id,))
        conn.commit()
        return note, None
    except Exception as e:
        return None, str(e)
