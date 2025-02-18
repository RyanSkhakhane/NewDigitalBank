from Users import User
from Accounts import Account
from Transactions import Transaction
from Cardmanager import CardManager


class BankingSystem:
    def __init__(self):
        self.user_manager = User()
        self.account_manager = Account()
        self.transaction_manager = Transaction()
        self.card_manager = CardManager()

    def register_user(self, full_name, email, phone, password):
        """Register a new user and create an account."""
        self.user_manager.create_user(full_name, email, phone, password)
        user = self.user_manager.get_user(email)

        if user:
            user_id = user[0]  # Extract user_id
            self.account_manager.create_account(user_id)
        else:
            print("User registration failed!")

    def get_user_details(self, email):
        """Retrieve user details."""
        return self.user_manager.get_user(email)

    def make_transfer(self, sender_account, receiver_account, amount):
        """Transfer money between accounts."""
        self.transaction_manager.create_transaction(sender_account, receiver_account, amount)

    def get_transaction_history(self, account_number):
        """Retrieve account transaction history."""
        return self.transaction_manager.get_transaction_history(account_number)

    def issue_card(self, account_number, card_type, spending_limit=None):
        """Issue a new card linked to an account."""
        self.card_manager.issue_card(account_number, card_type, spending_limit)

    def block_card(self, card_number):
        """Block a card."""
        self.card_manager.update_card_status(card_number, "Blocked")

    def get_cards(self, account_number):
        """Retrieve all cards linked to an account."""
        return self.card_manager.get_cards_by_account(account_number)

    def close_connections(self):
        """Close all database connections."""
        self.user_manager.close_connection()
        self.account_manager.close_connection()
        self.transaction_manager.close_connection()
        self.card_manager.close_connection()


# Example usage
if __name__ == "__main__":
    bank = BankingSystem()

    # Register a user and create an account
    bank.register_user("John Doe", "john@example.com", "1234567890", "securepass")

    # Transfer money
    bank.make_transfer("1234567890", "0987654321", 100)

    # Issue a debit card
    bank.issue_card("1234567890", "Debit")

    # Retrieve transactions
    print(bank.get_transaction_history("1234567890"))

    # Retrieve cards linked to account
    print(bank.get_cards("1234567890"))

    # Close DB connections
    bank.close_connections()
