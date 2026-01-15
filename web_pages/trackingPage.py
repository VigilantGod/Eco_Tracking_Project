import streamlit as st
from modules import database,encrypt,map,routing,gps_sim
from streamlit_folium import st_folium
import time
import threading

if "tracking_data" not in st.session_state:
    st.session_state.tracking_data = None
if "parcel_id" not in st.session_state:
    st.session_state.parcel_id = ""

st.title("Track your Parcels")

parcel_id = st.text_input("Enter your Parcel ID:",value=st.session_state.parcel_id)

if st.button("Track"):
    if parcel_id:
        db = database.get_db()

        parcel = db.query(database.Parcel_Details).filter(database.Parcel_Details.parcel_id == parcel_id).first()
        if parcel:
            latest_GPS_entry = db.query(database.GPSTracking).filter(database.GPSTracking.parcel_id == parcel_id).order_by(database.GPSTracking.timestamp.desc()).all()
            parcel_route = db.query(database.Routes).filter(database.Routes.parcel_id == parcel_id).first()

            st.session_state.tracking_data = {
                "parcel": parcel,
                "latest_GPS_entry": latest_GPS_entry if latest_GPS_entry else None,
                "parcel_route": parcel_route,
                "parcel_id": parcel_id
            }
            
        else:
            st.error("Parcel ID not found. Please check and try again.")
            st.session_state.tracking_data = None
    else:
        st.error("Please enter a Parcel ID to track.")

if st.session_state.tracking_data:
    data = st.session_state.tracking_data
    parcel = data["parcel"]
    parcel_route = data["parcel_route"]
    current_parcel_id = data["parcel_id"]

    db = database.get_db()

    latest_GPS_entry = db.query(database.GPSTracking).filter(database.GPSTracking.parcel_id == current_parcel_id).order_by(database.GPSTracking.timestamp.desc()).all()

    if not latest_GPS_entry:
        st.warning("Order placed,hasn't pickup yet")
        route_cords = routing.get_routes_as_list(parcel_route.route)

        cords_list = []
        if route_cords:
            cords_list = [[lat,lon] for lat,lon in route_cords]
        else:
            st.warning("Route isn't calculated")
            st.stop()
            

        new_db_session = database.get_db()
        
        tracking_thread = threading.Thread(
            target=gps_sim.simulate_GPS_tracking,
            args=(
                new_db_session,
                current_parcel_id,
                cords_list,
                parcel_route.duration
            )
        )
        tracking_thread.daemon = True
        tracking_thread.start()

    start_loc = encrypt.decrypt_data(parcel.start_loc)
    end_loc = encrypt.decrypt_data(parcel.end_loc)
    route = routing.get_routes_as_list(parcel_route.route)
    start_cords = [route[0][1],route[0][0]]
    end_cords = [route[-1][1],route[-1][0]]
    latest_location = latest_GPS_entry[0]

    st.success("Success! Parcel Found.")

    st.write(f"### **Parcel ID**: {current_parcel_id}")
    st.write(f"### **Start Location**: {start_loc}")
    st.write(f"### **End Location**: {end_loc}")
    st.write(f"### **Latest Location**: Latitude: {latest_location.latitude}, Longitude: {latest_location.longitude}")
    st.write(f"### **Status:** {latest_location.status}")

    track_map = map.get_map(location=[latest_location.latitude,latest_location.longitude],zoom_start=12,width=800,height=600)
    
    track_map.fit_bounds(bounds=[start_cords,end_cords])

    map.add_routes_to_map(
        folium_map=track_map,
        route_cords=[[lon,lat] for lat,lon in route],
        duration=parcel_route.duration,
        distance=parcel_route.distance,
        label="Parcel Route",
        color="blue"
        )
    map.add_marker_to_map(
        folium_map=track_map,
        location=[latest_location.latitude,latest_location.longitude],
        popup_text=f"Current Location",
        tooltip_text="Current Location",
        icon_color="red",
        icon="truck",
        prefix="fa"
        )
    map.add_marker_to_map(
        folium_map=track_map,
        location=end_cords,
        popup_text=f"Destination",
        tooltip_text="Destination",
        icon_color="green",
        icon="flag"
        )
    
    st_folium(track_map,width=800,height=600)
    
    st.subheader("GPS Tracking History:")
    for loc in latest_GPS_entry:
        st.write(f"#### Time: {loc.timestamp}")
        st.write(f"####  Latitude: {loc.latitude} | Longitude: {loc.longitude} ")
    
    if latest_location.status != "Delivered":
        time.sleep(2)
        st.rerun()

    
