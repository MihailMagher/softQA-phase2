from session import Session
from bank import Bank

if __name__ == "__main__":
    bank = Bank(accounts_file="../Phase#2FIX/current accounts/current_accounts.txt")
    session = Session(bank)
    session.run()
