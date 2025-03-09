from bank import Bank, write_transaction

class Account:
    # constructor method that runs when an instance of the class is created
    def __init__(self, account_info, bank, session):
        self.bank = bank
        self.session = session
        self.account_info = account_info
        self.is_admin = account_info.get("is_admin", False)
        self.balance = account_info.get("balance", 0.0)
    # Menu choices 
    def display_menu(self):
        user_name = f"{self.account_info['first_name']} {self.account_info['last_name']}"
        current_balance = self.account_info.get("balance", 0.0)
        print(f"\n--- Welcome {user_name}, your current balance is ${current_balance:.2f} ---")
        print("\n--- Account Menu ---")
        print("1. Withdraw")
        print("2. Transfer")
        print("3. Paybill")
        print("4. Deposit")
        if self.is_admin:
            print("5. Create Account")
            print("6. Delete Account")
            print("7. Disable Account")
            print("8. Change Plan")
            print("9. Logout")
        else:
            print("5. Logout")

    # Withdraws money for users account and write to transaction log as "01"
    def withdraw(self):
        if self.is_admin:
            holder_name = input("Enter the account holder's full name: ").strip()
            holder_account = self.bank.get_account(holder_name)
            if not holder_account:
                print(f"No valid account found for '{holder_name}'.")
                return
            print(f"Admin user selected: {holder_name} (Balance = {holder_account['balance']:.2f})")
        else:
            holder_name = f"{self.account_info['first_name']} {self.account_info['last_name']}"
            holder_account = self.account_info
        acc_number_input = input("Enter the account number: ").strip()
        if acc_number_input != holder_account["account_number"]:
            print("Error: The account number does not match the account holder's record.")
            return
        try:
            amount = float(input("Enter the amount to withdraw: ").strip())
        except ValueError:
            print("Invalid amount entered.")
            return
        if not self.is_admin and amount > 500.0:
            print("Error: Maximum withdrawal in standard mode is $500.00.")
            return
        current_balance = holder_account["balance"]
        if current_balance - amount < 0:
            print(f"Error: Insufficient funds. Current balance is {current_balance:.2f}.")
            return
        new_balance = current_balance - amount
        holder_account["balance"] = new_balance
        print(f"Withdrawal successful. New balance = {new_balance:.2f}.")
        plan_code = holder_account.get("status", "A")
        # writes to transaction log
        write_transaction(
            transaction_code="01",
            account_holder_name=holder_name,
            account_number=acc_number_input,
            amount=amount,
            plan_code=plan_code
        )

    # transfers money from one account to another
    def transfer(self):
        # If admin, prompt for source account; otherwise use current user
        if self.is_admin:
            source_name = input("Enter the source account holder's full name: ").strip()
            print()  # blank line after input
            source_account = self.bank.get_account(source_name)
            if not source_account:
                print(f"No valid account found for '{source_name}'.")
                return
            print(f"Admin selected source: {source_name} (Balance = {source_account['balance']:.2f})\n")
        else:
            source_name = f"{self.account_info['first_name']} {self.account_info['last_name']}"
            source_account = self.account_info

        source_acc_input = input("Enter the source account number: ").strip()
        print()  # blank line after input

        # Check for invalid characters in the account number
        if not source_acc_input.isdigit():
            print("Error: Invalid account number format. Must be numeric.")
            return

        # Check that the source account number matches the account holder's record
        if source_acc_input != source_account["account_number"]:
            print("Error: The account number does not match the source account holder's record.")
            return

        dest_acc_input = input("Enter the destination account number: ").strip()
        print()  # blank line after input

        if not dest_acc_input.isdigit():
            print("Error: Invalid destination account number format. Must be numeric.")
            return

        # Use the Bank method to find the destination account by number
        dest_account = self.bank.get_account_by_number(dest_acc_input)
        if not dest_account:
            print(f"No valid destination account found for account number '{dest_acc_input}'.")
            return

        # Get transfer amount
        amount_str = input("Enter the amount to transfer: ").strip()
        print()  # blank line after input
        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount entered.")
            return

        # Check for negative or zero
        if amount <= 0:
            print("Error: Negative or zero transfer amount is not allowed.")
            return

        # For standard users, limit is $1000.00
        if not self.is_admin and amount > 1000.0:
            print("Error: Maximum transfer in standard mode is $1000.00.")
            return

        # Check for insufficient funds
        if source_account["balance"] < amount:
            print(f"Error: Insufficient funds in source account. Current balance is {source_account['balance']:.2f}.")
            return

        # Optional check: destination account can't go negative (usually not needed for deposits)
        if dest_account["balance"] + amount < 0:
            print("Error: Destination account balance cannot go negative.")
            return

        # Perform the transfer
        source_account["balance"] -= amount
        dest_account["balance"] += amount
        print(f"Transfer successful.\n"
            f"New source balance = {source_account['balance']:.2f}, "
            f"destination balance = {dest_account['balance']:.2f}.\n")

        # Write transaction logs
        transaction_code = "02"
        source_plan = source_account.get("status", "A")
        dest_plan = dest_account.get("status", "A")

        # Source side transaction
        write_transaction(
            transaction_code=transaction_code,
            account_holder_name=source_name,
            account_number=source_acc_input,
            amount=amount,
            plan_code=source_plan
        )

        # Destination side transaction
        dest_name = f"{dest_account['first_name']} {dest_account['last_name']}"
        write_transaction(
            transaction_code=transaction_code,
            account_holder_name=dest_name,
            account_number=dest_acc_input,
            amount=amount,
            plan_code=dest_plan
        )

    # User can pay bills to the three available account and then this transaction
    # is written to the file as "03"
    def paybill(self):
        if self.is_admin:
            holder_name = input("Enter the account holder's full name: ").strip()
            holder_account = self.bank.get_account(holder_name)
            if not holder_account:
                print(f"No valid account found for '{holder_name}'.")
                return
            print(f"Admin selected: {holder_name} (Balance = {holder_account['balance']:.2f})")
        else:
            holder_name = f"{self.account_info['first_name']} {self.account_info['last_name']}"
            holder_account = self.account_info
        acc_number_input = input("Enter the account number: ").strip()
        if acc_number_input != holder_account["account_number"]:
            print("Error: The account number does not match the account holder's record.")
            return
        print("Select the company to pay:")
        print("1. The Bright Light Electric Company (EC)")
        print("2. Credit Card Company Q (CQ)")
        print("3. Fast Internet, Inc. (FI)")
        choice = input("Enter 1, 2, or 3: ").strip()
        company_codes = {"1": "EC", "2": "CQ", "3": "FI"}
        if choice not in company_codes:
            print("Invalid choice. Payment cancelled.")
            return
        company_code = company_codes[choice]
        try:
            amount = float(input("Enter the amount to pay: ").strip())
        except ValueError:
            print("Invalid amount entered.")
            return
        if not self.is_admin and amount > 2000.0:
            print("Error: Maximum bill payment in standard mode is $2000.00.")
            return
        current_balance = holder_account["balance"]
        if current_balance - amount < 0:
            print(f"Error: Insufficient funds. Current balance is {current_balance:.2f}.")
            return
        new_balance = current_balance - amount
        holder_account["balance"] = new_balance
        print(f"Bill payment successful. New balance = {new_balance:.2f}.")
        write_transaction(
            transaction_code="03",
            account_holder_name=holder_name,
            account_number=acc_number_input,
            amount=amount,
            plan_code=company_code
        )
    
    # Users can deposit amount tp the their account and the transaction is written as "04"
    def deposit(self):
        if self.is_admin:
            holder_name = input("Enter the account holder's full name: ").strip()
            holder_account = self.bank.get_account(holder_name)
            if not holder_account:
                print(f"No valid account found for '{holder_name}'.")
                return
            print(f"Admin selected: {holder_name} (Balance = {holder_account['balance']:.2f})")
        else:
            holder_name = f"{self.account_info['first_name']} {self.account_info['last_name']}"
            holder_account = self.account_info
        acc_number_input = input("Enter the account number: ").strip()
        if acc_number_input != holder_account["account_number"]:
            print("Error: The account number does not match the account holder's record.")
            return
        try:
            amount = float(input("Enter the amount to deposit: ").strip())
        except ValueError:
            print("Invalid amount entered.")
            return
        if amount <= 0:
            print("Error: Deposit amount must be greater than 0.")
            return
        plan_code = holder_account.get("status", "A")
        write_transaction(
            transaction_code="04",
            account_holder_name=holder_name,
            account_number=acc_number_input,
            amount=amount,
            plan_code=plan_code
        )
        print("Deposit successful. The deposited funds will be available next session.")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            if self.is_admin:
                if choice == "1":
                    self.withdraw()
                elif choice == "2":
                    self.transfer()
                elif choice == "3":
                    self.paybill()
                elif choice == "4":
                    self.deposit()
                elif choice == "5":
                    self.bank.create_account(is_admin=self.is_admin)
                elif choice == "6":
                    self.bank.delete_account(is_admin=self.is_admin)
                elif choice == "7":
                    self.bank.disable_account(is_admin=self.is_admin)
                elif choice == "8":
                    self.bank.change_plan(is_admin=self.is_admin)
                elif choice == "9":
                    self.session.logout()
                    break
                else:
                    print("Invalid option. Please try again.")
            else:
                if choice == "1":
                    self.withdraw()
                elif choice == "2":
                    self.transfer()
                elif choice == "3":
                    self.paybill()
                elif choice == "4":
                    self.deposit()
                elif choice == "5":
                    self.session.logout()
                    break
                else:
                    print("Invalid option. Please try again.")
