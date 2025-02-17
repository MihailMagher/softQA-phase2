import os
from colorama import Fore, Style
from bank import Bank

class CreateAccount:
    def __init__(self, users, accounts_file, session):
        self.users = users
        self.accounts_file = accounts_file
        self.session = session
        self.transaction_log = "../BigBank/bank account transaction file(output)/bank_transaction_log"

    def create_account(self):
        name = input("Enter full name for new account: ").strip()
        initial_balance_str = input("Enter initial deposit amount: ").strip()
        
        try:
            initial_balance = float(initial_balance_str)
            if initial_balance < 0:
                print(Fore.RED + "Initial balance cannot be negative." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "Invalid amount entered. Please enter a valid number." + Style.RESET_ALL)
            return

        new_account_id = str(max(map(int, self.users.keys())) + 1).zfill(5)  # Generate new account number
        self.users[new_account_id] = Bank(new_account_id, name, "A", initial_balance)  # Use Bank class instead of User
        self.session.newly_created_accounts.add(new_account_id)

        self.log_transaction(new_account_id, name, initial_balance)
        self.update_accounts_file(new_account_id, name, initial_balance)

        print(Fore.GREEN + f"Account created successfully! Account Number: {new_account_id}" + Style.RESET_ALL)
    
    def log_transaction(self, account_id, name, amount):
        transaction_code = "05"  # 05 for account creation
        formatted_name = name[:20].ljust(20)
        formatted_account = account_id.zfill(5)
        formatted_amount = f"{int(amount * 100):08d}"
        misc_info = "00"
        
        transaction_entry = f"{transaction_code}_{formatted_name}_{formatted_account}_{formatted_amount}_{misc_info}\n"
        try:
            with open(self.transaction_log, "a") as log_file:
                log_file.write(transaction_entry)
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def update_accounts_file(self, account_id, name, amount):
        try:
            with open(self.accounts_file, "a") as file:
                file.write(f"{account_id}_{name.ljust(20)}_A_{int(amount * 100):08d}\n")
        except Exception as e:
            print(f"Failed to update accounts file: {e}")