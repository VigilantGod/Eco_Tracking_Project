import streamlit as st
from  modules import database,tracking,ticketing


st.title("Your Parcels")

user_parcel_df = tracking.get_parcel_details_for_admins()

tabs = st.tabs(["Parcel Details","Tickets"])

with tabs[0]:
    st.dataframe(user_parcel_df)

with tabs[1]:
    low_df,medium_df,high_df = ticketing.get_tickets_by_urgency_admins()

    st.subheader("High Urgency Tickets")

    st.dataframe(high_df)

    st.subheader("Medium Urgency Tickets")

    st.dataframe(medium_df)

    st.subheader("Low Urgency Tickets")

    st.dataframe(low_df)