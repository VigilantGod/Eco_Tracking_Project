import streamlit as st
from modules import auth,tracking,routing,ticketing
from modules.login import login
from modules.register import register
st.set_page_config(
    page_title="Ecotrack Logistics",
    page_icon="assets/ico.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
def main():
    st.title("Welcome to Ecotrack Logistics")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    loginPage = st.Page(page=login,title="Login in to Ecotrack")
    registerPage = st.Page(page=register)
    trackingPage = st.Page("modules/tracking.py")
    routingPage = st.Page("modules/routing.py")
    ticketingPage = st.Page("modules/ticketing.py")
    
    if not st.session_state.logged_in:
        pg = st.navigation([loginPage, registerPage])
        pg.run()
    else:
        pg = st.navigation([trackingPage, routingPage, ticketingPage])
        pg.run()

if __name__ == "__main__":
    main()