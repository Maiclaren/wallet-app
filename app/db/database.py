import sqlite3

class Database:
    def __init__(self, db_name = "wallet_app.db"):
        self.db_name = db_name
        self.create_users_table()
        self.create_exchanges_table()
        self.create_tasks_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    #Δημιουργούμε πίνακα exchanges (αν δεν υπάρχει) που στεγάζει τα revenues & expenses
    def create_exchanges_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchanges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exchange_type TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        conn.close()

    #Δημιουργία συνάρτησης για την καταχώρηση εγγραφών σε exchanges
    def create_exchange(self, user_id, exchange_type, amount, date, category, description):
        conn = self.connect()
        cursor = conn.cursor()
        #try-finally ώστε να σκάσει αναίμακτα
        try:
            cursor.execute("""
                INSERT INTO exchanges (
                    user_id, exchange_type, amount, date, category, 
                    description     
                ) VALUES (?, ?, ?, ?, ?, ?);  
            """, (user_id, exchange_type, amount, date, category, description))
            conn.commit()
        finally:
            conn.close()

    #Def για να επιστρέφω τα exchanges ανά user (στο inspect Frame της gui)
    def get_user_exchanges(self,user_id):
        conn = self.connect()
        cursor =conn.cursor()
        cursor.execute("""
            SELECT id, user_id, exchange_type, amount, date, category, description
            FROM exchanges WHERE user_id = ? ORDER BY date DESC
        """,(user_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    #Με αυτή θα διαγράφω όλο το record που επιλέγω σε exchange
    def delete_exchange(self, record_id):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM exchanges WHERE id = ?",(record_id,))
            conn.commit()
        finally:
            conn.close()

    #Με αυτή θα διαγράφω όλο το record που επιλέγω σε task
    def delete_task(self, record_id):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tasks WHERE id = ?",(record_id,))
            conn.commit()
        finally:
            conn.close()
            
    #Δημιουργούμε πίνακα tasks (αν δεν υπάρχει) που στεγάζει τα obligations & wishlist
    def create_tasks_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_type TEXT NOT NULL,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                link TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        conn.close()
    
    #Δημιουργία συνάρτησης για την καταχώρηση εγγραφών σε tasks
    def create_task(self, user_id, task_type, name, amount, date, status, link):
        conn = self.connect()
        cursor = conn.cursor()
        #try-finally ώστε να σκάσει αναίμακτα
        try:
            cursor.execute("""
                INSERT INTO tasks (
                    user_id, task_type, name, amount, date, status, link)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (user_id, task_type, name, amount, date, status, link))
            conn.commit()
        finally:
            conn.close()

    #Def για να επιστρέφω τα tasks ανά user (στο inspect Frame της gui)
    def get_user_tasks(self,user_id):
        conn = self.connect()
        cursor =conn.cursor()
        cursor.execute("""
            SELECT id, user_id, task_type, name, amount, date, status, link
            FROM tasks WHERE user_id = ? ORDER BY date DESC
        """,(user_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    

    #Δημιουργούμε πίνακα users (αν δεν υπάρχει) με unique username
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
        return user
