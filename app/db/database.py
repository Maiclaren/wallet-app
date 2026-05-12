import sqlite3

class Database:
    def __init__(self, db_name = "wallet_app.db"):
        self.db_name = db_name
        self.create_users_table()
    
    def connect(self):
        return sqlite3.connect(self.db_name)
    
    #Δημιουργία πίνακα users (αν δεν υπάρχει) με unique username
    def create_users_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    #Δημιουργία χρήστη με return True - False 
    def create_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?,?)",
                (username,password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    #Έλεγχος εύρεσης ή μη χρήστη με fetchone και return 
    def validate_user(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username,password)
        )
        user = cursor.fetchone()
        conn.close()
        return user is not None
