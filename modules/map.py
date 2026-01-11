import folium
from geopy import Nominatim
import routingpy
from streamlit_js_eval import get_geolocation
import geocoder

geolocator = Nominatim(user_agent="student_eco_track_project")

def get_location():
    """returns tuple of location cords and Accuracy"""
    location = get_geolocation()
    #if coudn't get location this will return None
    if location and "cords" in location:
        longitude = location["coords"]["longitude"]
        latitude = location["coords"]["latitude"]
        userLocation = [latitude,longitude]

        accuracy = location["coords"]["accuracy"]
        
        return  (userLocation,accuracy)
    return None
    
def get_map(location,zoom_start:int,width:int,height:int):
    """"
    Returns a map Object
    """
    if location is None:
        return None
    return folium.Map(location=location,zoom_start=zoom_start,width=width,height=height)
