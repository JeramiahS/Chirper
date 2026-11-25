import psycopg

def get_database_connection():
    return psycopg.connect(
        "dbname=chirper user=jeramiah password=2142 host=localhost port=5432",
        autocommit=True
    )

# CREATE
def create_user(username, password):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password)
        )

def create_post(author_id, content):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO POSTS (author_id, content) VALUES (%s, %s)", (author_id, content)
        )

def reply_to_comment(comment_id, author_id, content):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO replies (comment_id, author_id, content) VALUES (%s, %s, %s)", (comment_id, author_id, content)
        )

def reply_to_reply(parent_reply_id, author_id, content):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO replies (parent_reply_id, author_id, content) VALUES (%s, %s, %s)", (parent_reply_id, author_id, content)
        )

def like_post(user_id, post_id):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)", (user_id, post_id)
        )

def repost_post(user_id, post_id):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO reposts (user_id, post_id) VALUES (%s, %s)", (user_id, post_id)
        )

def bookmark_post(user_id, post_id):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO bookmarks (user_id, post_id) VALUES (%s, %s)", (user_id, post_id)
        )

def follow_user(follower_id, follows_id):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "INSERT INTO follows (follower_id, follows_id) VALUES (%s, %s)", (follower_id, follows_id)
        )

# READ
def fetch_user_for_login_authentication(username):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "SELECT username, password FROM users WHERE username = %s", username
        )
        return cursor.fetchone()

def fetch_posts():
    with get_database_connection().cursor() as cursor:
        cursor.execute("""
            SELECT posts.post_id, users.username, posts.content
            FROM posts JOIN users ON user_id = posts.author_id
            ORDER BY posts.post_id DESC
        """)
        return cursor.fetchall()

# TODO: Create a function that fetches all posts that a user has liked for display within that user's profile

# TODO: Create a function that fetches all posts that a user has reposted for display within that user's profile

# TODO: Create a function that fetches all posts that a user has bookmarked for display within that user's profile

# TODO: Create a function that fetches all comments that a user has made to a post from another user for display within that user's profile

# UPDATE

# DELETE
def delete_user(username):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "DELETE FROM users WHERE username = %s", username
        )


def delete_post(post_id):
    with get_database_connection().cursor() as cursor:
        cursor.execute(
            "DELETE FROM posts WHERE post_id = %s", post_id
        )