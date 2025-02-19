from bank import Bank
from account import Account

class Session:
    # constructor method that runs when an instance of the class is created
    def __init__(self, bank):
        self.logged_in = False
        self.current_account = None
        self.bank = bank
        
    def display_menu(self):
        print("\nPlease choose an option:")
        print("1. Standard Login")
        print("2. Admin Login")
        print("3. Exit App")

    def standard_login(self):
        print("\n--- Standard Login ---")
        account_holder_name = input("Enter the account holder's full name: ")
        account_info = self.bank.get_account(account_holder_name)
        if account_info:
            if account_info["is_admin"]:
                print(f"'{account_holder_name}' is an admin user. Please use Admin Login instead.")
            else:
                self.logged_in = True
                self.current_account = account_info
                print(f"Standard login successful for {account_holder_name}.")
                account_obj = Account(account_info, self.bank, self)
                account_obj.run()
                self.logout()
        else:
            print("Account not found.")

    def admin_login(self):
        print("\n--- Admin Login ---")
        admin_name = input("Enter the admin's full name: ")
        account_info = self.bank.get_account(admin_name)
        if account_info and account_info["is_admin"]:
            self.logged_in = True
            self.current_account = account_info
            print(f"Admin login successful for {admin_name}.")
            account_obj = Account(account_info, self.bank, self)
            account_obj.run()
            self.logout()
        else:
            print("Invalid admin credentials or account not found.")

    def logout(self):
        if not self.current_account:
            print("No user is currently logged in.")
            return

        # Use current_account, not self.account_info
        user_full_name = f"{self.current_account['first_name']} {self.current_account['last_name']}"
        from bank import write_transaction  # local import to reduce circular import risk

        write_transaction(
            transaction_code="00",
            account_holder_name="end of session",
            account_number="00000", 
            amount=0.00,
            plan_code="  "         
        )

        print("\nYou have been logged out from your account session.")
        self.logged_in = False
        self.current_account = None

        # Prompt to log back in or exit
        while True:
            choice = input("\nWould you like to:\n"
                        "1) Log back in\n"
                        "2) Exit the application\n"
                        "Enter your choice: ").strip()
            if choice == "1":
                print("\nReturning to login menu...\n")
                break  # Simply break to return to the main session menu
            elif choice == "2":
                print("Exiting the application. Goodbye!")
                import sys
                sys.exit(0)
            else:
                print("Invalid option. Please try again.")




    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                self.standard_login()
            elif choice == "2":
                self.admin_login()
            elif choice == "3":
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
