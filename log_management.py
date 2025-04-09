import sqlite3
import datetime
from user_utils import get_user_role

"""
1. action:
   - REGISTER
   - LOGIN
   - INVALID_LOGIN
   - INVALID OTP
   - CHANGE : change password
   - FAILED_CHANGE : change failed
   - UPLOAD
   - UPLOAD_FAIL
   - DOWNLOAD 
   - DOWNLOAD_FAIL
   - LOGOUT
"""
class LogManagement:
    def __init__(self, name = "logs.db"):
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_log_table()
        
    def create_log_table(self):
        """Create logs table"""
        """timestamp is automatically set"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                content TEXT
            )
        """)

        self.conn.commit()
    
    def insert_log(self, username, action, content):
        """insert log by username and action"""
        self.cursor.execute("INSERT INTO logs (username, action, content) VALUES (?, ?, ?)", (username, action, content))
        self.conn.commit()
    
    def get_log(self, username):
        
        role = get_user_role(username)
        if role == "administrator":
            self.cursor.execute("SELECT * FROM logs")
        else:
            self.cursor.execute("SELECT * FROM logs WHERE username = ?",(username,))
        
        rows = self.cursor.fetchall()
        
        return rows


    def close(self):
        """close db"""
        self.conn.close()
