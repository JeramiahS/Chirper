import frontend.login_page as login_page
import frontend.home_page as home_page

import streamlit

# Gatekeeper: Stop execution if not logged in
if not streamlit.session_state.logged_in:
    login_page.render_login_page()
    streamlit.stop()

home_page.render_home_page()