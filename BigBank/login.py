from session import Session
from bank import Bank

if __name__ == "__main__":
    accounts_file_path = "../BigBank/current accounts/current_accounts.txt"
    transaction_log_path = "../BigBank/bank account transaction file(output)/bank_transaction_log"

    users = Bank.get_accounts(accounts_file_path)

    if users:
        bank = Bank(users=users, accounts_file=accounts_file_path, transaction_log=transaction_log_path)
        session = Session(users, accounts_file_path, bank)
        session.login()
    else:
        print("No users loaded. Please check the file and try again.")