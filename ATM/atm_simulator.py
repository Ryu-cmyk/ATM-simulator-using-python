''' #CONSOLE BASED
import time
from db import Database

print("="*50)
print(" "*15 + "ATM SIMULATOR")
print("="*50)


class Atmuser:
    def __init__(self, name, pin, balance, db):
        self.name = name
        self.pin = pin
        self.balance = balance
        self.db = db

    def menu(self):
        print(f"\nWelcome, {self.name}!")
        time.sleep(1)
        print("\n============MENU============\n")
        print("1) Withdraw")
        print("2) Deposit")
        print("3) Pin Change")
        print("4) View Transaction History")
        print("5) Check Balance")
        print("6) Exit\n")

    def withdraw(self):
        while True:
            try:
                withdraw_money = float(input("Enter the amount to withdraw: "))
                if withdraw_money <= 0:
                    print("Amount must be positive!")
                    continue
                    
                if self.balance >= withdraw_money:
                    self.balance -= withdraw_money
                    self.db.update_balance(self.pin, self.balance)
                    self.db.add_transaction(self.pin, "Withdrawal", withdraw_money)
                    print(f"Successfully withdrew {withdraw_money}. Remaining balance is {self.balance}")
                    break
                else:
                    print("Insufficient balance!")
                    break
            except ValueError:
                print("Invalid input! Please enter a valid number.")
                break

    def deposit(self):
        try:
            deposit_money = float(input("Enter the amount to deposit: "))
            if deposit_money <= 0:
                print("Amount must be positive!")
                return
                
            self.balance += deposit_money
            self.db.update_balance(self.pin, self.balance)
            self.db.add_transaction(self.pin, "Deposit", deposit_money)
            print(f"Successfully deposited {deposit_money}. Total balance is {self.balance}")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    def pin_change(self):
        current_pin = input("Enter current pin: ")
        if current_pin == self.pin:
            new_pin = input("Enter new pin: ")
            if len(new_pin) == 4 and new_pin.isdigit():
                if self.db.update_pin(self.pin, new_pin):
                    self.pin = new_pin
                    print("Successfully changed pin")
                else:
                    print("Pin already exists! Choose a different pin.")
            else:
                print("Pin must be 4 digits!")
        else:
            print("Wrong pin number")

    def view_transactions(self):
        transactions = self.db.get_transactions(self.pin)
        if transactions:
            print("\n===== Transaction History =====")
            for trans_type, amount, timestamp in transactions:
                print(f"{timestamp} - {trans_type}: {amount}")
            print("="*31)
        else:
            print("No transactions found.")
    
    def check_balance(self):
        print(f"\nYour current balance is: {self.balance}")

    def atm(self):
        while True:
            self.menu()
            
            try:
                choice = int(input("Which option do you like to proceed with?: "))

                if choice == 1:
                    self.withdraw()
                elif choice == 2:
                    self.deposit()
                elif choice == 3:
                    self.pin_change()
                elif choice == 4:
                    self.view_transactions()
                elif choice == 5:
                    self.check_balance()
                elif choice == 6:
                    print("Thank you for using our ATM")
                    break
                else:
                    print("Invalid option! Please choose 1-6")
            except ValueError:
                print("Invalid input! Please enter a number.")


class atm_system:
    def __init__(self):
        self.db = Database()
        self.initialize_default_users()
    
    #def initialize_default_users(self):
     # Add default users if they don't exist
       # self.db.add_user("Ayush Bhusal", "1234", 500000)
        #self.db.add_user("Ryu Bhusal", "5678", 300000)
        #self.db.add_user("Anita Sha", "0000", 20000)

    def initialize_default_users(self):
        default_users = [
            ("Ayush Bhusal", "1234", 500000),
            ("Ryu Bhusal", "5678", 300000),
            ("Srishti Bhusal", "9101", 200000),
            ("Kiran Sharma", "1122", 150000),
            ("Anjali Thapa", "3344", 250000),
            ("Rahul Singh", "5566", 100000),
            ("Priya Rai", "7788", 180000),
            ("Amit Joshi", "9900", 220000),
            ("Sneha Lama", "2233", 300000),
            ("Nitin KC", "4455", 120000),
            ("Rekha Shrestha", "6677", 200000),
            ("Sanjay Gurung", "8899", 160000)
        ]

    # Loop inside the method and call db.add_user
        for name, pin, balance in default_users:
            added = self.db.add_user(name, pin, balance)
            if added:
                 print(f"Added user: {name}")
            else:
                 print(f"User {name} already exists, skipping...")


    def insert_card(self):
        attempt = 3
        
        while attempt > 0:
            login_pin = input("\nEnter the pin: ")
            user_data = self.db.get_user(login_pin)

            if user_data:
                name, pin, balance = user_data
                user = Atmuser(name, pin, balance, self.db)
                print("Login Successful. Processing.....")
                time.sleep(1)
                return user
            else:
                attempt -= 1
                print(f"Incorrect Pin. Attempts left: {attempt}")

        print("Card blocked, too many attempts")
        return None
    
    def start(self):
        user = self.insert_card()
        if user:
            user.atm()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Initializing ATM System...")
    print("="*50 + "\n")
    
    #Start the ATM system
    atm = atm_system()
    atm.start()
    '''
