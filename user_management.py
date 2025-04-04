from database import create_users_table, connect_db
from log_management import LogManagement
import bcrypt

create_users_table()

log_manager = LogManagement()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(),salt)

admin_username = "administrator"
admin_password = "administrator"

conn = connect_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE username = ?", (admin_username,))
if not cursor.fetchone():
    hashed_password = hash_password(admin_password)
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (admin_username, hashed_password,"administrator"))
    conn.commit()
    log_manager.insert_log(admin_username, "REGISTER", "Administrator account created.")
    print("Administrator account created successfully.")
else:
    print("Administrator account already exists.")

conn.close()

def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return "Username already exists."

    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password,role) VALUES (?, ?, ?)", (username, hashed_password,"basic"))
    conn.commit()
    conn.close()
    
    log_manager.insert_log(username, "REGISTER" , "User registered successfully.")  
    return "User registered successfully."

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    
    if user_data and bcrypt.checkpw(password.encode(), user_data[0]):
        log_manager.insert_log(username, "LOGIN", "Successful log in")
        return "Login successful."
    else:
        log_manager.insert_log(username, "INVALID_LOGIN", "Invalid log in")
        return "Invalid username or password."

def reset_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        return "User does not exist."
    
    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()

    log_manager.insert_log(username, "CHANGE", "Password changed")
    return "Password reset successfully."

# def get_user_role(username):
#     conn = connect_db()
#     cursor = conn.cursor()
    
#     cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
#     user_data = cursor.fetchone()
    
#     conn.close()
    
#     if user_data:
#         return user_data[0]
#     return None
