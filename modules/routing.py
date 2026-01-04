from geopy import Nominatim
import routingpy

#web api for calculating routes
router = routingpy.OSRM()

geolocator = Nominatim(user_agent="Eco_track_prototype")

def get_routes(start_cords,end_cords,vehicleType):
    """
    returns list of route cordinates for start and end location
    alternative routes are included
    """
    cords = [[start_cords.longitude,start_cords.latitude],[end_cords.longitude,end_cords.latitude]]
    routes = router.directions(locations=cords,profile=vehicleType,alternatives=True)

    return routes

def get_cords(location:str):
    """ Returns location cordinates for string location"""
    return geolocator.geocode(location)
