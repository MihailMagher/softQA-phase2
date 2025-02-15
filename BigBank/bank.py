import random
from colorama import Fore, Style

class Bank:
    def __init__(self, user_id=None, name=None, status=None, balance=None, users=None, accounts_file=None, transaction_log=None):
        if users is not None and accounts_file is not None and transaction_log is not None:
            self.users = users
            self.accounts_file = accounts_file
            self.transaction_log = transaction_log
        else:
            self.user_id = user_id
            self.name = name.strip().replace("_", " ") if name else None
            self.status = status
            self.balance = balance
            self.default_password = "123456"

    def is_active(self):
        return self.status == "A"

    def is_admin(self):
        return self.name.lower() in ["jane smith", "james miller"]

    def format_balance(self, balance):
        # """ Convert stored balance from string (e.g., '0050000') to float (e.g., 500.00) """
        try:
            balance = int(balance) / 100
        except ValueError:
            balance = 0.0
        return balance

    @staticmethod
    def get_accounts(filename):
        users = {}
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("_")
                    if parts[0] == "00000":
                        break
                    if len(parts) < 5:
                        continue
                    
                    user_id, name, status, balance = parts[0], parts[1] + " " + parts[2], parts[3], parts[4]
                    users[user_id] = Bank(user_id, name, status, balance)

        except FileNotFoundError:
            print("Error: User data file not found.")
        
        return users

    def create_account(self, admin_user):
        """ Allows an admin to create a new account """
        if not admin_user.is_admin():
            print(Fore.RED + "Only admins can create new accounts." + Style.RESET_ALL)
            return

        name = input("Enter new account holder's name: ").strip().title()

        # Ensure unique account number
        existing_account_numbers = {user.user_id for user in self.users.values()}
        while True:
            account_number = str(random.randint(10000, 99999)).zfill(5)
            if account_number not in existing_account_numbers:
                break

        # Ask for initial balance
        while True:
            balance_str = input("Enter initial balance (Max: $99,999.99): ").strip()
            try:
                balance = float(balance_str)
                if balance < 0 or balance > 99999.99:
                    print(Fore.RED + "Invalid balance. Must be between $0.00 and $99,999.99." + Style.RESET_ALL)
                else:
                    break
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid amount." + Style.RESET_ALL)

        balance_cents = int(balance * 100)

        # Save new account to current accounts file
        self.save_to_accounts_file(account_number, name, balance_cents)

        # Log the account creation in the transaction log
        self.log_account_creation(account_number, name, balance_cents)

        print(Fore.GREEN + f"Account successfully created! Account Number: {account_number}" + Style.RESET_ALL)
        print(Fore.YELLOW + "This account will not be available for transactions in this session." + Style.RESET_ALL)

    def save_to_accounts_file(self, account_number, name, balance_cents):
        """ Adds the new account to the current accounts file """
        try:
            with open(self.accounts_file, "a") as file:
                file.write(f"{account_number}_{name.ljust(20)[:20]}_A_{str(balance_cents).zfill(8)}\n")
        except Exception as e:
            print(Fore.RED + f"Error saving account to file: {e}" + Style.RESET_ALL)

    def log_account_creation(self, account_number, name, balance_cents):
        """ Logs the new account creation to the transaction file """
        transaction_code = "05"
        misc_info = "00"
        log_entry = f"{transaction_code}_{name.ljust(20)[:20]}_{account_number}_{str(balance_cents).zfill(8)}_{misc_info}\n"

        try:
            with open(self.transaction_log, "a") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(Fore.RED + f"Error writing to transaction log: {e}" + Style.RESET_ALL)
