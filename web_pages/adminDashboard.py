import streamlit as st
from  modules import database,tracking


st.title("Your Parcels")

user_parcel_df = tracking.get_parcel_details_for_admins()

st.dataframe(user_parcel_df)