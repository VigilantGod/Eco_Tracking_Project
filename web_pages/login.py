from modules import auth
import streamlit as st
import time


def login():
    """
    Renders the login page
    """
st.title("Log in to EcoTrack")
with st.form(key='login_form'):
    #User input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    #link for registration page
    st.page_link(label ="Don't have an account? Register here.",page="web_pages/register.py")

    submit_button = st.form_submit_button(label='Login')

    if submit_button:
        #get database session
        db = auth.get_db()
        #get user from database
        user = db.query(auth.Users).filter(auth.Users.username == username).first()
        if user and auth.verify_password(password, user.password):
            st.success("Login successful!")
            #To ensure user don't have to login everytime UI component change occurs
            st.session_state.logged_in = True
            #to get time to show the success message
            time.sleep(0.3)
            st.rerun()
                
        else:
            #error msg if password is wrong
            st.error("Invalid username or password.")
