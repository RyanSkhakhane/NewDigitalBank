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
        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Purchase', 'Withdrawal', 'Refund', 'Deposit')),
        amount REAL NOT NULL,
        merchant TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
    );
    """)

    self.conn.commit()
