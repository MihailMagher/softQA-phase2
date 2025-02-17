import os
from colorama import Fore, Style

class DeleteAccount:
    def __init__(self, users, accounts_file, session):
        self.users = users
        self.accounts_file = accounts_file
        self.session = session
        self.transaction_log = "../BigBank/bank account transaction file(output)/bank_transaction_log"

    def delete_account(self):
        account_id = input("Enter the account number to delete: ").strip()
        
        if account_id not in self.users:
            print(Fore.RED + "Account not found." + Style.RESET_ALL)
            return

        user = self.users[account_id]
        if user.balance > 0:
            print(Fore.RED + "Account balance must be zero before deletion." + Style.RESET_ALL)
            return

        del self.users[account_id]
        self.log_transaction(account_id, user.name)
        self.update_accounts_file(account_id)

        print(Fore.GREEN + f"Account {account_id} deleted successfully." + Style.RESET_ALL)
    
    def log_transaction(self, account_id, name):
        transaction_code = "02"  # 02 for account deletion
        formatted_name = name[:20].ljust(20)
        formatted_account = account_id.zfill(5)
        formatted_amount = "00000000"  # No balance left
        misc_info = "00"
        
        transaction_entry = f"{transaction_code}_{formatted_name}_{formatted_account}_{formatted_amount}_{misc_info}\n"
        try:
            with open(self.transaction_log, "a") as log_file:
                log_file.write(transaction_entry)
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def update_accounts_file(self, account_id):
        try:
            with open(self.accounts_file, "r") as file:
                lines = file.readlines()
            
            with open(self.accounts_file, "w") as file:
                for line in lines:
                    if not line.startswith(account_id):
                        file.write(line)
        except Exception as e:
            print(f"Failed to update accounts file: {e}")
