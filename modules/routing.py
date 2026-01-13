from geopy import Nominatim
import routingpy
import json
from modules.database import store_route

#web api for calculating routes
router = routingpy.OSRM()

geolocator = Nominatim(user_agent="Eco_track_prototype")

def get_routes(start_cords,end_cords):
    """
    returns list of route cordinates for start and end location
    alternative routes are included
    """
    if start_cords is None or end_cords is None:
        return None
    start_lon_lat = [start_cords[1],start_cords[0]]
    end_lon_lat = [end_cords[1],end_cords[0]]
    cords = [start_lon_lat,end_lon_lat]
    try:
        routes = router.directions(locations=cords,alternatives=True)
    except:
        return None
    return routes

def get_cords(location:str):
    """ Returns location cordinates for string location"""
    try:
        location = geolocator.geocode(location,timeout=3)
        return [location.latitude,location.longitude]
    except:
        return None

def save_route(db,pid:str,user:str,route:list,duration:int,distance:float,route_type:str):
    """
    Stores a route as a json string and others normally
    """
    store_route(db,pid=pid,route = json.dumps(route),user=user,duration=duration,distance=distance,route_type=route_type)
    
def get_routes_as_list(routes):
    """Returns routes as list of lists"""
    return json.loads(routes)


def get_stored_route(db,parcel_id:str):
    """
    Reads json string and return route
    """
    parcel = db.query(db.Routes).get(parcel_id)
    return json.loads(parcel.route)