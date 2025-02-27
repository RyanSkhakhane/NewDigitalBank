import sqlite3
import bcrypt
from datetime import datetime

from cards.createCardTable import create_tables


class User:
    def __init__(self, db_path="ndb_bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()



    class User:
        def __init__(self, db_path="ndb_bank.db"):
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.create_tables()

        def create_tables(self):
            """Create users and sessions tables if they don't exist."""
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
            )

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions(
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            login_time TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """
            )

            self.conn.commit()

        def hash_password(self, password):
            """Hash the password before storing it."""
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        def verify_password(self, entered_password, stored_hash):
            """Verify password during login."""
            return bcrypt.checkpw(entered_password.encode(), stored_hash.encode())

        def create_user(self, full_name, email, phone, password):
            """Register a new user with a hashed password."""
            hashed_password = self.hash_password(password)
            created_at = datetime.now().isoformat()

            try:
                self.cursor.execute("""
                    INSERT INTO users (full_name, email, phone, password, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (full_name, email, phone, hashed_password, created_at))
                self.conn.commit()
                print("User registered successfully!")
            except sqlite3.IntegrityError:
                print("Error: Email or phone already exists.")

        def get_user(self, user_id):
            """Retrieve user details by ID."""
            self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
            return self.cursor.fetchone()

        def update_user(self, user_id, full_name=None, email=None, phone=None, password=None):
            """Update user details."""
            if full_name:
                self.cursor.execute("UPDATE users SET full_name=? WHERE user_id=?", (full_name, user_id))
            if email:
                self.cursor.execute("UPDATE users SET email=? WHERE user_id=?", (email, user_id))
            if phone:
                self.cursor.execute("UPDATE users SET phone=? WHERE user_id=?", (phone, user_id))
            if password:
                hashed_password = self.hash_password(password)
                self.cursor.execute("UPDATE users SET password=? WHERE user_id=?", (hashed_password, user_id))

            self.conn.commit()
            print("User details updated successfully!")

        def delete_user(self, user_id):
            """Delete a user and their session."""
            self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
            self.cursor.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
            self.conn.commit()
            print("User deleted successfully!")

        def login(self, email, password):
            """Authenticate a user and start a session."""
            self.cursor.execute("SELECT user_id, full_name, password FROM users WHERE email=?", (email,))
            user = self.cursor.fetchone()

            if user and self.verify_password(password, user[2]):
                session_time = datetime.now().isoformat()
                self.cursor.execute("""
                    INSERT INTO sessions (user_id, login_time) VALUES (?, ?)
                """, (user[0], session_time))
                self.conn.commit()
                print(f"Login successful! Welcome {user[1]}")
                return user[0]  # Return user_id for session tracking
            else:
                print("Invalid email or password.")
                return None

        def logout(self, user_id):
            """Logout a user by deactivating their session."""
            self.cursor.execute("""
                UPDATE sessions SET is_active=0 WHERE user_id=? AND is_active=1
            """, (user_id,))
            self.conn.commit()
            print("Logout successful!")

        def is_user_logged_in(self, user_id):
            """Check if a user has an active session."""
            self.cursor.execute("""
                SELECT 1 FROM sessions WHERE user_id=? AND is_active=1
            """, (user_id,))
            return bool(self.cursor.fetchone())

        def close_connection(self):
            """Close the database connection."""
            self.conn.close()

    class Account:
        def __init__(self, db_path="ndb_bank.db"):
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.create_table()

        def create_table(self):
            """Create the accounts table."""
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_number TEXT UNIQUE NOT NULL,
                balance REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """
            )
            self.conn.commit()

        def create_account(self, user_id, account_number):
            """
            Create
            a
            new
            bank
            account.
            """
            created_at = datetime.now().isoformat()
            self.cursor.execute("""
            INSERT
            INTO
            accounts(user_id, account_number, balance, created_at)
            VALUES(?, ?, 0.0, ?)
            """, (user_id, account_number, created_at))
            self.conn.commit()
            print("Account created successfully!")

        def get_account(self, account_number):
            """
            Retrieve
            account
            details.
            """
            self.cursor.execute("SELECT * FROM accounts WHERE account_number=?", (account_number,))
            return self.cursor.fetchone()

        def update_balance(self, account_number, amount):
            """
            Update
            account
            balance.
            """
            self.cursor.execute("""
            UPDATE
            accounts
            SET
            balance = balance + ? WHERE
            account_number =?
            """, (amount, account_number))
            self.conn.commit()
            print("Balance updated!")

        def delete_account(self, account_number):
            """
            Delete
            an
            account.
            """
            self.cursor.execute("DELETE FROM accounts WHERE account_number=?", (account_number,))
            self.conn.commit()
            print("Account deleted!")

        def close_connection(self):
            """
            Close
            the
            database
            connection.
            """
            self.conn.close()

    # Additional files like Transactions.py, CardManager.py, and BankingSystem.py will be added next.


    def hash_password(self, password):
        """Hash the password before storing it."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, entered_password, stored_hash):
        """Verify password during login."""
        return bcrypt.checkpw(entered_password.encode(), stored_hash.encode())

    def create_user(self, full_name, email, phone, password):
        """Register a new user with a hashed password."""
        hashed_password = self.hash_password(password)
        created_at = datetime.now().isoformat()

        try:
            self.cursor.execute("""
                INSERT INTO users (full_name, email, phone, password, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (full_name, email, phone, hashed_password, created_at))
            self.conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Error: Email or phone already exists.")

    def get_user(self, user_id):
        """Retrieve user details by ID."""
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, full_name=None, email=None, phone=None, password=None):
        """Update user details."""
        if full_name:
            self.cursor.execute("UPDATE users SET full_name=? WHERE user_id=?", (full_name, user_id))
        if email:
            self.cursor.execute("UPDATE users SET email=? WHERE user_id=?", (email, user_id))
        if phone:
            self.cursor.execute("UPDATE users SET phone=? WHERE user_id=?", (phone, user_id))
        if password:
            hashed_password = self.hash_password(password)
            self.cursor.execute("UPDATE users SET password=? WHERE user_id=?", (hashed_password, user_id))

        self.conn.commit()
        print("User details updated successfully!")

    def delete_user(self, user_id):
        """Delete a user and their session."""
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.cursor.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
        self.conn.commit()
        print("User deleted successfully!")

    def login(self, email, password):
        """Authenticate a user and start a session."""
        self.cursor.execute("SELECT user_id, full_name, password FROM users WHERE email=?", (email,))
        user = self.cursor.fetchone()

        if user and self.verify_password(password, user[2]):
            session_time = datetime.now().isoformat()
            self.cursor.execute("""
                INSERT INTO sessions (user_id, login_time) VALUES (?, ?)
            """, (user[0], session_time))
            self.conn.commit()
            print(f"Login successful! Welcome {user[1]}")
            return user[0]  # Return user_id for session tracking
        else:
            print("Invalid email or password.")
            return None

    def logout(self, user_id):
        """Logout a user by deactivating their session."""
        self.cursor.execute("""
            UPDATE sessions SET is_active=0 WHERE user_id=? AND is_active=1
        """, (user_id,))
        self.conn.commit()
        print("Logout successful!")

    def is_user_logged_in(self, user_id):
        """Check if a user has an active session."""
        self.cursor.execute("""
            SELECT 1 FROM sessions WHERE user_id=? AND is_active=1
        """, (user_id,))
        return bool(self.cursor.fetchone())

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()



