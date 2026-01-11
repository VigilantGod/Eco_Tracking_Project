from geopy import Nominatim
import routingpy
import json
from modules.database import store_route
from geopy.exc import GeocoderTimedOut,GeocoderUnavailable

#web api for calculating routes
router = routingpy.OSRM()

geolocator = Nominatim(user_agent="Eco_track_prototype")

def get_routes(start_cords,end_cords,vehicleType="car"):
    """
    returns list of route cordinates for start and end location
    alternative routes are included
    """
    if start_cords is None or end_cords is None:
        return None
    
    cords = [[start_cords.longitude,start_cords.latitude],[end_cords.longitude,end_cords.latitude]]
    routes = router.directions(locations=cords,profile=vehicleType,alternatives=True)

    return routes

def get_cords(location:str):
    """ Returns location cordinates for string location"""
    try:
        return geolocator.geocode(location,timeout=7)
    except(GeocoderUnavailable,GeocoderTimedOut):
        return None

def save_route(db,pid:str,route:list,duration:int,route_type:str):
    """
    Stores a route as a json string and others normally
    """
    store_route(pid=pid,route = json.dumps(route),duration=duration,route_type=route_type)
    

def get_stored_route(db,parcel_id:str):
    """
    Reads json string and return route
    """
    parcel = db.query(db.Routes).get(parcel_id)
    return json.loads(parcel.route)