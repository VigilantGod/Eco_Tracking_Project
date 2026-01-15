import streamlit as st
from  modules import database,tracking,ticketing


st.title("Dashboard")

tabs = st.tabs(["Your Parcels","Your Tickets"])


user_parcel_df = tracking.get_parcel_details_for_users(st.session_state.user)
user_ticket_df = ticketing.get_ticket_for_users(st.session_state.user)

with tabs[0]:
    st.subheader("Your Parcels")
    st.dataframe(user_parcel_df)

with tabs[1]:
    st.subheader("Your Tickets")
    st.dataframe(user_ticket_df)