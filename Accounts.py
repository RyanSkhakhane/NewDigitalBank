import sqlite3
import random
from datetime import datetime

class Account:
    def __init__(self, db_path="ndb_bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the accounts table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_number TEXT UNIQUE NOT NULL,
            balance REAL DEFAULT 0.0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)
        self.conn.commit()

    def generate_account_number(self):
        """Generate a unique 10-digit account number."""
        while True:
            account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))
            self.cursor.execute("SELECT 1 FROM accounts WHERE account_number=?", (account_number,))
            if not self.cursor.fetchone():
                return account_number

    def create_account(self, user_id):
        """Create a new account for a user."""
        account_number = self.generate_account_number()
        created_at = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO accounts (user_id, account_number, created_at)
            VALUES (?, ?, ?)
        """, (user_id, account_number, created_at))
        self.conn.commit()
        print(f"Account created successfully! Account Number: {account_number}")

    def get_account(self, account_number):
        """Retrieve account details by account number."""
        self.cursor.execute("SELECT * FROM accounts WHERE account_number=?", (account_number,))
        return self.cursor.fetchone()

    def update_balance(self, account_number, new_balance):
        """Update account balance."""
        self.cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, account_number))
        self.conn.commit()
        print("Account balance updated!")

    def delete_account(self, account_number):
        """Delete an account."""
        self.cursor.execute("DELETE FROM accounts WHERE account_number=?", (account_number,))
        self.conn.commit()
        print("Account deleted!")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
