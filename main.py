import streamlit

import frontend.home_page as home_page
import frontend.login_page as login_page
import frontend.registration_page as registration_page
import frontend.user_profile_page as user_profile_page


streamlit.session_state.setdefault("logged_in", False)
streamlit.session_state.setdefault("page", "login")

if not streamlit.session_state.logged_in:
    if streamlit.session_state.page == "register":
        registration_page.render_registration_page()
    else:
        login_page.render_login_page()
elif streamlit.session_state.page == "profile":
    user_profile_page.render_user_profile_page()
else:
    streamlit.session_state.page = "home"
    home_page.render_home_page()
