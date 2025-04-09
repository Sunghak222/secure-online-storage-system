from database import create_users_table, connect_db
from log_management import LogManagement
import bcrypt
import pyotp

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
    admin_secret = pyotp.random_base32()
    cursor.execute("INSERT INTO users (username, password, role, secret) VALUES (?, ?, ?, ?)", (admin_username, hashed_password, "administrator", admin_secret))
    conn.commit()
    log_manager.insert_log(admin_username, "REGISTER", "Administrator account created.")
    print("User registered successfully.\nYour OTP key is " + admin_secret) #gotta tell secret to user
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
    secret = pyotp.random_base32() #secret key for otp

    cursor.execute("INSERT INTO users (username, password,role, secret) VALUES (?, ?, ?, ?)", 
                   (username, hashed_password,"basic", secret))
    conn.commit()
    conn.close()
    
    log_manager.insert_log(username, "REGISTER" , "User registered successfully.")  
    return f"User registered successfully.\nYour OTP key is {secret}" #gotta tell secret to user

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    
    if user_data and bcrypt.checkpw(password.encode(), user_data[0]):
        return "Login successful."
    else:
        return "Invalid username or password."

def reset_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        return "User does not exist."
    
    secret = pyotp.random_base32()

    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ?, secret = ? WHERE username = ?", (hashed_password, secret, username))
    conn.commit()
    conn.close()

    return "Password reset successfully."
