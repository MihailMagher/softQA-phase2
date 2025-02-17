import os
from colorama import Fore, Style
#test
class Accounts:
    def __init__(self, user, users, accounts_file, bank, session):
        self.user = user
        self.users = users
        self.accounts_file = accounts_file
        self.bank = bank
        self.session = session
        self.transaction_log = "../BigBank/bank account transaction file(output)/bank_transaction_log"
    
    def display_account_info(self):
        self.clear_screen()
        print(f"\nWelcome {self.user.name}! You are now logged in.")
        print(f"Account Number: {self.user.user_id}")
        print(f"Balance: ${self.user.balance:.2f}")
        print(f"Status: {self.user.status}")
        print(f"Payment Plan: {self.user.payment_plan}")
        self.accounts_menu()
    
    def accounts_menu(self):
        while True:
            print("\nOptions:")
            print("[1] Withdraw Money")
            if self.user.is_admin():
                print("[2] Create New Account")      # For Administrators
                print("[3] Disable Account")         # Placeholder: Disable account function to be implemented
                print("[4] Change Payment Plan")       # Placeholder: Change payment plan function to be implemented
            print("[0] Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.withdraw()
            elif choice == "2" and self.user.is_admin():
                self.bank.create_account(self.session)
            elif choice == "3" and self.user.is_admin():
                print(Fore.YELLOW + "Disable Account functionality is not implemented yet." + Style.RESET_ALL)
            elif choice == "4" and self.user.is_admin():
                print(Fore.YELLOW + "Change Payment Plan functionality is not implemented yet." + Style.RESET_ALL)
            elif choice == "0":
                self.session.logout()
            else:
                print("Invalid choice. Please enter a valid option.")

    
    def withdraw(self, session):
        # """Withdraws money but prevents new accounts from being accessed in the same session."""
        account_identifier = input("Enter the account holder's name: ").strip().lower()
        
        # Find user by name
        target_user = next((u for u in self.users.values() if u.name.lower() == account_identifier), None)

        if not target_user:
            print(Fore.RED + "Account not found." + Style.RESET_ALL)
            return
        
        if target_user.status == "D":
            print(Fore.RED + "This account is disabled. No transactions allowed." + Style.RESET_ALL)
            return

        if target_user.user_id in self.session.newly_created_accounts:
            print(Fore.YELLOW + "This account was just created and cannot be accessed until next login." + Style.RESET_ALL)
            return

        amount_str = input("Enter amount to withdraw: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print(Fore.RED + "Withdrawal amount must be positive." + Style.RESET_ALL)
                return

            if not self.user.is_admin() and amount > 500.00:
                print(Fore.RED + "Standard users can only withdraw up to $500.00 per session." + Style.RESET_ALL)
                return

            if target_user.balance - amount < 0:
                print(Fore.RED + "Insufficient funds. Balance must remain at least $0.00." + Style.RESET_ALL)
                return

            target_user.balance -= amount
            print(Fore.GREEN + f"Withdrawal successful. New balance: ${target_user.balance:.2f}" + Style.RESET_ALL)

            self.log_transaction(target_user, amount)
            self.update_account_balance(target_user)

        except ValueError:
            print(Fore.RED + "Invalid amount entered. Please enter a valid number." + Style.RESET_ALL)

    
    def log_transaction(self, target_user, amount):
        # """ Logs transaction in bank_transaction_log with proper formatting """

        transaction_code = "01"  # 01 for withdrawal
        formatted_name = target_user.name.ljust(20)[:20]  # 20-char left-justified
        formatted_account = target_user.user_id.zfill(5)  # 5-char right-justified, zero-padded
        formatted_amount = f"{int(amount * 100):08d}"  # 8-char right-justified, zero-padded
        misc_info = "00"  # Placeholder for miscellaneous info
        transaction_entry = f"{transaction_code}_{formatted_name}_{formatted_account}_{formatted_amount}_{misc_info}\n"
        
        try:
            with open(self.transaction_log, "a") as log_file:
                log_file.write(transaction_entry)
        except Exception as e:
            print(f"Failed to write to log file: {e}")
    
    def update_account_balance(self, target_user):
        """ Updates the current account balance in the accounts file """
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            with open(self.accounts_file, "w", encoding="utf-8") as file:
                for line in lines:
                    parts = line.strip().split("_")
                    if parts[0] == target_user.user_id:
                        # For new formats： [id, first, last, status, balance, payment_plan]
                        if len(parts) >= 6:
                            parts[4] = f"{int(target_user.balance * 100):08d}"
                            line = "_".join(parts) + "\n"
                        else:
                            parts[4] = f"{int(target_user.balance * 100):08d}"
                            line = "_".join(parts) + "\n"
                    file.write(line)
        except Exception as e:
            print(f"Failed to update account balance: {e}")
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
