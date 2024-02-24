import tkinter as tk
from tkinter import messagebox
import mysql.connector
import base64

class ATM:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")
        self.root.title("ATM")

        self.label_card = tk.Label(self.root, text="Enter your card number:")
        self.label_card.grid(row=0, column=0, padx=10, pady=10)

        self.entry_card = tk.Entry(self.root)
        self.entry_card.grid(row=1, column=0, padx=10, pady=10)

        self.btn_login = tk.Button(self.root, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=0, padx=10, pady=10)

        self.account_number = None
        self.pin = None
        self.balance = None

    def login(self):
        card_number = self.entry_card.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="atm_db"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM accounts WHERE account_number=%s", (card_number,))
            account = cursor.fetchone()

            if account is not None:
                self.account_number = account[0]
                self.pin = self.decrypt_pin(account[1])
                self.balance = account[3]
                self.show_menu()
            else:
                messagebox.showerror("Error", "Invalid card number")

            conn.close()
        except mysql.connector.Error as e:
            print("Error connecting to MySQL:", e)
            messagebox.showerror("Error", "Error connecting to database")

    def show_menu(self):
        self.label_card.grid_remove()
        self.entry_card.grid_remove()

        self.label_menu = tk.Label(self.root, text="Select an option:")
        self.label_menu.grid(row=0, column=0, padx=10, pady=10)

        self.btn_balance = tk.Button(self.root, text="Check Balance", command=self.check_balance)
        self.btn_balance.grid(row=1, column=0, padx=10, pady=10)

        self.btn_withdraw = tk.Button(self.root, text="Withdraw Money", command=self.withdraw_money)
        self.btn_withdraw.grid(row=2, column=0, padx=10, pady=10)

        self.btn_deposit = tk.Button(self.root, text="Deposit Money", command=self.deposit_money)
        self.btn_deposit.grid(row=3, column=0, padx=10, pady=10)

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your balance is: ${self.balance}")

    def withdraw_money(self):
        pin_input = simpledialog.askstring("Input", "Enter your PIN:", show='*')
        if pin_input == self.pin:
            amount = simpledialog.askinteger("Input", "Enter amount to withdraw:")
            if amount is not None and amount > 0:
                if amount <= self.balance:
                    self.balance -= amount
                    self.update_balance()
                    messagebox.showinfo("Withdrawal", f"Successfully withdrew ${amount}")
                else:
                    messagebox.showerror("Error", "Insufficient funds")
            else:
                messagebox.showerror("Error", "Invalid amount")

    def deposit_money(self):
        pin_input = simpledialog.askstring("Input", "Enter your PIN:", show='*')
        if pin_input == self.pin:
            amount = simpledialog.askinteger("Input", "Enter amount to deposit:")
            if amount is not None and amount > 0:
                self.balance += amount
                self.update_balance()
                messagebox.showinfo("Deposit", f"Successfully deposited ${amount}")
            else:
                messagebox.showerror("Error", "Invalid amount")

    def decrypt_pin(self, encrypted_pin):
        key = b'your_16_byte_key'
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_pin = cipher.decrypt(base64.b64decode(encrypted_pin)).strip()
        return decrypted_pin.decode()

    def update_balance(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="atm_db"
            )
            cursor = conn.cursor()

            cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (self.balance, self.account_number))
            conn.commit()

            conn.close()
        except mysql.connector.Error as e:
            print("Error connecting to MySQL:", e)
            messagebox.showerror("Error", "Error updating balance")

root = tk.Tk()
app = ATM(root)
root.mainloop()