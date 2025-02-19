class Bank:
    # constructor method that runs when an instance of the class is created
    def __init__(self, accounts_file="../Phase#2FIX/current accounts/current_accounts.txt"):
        self.accounts_file = accounts_file

    #grabs the users account information from the current accounts file
    def get_account(self, name):
        """
        Returns a dict of account info for the given full name (e.g. 'John Doe').
        If no match is found, returns None.
        """
        name = name.strip().lower()
        admin_users = {"john doe", "jane smith"}
        is_admin = (name in admin_users)
        parts = name.split()
        if len(parts) < 2:
            return None
        first_name_input = parts[0]
        last_name_input = parts[1]

        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "END_OF_FILE" in line:
                        break
                    fields = line.split('_')
                    if len(fields) < 5:
                        continue
                    account_number = fields[0]
                    f_name = fields[1]
                    l_name = fields[2].strip()
                    status = fields[3]
                    balance_str = fields[4]
                    if f_name.lower() == first_name_input and l_name.lower() == last_name_input:
                        return {
                            "account_number": account_number,
                            "first_name": f_name.strip(),
                            "last_name": l_name.strip(),
                            "status": status,
                            "balance": float(balance_str) / 100,
                            "is_admin": is_admin
                        }
            return None
        except FileNotFoundError:
            print(f"Error: File '{self.accounts_file}' not found.")
            return None

    # create a new account, logs it to the transaction file as "05", 
    # but doesnt rewrite the current account file so that the user
    # cant be available in the current session. 
    def create_account(self, is_admin):
        if not is_admin:
            print("Error: Only admins can create new accounts.")
            return

        # 1. Prompt for new account holder's name (max 20 chars)
        holder_name = input("Enter the new account holder's full name: ").strip()
        if len(holder_name) > 20:
            print("Error: Name exceeds 20 characters. Aborting.")
            return

        # Optionally split into first/last names if needed, but for transaction logging
        # we can simply use the full string.
        
        # 2. Prompt for the initial balance (<= 99999.99)
        try:
            balance_str = input("Enter the initial balance: ").strip()
            initial_balance = float(balance_str)
        except ValueError:
            print("Invalid balance entered.")
            return

        if initial_balance < 0 or initial_balance > 99999.99:
            print("Error: Balance must be between 0.00 and 99999.99.")
            return

        # 3. Generate a unique 5-digit account number
        new_account_num = self.generate_new_account_number()

        # Writes to transaction log
        plan_code = "A"
        write_transaction(
            transaction_code="05",
            account_holder_name=holder_name,
            account_number=new_account_num,
            amount=initial_balance,
            plan_code=plan_code
        )
        print(f"Account creation transaction logged. New account number = {new_account_num}.")
        print("Note: This new account will not be available until the next session.")
    # Deletes the users account and then logs the transactions as "06"
    def delete_account(self, is_admin):

        if not is_admin:
            print("Error: Only admins can delete an account.")
            return

        holder_name = input("Enter the account holder's full name: ").strip()
        found_account = self.get_account(holder_name)
        if not found_account:
            print(f"Error: No valid account found for '{holder_name}'.")
            return

        acc_num_input = input("Enter the account number: ").strip()
        if acc_num_input != found_account["account_number"]:
            print("Error: The account number does not match the account holder's record.")
            return

        # 1) Remove from current_accounts.txt
        updated_lines = []
        deleted = False
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    line_strip = line.strip()
                    if not line_strip or "END_OF_FILE" in line_strip:
                        continue
                    parts = line_strip.split('_')
                    if parts[0] == acc_num_input:
                        deleted = True
                        continue  # skip this line (delete)
                    updated_lines.append(line_strip)
        except FileNotFoundError:
            print(f"Error: {self.accounts_file} not found.")
            return

        if not deleted:
            print(f"Account number {acc_num_input} not found in file.")
            return

        # Rewrite the file
        with open(self.accounts_file, "w") as f:
            for ln in updated_lines:
                f.write(ln + "\n")
            f.write("00000_END_OF_FILE_________ _ 00000000\n")

        print(f"Account {acc_num_input} physically removed from {self.accounts_file}.")

        # 2) Write transaction code '06'
        plan_code = found_account["status"]
        write_transaction(
            transaction_code="06",
            account_holder_name=holder_name,
            account_number=acc_num_input,
            amount=0.00,
            plan_code=plan_code
        )
        print("Delete transaction (06) logged.")

    #  Disable the users account and then logs the transaction as "07"
    def disable_account(self, is_admin):
        """
        Sets the account's status to 'D' in current_accounts.txt (if admin).
        Also writes a '07' transaction record.
        """
        if not is_admin:
            print("Error: Only admins can disable an account.")
            return

        holder_name = input("Enter the account holder's full name: ").strip()
        found_account = self.get_account(holder_name)
        if not found_account:
            print(f"Error: No valid account found for '{holder_name}'.")
            return

        acc_num_input = input("Enter the account number: ").strip()
        if acc_num_input != found_account["account_number"]:
            print("Error: The account number does not match the account holder's record.")
            return

        if found_account["status"] == "D":
            print("Warning: This account is already disabled.")
            return

        # 1) Update status to 'D' in current_accounts.txt
        updated_lines = []
        changed = False
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    line_strip = line.strip()
                    if not line_strip or "END_OF_FILE" in line_strip:
                        continue
                    parts = line_strip.split('_')
                    if len(parts) < 5:
                        updated_lines.append(line_strip)
                        continue
                    if parts[0] == acc_num_input:
                        # found the account line, set status to 'D'
                        parts[3] = "D"
                        changed = True
                        line_strip = "_".join(parts)
                    updated_lines.append(line_strip)
        except FileNotFoundError:
            print(f"Error: {self.accounts_file} not found.")
            return

        if not changed:
            print(f"Account {acc_num_input} not found in file.")
            return

        # rewrite the file
        with open(self.accounts_file, "w") as f:
            for ln in updated_lines:
                f.write(ln + "\n")
            f.write("00000_END_OF_FILE_________ _ 00000000\n")

        print(f"Account {acc_num_input} status changed to 'D' in {self.accounts_file}.")

        # 2) Write transaction code '07'
        write_transaction(
            transaction_code="07",
            account_holder_name=holder_name,
            account_number=acc_num_input,
            amount=0.00,
            plan_code="D"
        )
        print("Disable transaction (07) logged.")

    # Changes a users plan and then logs the transaction as "08"
    def change_plan(self, is_admin):
        if not is_admin:
            print("Error: Only admins can change the payment plan.")
            return
        holder_name = input("Enter the account holder's full name: ").strip()
        found_account = self.get_account(holder_name)
        if not found_account:
            print(f"Error: No valid account found for '{holder_name}'.")
            return
        acc_num_input = input("Enter the account number: ").strip()
        if acc_num_input != found_account["account_number"]:
            print("Error: The account number does not match the account holder's record.")
            return


        write_transaction(
            transaction_code="08",
            account_holder_name=holder_name,
            account_number=acc_num_input,
            amount=0.00,
            plan_code="NP"
        )
        print(f"Change plan transaction logged. (No file update in this example)")

    #generates a new account number for create account based on the largest account numbner
    def generate_new_account_number(self):
       
        max_acc_num = 0
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "END_OF_FILE" in line:
                        continue
                    parts = line.split('_')
                    if len(parts) < 5:
                        continue
                    try:
                        acc_num_int = int(parts[0])
                        if acc_num_int > max_acc_num:
                            max_acc_num = acc_num_int
                    except ValueError:
                        continue
        except FileNotFoundError:
            pass
        new_acc_num_int = max_acc_num + 1
        return str(new_acc_num_int).zfill(5)

# Writes transactions to the trasaction file
def write_transaction(transaction_code, account_holder_name, account_number, amount, plan_code):
    # Up to 20 chars for name, left-justified
    name_field = account_holder_name[:20].ljust(20)
    # 5-char account number
    acct_field = str(account_number).rjust(5, '0')
    # Convert to cents, pad with 'X' for demonstration
    amount_cents = int(round(amount * 100))
    amount_field = str(amount_cents).rjust(8, 'X')
    # 2-char plan
    plan_field = plan_code[:2].ljust(2)

    line = f"{transaction_code}_{name_field}_{acct_field}_{amount_field}_{plan_field}"

    TRANSACTION_FILE_PATH = r"../softQA-phase2/BigBank/bank account transaction file(output)/bank_transaction_log"
    with open(TRANSACTION_FILE_PATH, "a") as f:
        f.write(line + "\n")
