#Tandin Tshering Norbu
#Electrical Department
#02230078
#reference
#https://www.youtube.com/watch?v=_uQrJ0TkZlc&pp=ygUQcHkgZm9yIGJlZ2lubmVycw%3D%3D
#https://learn.microsoft.com/en-us/training/paths/minecraft-python-coding-academy/
#https://www.youtube.com/watch?v=OZIRAavoGng&list=PLjVLYmrlmjGcQfNj_SLlLV4Ytf39f8BF7
#https://www.codecademy.com/learn/learn-python-3
#https://www.youtube.com/watch?v=xTh-ln2XhgU&pp=ygUOcHkgY29kaW5nIGJhbms%3D
#https://coding-academy.com/en/courses/python-course-training-education


import os
import random
import string
import getpass

# Base class for Accounts
class Account:
    def __init__(self, acc_number, acc_password, acc_type, acc_balance=0):
        self.acc_number = acc_number
        self.acc_password = acc_password
        self.acc_type = acc_type
        self.acc_balance = acc_balance

    def deposit(self, amount):
        if amount > 0:
            self.acc_balance += amount
            print(f"Deposited: Nu{amount}. New Balance: Nu{self.acc_balance}")
        else:
            print("Invalid amount. Please enter a valid amount.")
        self.save_to_file()

    def withdraw(self, amount):
        if amount > 0 and amount <= self.acc_balance:
            self.acc_balance -= amount
            print(f"Withdrawn: Nu{amount}. New Balance: Nu{self.acc_balance}")
        else:
            print("Insufficient funds or invalid amount.")
        self.save_to_file()

    def save_to_file(self, file_name='accounts.txt'):
        accounts = Account.load_accounts(file_name)
        accounts[self.acc_number] = self
        with open(file_name, 'w') as f:
            for acc in accounts.values():
                f.write(f"{acc.acc_number},{acc.acc_password},{acc.acc_type},{acc.acc_balance}\n")

    def delete_from_file(self, file_name='accounts.txt'):
        accounts = Account.load_accounts(file_name)
        if self.acc_number in accounts:
            del accounts[self.acc_number]
        with open(file_name, 'w') as f:
            for acc in accounts.values():
                f.write(f"{acc.acc_number},{acc.acc_password},{acc.acc_type},{acc.acc_balance}\n")

    def transfer_funds(self, recipient_account, amount):
        if amount > 0 and self.acc_balance >= amount:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            print(f"Transferred Nu{amount} to {recipient_account.acc_number}")
        else:
            print("Insufficient funds or invalid amount.")

    #creating account
    def load_accounts(file_name='accounts.txt'):
        accounts = {}
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    acc_number, acc_password, acc_type, acc_balance = line.strip().split(',')
                    acc_balance = float(acc_balance)
                    if acc_type == 'personal':
                        account = PersonalAccount(acc_number, acc_password, acc_balance)
                    elif acc_type == 'business':
                        account = BusinessAccount(acc_number, acc_password, acc_balance)
                    accounts[acc_number] = account
        return accounts

    #generate account number
    def generate_account_number():
        return ''.join(random.choices(string.digits, k=5))

    #generate password
    def generate_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    #login
    def login(accounts):
        acc_number = input("Enter your account number: ")
        acc_password = getpass.getpass("Enter your password: ")
        account = accounts.get(acc_number)
        if account and account.acc_password == acc_password:
            print("Login successful!")
            return account
        else:
            print("Invalid account number or password.")
            return None


class PersonalAccount(Account):
    def __init__(self, acc_number, acc_password, acc_balance=0):
        super().__init__(acc_number, acc_password, 'personal', acc_balance)


class BusinessAccount(Account):
    def __init__(self, acc_number, acc_password, acc_balance=0):
        super().__init__(acc_number, acc_password, 'business', acc_balance)


def main():
    accounts = Account.load_accounts()

    while True:
        print("\n..Welcome to Bank of Bhutan..")
        print("1. Open an Account")
        print("2. Login to Account")
        print("3. Exit")
        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            print("Select Account Type:")
            print("1. Personal Account")
            print("2. Business Account")
            acc_type_choice = input("Enter your choice: ")
            if acc_type_choice in ['1', '2']:
                acc_number = Account.generate_account_number()
                acc_password = Account.generate_password()
                if acc_type_choice == '1':
                    account = PersonalAccount(acc_number, acc_password)
                else:
                    account = BusinessAccount(acc_number, acc_password)
                account.save_to_file()
                accounts[acc_number] = account
                print(f"Account created successfully! Account Number: {acc_number}, Password: {acc_password}")
            else:
                print("Invalid account type selected.")

        elif user_choice == '2':
            account = Account.login(accounts)
            if account:
                while True:
                    print("\n..Account Menu..")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer Funds")
                    print("5. Delete Account")
                    print("6. Logout")
                    account_action_choice = input("Enter your choice: ")

                    if account_action_choice == '1':
                        print(f"Your Balance: Nu{account.acc_balance}")
                    elif account_action_choice == '2':
                        try:
                            amount = float(input("Enter amount to deposit: "))
                            account.deposit(amount)
                        except ValueError:
                            print("Invalid input. Please enter a numeric value.")
                    elif account_action_choice == '3':
                        try:
                            amount = float(input("Enter amount to withdraw: "))
                            account.withdraw(amount)
                        except ValueError:
                            print("Invalid input. Please enter a numeric value.")
                    elif account_action_choice == '4':
                        to_acc_number = input("Enter the recipient's account number: ")
                        if to_acc_number in accounts:
                            recipient_account = accounts[to_acc_number]
                            try:
                                amount = float(input("Enter the amount to send: "))
                                account.transfer_funds(recipient_account, amount)
                            except ValueError:
                                print("Invalid input. Please enter a numeric value.")
                        else:
                            print("Recipient account not found.")
                    elif account_action_choice == '5':
                        confirm = input("Are you sure you want to delete this account? (yes/no): ")
                        if confirm.lower() == 'yes':
                            account.delete_from_file()
                            del accounts[account.acc_number]
                            print("Account deleted successfully.")
                            break
                    elif account_action_choice == '6':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")

        elif user_choice == '3':
            print("..Thank you for using Bank of Bhutan..")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()