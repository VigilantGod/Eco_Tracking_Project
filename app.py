import streamlit as st
from  modules import database,auth


st.set_page_config(
    page_title="Ecotrack Logistics",
    page_icon="assets/ico.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
     
def main():
    if "admin_setup_done" not in st.session_state:
        try:
            admin_user = st.secrets["ADMIN_USERNAME"]
            admin_psw = st.secrets["ADMIN_PASSWORD"]
            admin_email = st.secrets["ADMIN_EMAIL"]

            auth.create_user(
                full_name="Administrator",
                username=admin_user,
                email=admin_email,
                phone_number="+0000000000",
                password=admin_psw
            )
            st.session_state.admin_setup_done = True
        except FileNotFoundError:
            print("No admin setup found. Skipping admin user creation.")
        except Exception as e:
            print(f"Error during admin setup: {e}")


    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    dashboard_page = st.Page(page="web_pages/dashboard.py",icon=":material/home:",title="Dashboard")
    admin_dashboard_page = st.Page(page="web_pages/adminDashboard.py",icon=":material/admin_panel_settings:",title="Admin Dashboard")
    login_page = st.Page(page="web_pages/loginPage.py",icon=":material/login:",title="Login")
    register_page = st.Page(page="web_pages/registerPage.py",icon=":material/person_add:",title="Register")
    tracking_page = st.Page("web_pages/trackingPage.py",icon=":material/location_on:",title="Tracking")
    routing_page = st.Page("web_pages/userOrderPage.py",icon=":material/shopping_cart_checkout:",title="Place Order")
    feedback_page = st.Page("web_pages/feedbackPage.py",icon=":material/thumbs_up_down:", title="Feedback")
    ticketing_page = st.Page("web_pages/ticketingPage.py",icon=":material/contact_support:",title="Place Ticket")
    
    if not st.session_state.logged_in:
        pg = st.navigation([login_page, register_page])
        pg.run()
    else:
        if database.get_db().query(database.Users).filter(database.Users.is_admin==True, database.Users.username==st.session_state.user).first():
            pg= st.navigation([admin_dashboard_page, tracking_page,routing_page])
        else:
            pg = st.navigation([dashboard_page, tracking_page, routing_page, feedback_page,ticketing_page])
        with st.sidebar:
            st.write(f"Logged in as {st.session_state.user}")
            logout_bt = st.button("Logout",icon=":material/logout:")
            if logout_bt:
                st.session_state.logged_in = False
                st.rerun()
        pg.run()

if __name__ == "__main__":
    main()