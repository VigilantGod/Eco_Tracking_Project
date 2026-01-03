import streamlit as st
from modules import auth

loginPage = st.Page("modules/login.py")

def register():
    with st.form(key='register_form'):
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        st.page_link(page=loginPage, label="Already have an account? Login here.")
        submit_button = st.form_submit_button(label='Register')

        if submit_button:
            db = auth.get_db()
            existing_User = db.query(auth.Users).filter(auth.Users.username == username).first()
            if existing_User:
                st.error("Username already exists. Please choose a different one.")
            else:
                auth.create_user(db, username, password)
                
                st.success("Registration successful! You can now log in.")