from session import Session
from bank import Bank

def change_payment_plan(session):
    
    # Check if the current user is an admin
    if not session.logged_in_user.is_admin():
        print("Access Denied: Only admins can change payment plans.")
        return

    # Prompt for the account holder's name and account number
    account_holder_name = input("Enter the bank account holder's name: ").strip()
    account_number = input("Enter the account number: ").strip()

    # Find the matching account (both name and account number must match)
    found_account = None
    for acc in session.bank.users.values():
        if acc.name.lower() == account_holder_name.lower() and acc.user_id == account_number:
            found_account = acc
            break

    if found_account is None:
        print("Error: No account found with the provided name and account number.")
        return

    # Check if the account's payment plan is currently "SP"
    if found_account.payment_plan != "SP":
        print("The account payment plan is not set to 'SP'. No change needed.")
        return

    # Change the payment plan to "NP"
    found_account.payment_plan = "NP"

    # Update the account record in the accounts file (format: user_id, first_name, last_name, status, balance, payment_plan)
    try:
        with open(session.accounts_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(session.accounts_file, "w", encoding="utf-8") as file:
            for line in lines:
                parts = line.strip().split("_")
                if parts[0] == found_account.user_id:
                    # Update the payment plan field (index 5) to "NP"
                    parts[5] = "NP"
                    updated_line = "_".join(parts) + "\n"
                    file.write(updated_line)
                else:
                    file.write(line)
        print("Payment plan changed successfully.")
    except Exception as e:
        print("Error updating accounts file:", e)
        return

    # Log the change plan transaction using transaction code "07"
    transaction_code = "07"
    formatted_name = found_account.name.ljust(20)[:20]
    # For the change plan operation, no monetary value applies; use "00000000" as a placeholder
    log_entry = f"{transaction_code}_{formatted_name}_{found_account.user_id}_00000000_00\n"
    try:
        with open(session.bank.transaction_log, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
        print("Change plan transaction logged successfully.")
    except Exception as e:
        print("Error writing to transaction log:", e)

if __name__ == "__main__":
    # File paths configuration, similar to login.py format
    accounts_file_path = "../BigBank/current accounts/current_accounts.txt"
    transaction_log_path = "../BigBank/bank account transaction file/output/bank_transaction_log"

    # Load account information from the file
    users = Bank.get_accounts(accounts_file_path)
    if users:
        bank = Bank(users=users, accounts_file=accounts_file_path, transaction_log=transaction_log_path)
        session = Session(users, accounts_file_path, bank)
        # Admin login is required; only admins can perform the change payment plan transaction
        print("Admin Login for Change Payment Plan Transaction")
        session.admin_login()
        if session.logged_in_user is not None:
            change_payment_plan(session)
        else:
            print("Admin login failed. Exiting.")
    else:
        print("No users loaded. Please check the file and try again.")
