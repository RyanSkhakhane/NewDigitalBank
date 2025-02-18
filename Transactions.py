import sqlite3
from datetime import datetime


class Transaction:
    def __init__(self, db_path="ndb_bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the transactions table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_account TEXT NOT NULL,
            receiver_account TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (sender_account) REFERENCES accounts(account_number) ON DELETE CASCADE,
            FOREIGN KEY (receiver_account) REFERENCES accounts(account_number) ON DELETE CASCADE
        );
        """)
        self.conn.commit()

    def create_transaction(self, sender_account, receiver_account, amount):
        """Process a transaction between two accounts."""
        self.cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (sender_account,))
        sender_balance = self.cursor.fetchone()

        self.cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (receiver_account,))
        receiver_balance = self.cursor.fetchone()

        if not sender_balance or not receiver_balance:
            print("One or both accounts do not exist.")
            return

        sender_balance = sender_balance[0]
        receiver_balance = receiver_balance[0]

        if sender_balance < amount:
            print("Insufficient funds!")
            return

        # Deduct from sender
        new_sender_balance = sender_balance - amount
        self.cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?",
                            (new_sender_balance, sender_account))

        # Add to receiver
        new_receiver_balance = receiver_balance + amount
        self.cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?",
                            (new_receiver_balance, receiver_account))

        # Record transaction
        timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO transactions (sender_account, receiver_account, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """, (sender_account, receiver_account, amount, timestamp))

        self.conn.commit()
        print(f"Transaction successful! New sender balance: {new_sender_balance}")

    def get_transaction_history(self, account_number):
        """Retrieve transaction history for an account."""
        self.cursor.execute("""
            SELECT transaction_id, sender_account, receiver_account, amount, timestamp 
            FROM transactions WHERE sender_account=? OR receiver_account=?
            ORDER BY timestamp DESC
        """, (account_number, account_number))
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
