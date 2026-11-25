import streamlit
import psycopg

import backend.postgres_api as postgres

@streamlit.cache_resource
def get_database_connection():
    return psycopg.connect(
        "dbname=chirper user=jeramiah password=2142 host=localhost port=5432",
        autocommit=True
    )

def render_home_page():
    posts = postgres.fetch_posts()
    render_header()
    render_sidebar()
    render_posts(posts)


def logout():
    streamlit.session_state.logged_in = False
    streamlit.rerun()

def render_header():
    streamlit.title("Chirper", text_alignment="center")

def render_sidebar():
    with streamlit.sidebar:
        streamlit.title("Chirper")
        streamlit.write("## Admin")  # TODO: Replace this with the logged in user's username
        streamlit.button("Profile")
        streamlit.button("Search")
        streamlit.button("Log Out", on_click=logout)

def render_posts(posts):
    for post_id, username, content in posts:
        with streamlit.container(border=True):
            streamlit.markdown(f"**@{username}**")
            streamlit.write(content)
            streamlit.button("Like", key=f"like_post{post_id}")
            streamlit.button("Repost", key=f"repost_post{post_id}")