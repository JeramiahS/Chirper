import psycopg


def get_database_connection():
    return psycopg.connect(
        "dbname=chirper user=jeramiah password=2142 host=localhost port=5432",
        autocommit=True,
    )


def create_user(username, password):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id",
                (username, password),
            )
            return cursor.fetchone()[0]


def create_post(author_id, content):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO posts (author_id, content) VALUES (%s, %s) RETURNING post_id",
                (author_id, content),
            )
            return cursor.fetchone()[0]


def create_comment(post_id, author_id, content):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO comments (post_id, author_id, content) VALUES (%s, %s, %s)",
                (post_id, author_id, content),
            )


def reply_to_comment(comment_id, author_id, content):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO replies (comment_id, author_id, content) VALUES (%s, %s, %s)",
                (comment_id, author_id, content),
            )


def reply_to_reply(parent_reply_id, author_id, content):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO replies (parent_reply_id, author_id, content) VALUES (%s, %s, %s)",
                (parent_reply_id, author_id, content),
            )


def like_post(user_id, post_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM likes WHERE user_id = %s AND post_id = %s",
                (user_id, post_id),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)",
                    (user_id, post_id),
                )


def repost_post(user_id, post_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM reposts WHERE user_id = %s AND post_id = %s",
                (user_id, post_id),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO reposts (user_id, post_id) VALUES (%s, %s)",
                    (user_id, post_id),
                )


def bookmark_post(user_id, post_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM bookmarks WHERE user_id = %s AND post_id = %s",
                (user_id, post_id),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO bookmarks (user_id, post_id) VALUES (%s, %s)",
                    (user_id, post_id),
                )


def follow_user(follower_id, follows_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO follows (follower_id, follows_id) VALUES (%s, %s)",
                (follower_id, follows_id),
            )


def fetch_user_for_login_authentication(username):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT username, password FROM users WHERE username = %s",
                (username,),
            )
            return cursor.fetchone()


def fetch_user_by_username(username):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, username, password FROM users WHERE username = %s",
                (username,),
            )
            return cursor.fetchone()


def fetch_posts(limit=10, offset=0):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content
                FROM posts JOIN users ON users.user_id = posts.author_id
                ORDER BY posts.post_id DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return cursor.fetchall()


def fetch_posts_with_counts(limit=10, offset=0):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content,
                    (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM reposts WHERE reposts.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM bookmarks WHERE bookmarks.post_id = posts.post_id)
                FROM posts
                JOIN users ON users.user_id = posts.author_id
                ORDER BY posts.post_id DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return cursor.fetchall()


def fetch_post_by_id(post_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content,
                    (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM reposts WHERE reposts.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM bookmarks WHERE bookmarks.post_id = posts.post_id)
                FROM posts
                JOIN users ON users.user_id = posts.author_id
                WHERE posts.post_id = %s
                """,
                (post_id,),
            )
            return cursor.fetchone()


def fetch_comments_for_post(post_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT comments.comment_id, users.username, comments.content
                FROM comments
                JOIN users ON users.user_id = comments.author_id
                WHERE comments.post_id = %s
                ORDER BY comments.comment_id
                """,
                (post_id,),
            )
            return cursor.fetchall()


def fetch_user_posts(user_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content,
                    (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM reposts WHERE reposts.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM bookmarks WHERE bookmarks.post_id = posts.post_id)
                FROM posts
                JOIN users ON users.user_id = posts.author_id
                WHERE posts.author_id = %s
                ORDER BY posts.post_id DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()


def fetch_user_liked_posts(user_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content,
                    (SELECT COUNT(*) FROM likes AS post_likes WHERE post_likes.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM reposts WHERE reposts.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM bookmarks WHERE bookmarks.post_id = posts.post_id)
                FROM likes
                JOIN posts ON posts.post_id = likes.post_id
                JOIN users ON users.user_id = posts.author_id
                WHERE likes.user_id = %s
                ORDER BY posts.post_id DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()


def fetch_user_reposted_posts(user_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content,
                    (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM reposts AS post_reposts WHERE post_reposts.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM bookmarks WHERE bookmarks.post_id = posts.post_id)
                FROM reposts
                JOIN posts ON posts.post_id = reposts.post_id
                JOIN users ON users.user_id = posts.author_id
                WHERE reposts.user_id = %s
                ORDER BY posts.post_id DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()


def fetch_user_bookmarked_posts(user_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT posts.post_id, users.username, posts.content,
                    (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM reposts WHERE reposts.post_id = posts.post_id),
                    (SELECT COUNT(*) FROM bookmarks AS post_bookmarks WHERE post_bookmarks.post_id = posts.post_id)
                FROM bookmarks
                JOIN posts ON posts.post_id = bookmarks.post_id
                JOIN users ON users.user_id = posts.author_id
                WHERE bookmarks.user_id = %s
                ORDER BY posts.post_id DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()


def fetch_user_comments(user_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT users.username, comments.content
                FROM comments JOIN users ON users.user_id = comments.author_id
                WHERE comments.author_id = %s
                ORDER BY comments.comment_id DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()


def delete_user(username):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))


def delete_post(post_id):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
