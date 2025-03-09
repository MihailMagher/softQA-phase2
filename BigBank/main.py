from session import Session
from bank import Bank

if __name__ == "__main__":
    bank = Bank(accounts_file="./current_bank_accounts_file.txt")
    session = Session(bank)
    session.run()
