
# ATM Simulator (Python + SQLite)

**ATM Simulator** is a Python application that simulates an **Automated Teller Machine (ATM)** with both **console and GUI interfaces**.
It demonstrates Python programming, GUI design with **Tkinter**, and database management using **SQLite**.

## Features

* **User Authentication:** Login using a secure PIN
* **Account Management:** Check balance, deposit funds,withdraw cash and check transactions history
* **PIN Management:** Change PIN securely
* **Transaction History:** Tracks all deposits and withdrawals stored in **SQLite**
* **Multiple Interfaces:** Terminal (console) menu and GUI using Tkinter

## Technical Details

* **Language:** Python 3

* **GUI Framework:** Tkinter

* **Database:** SQLite for storing account information and transaction history

* **Program Flow:**

  1. User logs in with a PIN
  2. User selects an operation: Check Balance / Deposit / Withdraw / Change PIN / Transaction History
  3. Input is validated and the SQLite database is updated
  4. Transactions are recorded in the database and displayed in the GUI or console

* **Error Handling:** Validates PIN, deposits, and withdrawals to prevent invalid operations

* **Extensibility:** Can be expanded to support multiple users, persistent account management, and advanced banking features

## Download GUI Version

You can **download the GUI version** of this project by getting the **`dist.zip`** file from the GitHub repository.
[ATM Simulator using Python](https://github.com/Ryu-cmyk/ATM-simulator-using-python)

## Purpose

This project is intended for learning and demonstrating:

* Python programming with functions and conditional logic
* GUI development using Tkinter
* Database integration with SQLite
* Managing transactions and user data securely
