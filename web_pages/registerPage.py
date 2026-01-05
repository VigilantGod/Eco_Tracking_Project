import streamlit as st
from modules import database
from modules import auth


st.title("Register to Ecotrack")

with st.form(key='register_form'):
    #user input fields
    username = st.text_input("Choose a Username")
    email = st.text_input("Enter your email")
    phone_number = st.text_input("Enter your phone",placeholder="+94 XXX XXXX")
    password = st.text_input("Choose a Password", type="password")
    #link for login page
    st.page_link(page="web_pages/registerPage.py", label="Already have an account? Login here.")

    submit_button = st.form_submit_button(label='Register')

    if submit_button:
        #get database session
        db = database.get_db()
        validate_phone_number = auth.validate_phone_number(phone_number=phone_number)
        existing_User = db.query(database.Users).filter(database.Users.username == username).first()
        if existing_User:
            #checks if the usrname still exists
            st.error("Username already exists. Please choose a different one.")
        elif not auth.validate_email(email=email):
            st.error("Given email is not valid")
        elif not auth.validate_phone_number(phone_number=phone_number):
            st.warning("Given phone number is not valid")
        else:
            #store user details
            auth.create_user( username,email,phone_number, password)
            #success message
            st.success("Registration successful! You can now log in.")