from db import Database
from gui_main import ATMApp  # import your GUI class
import tkinter as tk

class Atmuser:
    def __init__(self, name, pin, balance, db):
        self.name = name
        self.pin = pin
        self.balance = balance
        self.db = db

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Amount must be positive!"
        if self.balance >= amount:
            self.balance -= amount
            self.db.update_balance(self.pin, self.balance)
            self.db.add_transaction(self.pin, "Withdrawal", amount)
            return True, f"Withdrew {amount}. Remaining balance: {self.balance}"
        return False, "Insufficient balance!"

    def deposit(self, amount):
        if amount <= 0:
            return False, "Amount must be positive!"
        self.balance += amount
        self.db.update_balance(self.pin, self.balance)
        self.db.add_transaction(self.pin, "Deposit", amount)
        return True, f"Deposited {amount}. Total balance: {self.balance}"

    def pin_change(self, new_pin):
        if len(new_pin) != 4 or not new_pin.isdigit():
            return False, "Pin must be 4 digits!"
        if self.db.update_pin(self.pin, new_pin):
            self.pin = new_pin
            return True, "Pin changed successfully"
        return False, "Pin already exists!"

    def view_transactions(self):
        return self.db.get_transactions(self.pin)

    def check_balance(self):
        return self.balance


class atm_system:
    def __init__(self):
        self.db = Database()
        self.initialize_default_users()

    def initialize_default_users(self):
        default_users = [
            ("Ayush Bhusal", "1234", 500000),
            ("Ryu Bhusal", "5678", 300000),
            ("Srishti Bhusal", "9101", 200000),
            ("Kiran Sharma", "1122", 150000),
            ("Anjali Thapa", "3344", 250000),
            ("Rahul Singh", "5566", 100000),
            ("Priya Rai", "7788", 180000),
            ("Amit Joshi", "9900", 220000),
            ("Sneha Lama", "2233", 300000),
            ("Nitin KC", "4455", 120000),
            ("Rekha Shrestha", "6677", 200000),
            ("Sanjay Gurung", "8899", 160000)
        ]
        for name, pin, balance in default_users:
            self.db.add_user(name, pin, balance)

    def get_user(self, pin):
        data = self.db.get_user(pin)
        if data:
            name, pin, balance = data
            return Atmuser(name, pin, balance, self.db)
        return None


if __name__ == "__main__":
    atm = atm_system()
    root = tk.Tk()           # Create GUI root window
    app = ATMApp(root)  # Pass root AND atm_system instance
    root.mainloop()           # Start GUI loop
