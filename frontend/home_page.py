from pathlib import Path

import streamlit

import backend.postgres_api as postgres

PAGE_SIZE = 10
LOGO_PATH = Path(__file__).parent / "icons" / "chirper_icon.png"


def _show_profile(user_id, username):
    streamlit.session_state.profile_user_id = user_id
    streamlit.session_state.profile_username = username
    streamlit.session_state.page = "profile"
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
            _show_profile(user[0], user[1])


def render_home_page():
    header_columns = streamlit.columns([1, 5])
    with header_columns[0]:
        streamlit.image(str(LOGO_PATH), width=90)
    with header_columns[1]:
        streamlit.title("Chirper")

    sidebar, feed = streamlit.columns([1, 3])
    with sidebar:
        streamlit.subheader(f"@{streamlit.session_state.username}")
        if streamlit.button("👤 My profile", use_container_width=True):
            _show_profile(
                streamlit.session_state.user_id,
                streamlit.session_state.username,
            )
        if streamlit.button("🔍 Search for a user", use_container_width=True):
            _search_user_dialog()
        if streamlit.button("🚪 Log out", use_container_width=True):
            streamlit.session_state.logged_in = False
            streamlit.session_state.page = "login"
            streamlit.session_state.pop("user_id", None)
            streamlit.session_state.pop("username", None)
            streamlit.rerun()

    with feed:
        streamlit.header("Your feed")
        limit = streamlit.session_state.get("feed_limit", PAGE_SIZE)
        posts = postgres.fetch_posts(limit=limit)
        for post_id, username, content in posts:
            with streamlit.container(border=True):
                if streamlit.button(
                    f"@{username}",
                    key=f"post_author_{post_id}",
                    type="tertiary",
                ):
                    user = postgres.fetch_user_by_username(username)
                    if user is not None:
                        _show_profile(user[0], user[1])
                streamlit.write(content)
                actions = streamlit.columns(3)
                with actions[0]:
                    if streamlit.button("❤️ Like", key=f"like_{post_id}"):
                        postgres.like_post(
                            streamlit.session_state.user_id, post_id
                        )
                        streamlit.rerun()
                with actions[1]:
                    if streamlit.button("🔁 Repost", key=f"repost_{post_id}"):
                        postgres.repost_post(
                            streamlit.session_state.user_id, post_id
                        )
                        streamlit.rerun()
                with actions[2]:
                    if streamlit.button("🔖 Bookmark", key=f"bookmark_{post_id}"):
                        postgres.bookmark_post(
                            streamlit.session_state.user_id, post_id
                        )
                        streamlit.rerun()

        if len(posts) == limit:
            if streamlit.button("⬇️ Load more posts"):
                streamlit.session_state.feed_limit = limit + PAGE_SIZE
                streamlit.rerun()
