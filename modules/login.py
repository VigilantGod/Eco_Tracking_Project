from modules import auth
import streamlit as st
from modules.register import register

registerPage = st.Page(page=register)

def login():
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.page_link(label ="Don't have an account? Register here.",page=registerPage)

        submit_button = st.form_submit_button(label='Login')

        if submit_button:
            db = auth.get_db()
            user = db.query(auth.Users).filter(auth.Users.username == username).first()
            if user and auth.verify_password(password, user.password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.rerun()
                
            else:
                st.error("Invalid username or password.")
