# Study QR

Study QR is a Python project designed to help students create, manage, and share study notes efficiently using QR codes. The project leverages FastAPI for building a robust backend, Supabase as a scalable cloud database, and Streamlit to provide an interactive and user-friendly frontend. Study QR enables users to quickly access and share notes by scanning QR codes, making studying and collaboration seamless.

# Features

- User Registration and Login
- Add, Edit, and View Notes
- Automatic QR Code Generation for each note
- Interactive Streamlit Dashboard for managing notes and QR codes
- Secure cloud storage of notes using Supabase
- Quick access and sharing of notes via QR codes

# Project Structure 

STUDQR/
|
|---src/            # Core Application logic 
|   |__logic.py     # Buisness logic and task operations 
|   |__db.py        # Database operations
|---API/            # Backend API
|   |__main.py      # FastAPI endpoints
|---Frontend/       # Frontend application 
|   |__app.py       # Streamlit web interface
|
|___requirements.txt  # Python Dependencies 
|
|___README.md       # Project Documentation
|
|___.env            # Pyhton Variables 

# Quick Start

## Prerequisites

- python 3.8 or higher 
- A supabase account
- Git(push,cloning)

### 1. clone or Download the project 

# Option 1 : Clone with Gt
git clone <repository-url>

# Option 2 : Downoload and extract the ZIP file

### 2. Install Dependencies

# Install all require dpython packages 
pip install -r requirements.txt

### 3. Set Up supabse Database

1. Create a supabase Project :

2. Create the Tasks Table :

- Go to the SQL editor in Supabase Dashboard
- Run this SQL command :

```sql
CREATE TABLE Users (
    Id INTEGER PRIMARY KEY,
    User_Name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Notes (
    Id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    qr_code_data TEXT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(Id) ON DELETE CASCADE
);

```
3. Get your credentials :


### 4. Configure Environmental variables

1. create a '.new' file in the project root
2. Add your Supabase credentials to '.env' :
    SUPABASE_URL=your_project_url_here
    SUPABASE_key=your_anon_key_here

**Example:**
    SUPABASE_URL = "https://vjqnyahwffqgbevanldk.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqcW55YWh3ZmZxZ2JldmFubGRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODM1MjQsImV4cCI6MjA3MzY1OTUyNH0.z4CQonHNDhqxhFmAn2AhDl6-3mEkmHpFEeLnc4ANmZI"

### 5. Run the Application 

# Streamlit Frontend 
streamlit run frontend/app.py

The app wil open in your browser at `http://localhost:8501`

# FastAPI Backend

cd api 
python main.py

The API wil be open at browser `http://localhost:8000`

# How to use

# Technical Details
 
### Technologies used 

- **Frontend** : Streamlit (Python web frame work)
- **Backend** : FastAPI(Python REST API framework)
- **Database** : Supabase(PostgreSQL-based-backend-as-a-service)
- **Language** : Python 3.8+

### Key components

1. **`src/db.py`** : Database Operations - handle all CRUD Operations with Supabase
2. **`src/logic.py`** : Business logic - Task validation and processing
3. **`API/main.py`** : FastAPI endpoints – user registration, login, and note CRUD operations.
4. **`Frontend/app.py`** : Streamlit dashboard – allows users to add, edit, view notes, and scan QR codes.
5. **`requirements.txt`** : Python dependencies required for backend and frontend.
6. **`.env`** : Environment variables – stores Supabase URL and API Key.

### Troubleshooting

# Common Issues

1. **Module Not found error** :
    - Make sure you've installed all dependencies : `pip install -r requirements.txt`
    - Check that you're running commnands from the correct directory

### Future Enhancements 

Ideas for extending these project :

- **User Authentication** : Add user acounts and login
- **Task Categories** : Organize tasks by subject or categories
- **Notifications** : Email or push notifications for due details
- **File Attachments** : Attach files to tasks
- **Collaboration** : Share tasks with classmates 
- **Mobile App** : React native or Flutter mobile version
- **Data Export** : Export tasks to CSV or PDF
- **Task Templates** : Create reusable task templates

### Support 

If you encounter any issues are have questions :
    - Contact number : 7396086980
    - email : bendasreeja@gmail.com