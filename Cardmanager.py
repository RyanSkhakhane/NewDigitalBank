import sqlite3
import random
from datetime import datetime, timedelta


class CardManager:
    def __init__(self, db_path="ndb_bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create required tables if they don't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            card_number TEXT UNIQUE NOT NULL,
            card_type TEXT NOT NULL CHECK(card_type IN ('Debit', 'Credit')),
            cvv TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Active', 'Blocked')),
            spending_limit REAL DEFAULT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS card_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Purchase', 'Withdrawal', 'Refund')),
            amount REAL NOT NULL,
            merchant TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
        );
        """)

        self.conn.commit()

    def generate_card_number(self):
        """Generate a unique 16-digit card number."""
        while True:
            card_number = ''.join(str(random.randint(0, 9)) for _ in range(16))
            self.cursor.execute("SELECT 1 FROM cards WHERE card_number=?", (card_number,))
            if not self.cursor.fetchone():
                return card_number

    def generate_cvv(self):
        """Generate a 3-digit CVV."""
        return str(random.randint(100, 999))

    def generate_expiry_date(self):
        """Generate an expiry date (3 years from now)."""
        expiry = datetime.now() + timedelta(days=3 * 365)
        return expiry.strftime("%m/%y")

    def issue_card(self, account_number, card_type, spending_limit=None):
        """Issue a new card for an account."""
        self.cursor.execute("SELECT account_id FROM accounts WHERE account_number=?", (account_number,))
        account = self.cursor.fetchone()

        if not account:
            print("Account not found!")
            return

        account_id = account[0]
        card_number = self.generate_card_number()
        cvv = self.generate_cvv()
        expiry_date = self.generate_expiry_date()
        created_at = datetime.now().isoformat()

        self.cursor.execute("""
            INSERT INTO cards (account_id, card_number, card_type, cvv, expiry_date, status, spending_limit, created_at)
            VALUES (?, ?, ?, ?, ?, 'Active', ?, ?)
        """, (account_id, card_number, card_type, cvv, expiry_date, spending_limit, created_at))

        self.conn.commit()
        print(f"Card issued successfully! Card Number: {card_number}, CVV: {cvv}, Expiry: {expiry_date}")

    def get_cards_by_account(self, account_number):
        """Fetch all cards linked to an account."""
        self.cursor.execute("""
            SELECT card_id, card_number, card_type, expiry_date, status, spending_limit 
            FROM cards WHERE account_id = (SELECT account_id FROM accounts WHERE account_number=?)
        """, (account_number,))
        return self.cursor.fetchall()

    def update_card_status(self, card_number, new_status):
        """Block or activate a card."""
        if new_status not in ["Active", "Blocked"]:
            print("Invalid status! Use 'Active' or 'Blocked'.")
            return

        self.cursor.execute("UPDATE cards SET status=? WHERE card_number=?", (new_status, card_number))
        self.conn.commit()
        print(f"Card {card_number} is now {new_status}.")

    def set_spending_limit(self, card_number, limit):
        """Set a spending limit on a card."""
        self.cursor.execute("UPDATE cards SET spending_limit=? WHERE card_number=?", (limit, card_number))
        self.conn.commit()
        print(f"Spending limit set to {limit}.")

    def get_card_balance(self, card_number):
        """Fetch the balance of the account linked to the card."""
        self.cursor.execute("""
            SELECT a.balance FROM accounts a
            JOIN cards c ON a.account_id = c.account_id
            WHERE c.card_number = ?
        """, (card_number,))
        account = self.cursor.fetchone()
        return account[0] if account else None

    def record_card_transaction(self, card_number, transaction_type, amount, merchant=None):
        """Record a transaction made using a card."""
        self.cursor.execute("SELECT card_id, account_id, spending_limit FROM cards WHERE card_number=?", (card_number,))
        card = self.cursor.fetchone()

        if not card:
            print("Card not found!")
            return

        card_id, account_id, spending_limit = card

        # Fetch linked account balance
        self.cursor.execute("SELECT balance FROM accounts WHERE account_id=?", (account_id,))
        account_balance = self.cursor.fetchone()[0]

        # Check if spending limit is set and exceeded
        if spending_limit and amount > spending_limit:
            print("Transaction declined: Spending limit exceeded.")
            return

        # Check for sufficient balance
        if account_balance < amount:
            print("Transaction declined: Insufficient funds.")
            return

        # Deduct from account balance
        new_balance = account_balance - amount
        self.cursor.execute("UPDATE accounts SET balance=? WHERE account_id=?", (new_balance, account_id))
        self.conn.commit()

        # Record the transaction
        timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO card_transactions (card_id, transaction_type, amount, merchant, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (card_id, transaction_type, amount, merchant, timestamp))

        self.conn.commit()
        print(f"Transaction successful! New Account Balance: {new_balance}")

    def get_card_transaction_history(self, card_number):
        """Fetch card transaction history."""
        self.cursor.execute("""
            SELECT transaction_id, transaction_type, amount, merchant, timestamp 
            FROM card_transactions WHERE card_id = (SELECT card_id FROM cards WHERE card_number=?)
            ORDER BY timestamp DESC
        """, (card_number,))
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()


db_manager = CardManager()

db_manager.create_tables()