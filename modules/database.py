from sqlalchemy import create_engine,Column,String,Float,ForeignKey,LargeBinary,Boolean,Integer,DateTime
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column
from modules import encrypt
from datetime import datetime
import os

#creates the data directory if not exist
if not os.path.exists("data"):
    os.mkdir("data")

#database url
db_URL = "sqlite:///data/ecotrack.db"
#engine to connect to the database
engine = create_engine(db_URL)
session = sessionmaker(bind=engine)
base = declarative_base()

#Users table
class Users(base):
    __tablename__ = "users"

    username = Column(String,primary_key=True,index=True)
    full_name = Column(LargeBinary,nullable=False)
    phone_number = Column(LargeBinary,nullable=True)
    password = Column(String(128),nullable=False)
    email = Column(LargeBinary,nullable=False)
    is_admin = Column(Boolean,default=False,nullable=False)

class Parcel_Details(base):
    __tablename__ = "parcel_details"

    username = Column(String,ForeignKey("users.username"))
    sender_name = Column(LargeBinary,nullable=False)
    contact_number = Column(LargeBinary,nullable=False)
    parcel_id = Column(String,primary_key=True,nullable=False,index=True)
    parcel_type = Column(LargeBinary,index=True)
    start_loc = Column(LargeBinary,nullable=False)
    end_loc = Column(LargeBinary,nullable=False)
    is_fragile = Column(Boolean,nullable=False)
    is_gift = Column(Boolean,nullable=False)
    description = Column(LargeBinary,nullable=True)

class Routes(base):
    __tablename__ = "routes"

    parcel_id = Column(String,ForeignKey("parcel_details.parcel_id"),primary_key=True,nullable=False)
    username = Column(String,ForeignKey("users.username"))
    route = Column(String,nullable=False)
    distance = Column(Float,nullable=False)
    duration = Column(Integer,nullable=False)
    route_type = Column(String,nullable=False)

class Feedback(base):
    __tablename__ = "feedback"

    feedback_id = Column(String,primary_key=True,nullable=False)
    star_rating = Column(Float)
    feedback = Column(String)

class GPSTracking(base):
    __tablename__ = "gps_tracking"

    id = Column(Integer,primary_key=True,autoincrement=True)
    parcel_id = Column(String,ForeignKey("parcel_details.parcel_id"),nullable=False,index=True)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False)
    timestamp = Column(DateTime,default=datetime.utcnow,nullable=False)
    status = Column(String,nullable=False)

class Tickets(base):
    __tablename__ = "tickets"
    
    ticket_id = Column(String,primary_key=True,nullable=False)
    username = Column(String,ForeignKey("users.username"),nullable=False)
    parcel_id = Column(String,ForeignKey("parcel_details.parcel_id"),nullable=False)
    issue_description = Column(String,nullable=False)
    urgency_level = Column(String,nullable=False)
    status = Column(String,default="Open",nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)

base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns a session of the database
    """
    return session()

def store_route(db,pid:str,user:str,route:str,distance:Float,duration:int,route_type:str):
    new_route = Routes(
        parcel_id = pid,
        username = user,
        route = route,
        distance= distance,
        duration = duration,
        route_type = route_type
    )
    db.add(new_route)
    db.commit()
    db.refresh(new_route)

def store_feedback(db,fd_id:str,stars:float,feedbaack_text:str):
    new_feedback = Feedback(
        feedback_id = fd_id,
        star_rating = stars,
        feedback = feedbaack_text
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

def store_parcel(db,user:str,full_name:str,phone_number:str,parcel_id:str,parcel_type:str,start_loc:str,end_loc:float,is_gift:bool,is_fragile:bool,description:str):
    full_name = encrypt.encrypt_data(full_name)
    phone_number = encrypt.encrypt_data(phone_number)
    parcel_type = encrypt.encrypt_data(parcel_type)
    start_loc = encrypt.encrypt_data(start_loc)
    end_loc = encrypt.encrypt_data(end_loc)
    description = encrypt.encrypt_data(description)

    new_parcel = Parcel_Details(
        username=user,
        sender_name = full_name,
        contact_number = phone_number,
        parcel_id = parcel_id,
        parcel_type=parcel_type,
        start_loc = start_loc,
        end_loc = end_loc,
        is_fragile = is_fragile,
        is_gift = is_gift,
        description =description
        )
    
    db.add(new_parcel)
    db.commit()
    db.refresh(new_parcel)


def  store_user(db,full_name:str,user:str,email:str,phone_number:str,hashed_password:str,is_admin:bool=False):
    """store encrypted user details in the database"""
    full_name = encrypt.encrypt_data(full_name)
    email = encrypt.encrypt_data(email)
    phone_number = encrypt.encrypt_data(phone_number)
    new_user = Users(full_name=full_name,username=user,email=email,phone_number=phone_number,password=hashed_password,is_admin=is_admin)

    db.add(new_user)

    db.commit()

    db.refresh(new_user)
