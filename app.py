import streamlit as st

st.set_page_config(
    page_title="Ecotrack Logistics",
    page_icon="assets/ico.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
def main():

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    loginPage = st.Page(page="web_pages/loginPage.py",icon=":material/login:",title="Login")
    registerPage = st.Page(page="web_pages/registerPage.py",icon=":material/person_add:",title="Register")
    trackingPage = st.Page("web_pages/trackingPage.py",icon=":material/location_on:",title="Tracking")
    routingPage = st.Page("web_pages/userOrderPage.py",icon=":material/route:",title="Place Order")
    feedbackPage = st.Page("web_pages/FeedbackPage.py",icon=":material/confirmation_number:", title="Feedback")
    
    if not st.session_state.logged_in:
        pg = st.navigation([loginPage, registerPage])
        pg.run()
    else:
        pg = st.navigation([trackingPage, routingPage, feedbackPage])
        with st.sidebar:
            st.write(f"Logged in as {st.session_state.user}")
            logout_bt = st.button("Logout",icon=":material/logout:")
            if logout_bt:
                st.session_state.logged_in = False
                st.rerun()
        pg.run()

if __name__ == "__main__":
    main()