import random


class User:
    account_list = []
    loan_on = True

    def __init__(self, name, email, address, account_type, password) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.password = password
        self.balance = 0
        self.loan_count = 0
        self.total_loan = 0
        self.transection_history = []

        self.account_number = self.random_acc()
        User.account_list.append(self)

    def random_acc(self):
        return random.randint(1000, 9999)

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount
                self.transection_history.append(f"deposit : $({amount})")
                print(f"\nDeposit successful: ${amount}")
            else:
                print(f"\nInvalid amount: ${amount}")
        except ValueError:
            print("\nInvalid input. Please enter a valid amount.")

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                self.transection_history.append(f"withdraw : $({amount})")
                print(f"\nWithdrawal successful: ${amount}")
            else:
                print(f"\nWithdrawal amount exceeds balance: ${amount}")
        except ValueError:
            print("\nInvalid input. Please enter a valid amount.")

    def show_info(self):
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Type: {self.account_type}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ${self.balance}")
        print(f"Total Loan: ${self.total_loan}")

    def available_balance(self):
        print(f"\nAvailable Balance: ${self.balance}")

    def loan_withdraw(self, amount):
        if User.loan_on:
            print(User.loan_on)
            try:
                amount = float(amount)
                if self.loan_count < 2:
                    self.total_loan += amount
                    self.balance += amount
                    self.loan_count += 1
                    self.transection_history.append(f"Loan : $({amount})")
                    print(f"\nLoan of ${amount} withdrawn successfully.")
                else:
                    print("Sorry, you have already taken 2 loans!")
            except ValueError:
                print("\nInvalid input. Please enter a valid amount.")

        else:
            print("Loan Servies Off Now !\n")

    def transfer_amount(self, amount, recipient_acc_no):
        try:
            amount = float(amount)
            recipient_acc_no = int(recipient_acc_no)
            recipient = None
            for user in User.account_list:
                if recipient_acc_no == user.account_number:
                    if self.balance >= amount:
                        user.balance += amount
                        self.balance -= amount
                        self.transection_history.append(f"withdraw : $({amount})")
                        print(
                            f"\nTransfer successful: ${amount} to Account No. {recipient_acc_no}"
                        )
                    else:
                        print("\nInsufficient balance for the transfer.")
                    recipient = user
                    break

            if recipient is None:
                print("\nRecipient account does not exist!")
        except ValueError:
            print(
                "\nInvalid input. Please enter valid amounts and recipient account number."
            )

    def transection(self):
        for i in self.transection_history:
            print(i)

    def bankrupt(self):
        if self.balance == 0:
            print("\nYour account is bankrupt.")
        else:
            print("\nYour account is not bankrupt.")


class SavingAccount(User):
    def __init__(self, name, email, address, password) -> None:
        super().__init__(name, email, address, "Savings", password)


class CurrentAccount(User):
    def __init__(self, name, email, address, password) -> None:
        super().__init__(name, email, address, "Current", password)


class Bank:
    def __init__(self, name, password) -> None:
        self.total_balance = 0
        self.acc_list = []
        self.name = name
        self.password = password

    def create_account(self, name, email, address, account_type, password):
        try:
            new_account = None
            if account_type.lower() == "savings":
                new_account = SavingAccount(name, email, address, password)
            elif account_type.lower() == "current":
                new_account = CurrentAccount(name, email, address, password)

            if new_account:
                self.acc_list.append(new_account)
                print("\nAccount created successfully.")
                print(f"Account Number: {new_account.account_number}")
        except ValueError:
            print("\nInvalid input. Please enter valid information.")

    def delete_account(self, password, account_number):
        try:
            account_number = int(account_number)
            for user in User.account_list:
                if password == user.password and account_number == user.account_number:
                    User.account_list.remove(user)
                    print("\nAccount deleted successfully.")
                    return

            print("\nInvalid Account Number or Password.")
        except ValueError:
            print("\nInvalid input. Please enter valid information.")

    def show_all_accounts(self):
        for user in User.account_list:
            user.show_info()

    def total_available_balance(self):
        self.total_balance = sum(user.balance for user in User.account_list)
        return self.total_balance

    def loan_feature(self, option):
        if option == 1:
            User.loan_on = True
            print("loan Is ON !\n")
        elif option == 2:
            User.loan_on = False
            print("Loan is off !\n")
        else:
            print("Invalid option\n")

    def is_bankrupt(self):
        if not User.account_list:
            print("\nBank is empty. It's bankrupt.")
        else:
            print("\nBank is not bankrupt.")


