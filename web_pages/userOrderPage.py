import streamlit as st


st.title("Place an Order")

with st.form(key="Parcel Form"):
    st.text_input(label="Enter Full Name")
    st.text_input(label="Enter phone number",placeholder="+94 XXX XXXX")
    st.selectbox(label="Enter Parcel Trype",options=["Sanitory","Toys","Foods","Accesseries","Gift","Aparel","Electronics"])
    st.text_input(label="Where should we get the package?")
    st.text_input(label="Where do you wan't to send the Package?")
    sub_button = st.form_submit_button("Confirm Order")