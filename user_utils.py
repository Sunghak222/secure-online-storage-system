from database import connect_db

def get_user_role(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return user_data[0]
    return None

def get_user_secret(username):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT secret FROM users WHERE username = ?", (username,))
    user_secret = cursor.fetchone()

    conn.close()

    return user_secret[0] if user_secret else None
