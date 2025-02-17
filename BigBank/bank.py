import random
from colorama import Fore, Style

class Bank:
    def __init__(self, user_id=None, name=None, status=None, balance=None, users=None, accounts_file=None, transaction_log=None, logged_in_user=None):
        if users is not None and accounts_file is not None and transaction_log is not None:
            self.users = users
            self.accounts_file = accounts_file
            self.transaction_log = transaction_log
            self.logged_in_user = logged_in_user  
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
                    if parts[0] == "00000":  # End of file marker
                        break
                    if len(parts) < 5:
                        continue

                    user_id = parts[0]
                    if len(parts) >= 6:
                        name = parts[1] + " " + parts[2]
                        status = parts[3]
                        balance_str = parts[4]
                        payment_plan = parts[5]
                    else:
                        name = parts[1] + " " + parts[2]
                        status = parts[3]
                        balance_str = parts[4]
                        payment_plan = "SP" 

                    # Ensure balance is a valid number
                    if not balance_str.isdigit():
                        print(Fore.YELLOW + f"Warning: Invalid balance '{balance_str}' for {name}. Skipping account." + Style.RESET_ALL)
                        continue
                    balance = int(balance_str) / 100  # Convert cents to dollars
                    users[user_id] = Bank(user_id, name, status, balance, payment_plan=payment_plan)
            print(Fore.CYAN + f"🔄 Successfully loaded {len(users)} accounts from file." + Style.RESET_ALL)
        except FileNotFoundError:
            print(Fore.RED + "Error: User data file not found." + Style.RESET_ALL)
        return users

    def create_account(self, session):
        # """Creates a new account, writes it to file, and prevents access in the same session."""
        if not session.logged_in_user.is_admin():
            print(Fore.RED + "Access Denied: Only admins can create accounts." + Style.RESET_ALL)
            return

        print("\nCreating New Account")
        first_name = input("Enter account holder's first name: ").strip()
        last_name = input("Enter account holder's last name: ").strip()

        if not first_name or not last_name:
            print(Fore.RED + "Error: Both first and last names are required." + Style.RESET_ALL)
            return

        # Ensure name format (replace spaces with underscores, limit to 20 characters)
        formatted_first_name = first_name.ljust(10)[:10]
        formatted_last_name = last_name.ljust(10)[:10]

        initial_balance = input("Enter initial balance (Max: $99,999.99): ").strip()

        try:
            balance = float(initial_balance)
            if balance < 0 or balance > 99999.99:
                print(Fore.RED + "Error: Balance must be between $0.00 and $99,999.99." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "Error: Invalid balance amount." + Style.RESET_ALL)
            return

        # Generate a **unique 5-digit** account number
        existing_ids = [int(acc.user_id) for acc in self.users.values()]
        new_account_id = str(max(existing_ids) + 1).zfill(5) if existing_ids else "00001"

        # Format balance (8-digit, zero-padded)
        balance_cents = str(int(balance * 100)).zfill(8)

        # The default payment plan is "SP"
        payment_plan = "SP"

        # Correctly formatted account entry
        new_account_entry = f"{new_account_id}_{formatted_first_name}_{formatted_last_name}_A_{balance_cents}_{payment_plan}\n"

         try:
            with open(self.accounts_file, "r+", encoding="utf-8") as file:
                lines = file.readlines()
                inserted = False
                for i, line in enumerate(lines):
                    if "END_OF_FILE" in line:
                        lines.insert(i, new_account_entry)
                        inserted = True
                        break
                if not inserted:
                    lines.append(new_account_entry)
                file.seek(0)
                file.writelines(lines)

            print(Fore.GREEN + f"Account successfully created! Account Number: {new_account_id}" + Style.RESET_ALL)


            # Store the new account in session but BLOCK ACCESS in same session
            ew_user = Bank(new_account_id, f"{first_name} {last_name}", "A", balance, payment_plan=payment_plan)
            self.users[new_account_id] = new_user
            session.newly_created_accounts.append(new_account_id)
            print(Fore.YELLOW + "This account will be available after the next login session." + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"Error writing to accounts file: {e}" + Style.RESET_ALL)




    def save_to_accounts_file(self, name, balance_cents):
        # """ Inserts new account above END_OF_FILE in current_accounts.txt and returns the new account number """
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            new_account_number = str(random.randint(0, 99999)).zfill(5)
            existing_accounts = {line[:5] for line in lines if line.strip() and "END_OF_FILE" not in line}
            while new_account_number in existing_accounts:
                new_account_number = str(random.randint(0, 99999)).zfill(5)

            # Ensure underscores instead of spaces in name
             name_parts = name.split()
            if len(name_parts) < 2:
                formatted_first_name = name.replace(" ", "").ljust(10)[:10]
                formatted_last_name = "".ljust(10)
            else:
                formatted_first_name = name_parts[0].ljust(10)[:10]
                formatted_last_name = name_parts[1].ljust(10)[:10]

            formatted_balance = str(balance_cents).zfill(8)
            payment_plan = "SP"
            new_entry = f"{new_account_number}_{formatted_first_name}_{formatted_last_name}_A_{formatted_balance}_{payment_plan}\n"
            # Insert above END_OF_FILE
            with open(self.accounts_file, "w", encoding="utf-8") as file:
                for line in lines:
                    if "END_OF_FILE" in line:
                        file.write(new_entry) # Insert new account before EOF line
                    file.write(line)

            print(Fore.GREEN + f"Account successfully created! Account Number: {new_account_number}" + Style.RESET_ALL)
            return new_account_number # eturn the generated account number

        except Exception as e:
            print(Fore.RED + f"Error saving account to file: {e}" + Style.RESET_ALL)
            return None # Return None if something goes wrong
            
            

    def log_account_creation(self, account_number, name, balance_cents):
        # """ Logs the new account creation to the transaction file """
        transaction_code = "05"
        formatted_name = name.ljust(20)[:20]
        log_entry = f"{transaction_code}_{formatted_name}_{account_number}_{str(balance_cents).zfill(8)}_00\n"
        try:
            with open(self.transaction_log, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(Fore.RED + f"Error writing to transaction log: {e}" + Style.RESET_ALL)
