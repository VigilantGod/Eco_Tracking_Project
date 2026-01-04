import streamlit as st

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

    loginPage = st.Page(page="web_pages/loginPage.py")
    registerPage = st.Page(page="web_pages/registerPage.py")
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