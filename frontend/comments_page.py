import streamlit

import backend.postgres_api as postgres
from frontend.home_page import render_header, render_sidebar
from frontend.post_components import render_post_card


def render_comments_page():
    with streamlit.container(horizontal_alignment="center", width="stretch"):
        render_header()
        sidebar, content = streamlit.columns([30, 70], width=1024)
        with sidebar:
            render_sidebar(comments_page=True)

        with content:
            post_id = streamlit.session_state.get("comment_post_id")
            post = (
                postgres.fetch_post_by_id(post_id)
                if post_id is not None
                else None
            )
            if post is None:
                streamlit.error("This post could not be found.")
                return

            streamlit.header("Post")
            with streamlit.container(border=True):
                render_post_card(post, "comments_original")

            streamlit.header("Comments")
            comments = postgres.fetch_comments_for_post(post_id)
            if not comments:
                streamlit.info("No comments yet. Be the first to comment!")
                return

            for _comment_id, username, content in comments:
                with streamlit.container(border=True):
                    streamlit.markdown(
                        f"**@{username} replying to @{post[1]}'s post**"
                    )
                    streamlit.write(content)
