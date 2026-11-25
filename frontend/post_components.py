import streamlit

import backend.postgres_api as postgres


def _show_profile(username):
    user = postgres.fetch_user_by_username(username)
    if user is not None:
        streamlit.session_state.profile_user_id = user[0]
        streamlit.session_state.profile_username = user[1]
        streamlit.session_state.page = "profile"
        streamlit.rerun()


def _open_comments(post_id):
    streamlit.session_state.comment_post_id = post_id
    streamlit.session_state.page = "comments"
    streamlit.rerun()


def render_post_card(post, key_prefix):
    (
        post_id,
        username,
        content,
        like_count,
        comment_count,
        repost_count,
        bookmark_count,
    ) = post

    if streamlit.button(
        f"@{username}",
        key=f"{key_prefix}_author_{post_id}",
        type="tertiary",
    ):
        _show_profile(username)

    streamlit.write(content)
    action_data = (
        ("❤️ Like", like_count, "like", postgres.like_post),
        ("💬 Comment", comment_count, "comment", None),
        ("🔁 Repost", repost_count, "repost", postgres.repost_post),
        ("🔖 Bookmark", bookmark_count, "bookmark", postgres.bookmark_post),
    )
    for row_start in range(0, len(action_data), 2):
        actions = streamlit.columns(2)
        for column, (label, count, name, action) in zip(
            actions, action_data[row_start : row_start + 2]
        ):
            with column:
                button_column, count_column = streamlit.columns([5, 1])
                with button_column:
                    clicked = streamlit.button(
                        label,
                        key=f"{key_prefix}_{name}_{post_id}",
                        use_container_width=True,
                    )
                with count_column:
                    streamlit.markdown(
                        f"<div style='padding-top: 0.45rem'>{count}</div>",
                        unsafe_allow_html=True,
                    )
                if clicked:
                    if name == "comment":
                        _open_comments(post_id)
                    else:
                        action(streamlit.session_state.user_id, post_id)
                        streamlit.rerun()
