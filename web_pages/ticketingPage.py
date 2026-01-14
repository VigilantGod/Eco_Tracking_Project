import streamlit as st
from modules import database,ticketing


st.title("Ticketing Page")

with st.form(key="ticket_form"):
    username = st.session_state.user

    parcel_id = st.text_input("Parcel ID")
    issue_description = st.text_area("Issue Description")
    related_issue = st.selectbox("Related Issue", ["Parcel Arrived Late", "Parcel is Damaged", "Parcel is Missing","Bad Service"])
    
    submit_button = st.form_submit_button(label="Submit Ticket")

    if submit_button:
        if not all(username,parcel_id,related_issue,issue_description):
            st.warning("Please fill all the fields")
        else:
            db = database.get_db()

            ticketing.store_tickets(
                db = db,
                username = username,
                parcel_id= parcel_id,
                issue_description= issue_description,
                realated_issue= related_issue
                )
            
            st.success("Submitted the ticket")
            

            
