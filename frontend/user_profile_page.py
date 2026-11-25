import streamlit

import backend.postgres_api as postgres


def _render_posts(posts, empty_message):
    if not posts:
        streamlit.info(empty_message)
        return

    for post_id, username, content in posts:
        with streamlit.container(border=True):
            if streamlit.button(
                f"@{username}",
                key=f"profile_author_{post_id}",
                type="tertiary",
            ):
                user = postgres.fetch_user_by_username(username)
                if user is not None:
                    streamlit.session_state.profile_user_id = user[0]
                    streamlit.session_state.profile_username = user[1]
                    streamlit.rerun()

            streamlit.write(content)
            actions = streamlit.columns(3)
            with actions[0]:
                if streamlit.button("❤️ Like", key=f"profile_like_{post_id}"):
                    postgres.like_post(streamlit.session_state.user_id, post_id)
                    streamlit.rerun()
            with actions[1]:
                if streamlit.button("🔁 Repost", key=f"profile_repost_{post_id}"):
                    postgres.repost_post(streamlit.session_state.user_id, post_id)
                    streamlit.rerun()
            with actions[2]:
                if streamlit.button(
                    "🔖 Bookmark", key=f"profile_bookmark_{post_id}"
                ):
                    postgres.bookmark_post(
                        streamlit.session_state.user_id, post_id
                    )
                    streamlit.rerun()


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
        _render_posts(posts, empty_message)

    with profile_tabs[1]:
        _render_posts(
            postgres.fetch_user_liked_posts(user_id),
            "You have not liked any posts yet."
            if is_own_profile
            else f"This user (@{username}) has not liked any posts yet.",
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
            )
