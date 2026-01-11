import random

def generate_trackingID():
    """
    generate a ID for a parcel
    returns:
        tracking_id
    """
    suffix = random.randint(100000,999999)
    return f"ECO-{suffix}"

