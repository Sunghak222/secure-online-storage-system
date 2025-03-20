import sqlite3
import datetime

"""
1. action:
   - REGISTER
   - LOGIN
   - INVALID_LOGIN
   - CHANGE : change password
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
        """access for admistrator should be implemented"""
        self.cursor.execute("SELECT * FROM logs WHERE username = ?",(username,))

    def close(self):
        """close db"""
        self.conn.close()
