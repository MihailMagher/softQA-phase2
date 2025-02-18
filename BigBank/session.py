import getpass
import os
from account import Accounts

class Session:
    def __init__(self, users, accounts_file, bank):
        self.users = users
        self.accounts_file = accounts_file
        self.bank = bank 
        self.logged_in_user = None

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
                print("Invalid selection. Please choose 1, 2, or 0.")

    def standard_login(self):
        input_name = input("Enter your Name: ").strip().replace("_", " ")  
        
        # Find matching user (not an admin)
        found_user = next((user for user in self.users.values() if user.name.lower() == input_name.lower() and not user.is_admin()), None)

        if not found_user:
            print("Invalid Name. Please try again.")
            return

        self.authenticate(found_user) 


    def admin_login(self):
        input_name = input("Enter your Admin Name: ").strip().replace("_", " ")

        found_user = None
        for user in self.users.values():
            if user.name.lower() == input_name.lower() and user.is_admin():
                found_user = user
                break

        if found_user:
            self.authenticate(found_user)
        else:
            print("Invalid Admin Name. Please try again.")

    def authenticate(self, user):
        password = getpass.getpass("Enter your password: ") 
        if password != user.default_password:
            print("Invalid password. Please try again.")
            return

        if not user.is_active():
            print("Access Denied: Your account is disabled.")
            return

        self.logged_in_user = user
        account = Accounts(user, self.users, self.accounts_file, self.bank)  
        account.display_account_info()
        self.logout()

    
    def logout(self):
        print("Logging out...")
        self.logged_in_user = None
        print("You have been logged out. Returning to login screen.\n")
        self.login()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

