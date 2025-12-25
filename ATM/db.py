
import sqlite3

class Database:
    def __init__(self, db_name='atm.db'):
        self.db_name = db_name
        self.create_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                pin TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_pin TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_pin) REFERENCES users(pin)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, name, pin, balance=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, pin, balance) VALUES (?, ?, ?)",
                (name, pin, balance)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, pin):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, pin, balance FROM users WHERE pin = ?", (pin,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def update_balance(self, pin, new_balance):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE pin = ?", (new_balance, pin))
        conn.commit()
        conn.close()
    
    def update_pin(self, old_pin, new_pin):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET pin = ? WHERE pin = ?", (new_pin, old_pin))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_transaction(self, user_pin, transaction_type, amount):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_pin, transaction_type, amount) VALUES (?, ?, ?)",
            (user_pin, transaction_type, amount)
        )
        conn.commit()
        conn.close()
    
    def get_transactions(self, user_pin, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT transaction_type, amount, timestamp FROM transactions WHERE user_pin = ? ORDER BY timestamp DESC LIMIT ?",
            (user_pin, limit)
        )
        results = cursor.fetchall()
        conn.close()
        return results