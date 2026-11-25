from pathlib import Path

import streamlit

import backend.postgres_api as postgres
from frontend.post_components import render_post_card

PAGE_SIZE = 10
LOGO_PATH = Path(__file__).parent / "icons" / "chirper_icon.png"

streamlit.set_page_config(layout="wide")

def render_header():
    with streamlit.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
        streamlit.image(str(LOGO_PATH), width=90)
        streamlit.title("Chirper")


@streamlit.dialog("Create a post")
def _create_post_dialog():
    with streamlit.form("create_post_form"):
        content = streamlit.text_area(
            "What would you like to post?", max_chars=255
        )
        submitted = streamlit.form_submit_button("📝 Post")

    if submitted:
        content = content.strip()
        if not content:
            streamlit.error("A post cannot be empty.")
        else:
            streamlit.session_state.created_post_id = postgres.create_post(
                streamlit.session_state.user_id, content
            )
            streamlit.session_state.feed_limit = max(
                streamlit.session_state.get("feed_limit", PAGE_SIZE), PAGE_SIZE
            )
            streamlit.session_state.page = "home"
            streamlit.rerun()


@streamlit.dialog("Write a comment")
def _write_comment_dialog():
    post = postgres.fetch_post_by_id(streamlit.session_state.comment_post_id)
    if post is None:
        streamlit.error("This post could not be found.")
        return

    post_id, username = post[0], post[1]
    streamlit.header(f"Replying to {username}'s post")
    with streamlit.form("write_comment_form"):
        content = streamlit.text_area("Your comment", max_chars=255)
        submitted = streamlit.form_submit_button("💬 Comment")

    if submitted:
        content = content.strip()
        if not content:
            streamlit.error("A comment cannot be empty.")
        else:
            postgres.create_comment(
                post_id, streamlit.session_state.user_id, content
            )
            streamlit.rerun()


def render_sidebar(comments_page=False):
    render_header()
    with streamlit.container():
        streamlit.subheader(f"@{streamlit.session_state.username}")
        if streamlit.button("👤 My profile", use_container_width=True):
            streamlit.session_state.profile_user_id = (
                streamlit.session_state.user_id
            )
            streamlit.session_state.profile_username = (
                streamlit.session_state.username
            )
            streamlit.session_state.page = "profile"
            streamlit.rerun()
        if streamlit.button("🔍 Search for a user", use_container_width=True):
            _search_user_dialog()
        if comments_page:
            if streamlit.button("💬 Write a Comment", use_container_width=True):
                _write_comment_dialog()
            if streamlit.button("⬅️ Back to home", use_container_width=True):
                streamlit.session_state.page = "home"
                streamlit.rerun()
        elif streamlit.button("✏️ Create a post", use_container_width=True):
            _create_post_dialog()
        if streamlit.button("🚪 Log out", use_container_width=True):
            streamlit.session_state.logged_in = False
            streamlit.session_state.page = "login"
            streamlit.session_state.pop("user_id", None)
            streamlit.session_state.pop("username", None)
            streamlit.rerun()


@streamlit.dialog("Search for a user")
def _search_user_dialog():
    with streamlit.form("search_user_form"):
        username = streamlit.text_input("Username")
        submitted = streamlit.form_submit_button("🔍 Search")

    if submitted:
        user = postgres.fetch_user_by_username(username.strip())
        if user is None:
            streamlit.error("No user found with that username.")
        else:
            streamlit.session_state.profile_user_id = user[0]
            streamlit.session_state.profile_username = user[1]
            streamlit.session_state.page = "profile"
            streamlit.rerun()


def render_home_page():
    with streamlit.container(horizontal_alignment="center", width="stretch"):
        sidebar, feed = streamlit.columns([30, 70], width="stretch")
        with sidebar:
            render_sidebar()

        with feed:
            streamlit.header("Your feed")
            limit = streamlit.session_state.get("feed_limit", PAGE_SIZE)
            posts = postgres.fetch_posts_with_counts(limit=limit)
            created_post_id = streamlit.session_state.get("created_post_id")
            if created_post_id is not None:
                created_post = postgres.fetch_post_by_id(created_post_id)
                if created_post is not None:
                    posts = [created_post] + [
                        post for post in posts if post[0] != created_post_id
                    ]
                    posts = posts[:limit]
                streamlit.session_state.pop("created_post_id", None)

            for post in posts:
                with streamlit.container(border=True):
                    render_post_card(post, "home")

            if len(posts) == limit:
                if streamlit.button("⬇️ Load more posts"):
                    streamlit.session_state.feed_limit = limit + PAGE_SIZE
                    streamlit.rerun()