brac = Bank("admin", "admin")
cur_user = None

while True:
    print("\n1. Admin")
    print("2. User")
    print("3. Exit")
    option = input("Enter your option: ")

    if option == "1":
        admin_pass = input("Enter password: ")
        if admin_pass == brac.password:
            print(f"\nWelcome Admin -->\n")
            while True:
                print("1. Create an account")
                print("2. Delete an account")
                print("3. User account List")
                print("4. Total available balance in the bank")
                print("5. Bankrupt Status")
                print("6. Loan on/off ")
                print("7. Exit")
                admin_option = input("Enter your option: ")
                if admin_option == "1":
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    address = input("Enter your Address: ")
                    account_type = input("Enter your Account Type (Savings/Current): ")
                    password = input("Enter password: ")
                    brac.create_account(name, email, address, account_type, password)
                elif admin_option == "2":
                    account_number = input("Enter Account Number to delete: ")
                    password = input("Enter password: ")
                    brac.delete_account(password, account_number)
                elif admin_option == "3":
                    brac.show_all_accounts()
                elif admin_option == "4":
                    print(f"Total Bank balance: ${brac.total_available_balance()}")
                elif admin_option == "5":
                    brac.is_bankrupt()
                elif admin_option == "6":
                    print("1.ON ")
                    print("2.OFF ")
                    op = int(input("enter option: "))
                    brac.loan_feature(op)
                elif admin_option == "7":
                    break

    elif option == "2":
        if cur_user is None:
            login_option = input("Register/Login (r/l): ")
            if login_option == "r":
                print("1. Register Savings account")
                print("2. Register Current account\n")
                registration_option = input("Enter your option: ")
                if registration_option == "1":
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    address = input("Enter your Address: ")
                    password = input("Enter password: ")
                    cur_user = SavingAccount(name, email, address, password)
                    print(f"Register Successful -- Savings Account")
                    cur_user.show_info()
                elif registration_option == "2":
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    address = input("Enter your Address: ")
                    password = input("Enter password: ")
                    cur_user = CurrentAccount(name, email, address, password)
                    print(f"Register Successful -- Current Account")
                    cur_user.show_info()
                else:
                    print("Invalid option!")
            elif login_option == "l":
                account_number = input("Enter your Account Number: ")
                password = input("Enter your password: ")
                found_user = None
                for user in User.account_list:
                    if (
                        int(account_number) == user.account_number
                        and password == user.password
                    ):
                        cur_user = user
                        found_user = user
                        print(f"Login Successful --> {user.account_type} Account")
                        break
                if found_user is None:
                    print("Invalid Account Number or Password!")

        while cur_user:
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. Loan Withdraw")
            print("4. Transfer Balance")
            print("5. Show Account Info")
            print("6. transection")
            print("7. Logout")

            user_option = input("Choose option: ")
            if user_option == "1":
                amount = input("Enter amount to deposit: $")
                cur_user.deposit(amount)
            elif user_option == "2":
                amount = input("Enter amount to withdraw: $")
                cur_user.withdraw(amount)
            elif user_option == "3":
                amount = input("Enter loan amount to withdraw: $")
                cur_user.loan_withdraw(amount)
            elif user_option == "4":
                amount = input("Enter amount to transfer: $")
                recipient_acc_no = input("Enter recipient's Account Number: ")
                cur_user.transfer_amount(amount, recipient_acc_no)
            elif user_option == "5":
                cur_user.show_info()

            elif user_option == "6":
                cur_user.transection()

            elif user_option == "7":
                print("Logout Successful!")
                cur_user = None

    elif option == "3":
        break
