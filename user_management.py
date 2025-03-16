from database import create_users_table, connect_db
from log_management import LogManagement
import hashlib

# Call this function once to create the table
create_users_table()

log_manager = LogManagement()

# Hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return "Username already exists."

    # Hash the password and store the user
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    
    #insert REGISTER into logs table
    log_manager.insert_log(username, "REGISTER")
    return "User registered successfully."

# Log in a user
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Retrieve user data
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    
    if user_data and user_data[0] == hash_password(password):
        #insert LOGIN log into logs table
        log_manager.insert_log(username, "LOGIN", "Successful log in")
        return "Login successful."
    else:
        #insert INVALID_LOGIN log into logs table
        log_manager.insert_log(username, "INVALID_LOGIN", "Invalid log in")
        return "Invalid username or password."

# Reset user password
def reset_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        return "User does not exist."
    
    # Hash the new password and update
    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()

    #insert CHANGE log into logs table
    log_manager.insert_log(username, "CHANGE", "Password changed")
    return "Password reset successfully."
