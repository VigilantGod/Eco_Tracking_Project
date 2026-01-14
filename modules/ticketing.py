import streamlit as st
from modules import database
import random
import pandas as pd

@st.cache_data
def get_urgecy(related_issue):
    urgency = {
        "Parcel Arrived Late":"Low",
          "Parcel is Damaged":"Medium",
            "Parcel is Missing":"High",
            "Bad Service":"Low"
            }

def generate_feedbackID():

    """
    Generates a ID for feedbacks
    returns:
        feedback_id
    """
    suffix = random.randint(100000,999999)

    return f"FD-{suffix}"

def generate_ticketingID():
    """Genearates a ID for tracking tickets(problems)"""
    suffix = random.randint(100000,999999)
    
    return f"TK-{suffix}"

def store_tickets(db,username:str,parcel_id:str,issue_description:str,related_issue:str):

    ticket_id = generate_ticketingID()
    new_ticket = database.Tickets(
        ticket_id = ticket_id,
        username = username,
        parcel_id = parcel_id,
        issue_description = issue_description,
        urgency_level = get_urgecy(related_issue)
    )
    db.add(new_ticket)
    db.commit()
    return ticket_id

def get_tickets_by_urgency_admins():
    """returns tuple of dataframes(low,medium,high urgency)"""

    db = database.get_db()

    sql_statement_ticket = db.query(database.Tickets).statement

    ticket_df = pd.read_sql(sql_statement_ticket,db.bind)

    low_urg_df = ticket_df[ticket_df["urgency_level"] == "Low"]
    medium_urg_df = ticket_df[ticket_df["urgency_level"] == "Medium"]
    high_urg_df = ticket_df[ticket_df["urgency_level"] == "High"]

    return (low_urg_df,medium_urg_df,high_urg_df)

def get_ticket_for_users(user:str):
    """"return all the ticket details submitted by user"""

    db = database.get_db()

    sql_statement_ticket = db.query(database.Tickets).filter(database.Tickets.username).statement

    ticket_user_df = pd.read_sql(sql_statement_ticket,db.bind)

    return ticket_user_df[["ticket_id","parcel_id","urgency_level","issue_description","status","created_at"]] 
