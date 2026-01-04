import streamlit as st
from modules import auth
from web_pages.login import login

st.title(title="Register to Ecotrack")
with st.form(key='register_form'):
    #user input fields
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    #link for login page
    st.page_link(page="web_pages/regiter.py", label="Already have an account? Login here.")
    submit_button = st.form_submit_button(label='Register')

    if submit_button:
        #get database session
        db = auth.get_db()
        existing_User = db.query(auth.Users).filter(auth.Users.username == username).first()
        if existing_User:
            #checks if the usrname still exists
            st.error("Username already exists. Please choose a different one.")
        else:
            #store user details
            auth.create_user(db, username, password)
            #success message
            st.success("Registration successful! You can now log in.")