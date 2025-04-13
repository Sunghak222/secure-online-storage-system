import sqlite3

class FileManager:
    def __init__(self, db_name="files.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shared_files (
                owner TEXT NOT NULL,
                filename TEXT NOT NULL,
                shared_name TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def share_file(self, owner, filename, recipient):
        self.cursor.execute("INSERT INTO shared_files (owner, filename, shared_name) VALUES (?, ?, ?)",
                            (owner, filename, recipient))
        self.conn.commit()

    def has_access(self, username, filename):
        self.cursor.execute("""
            SELECT 1 FROM shared_files 
            WHERE (owner = ? AND filename = ?) 
               OR (shared_name = ? AND filename = ?)
        """, (username, filename, username, filename))
        return self.cursor.fetchone() is not None

    def get_files_shared_with(self, recipient):
        self.cursor.execute("""
            SELECT filename FROM shared_files WHERE shared_name = ?
        """, (recipient,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def is_owner(self, username, filename):
        self.cursor.execute("""
            SELECT 1 FROM shared_files WHERE owner = ? AND filename = ?
        """, (username, filename))
        return self.cursor.fetchone() is not None


    def close(self):
        self.conn.close()
