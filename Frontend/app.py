import streamlit as st
import requests
import qrcode
from io import BytesIO

API_URL = "https://predatorily-hyperopic-kimber.ngrok-free.dev"  # Replace with your ngrok URL

st.set_page_config(page_title="STUDYQR", layout="wide")

# ---------------- Session State ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None

# ---------------- QR Code Generator ----------------
def generate_qr_image(data):
    qr_img = qrcode.make(data)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    return buf.getvalue()

# ---------------- Sidebar Menu ----------------
menu = ["My Notes", "View Note by QR", "Admin: Users"] if st.session_state.logged_in else ["Home", "Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Home ----------------
if choice == "Home":
    st.subheader("Welcome to STUDYQR App!")
    st.info("Please login or register to start.")

# ---------------- Login ----------------
elif choice == "Login":
    st.subheader("🔑 User Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if email and password:
                try:
                    # Always use json= for FastAPI Pydantic models
                    res = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = data["user_id"]
                        st.session_state.user_name = data["user_name"]
                        st.success(f"✅ Welcome {st.session_state.user_name}!")
                        st.rerun()  # refresh sidebar immediately
                    else:
                        st.error(res.json().get("detail", "Login failed."))
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("⚠ Please enter email and password.")

# ---------------- Register ----------------
elif choice == "Register":
    st.subheader("📝 Register New User")
    with st.form("register_form"):
        user_name = st.text_input("User Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            if user_name and email and password:
                try:
                    res = requests.post(f"{API_URL}/register", json={
                        "username": user_name,
                        "email": email,
                        "password": password
                    })
                    if res.status_code in [200, 201]:
                        st.success("✅ Registration successful! Please login.")
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Registration failed."))
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("⚠ Fill all fields!")

# ---------------- My Notes ----------------
elif choice == "My Notes" and st.session_state.logged_in:
    st.subheader(f"📝 {st.session_state.user_name}'s Notes")

    # --- Add New Note ---
    with st.expander("Add New Note"):
        with st.form("add_note_form"):
            subject = st.text_input("Subject")
            content = st.text_area("Note Content")
            uploaded_file = st.file_uploader("Upload File (optional)")
            if st.form_submit_button("Add Note & Generate QR"):
                if subject and content:
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.read())} if uploaded_file else None
                        payload = {"subject": subject, "content": content, "user_id": st.session_state.user_id}
                        res = requests.post(f"{API_URL}/notes", data=payload, files=files)
                        if res.status_code in [200, 201]:
                            note = res.json()["data"]
                            note_id = note["Id"]
                            st.success(f"✅ Note {note_id} added successfully!")
                            note_url = f"{API_URL}/notes/view/{note_id}"
                            st.image(generate_qr_image(note_url), width=200)
                            st.text_input("Copy this link:", note_url, key=f"add_link_{note_id}")
                        else:
                            st.error(res.json().get("detail", "Failed to add note."))
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("⚠ Subject and content are required.")

    # --- Existing Notes ---
    st.subheader("Existing Notes")
    try:
        res = requests.get(f"{API_URL}/notes/user/{st.session_state.user_id}")
        if res.status_code == 200:
            notes = res.json().get("data", [])
            if notes:
                for n in notes:
                    note_id = n["Id"]
                    st.markdown(f"*Note ID:* {note_id} | *Subject:* {n.get('subject','')}")
                    st.code(n.get("content",""))

                    note_url = f"{API_URL}/notes/view/{note_id}"
                    st.image(generate_qr_image(note_url), width=150)
                    st.text_input("Link:", note_url, key=f"link_{note_id}")

                    # Download file if exists
                    if n.get("file_name"):
                        file_res = requests.get(f"{API_URL}/notes/download/{note_id}", stream=True)
                        if file_res.status_code == 200:
                            st.download_button(
                                label=f"Download File ({n['file_name']})",
                                data=file_res.content,
                                file_name=n["file_name"]
                            )

                    # Edit / Delete
                    with st.expander("Edit / Delete Note"):
                        new_content = st.text_area("Update Content", value=n.get("content",""), key=f"edit_{note_id}")
                        if st.button("Update", key=f"update_{note_id}"):
                            requests.put(f"{API_URL}/notes/{note_id}", params={"content": new_content, "user_id": st.session_state.user_id})
                            st.success("✅ Note updated!")
                            st.rerun()
                        if st.button("Delete", key=f"delete_{note_id}"):
                            requests.delete(f"{API_URL}/notes/{note_id}", params={"user_id": st.session_state.user_id})
                            st.success("✅ Note deleted!")
                            st.rerun()
                    st.markdown("---")
            else:
                st.info("No notes found.")
        else:
            st.error("Failed to fetch notes.")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- View Note by QR ----------------
elif choice == "View Note by QR":
    st.subheader("🔍 View Note by ID")
    note_id_input = st.number_input("Note ID", min_value=1, step=1)
    if st.button("Fetch Note"):
        try:
            res = requests.get(f"{API_URL}/notes/{note_id_input}")
            if res.status_code == 200:
                note = res.json().get("data", {})
                st.markdown(f"*Subject:* {note.get('subject','')}")
                st.code(note.get("content",""))

                note_url = f"{API_URL}/notes/view/{note['Id']}"
                st.image(generate_qr_image(note_url), width=200)
                st.text_input("Link:", note_url, key=f"view_link_{note['Id']}")

                if note.get("file_name"):
                    file_res = requests.get(f"{API_URL}/notes/download/{note_id_input}", stream=True)
                    if file_res.status_code == 200:
                        st.download_button(
                            label=f"Download File ({note['file_name']})",
                            data=file_res.content,
                            file_name=note["file_name"]
                        )
            else:
                st.error("Note not found.")
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- Admin Users ----------------
elif choice == "Admin: Users" and st.session_state.logged_in:
    st.subheader("👥 Admin Users Management")
    try:
        res_users = requests.get(f"{API_URL}/users")
        if res_users.status_code == 200:
            users = res_users.json().get("data", [])
            for u in users:
                st.markdown(f"*User ID:* {u.get('Id')} | Name: {u.get('User_Name')} | Email: {u.get('email')}")
                res_notes = requests.get(f"{API_URL}/notes/user/{u.get('Id')}")
                if res_notes.status_code == 200:
                    notes = res_notes.json().get("data", [])
                    for n in notes:
                        st.markdown(f"- Note ID: {n['Id']} | Subject: {n.get('subject','')}")
                st.markdown("---")
        else:
            st.error("Failed to fetch users.")
    except Exception as e:
        st.error(f"Error: {e}")
