import random
import pandas as pd
from modules import database
from modules import encrypt
from modules import routing

def generate_trackingID():
    """
    generate a ID for a parcel
    returns:
        tracking_id
    """
    suffix = random.randint(100000,999999)
    return f"ECO-{suffix}"

def get_all_parcel_routes():
    """Returns a dataframe of routes Table"""
    db = database.get_db()

    sql_query = db.query(database.Routes).statement

    parcels = pd.read_sql(sql_query,db.bind)

    parcels["route"] = parcels["route"].apply(routing.get_routes_as_list)

    return parcels

def get_all_parcel_details():
    """Return joined decrypted dataframe of parcel details"""

    db = database.get_db()

    sql_query_routes = db.query(database.Routes).statement
    sql_query_parcels = db.query(database.Parcel_Details).statement

    route_df = pd.read_sql(sql_query_routes,db.bind)
    parcel_df = pd.read_sql(sql_query_parcels,db.bind)

    route_df["route"] = route_df["route"].apply(routing.get_routes_as_list)

    encrypted_cols = ["sender_name","contact_number","parcel_type","start_loc","end_loc","description"]
    
    for col in encrypted_cols:
        parcel_df[col] = parcel_df[col].apply(encrypt.decrypt_data)

    complete_parcel_df = parcel_df.merge(route_df,on=["username","parcel_id"],how="left")

    return complete_parcel_df
