import streamlit as st
from streamlit_star_rating import st_star_rating
from modules import database
import time
from modules import ticketing

st.title("Provide your feedback")

with st.form(key="feedback_form",clear_on_submit=True):
    st.write(f"### User Name: {st.session_state.user}")
    # 0 = 1 star and 4= 5 stars
    n_stars = st_star_rating(
        label = "Please rate your experience",
        maxValue = 5,
        defaultValue= 1,
        key="rating",
        dark_theme = True
    )
    st.write("#### We value your feedback and Tell us how to improve this app")
    feedbaack_text = st.text_area(" ")

    save_feedback_button = st.form_submit_button("Send Feedback")

if save_feedback_button:
    db = database.get_db()
    database.store_feedback(
        db,
        ticketing.generate_feedbackID(),
        n_stars,
        feedbaack_text=feedbaack_text
        )
    st.success("Feedback sent Successfully")
    time.sleep(0.7)
    
    st.rerun()