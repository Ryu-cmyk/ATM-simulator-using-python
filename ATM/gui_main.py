import tkinter as tk
from tkinter import messagebox, ttk
from db import Database
import time

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Simulator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        self.db = Database()
        self.initialize_default_users()
        
        self.current_user = None
        self.user_name = None
        self.user_pin = None
        self.user_balance = None
        self.login_attempts = 3
        
        self.show_login_screen()
    
    def initialize_default_users(self):
        self.db.add_user("Ayush Bhusal", "1234", 500000)
        self.db.add_user("Ryu Bhusal", "5678", 300000)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        self.clear_screen()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#34495e", height=100)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="ATM SIMULATOR", font=("Arial", 24, "bold"), 
                bg="#34495e", fg="white").pack(pady=30)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(main_frame, text="Enter Your PIN", font=("Arial", 16), 
                bg="#2c3e50", fg="white").pack(pady=20)
        
        self.pin_entry = tk.Entry(main_frame, font=("Arial", 18), show="*", 
                                  justify="center", width=15)
        self.pin_entry.pack(pady=10)
        self.pin_entry.focus()
        
        tk.Label(main_frame, text=f"Attempts remaining: {self.login_attempts}", 
                font=("Arial", 10), bg="#2c3e50", fg="#95a5a6").pack(pady=5)
        
        login_btn = tk.Button(main_frame, text="LOGIN", font=("Arial", 14, "bold"),
                             bg="#27ae60", fg="white", width=15, height=2,
                             cursor="hand2", command=self.login)
        login_btn.pack(pady=20)
        
        self.pin_entry.bind("<Return>", lambda e: self.login())
    
    def login(self):
        pin = self.pin_entry.get()
        
        if not pin:
            messagebox.showerror("Error", "Please enter your PIN")
            return
        
        user_data = self.db.get_user(pin)
        
        if user_data:
            self.user_name = user_data[0]
            self.user_pin = user_data[1]
            self.user_balance = user_data[2]
            messagebox.showinfo("Success", f"Welcome, {self.user_name}!")
            self.show_main_menu()
        else:
            self.login_attempts -= 1
            if self.login_attempts > 0:
                messagebox.showerror("Error", f"Incorrect PIN!\nAttempts remaining: {self.login_attempts}")
                self.pin_entry.delete(0, tk.END)
                self.show_login_screen()
            else:
                messagebox.showerror("Blocked", "Card blocked due to too many incorrect attempts!")
                self.root.quit()
    
    def show_main_menu(self):
        self.clear_screen()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#34495e", height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"Welcome, {self.user_name}!", 
                font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=25)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Menu buttons
        buttons = [
            ("💰 Withdraw", self.show_withdraw_screen, "#e74c3c"),
            ("💵 Deposit", self.show_deposit_screen, "#27ae60"),
            ("🔑 Change PIN", self.show_change_pin_screen, "#3498db"),
            ("📊 Transaction History", self.show_transaction_history, "#9b59b6"),
            ("💳 Check Balance", self.show_balance, "#f39c12"),
            ("🚪 Exit", self.exit_app, "#95a5a6")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(main_frame, text=text, font=("Arial", 14), 
                          bg=color, fg="white", width=25, height=2,
                          cursor="hand2", command=command)
            btn.pack(pady=8)
    
    def show_withdraw_screen(self):
        self.clear_screen()
        
        # Header
        self.create_header("Withdraw Money")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(main_frame, text=f"Current Balance: Rs. {self.user_balance:,.2f}", 
                font=("Arial", 14), bg="#2c3e50", fg="#27ae60").pack(pady=20)
        
        tk.Label(main_frame, text="Enter Amount to Withdraw:", 
                font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
        
        amount_entry = tk.Entry(main_frame, font=("Arial", 16), justify="center", width=20)
        amount_entry.pack(pady=10)
        amount_entry.focus()
        
        def withdraw():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive!")
                    return
                
                if amount > self.user_balance:
                    messagebox.showerror("Error", "Insufficient balance!")
                    return
                
                self.user_balance -= amount
                self.db.update_balance(self.user_pin, self.user_balance)
                self.db.add_transaction(self.user_pin, "Withdrawal", amount)
                messagebox.showinfo("Success", f"Successfully withdrew Rs. {amount:,.2f}\nRemaining balance: Rs. {self.user_balance:,.2f}")
                self.show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
        
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Withdraw", font=("Arial", 12, "bold"),
                 bg="#27ae60", fg="white", width=12, height=2,
                 cursor="hand2", command=withdraw).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Back", font=("Arial", 12),
                 bg="#95a5a6", fg="white", width=12, height=2,
                 cursor="hand2", command=self.show_main_menu).pack(side="left", padx=10)
        
        amount_entry.bind("<Return>", lambda e: withdraw())
    
    def show_deposit_screen(self):
        self.clear_screen()
        
        # Header
        self.create_header("Deposit Money")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(main_frame, text=f"Current Balance: Rs. {self.user_balance:,.2f}", 
                font=("Arial", 14), bg="#2c3e50", fg="#27ae60").pack(pady=20)
        
        tk.Label(main_frame, text="Enter Amount to Deposit:", 
                font=("Arial", 12), bg="#2c3e50", fg="white").pack(pady=10)
        
        amount_entry = tk.Entry(main_frame, font=("Arial", 16), justify="center", width=20)
        amount_entry.pack(pady=10)
        amount_entry.focus()
        
        def deposit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive!")
                    return
                
                self.user_balance += amount
                self.db.update_balance(self.user_pin, self.user_balance)
                self.db.add_transaction(self.user_pin, "Deposit", amount)
                messagebox.showinfo("Success", f"Successfully deposited Rs. {amount:,.2f}\nNew balance: Rs. {self.user_balance:,.2f}")
                self.show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
        
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Deposit", font=("Arial", 12, "bold"),
                 bg="#27ae60", fg="white", width=12, height=2,
                 cursor="hand2", command=deposit).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Back", font=("Arial", 12),
                 bg="#95a5a6", fg="white", width=12, height=2,
                 cursor="hand2", command=self.show_main_menu).pack(side="left", padx=10)
        
        amount_entry.bind("<Return>", lambda e: deposit())
    
    def show_change_pin_screen(self):
        self.clear_screen()
        
        # Header
        self.create_header("Change PIN")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(main_frame, text="Current PIN:", font=("Arial", 12), 
                bg="#2c3e50", fg="white").pack(pady=10)
        current_pin_entry = tk.Entry(main_frame, font=("Arial", 16), show="*", 
                                     justify="center", width=15)
        current_pin_entry.pack(pady=5)
        current_pin_entry.focus()
        
        tk.Label(main_frame, text="New PIN (4 digits):", font=("Arial", 12), 
                bg="#2c3e50", fg="white").pack(pady=10)
        new_pin_entry = tk.Entry(main_frame, font=("Arial", 16), show="*", 
                                justify="center", width=15)
        new_pin_entry.pack(pady=5)
        
        def change_pin():
            current_pin = current_pin_entry.get()
            new_pin = new_pin_entry.get()
            
            if current_pin != self.user_pin:
                messagebox.showerror("Error", "Incorrect current PIN!")
                return
            
            if len(new_pin) != 4 or not new_pin.isdigit():
                messagebox.showerror("Error", "PIN must be 4 digits!")
                return
            
            if self.db.update_pin(self.user_pin, new_pin):
                self.user_pin = new_pin
                messagebox.showinfo("Success", "PIN changed successfully!")
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "PIN already exists! Choose a different PIN.")
        
        btn_frame = tk.Frame(main_frame, bg="#2c3e50")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="Change PIN", font=("Arial", 12, "bold"),
                 bg="#27ae60", fg="white", width=12, height=2,
                 cursor="hand2", command=change_pin).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Back", font=("Arial", 12),
                 bg="#95a5a6", fg="white", width=12, height=2,
                 cursor="hand2", command=self.show_main_menu).pack(side="left", padx=10)
    
    def show_transaction_history(self):
        self.clear_screen()
        
        # Header
        self.create_header("Transaction History")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(main_frame, bg="#2c3e50", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2c3e50")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        transactions = self.db.get_transactions(self.user_pin, 20)
        
        if transactions:
            for trans_type, amount, timestamp in transactions:
                color = "#27ae60" if trans_type == "Deposit" else "#e74c3c"
                sign = "+" if trans_type == "Deposit" else "-"
                
                trans_frame = tk.Frame(scrollable_frame, bg="#34495e", relief="raised", bd=1)
                trans_frame.pack(fill="x", padx=10, pady=5)
                
                tk.Label(trans_frame, text=f"{trans_type}", font=("Arial", 12, "bold"),
                        bg="#34495e", fg=color, anchor="w").pack(side="left", padx=10, pady=10)
                
                tk.Label(trans_frame, text=f"{sign} Rs. {amount:,.2f}", font=("Arial", 12),
                        bg="#34495e", fg="white", anchor="e").pack(side="right", padx=10, pady=10)
                
                tk.Label(trans_frame, text=timestamp, font=("Arial", 9),
                        bg="#34495e", fg="#95a5a6").pack(side="bottom", padx=10, pady=5)
        else:
            tk.Label(scrollable_frame, text="No transactions found", 
                    font=("Arial", 14), bg="#2c3e50", fg="#95a5a6").pack(pady=50)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Button(self.root, text="Back to Menu", font=("Arial", 12),
                 bg="#95a5a6", fg="white", width=15, height=2,
                 cursor="hand2", command=self.show_main_menu).pack(pady=10)
    
    def show_balance(self):
        messagebox.showinfo("Current Balance", 
                          f"Your current balance is:\nRs. {self.user_balance:,.2f}")
    
    def create_header(self, title):
        header_frame = tk.Frame(self.root, bg="#34495e", height=80)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text=title, font=("Arial", 18, "bold"),
                bg="#34495e", fg="white").pack(pady=25)
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            messagebox.showinfo("Thank You", "Thank you for using our ATM!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop() 

