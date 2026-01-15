import streamlit as st
from modules import map,database,routing,encrypt,gps_sim
from streamlit_folium import st_folium
from modules.tracking import generate_trackingID
import time

def format_time(duration_sec):
    """Formats Time"""
    hours = int(duration_sec // 3600)
    mins = int((duration_sec % 3600)// 60)

    if hours >0:
        return f"{hours}h {mins}min"
    return f"{mins} min"
            
def show_route(route):
    """Show route detail in app"""
    st.subheader(f"{route['label']}")

    st.metric(label="Distance",value=f"{route['distance']/1000} Km")

    st.metric(label="Duration",value = format_time(route["duration"]))

    truck_emission = round(0.192  * route["distance"],2)
    
    st.metric(label = "Co2 emitted",value=f"{truck_emission}kg")

def update_selection(selected_index:int,total_routes):
    """Updates select selection"""
    st.session_state.route_ind = selected_index

    for i in range(total_routes):
        key_name = f"route_{i}"
        if i == selected_index:
            st.session_state[key_name] = True
        else:
            st.session_state[key_name] = False
def parcel_form():
    st.session_state.fitted_bounds = False
    st.session_state.line_added_maps = False

    st.title("Place an Order")
    from_user_details = st.toggle("Your details")
    with st.form(key="Parcel Form"):
            if from_user_details:
                db = database.get_db()
                user_details = db.query(database.Users).filter(database.Users.username==st.session_state.user).first()
                full_name = encrypt.decrypt_data(user_details.full_name)
                ph_number = encrypt.decrypt_data(user_details.phone_number)
                st.write(f"Full Name : {full_name}")
                st.write(f"Phone Number : {ph_number}")
            else:
                full_name = st.text_input(label="Enter Full Name")
                ph_number = st.text_input(label="Enter phone number",placeholder="+94XX XXX XXXX" )
            
            parcel_type = st.selectbox(label="Enter Parcel Type",options=["Sanitory","Toys","Foods","Accesseries","Aparel","Electronics"])
            start_location = st.text_input(label="Where From")
            end_location = st.text_input(label="Where to")

            weight = st.number_input(label="Weight(kg)",step=0.25,min_value=0,format="%.2f")
            
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
            st.session_state.parcel_id = generate_trackingID()
            user = st.session_state.user
            start_cords = routing.get_cords(start_location)
            end_cords = routing.get_cords(end_location)

            if start_cords is None or end_cords is None:
                st.error("Coudn't Find the location.Check your spelling")
            if st.session_state.fitted_bounds == False:
                st.session_state.map.fit_bounds(bounds=[start_cords,end_cords],padding=(50,50),max_zoom=15)
            
            st.session_state.routes = routing.get_routes(start_cords=start_cords,end_cords=end_cords)

            if st.session_state.routes is None:
                st.error("Problem with getting locations")
            else:
                database.store_parcel(
                    database.get_db(),
                    user=user,
                    full_name=full_name,
                    phone_number=ph_number,
                    parcel_id=st.session_state.parcel_id,
                    parcel_type=parcel_type,
                    start_loc=start_location,
                    end_loc=end_location,
                    is_fragile=True if fragile == "Yes" else False,
                    is_gift=True if gift == "Yes" else False,
                    description=description
                    )

                st.success("Successfully saved parcel details")
                st.toast("Successfully saved parcel details")
                st.session_state.order_step += 1
                time.sleep(0.5)
                st.rerun()

def start_delivery(route):
    def simulation_threading(parcel_id,route_cords,duration):
        thread_db = database.get_db()

        try:
            gps_sim.simulate_GPS_tracking(
                db=thread_db,
                parcel_id=parcel_id,
                route_cords=route_cords,
                duration=duration
                )
        except Exception as e:
            print(f"Error in GPS simulation thread: {e}")
        finally:
            thread_db.close()

    import threading

    cords_list = [[lat,lon] for lon,lat in route["route"]]

    tracking_thread = threading.Thread(
        target=simulation_threading,
        args=(
            st.session_state.parcel_id,
            cords_list,
            route["duration"])
            )

    tracking_thread.daemon= True
    tracking_thread.start()
    
def route_selection(show_route, update_selection):
    st.title("Select Route")
    
    
    route_list = []
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

    sorted_by_time = sorted(route_list,key=lambda x:x["duration"])
    sorted_by_time[0]["label"] = "Fastest Route"

    sorted_by_dist = sorted(route_list,key=lambda x: x["distance"])
    sorted_by_dist[0]["label"] = "Eco-Friendly Route"

    colors ={
            "Fastest Route":"#0f36c0",
            "Eco-Friendly Route": "#2fc00f",
            "Standard Route":"#c0190f"
        }
    
    if st.session_state.line_added_maps == False:        
        for i in range(len(route_list) if len(route_list) <= 3 else 3):
            route = route_list[i]
            route_cords = [[lat,lon] for lon,lat in route["route"]]
            map.add_routes_to_map(
                st.session_state.map,
                route_cords=route_cords,
                distance=route["distance"],
                duration=route["duration"],
                label = route["label"],
                color = colors[route["label"]]
                )
            
    st.session_state.line_added_maps = True
        
    cols = st.columns(len(route_list))

    for i,(col,route) in enumerate(zip(cols,route_list)):
        with col:
            show_route(route)

            color = colors[route["label"]]
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <div style="width: 16px; height: 16px; background-color: {color}; 
                                border-radius: 50%; border: 2px solid white;"></div>
                    <h3 style="margin: 0;"></h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.checkbox(
                "Select Route",
                key=f"route_{i}",
                on_change=update_selection,
                args=(i,len(route_list))
                )
    st_folium(st.session_state.map)        

    confirm_button = st.button("Confirm Selection",use_container_width=True)
    
    if confirm_button:
        route = route_list[st.session_state.route_ind]
        start_delivery(route)
        routing.save_route(
            db=database.get_db(),
            pid=st.session_state.parcel_id,
            user=st.session_state.user,
            route=route["route"],
            distance=route["distance"],
            duration=route["duration"],
            route_type= route["label"]
            )
        st.session_state.parcel_id = None
        st.success("Successfully saved route")
        st.toast("Successfully saved route")
        st.session_state.order_step = 0
        time.sleep(0.5)
        st.rerun()

if not "order_step" in st.session_state:
    st.session_state.order_step = 0

if not "map" in st.session_state:
    st.session_state.map = map.get_map(location = [6.885015752177213,79.91146087646486],zoom_start = 13,width = 700,height=500)

if not "routes" in st.session_state:
    st.session_state.routes = None

if not "route_ind" in st.session_state:
    st.session_state.route_ind = 0

if not "parcel_id" in st.session_state:
    st.session_state.parcel_id = None

if not "fitted_bounds" in st.session_state:
    st.session_state.fitted_bounds = False

if not "line_added_maps" in st.session_state:
    st.session_state.line_added_maps = False

def main(show_route, update_selection, parcel_form, route_selection):
    if st.session_state.order_step == 0:
        parcel_form()                   

    elif st.session_state.order_step == 1:
        route_selection(show_route, update_selection)

#starting point
main(show_route, update_selection, parcel_form, route_selection)