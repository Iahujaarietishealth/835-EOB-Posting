
import streamlit as st
import bcrypt
from db import fetch_one, execute

# User CRUD helpers

def get_user_by_username(username: str):
    return fetch_one('SELECT * FROM public."EOB835UserMaster" WHERE username=:u', {'u': username})


def create_user(username: str, password: str, role: str):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    execute('INSERT INTO public."EOB835UserMaster" (username, password_hash, role) VALUES (:u,:p,:r)',
            {'u': username, 'p': password_hash, 'r': role})


def update_user_role(user_id: int, role: str, active: bool):
    execute('UPDATE public."EOB835UserMaster" SET role=:r, active=:a WHERE id=:id', {'r': role, 'a': active, 'id': user_id})


def delete_user(user_id: int):
    execute('DELETE FROM public."EOB835UserMaster" WHERE id=:id', {'id': user_id})


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def login_form():
    st.title('EOB Posting — Login')
    with st.form('login_form', clear_on_submit=False):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')
    if submitted:
        user = get_user_by_username(username)
        if not user:
            st.error('Invalid username or password')
            return False
        if not user['active']:
            st.error('User is inactive')
            return False
        if verify_password(password, user['password_hash']):
            st.session_state['user'] = dict(user)
            st.success(f"Welcome, {user['username']} ({user['role']})")
            st.switch_page('pages/Dashboard.py')
            return True
        else:
            st.error('Invalid username or password')
            return False


def require_login():
    if 'user' not in st.session_state:
        st.switch_page('app.py')


def current_user():
    return st.session_state.get('user')

