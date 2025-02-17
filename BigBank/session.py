import getpass
import os
from account import Accounts
from colorama import Fore, Style

class Session:
    def __init__(self, users, accounts_file, bank):
        self.users = users
        self.accounts_file = accounts_file
        self.bank = bank  
        self.logged_in_user = None  
        self.newly_created_accounts = []

    def login(self):
       
        while True:
            self.clear_screen()
       


            print("Welcome to the Bank Console Application!")
            print("Select session type:")
            print("[1] Standard Session")
            print("[2] Admin Session")
            print("[0] Quit Application")
            session_type = input("Enter choice (1, 2, or 0): ").strip()
            
            if session_type == "1":
                self.standard_login()
            elif session_type == "2":
                self.admin_login()
            elif session_type == "0":
                print("Exiting application...")
                exit()
            else:
                print(Fore.RED + "Invalid selection. Please choose 1, 2, or 0." + Style.RESET_ALL)

    def standard_login(self):
        
        input_name = input("Enter your Name: ").strip().replace("_", " ")  
        
        found_user = next((user for user in self.users.values() if user.name.lower() == input_name.lower() and not user.is_admin()), None)

        if not found_user:
            print(Fore.RED + "Invalid Name. Please try again." + Style.RESET_ALL)
            return

        self.authenticate(found_user)  

    def admin_login(self):
        input_name = input("Enter your Admin Name: ").strip().replace("_", " ")

        found_user = next((user for user in self.users.values() if user.name.lower() == input_name.lower() and user.is_admin()), None)

        if not found_user:
            print(Fore.RED + "Invalid Admin Name. Please try again." + Style.RESET_ALL)
            return

        self.authenticate(found_user)

    def authenticate(self, user):
        password = getpass.getpass("Enter your password: ")
        if password != user.default_password:
            print(Fore.RED + "Invalid password. Please try again." + Style.RESET_ALL)
            return

        if not user.is_active():
            print(Fore.RED + "Access Denied: Your account is disabled." + Style.RESET_ALL)
            return

        self.logged_in_user = user  #Set logged-in user
        self.bank.logged_in_user = user  #Also update Bank instance

        # Refresh users list to include newly created accounts
        self.bank.users = self.bank.get_accounts(self.accounts_file)  

        # Pass self.bank to Accounts so it has updated data
        account = Accounts(user, self.bank.users, self.accounts_file, self.bank, self)  
        account.display_account_info()


    def logout(self):

        while True:
            self.clear_screen()
            print("Logging out...")
            self.logged_in_user = None

            #Clear new accounts so they can be accessed in the next session
            self.newly_created_accounts.clear()

            print("You have been logged out. Would you like to log back in or exit the application?\n")
            print("[1] to login")
            print("[0] to exit the application")
            session_type = input("Enter choice (1 or 0): ").strip()

            if session_type == "1":
                self.login()
            elif session_type == "0":
                print("Exiting application...")
                exit()
            else:
                print(Fore.RED + "Invalid selection. Please choose 1 or 0." + Style.RESET_ALL)


    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
