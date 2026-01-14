
import streamlit as st
from auth import login_form, current_user

st.set_page_config(page_title='EOB Posting', page_icon='💳', layout='wide')

if 'user' not in st.session_state:
    login_form()
else:
    st.title('Welcome to EOB Posting')
    user = current_user()
    st.write(f"Logged in as **{user['username']}** ({user['role']})")
    st.page_link('pages/Dashboard.py', label='📊 Dashboard', icon='📊')
    st.page_link('pages/EOB_Audit.py', label='📁 EOB Audit', icon='📁')
    st.page_link('pages/EOB_Details.py', label='📁 EOB Details', icon='📁')
    if user['role'] == 'Admin':
        st.page_link('pages/User_Management.py', label='👥 User Management', icon='👥')
    if st.button('Logout'):
        st.session_state.pop('user', None)
        st.rerun()
