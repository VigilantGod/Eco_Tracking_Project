from sqlalchemy import create_engine,Column,String,Float,ForeignKey,LargeBinary
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column
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
    phone_number = Column(LargeBinary,nullable=True)

class Parcel_Details(base):
    __tablename__ = "parcel_details"

    username = Column(String,ForeignKey("users.username"))
    parcelId = Column(LargeBinary,primary_key=True,nullable=False,index=True)
    parcel_type = Column(LargeBinary,index=True)
    start_loc_lat = Column(Float,nullable=False)
    start_loc_lon = Column(Float,nullable=False)
    end_loc_lat = Column(Float,nullable=False)
    end_loc_lon = Column(Float,nullable=False)
    is_fragile = Column(String,nullable=False)
    is_gift = Column(String,nullable=False)
    description = Column(LargeBinary,nullable=True)

base.metadata.create_all(bind=engine)

def get_db():
    """
    Returns a session of the database
    """
    return session()

def  store_user(db,full_name:str,user:str,email:str,phone_number:str,hashed_password:str):
    """store a user details in the database"""
    new_user = Users(full_name=full_name,username=user,email=email,phone_number=phone_number,password=hashed_password)
    #add new_user to the temporary memory of db
    db.add(new_user)
    #permenently saving details
    db.commit()
    #reloads the db so it will get the most recent data
    db.refresh(new_user)
    return new_user
