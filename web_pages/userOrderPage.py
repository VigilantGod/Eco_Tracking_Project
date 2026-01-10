import streamlit as st
from modules import map
from streamlit_folium import st_folium



if not "map" in st.session_state:
    st.session_state.map = map.get_map(location = [6.885015752177213,79.91146087646486],zoom_start = 13,width = 700,height=500)

def switch_CheckBox():
    st.session_state.fragile = True if st.session_state.fragile == True  else False
    st.session_state.not_fragile = True if st.session_state.fragile == False else True

st.title("Place an Order")

st_data = st_folium(st.session_state.map,key="place_order_map")

with st.form(key="Parcel Form"):
    full_name = st.text_input(label="Enter Full Name")
    ph_number = st.text_input(label="Enter phone number",placeholder="+94 XXX XXXX")
    parcel_type = st.selectbox(label="Enter Parcel Trype",options=["Sanitory","Toys","Foods","Accesseries","Aparel","Electronics"])
    start_location = st.text_input(label="Where From")
    end_location = st.text_input(label="Where to")

    weight = st.number_input(label="Weight(kg)")
    
    col1,col2 = st.columns(2)
    with col1:
        fragile = st.selectbox(label = "Is it Fragile?",options=["No","Yes"])
    with col2:    
        gift  = st.selectbox(label="Is it a Gift?",options=["No","Yes"])

    description = st.text_area(label="Description of the parcel")

    
    confirm_button = st.form_submit_button("Confirm Order")

    if  confirm_button:
        if not all([full_name,ph_number,parcel_type,start_location,end_location,weight,fragile,gift,description]):
            st.error("Fill all the feilds to continue")
        else:
            pass
            
