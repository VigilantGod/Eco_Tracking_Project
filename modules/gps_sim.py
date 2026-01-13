import time
from datetime import datetime,timezone
from modules.database import GPSTracking
import random
def inject_GPS_points_route(route_cords,num_points=20):
    """
    injects GPS points to simulate moveing through the route
    """
    if len(route_cords) < 2:
        return route_cords
    
    injected = []
    #each codinate space between route is now a part
    total_parts = len(route_cords) - 1
    #how much points per part
    points_per_part = num_points // total_parts

    for i in range(len(route_cords)-1):
        start = route_cords[i]
        end = route_cords[i+1]

        for j in range(points_per_part):
            ratio = j / points_per_part
            lat = start[0] + (end[0] - start[0]) * ratio
            lon = start[1] + (end[1] - start[1]) * ratio
            injected.append([lat,lon])
    # add the last point
    injected.append(route_cords[-1])
    
    return injected

def save_GPS_loc(db,parcel_id:str,lat,lon,status:str):
    """Saves a given GPS location to database"""
    tracking_entry = GPSTracking(
        id = random.randint(1,10000),
        parcel_id = parcel_id,
        latitude = lat,
        longitude = lon,
        status = status
    )
    db.add(tracking_entry)
    db.commit()
    db.refresh(tracking_entry)

def delivery_status(progress_percent:float):
    """ Returns delivery status based on progess percentage of the delivery"""
    if progress_percent < 10:
        return "Ready for Pickup"
    elif progress_percent < 90:
        return "Delivery in Progress"
    elif progress_percent < 100:
        return "Out for Delivery"
    else:
        return "Delivered"
    
def simulate_GPS_tracking(db,parcel_id:str,route_cords:list,duration:int):
    """Simulates GPS tracking by injecting points and saving them to database"""
    gps_points = inject_GPS_points_route(route_cords,num_points=30)

    update_interval = 10#duration / len(gps_points)

    for i,(lat,lon) in enumerate(gps_points):
        progress_percent = (i+1) / len(gps_points) * 100
        status = delivery_status(progress_percent)
        save_GPS_loc(db,parcel_id,lat,lon,status)
        #simulate moving with a certain speed based on the duration
        time.sleep(update_interval)