import streamlit as st
from modules import map
from streamlit_folium import st_folium
from modules.database import store_parcel,get_db
from modules.tracking import generate_trackingID
from modules import routing


def format_time(duration_sec):
    hours = int(duration_sec // 3600)
    mins = int((duration_sec% 3600)// 60)

    if hours >0:
        return f"{hours}h {mins}min"
    return f"{mins} min"
            
def show_route(route):
    st.subheader(f"{route["label"]}")

    st.metric(label="Distance",value=f"{route["distance"]/1000} Km")

    st.metric(label="Duration",value = format_time(route["duration"]))

    truck_emission = round(0.192  * route["distance"],2)
    
    st.metric(label = "Co2 emitted",value=f"{truck_emission}kg")

if not "order_step" in st.session_state:
    st.session_state.order_step = 0

if not "map" in st.session_state:
    st.session_state.map = map.get_map(location = [6.885015752177213,79.91146087646486],zoom_start = 13,width = 700,height=500)

if not "routes" in st.session_state:
    st.session_state.routes = None

if st.session_state.order_step == 0:
    st.title("Place an Order")

    with st.form(key="Parcel Form"):
        full_name = st.text_input(label="Enter Full Name")
        ph_number = st.text_input(label="Enter phone number",placeholder="+94XX XXX XXXX" )
        parcel_type = st.selectbox(label="Enter Parcel Type",options=["Sanitory","Toys","Foods","Accesseries","Aparel","Electronics"])
        start_location = st.text_input(label="Where From")
        end_location = st.text_input(label="Where to")

        weight = st.number_input(label="Weight(kg)")
        
        col1,col2 = st.columns(2)
        with col1:
            fragile = st.selectbox(label = "Is it Fragile?",options=["No","Yes"])
        with col2:    
            gift  = st.selectbox(label="Is it a Gift?",options=["No","Yes"])

        description = st.text_area(label="Description of the parcel")

        
        confirm_button = st.form_submit_button("Place Order")

        if  confirm_button:
            if not all([full_name,ph_number,parcel_type,start_location,end_location,weight,description]):
                st.error("Fill all the feilds to continue")
            else:
                parcel_id = generate_trackingID()
                user = st.session_state.user
                start_cords = routing.get_cords(start_location)
                end_cords = routing.get_cords(end_location)

                if start_cords is None or end_cords is None:
                    st.error("Coudn't Find the location.Check your internet connection")

                st.session_state.routes = routing.get_routes(start_cords=start_cords,end_cords=end_cords)

                if st.session_state.routes is None:
                    st.error("Problem with getting locations")
                else:
                    store_parcel(
                        get_db(),
                        user=user,
                        full_name=full_name,
                        phone_number=ph_number,
                        parcel_id=parcel_id,
                        parcel_type=parcel_type,
                        start_loc=start_location,
                        end_loc=end_location,
                        is_fragile=True if fragile == "Yes" else False,
                        is_gift=True if gift == "Yes" else False,
                        description=description
                        )

                    st.success("Successfully saved parcel details")

                    st.session_state.order_step += 1
                

elif st.session_state.order_step == 1:
    st.title("Select Route")
    
    
    route_list = []
    count_routes = 0
    for index,route in enumerate(st.session_state.routes):   
        duration_sec = route.duration
        distance_meters = route.distance
        route_cords = route.geometry

        route_list.append({
            "duration": duration_sec,
            "distance":distance_meters,
            "route":route_cords,
            "label":"Standard Route"
        })
        count_routes += 1
    
    sorted_by_time = sorted(route_list,key=lambda x:x["duration"])
    sorted_by_time[0]["label"] = "Fastest Route"

    sorted_by_dist = sorted(route_list,key=lambda x: x["distance"])
    sorted_by_dist[0]["label"] = "Eco-Friendly Route"

    if count_routes == 0:
        st.write_stream("Coudn't find any routes,Cannot Proceed")
    elif count_routes == 1:
        route = sorted_by_dist[0]
        show_route(route=route)
    elif count_routes == 2:
        col1,col2 = st.columns(2)

        route1 = sorted_by_dist[0]
        route2 = sorted_by_dist[-1]

        with col1:
            show_route(route1)
        with col2:
            show_route(route2)
    else:
        col1,col2,col3 = st.columns(3)
        
        with col1:
            route1 = sorted_by_time[0]
            show_route(route1)
        with col2:
            route2 = sorted_by_dist[0]
            show_route(route2)
        with col3:
            route3 = sorted_by_dist[-1]
            show_route[route3]

