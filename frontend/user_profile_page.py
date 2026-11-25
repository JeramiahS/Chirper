import streamlit

import backend.postgres_api as postgres
from frontend.post_components import render_post_card


def _render_posts(posts, empty_message, key_prefix):
    if not posts:
        streamlit.info(empty_message)
        return

    for post in posts:
        with streamlit.container(border=True):
            render_post_card(post, key_prefix)


def render_user_profile_page():
    user_id = streamlit.session_state.profile_user_id
    username = streamlit.session_state.profile_username
    is_own_profile = user_id == streamlit.session_state.user_id

    if streamlit.button("⬅️ Back to home"):
        streamlit.session_state.page = "home"
        streamlit.rerun()

    streamlit.title(f"{username}'s Profile Page")
    tabs = ["Posts", "Liked posts", "Comments"]
    if is_own_profile:
        tabs.append("Bookmarks")
    profile_tabs = streamlit.tabs(tabs)

    with profile_tabs[0]:
        posts = postgres.fetch_user_posts(user_id)
        empty_message = (
            "You have not made any posts yet."
            if is_own_profile
            else f"This user (@{username}) has not made any posts yet."
        )
        _render_posts(posts, empty_message, "profile_posts")

    with profile_tabs[1]:
        _render_posts(
            postgres.fetch_user_liked_posts(user_id),
            "You have not liked any posts yet."
            if is_own_profile
            else f"This user (@{username}) has not liked any posts yet.",
            "profile_liked",
        )

    with profile_tabs[2]:
        comments = postgres.fetch_user_comments(user_id)
        if not comments:
            streamlit.info(
                "You have not made any comments yet."
                if is_own_profile
                else f"This user (@{username}) has not made any comments yet."
            )
        else:
            for author, content in comments:
                with streamlit.container(border=True):
                    streamlit.markdown(f"**@{author} commented:**")
                    streamlit.write(content)

    if is_own_profile:
        with profile_tabs[3]:
            _render_posts(
                postgres.fetch_user_bookmarked_posts(user_id),
                "You have not bookmarked any posts yet.",
                "profile_bookmarks",
            )
