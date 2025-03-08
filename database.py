import sqlite3

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('users.db')  # Use your database name
    return conn

# Create the users table if it doesn't exist
def create_users_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
