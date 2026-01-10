import folium
from geopy import Nominatim
import routingpy
from streamlit_js_eval import get_geolocation
import geocoder


def getLocation():
    """returns tuple of location cords and Accuracy"""
    location = get_geolocation()
    #if coudn't get location this will return None
    if location:
        longitude = location["coords"]["longitude"]
        latitude = location["coords"]["latitude"]
        userLocation = [latitude,longitude]

        accuracy = location["coords"]["accuracy"]
        
        return  (userLocation,accuracy)

def get_map(location,zoom_start:int,width:int,height:int):
    return folium.Map(location=location,zoom_start=zoom_start,width=width,height=height)
def getLocationAproximately():
    g_ip = geocoder.ip("me")
    return g_ip.latlng